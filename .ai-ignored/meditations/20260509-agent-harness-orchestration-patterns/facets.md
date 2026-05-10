---
topic: "agent harness orchestration patterns"
created: 2026-05-09T19:29:00+10:00
depth: 0
---

# Meditation Facets: Agent Harness Orchestration Patterns

## Parent Context

Exploring agent harness orchestration patterns — how multi-agent systems coordinate execution, manage state handoff, handle failures, and bound recursion in LLM-based tooling environments like Cursor.

## Facet Partitioning

The topic "agent harness orchestration patterns" naturally decomposes into three complementary concerns: the mechanisms by which agents share data and coordinate (the plumbing), the strategies for coping when parts of the system fail (the resilience), and the constraints that keep the system efficient and bounded (the governance). These three dimensions are orthogonal — each can be explored deeply without needing the others, yet together they fully characterize what makes an agent harness work.

## Facets

### Facet 1: State Coordination and Handoff Mechanisms

How do multi-agent systems pass state, context, and results between parent and child agents? This encompasses file-based coordination protocols (predictable paths, polling for existence, frontmatter contracts), message-based approaches (in-context returns, transcript parsing), session-scope inheritance (flags, config propagation to subagents), and the serialization formats that make inter-agent data exchange reliable.

### Facet 2: Failure Handling and Resilience in Multi-Agent Workflows

How do agent harnesses detect, recover from, and adapt to partial failures when one or more agents in a parallel or sequential workflow crash, hang, produce malformed output, or hit rate limits? This covers retry strategies (exponential backoff, jitter), timeout and hang detection, graceful degradation when a branch fails, the boundary between automatic recovery and user escalation, and adversarial verification as a failure-catching mechanism.

### Facet 3: Resource Governance and Bounded Execution

How do agent harnesses manage computational resources, control costs, and prevent unbounded growth? This includes recursion depth limits, concurrency caps (fan-out width, max parallel agents), cost-aware execution gating (skip-by-default for expensive operations), wall-clock deadlines, and the design patterns that trade off exploration breadth against resource consumption in LLM-powered multi-agent systems.
