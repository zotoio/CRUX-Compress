---
branch: 2
depth: 3
subfocus_index: 2
subfocus: "Backoff Parameter Tuning and Retry Budget Optimisation"
parent_subfocus: "Retry Strategies and Transient Error Recovery"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The parent facet established how the harness classifies errors and implements retry logic. This leaf narrows to the quantitative question: are the concrete backoff parameters (BASE_DELAY, MAX_DELAY, retry count, jitter width) mathematically optimal for the constraints they operate under (test timeouts, rate-limit window alignment, fork-count collision avoidance)?

## Discoveries

### 1. Corrected Worst-Case Retry Timeline

[memory:Exponential backoff with jitter on rate-limit errors] Memory `6265f8f` states the worst-case total delay is "2+4+8+16+32+60 ≈ 122s", implying 6 delay intervals. However, the actual code computes only **5 delays** (attempts 0–4) before throwing at attempt 5:

```
for (let attempt = 0; ; attempt++) {
  try { return await fn(); }
  catch (err) {
    if (!isRateLimitError(err) || attempt >= maxRetries) { throw err; }
    //  attempt=5 → 5 >= 5 → throw immediately, no delay computed
    const delay = backoffDelay(attempt);
    await sleep(delay);
  }
}
```

Correct delay budget (5 intervals, not 6):

| Attempt | Un-jittered (ms) | Min (j=0.85) | Max (j=1.15) |
|---------|------------------|--------------|--------------|
| 0       | 2,000            | 1,700        | 2,300        |
| 1       | 4,000            | 3,400        | 4,600        |
| 2       | 8,000            | 6,800        | 9,200        |
| 3       | 16,000           | 13,600       | 18,400       |
| 4       | 32,000           | 27,200       | 36,800       |
| **Sum** | **62,000**       | **52,700**   | **71,300**   |

None of these intervals hit the 60,000ms cap — the cap only activates at `2000 × 2^5 = 64,000`, which is never reached because attempt 5 throws before computing its delay. The memory's "60s" final entry is a phantom delay.

**Corrected budget: 53–71s total delay, nominal 62s** — roughly half the memory's 122s figure.

### 2. Budget Fit Within Test Timeouts

[memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE] With the corrected 62s nominal delay budget:

| Scenario | Delay | Error returns (5 × ~1s) | Final op | Total | 300s headroom |
|----------|-------|------------------------|----------|-------|---------------|
| Nominal  | 62s   | 5s                     | 90s      | 157s  | 143s          |
| Worst    | 71s   | 5s                     | 120s     | 196s  | 104s          |
| Best     | 53s   | 5s                     | 60s      | 118s  | 182s          |

Rate-limited responses return fast (~1s), so only the final successful attempt contributes full operation time. The retry budget consumes 17–24% of a 300s timeout — well within margin. For 480s meditate timeouts, utilisation drops to 11–15%.

The corrected math reveals the parameters are **more conservative than documented** — there is substantial unused budget, suggesting room to either increase resilience (more retries) or decrease base delay sensitivity.

### 3. Jitter Width Analysis — ±15% vs Alternatives

The current ±15% jitter produces a delay spread of 30% of the base value:

| Delay interval | Window width (ms) | As fraction of reset window (60s) |
|----------------|-------------------|-----------------------------------|
| delay(0)       | 600               | 1.0%                              |
| delay(1)       | 1,200             | 2.0%                              |
| delay(2)       | 2,400             | 4.0%                              |
| delay(3)       | 4,800             | 8.0%                              |
| delay(4)       | 9,600             | 16.0%                             |

**For 2 concurrent forks** (the current `maxForks` recommendation), the probability of two forks landing in the same 1-second sub-window within delay(4)'s 9.6s spread is approximately 1/9.6 ≈ 10.4%. Acceptable.

**For N forks**, collision probability follows the birthday-problem analogue: with K forks in a W-second window, P(any collision) ≈ 1 - e^(-K²/2W). At delay(4):

| Forks (K) | ±15% (W=9.6s) | ±50% (W=32s) | Full jitter (W=64s) | Decorrelated (adaptive) |
|-----------|---------------|--------------|---------------------|------------------------|
| 2         | 10.4%         | 3.1%         | 1.6%                | ~1%                    |
| 4         | 56.3%         | 22.1%        | 11.8%               | ~5%                    |
| 8         | 96.7%         | 63.2%        | 39.3%               | ~15%                   |

At 4+ forks, ±15% jitter becomes problematic — over half the time, at least two forks will collide. The current mitigation (keeping maxForks=2) makes this acceptable, but the jitter width would need widening if parallelism increases.

**Strategy comparison:**

- **Equal jitter ±15% (current)**: Simple, predictable, maintains ~85% of the intended backoff. Adequate for low concurrency.
- **Equal jitter ±50%**: Better spread with minimal complexity increase. Delay ∈ [0.5x, 1.5x] base — floor stays meaningful.
- **Full jitter (0 to 2x)**: Maximum spread but can produce near-zero delays, partially defeating the purpose of exponential backoff. AWS recommendation for general use but risks early re-throttle.
- **Decorrelated jitter** (`delay = min(cap, random(base, prev_delay × 3))`): Best theoretical performance per AWS analysis — each retry's delay is influenced by its predecessor, creating adaptive spread. Requires carrying state between attempts (minor complexity).

### 4. Base Delay Alignment with Rate-Limit Windows

API rate limits commonly reset on boundaries of 10s, 30s, or 60s. With BASE_DELAY=2s:

- Attempt 0 retries after 2s — almost certainly **within** the same rate window
- Attempt 1 retries after cumulative 6s — likely still within a 10s window
- Attempt 2 retries after cumulative 14s — clears 10s windows
- Attempt 3 retries after cumulative 30s — clears 30s windows

The first 1–2 retries are likely to be "wasted" against any rate limit with a ≥10s reset window. A BASE_DELAY of 5s would clear 10s windows on second retry (cumulative 15s), while a 10s base would clear on first retry.

**Tradeoff**: Longer base delay increases minimum wait (penalises the common case where one retry suffices) but reduces total attempts to success (saving API calls and wall-clock). Given the generous 300s budget:

| Config              | Delay sum (nominal) | Expected attempts to clear 60s window | Budget % |
|---------------------|--------------------|-----------------------------------------|----------|
| BASE=2s, retries=5  | 62s                | 4 (cumulative 30s may still miss)       | 21%      |
| BASE=5s, retries=4  | 75s                | 3 (cumulative 35s clears most windows)  | 25%      |
| BASE=10s, retries=3 | 70s                | 2 (cumulative 30s clears 30s windows)   | 23%      |
| BASE=15s, retries=3 | 105s               | 2 (cumulative 45s clears most windows)  | 35%      |

The sweet spot appears to be **BASE=5s with 4 retries** — similar total budget (75s), fewer wasted early retries, same timeout margin.

### 5. Concurrency Reduction as Proactive Budget Conservation

[memory:Shared-agent-runs-per-describe-block reduce API cost] The shared-beforeAll pattern reduces concurrent API calls from N to 1 per describe block. This interacts with the retry budget multiplicatively:

- **Without sharing**: 3 tests × 2 forks = 6 concurrent requests. At 4+ concurrent requests, ±15% jitter collision probability exceeds 56%.
- **With sharing**: 1 shared run × 2 forks = 2 concurrent requests. Collision probability drops to ~10%.

This means the shared-run pattern isn't just a cost optimisation — it's a **structural prerequisite** for the narrow jitter width to remain effective. If the test suite abandoned shared runs while keeping maxForks=2, the effective concurrency would increase enough to expose the jitter weakness.

## Connections

1. **Memory error as design signal**: The off-by-one in memory `6265f8f`'s budget calculation (122s vs actual 62s) suggests the parameters were chosen with an implicit 2x safety margin assumption. The *perceived* budget of 122s filling 40% of a 300s timeout felt right — the *actual* budget of 62s filling only 21% is even more conservative than intended. This accidental over-provisioning is harmless but means there's room to add retries or increase base delay without timeout risk.

2. **Jitter width couples to parallelism strategy**: The ±15% jitter and `maxForks: 2` recommendation form a tightly coupled pair — either parameter changing requires re-evaluating the other. If `maxForks` increases to 4, the jitter should widen to ±50% or switch to decorrelated. If jitter widens, maxForks could safely increase. Neither should change independently.

3. **Rate-limit window alignment creates a natural BASE_DELAY floor**: Any BASE_DELAY shorter than the rate-limit reset window's granularity guarantees wasted retries. The optimal BASE_DELAY is `ceil(reset_window / 2)` — long enough that first retry *might* clear the window, short enough that it doesn't dominate the budget. For 10s reset windows, this suggests BASE=5s; for 60s windows, BASE=30s (but 30s is too aggressive for the first retry). The current 2s is optimal only for <5s reset windows.

4. **The retry budget and the global deadline operate on different scales**: Per-test retry budget (~62s) protects individual tests. The global `SDK_EVAL_MAX_DURATION_MS` (60min) protects cumulative cost. A pathological suite where every test hits max retries would consume 62s × N_tests in pure delay, but this is bounded by the global deadline. The two mechanisms are complementary — neither subsumes the other.

5. **Backoff cap (MAX_DELAY_MS=60s) is never actually reached**: With 5 delays (attempts 0–4), the maximum un-jittered delay is 32s at attempt 4. The 60s cap is dead code under current parameters. It would activate only at attempt 5+ (retries ≥ 6). This is fine as a safety net but could create false confidence about the cap's role.

## Summary

The CRUX harness backoff parameters are more conservative than their documentation suggests — the actual worst-case delay budget is **62s nominal (53–71s with jitter)**, not the 122s stated in memory `6265f8f`, due to an off-by-one in the delay count. This leaves 75%+ of the 300s test timeout for actual operations. The ±15% jitter is adequate for the current `maxForks: 2` ceiling but would need widening to ±50% or decorrelated jitter at 4+ forks (collision probability jumps from 10% to 56%). The 2s base delay likely wastes the first 1–2 retry attempts against typical 10–60s rate-limit reset windows; a base of 5s with 4 retries would maintain the same total budget while reducing wasted attempts. The MAX_DELAY cap of 60s is effectively unreachable under current parameters. Most importantly, the shared-agent-runs-per-describe-block pattern is a structural enabler for the narrow jitter — without it, effective concurrency would exceed what ±15% jitter can safely desynchronise.
