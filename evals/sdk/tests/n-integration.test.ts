/**
 * Category N: Cross-Platform Integration SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenario N1 (Cursor full flow).
 * Multi-turn integration test exercising the complete CRUX Memories command
 * chain in a single agent session: Dream → Recall → Remember → Forget → Amnesia.
 *
 * GATED behind SDK_EVAL_SKIP_EXPENSIVE (default: skip).
 * Run explicitly: SDK_EVAL_SKIP_EXPENSIVE=false pnpm test:integration
 *
 * All tests run in an isolated git worktree — the real repo is never modified.
 */

import { Agent } from "@cursor/february/agent";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type CollectedRun,
  type IsolatedWorkspace,
  assertOutputContains,
  collectRun,
  countMemoryFiles,
  createIsolatedWorkspace,
  createMemoryFixture,
  createSpecFixture,
  listMemoryFiles,
  readMemoryIndex,
  rebuildMemoryIndex,
  requireApiKey,
  sendWithRetry,
} from "../helpers/harness.js";

const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";

describe.skipIf(skipExpensive)("N: Cross-Platform Integration", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;
  let initialMemoryCount: number;
  let initialMemoryFiles: string[];

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    createSpecFixture(ws.root, "20260420-test-feature");

    createMemoryFixture(
      {
        slug: "sdk-test-integ-resilience",
        type: "learning",
        title: "Circuit breakers prevent cascading failures",
        description: "Use circuit breaker pattern for external service calls",
        tags: ["resilience", "patterns", "api"],
        body: "Wrap external service calls in circuit breakers to prevent cascading failures during outages.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-integ-testing",
        type: "core",
        title: "Contract tests validate API boundaries",
        description: "Consumer-driven contracts catch integration issues early",
        tags: ["testing", "api", "contracts"],
        body: "Use consumer-driven contract tests to verify API compatibility between services.",
        strength: 4,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-integ-observability",
        type: "idea",
        title: "Structured logging with correlation IDs",
        description: "Trace requests across services with correlation IDs in structured logs",
        tags: ["observability", "logging", "tracing"],
        body: "Inject correlation IDs at the API gateway and propagate through all downstream service calls.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-integ-security",
        type: "redflag",
        title: "Never expose internal error details to clients",
        description: "Sanitize error responses to prevent information leakage",
        tags: ["security", "errors", "api"],
        body: "Return generic error messages to clients; log full details server-side only.",
        strength: 5,
      },
      ws.root
    );

    rebuildMemoryIndex(ws.root);

    initialMemoryCount = countMemoryFiles(ws.root);
    initialMemoryFiles = listMemoryFiles(ws.root);

    agent = Agent.create({
      apiKey: getApiKey(),
      model: { id: "composer-2" },
      local: { cwd: ws.root },
    });
  }, 60_000);

  afterAll(async () => {
    if (agent) {
      await agent[Symbol.asyncDispose]();
    }
    ws.cleanup();
  });

  // ---------------------------------------------------------------------------
  // N1.1: Dream extracts memories from completed spec
  // ---------------------------------------------------------------------------

  it(
    "N1.1: Dream extracts memories from completed spec",
    async () => {
      const run = await sendWithRetry(
        agent,
        "/crux-dream 20260420-test-feature — accept all candidate facts and write the dream summary"
      );
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const hasCandidateLanguage =
        /candidate|fact|extract|finding|insight|observation|memor/i.test(
          result.assistantText
        );
      const hasTypeLabels =
        /\[?(learning|redflag|red.flag|idea|goal|core)\]?/i.test(
          result.assistantText
        );
      expect(hasCandidateLanguage || hasTypeLabels).toBe(true);

      const postDreamCount = countMemoryFiles(ws.root);
      const postDreamFiles = listMemoryFiles(ws.root);
      const newFiles = postDreamFiles.filter(
        (f) => !initialMemoryFiles.includes(f)
      );

      expect(
        postDreamCount > initialMemoryCount || newFiles.length > 0
      ).toBe(true);
    },
    { timeout: 180_000 }
  );

  // ---------------------------------------------------------------------------
  // N1.2: Recall retrieves memories including dreamed ones
  // ---------------------------------------------------------------------------

  it(
    "N1.2: Recall retrieves memories including dreamed ones",
    async () => {
      const run = await sendWithRetry(agent, "/crux-recall");
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const text = result.assistantText.toLowerCase();
      const mentionsMemory =
        text.includes("memory") || text.includes("recall");
      expect(mentionsMemory).toBe(true);

      const hasStructuredFormat =
        /\[?(core|learning|redflag|idea|goal)\]?/i.test(
          result.assistantText
        ) ||
        /##\s*(core|learning|redflag|goal|idea)/i.test(
          result.assistantText
        ) ||
        /\|.*\|.*\|/.test(result.assistantText) ||
        /`(core|learning|redflag)`/.test(result.assistantText);
      expect(hasStructuredFormat).toBe(true);
    },
    { timeout: 120_000 }
  );

  // ---------------------------------------------------------------------------
  // N1.3: Remember creates ad-hoc memory
  // ---------------------------------------------------------------------------

  it(
    "N1.3: Remember creates ad-hoc memory",
    async () => {
      const beforeRememberFiles = listMemoryFiles(ws.root);

      const run = await sendWithRetry(
        agent,
        '/crux-remember "Integration test: always verify state continuity across agent turns" --type learning'
      );
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const text = result.assistantText.toLowerCase();
      const confirmsCreation =
        text.includes("created") ||
        text.includes("saved") ||
        text.includes("stored") ||
        text.includes("memory") ||
        text.includes("remember");
      expect(confirmsCreation).toBe(true);

      const afterRememberFiles = listMemoryFiles(ws.root);
      const newFiles = afterRememberFiles.filter(
        (f) => !beforeRememberFiles.includes(f)
      );
      expect(newFiles.length).toBeGreaterThanOrEqual(1);

      const learningFiles = newFiles.filter((f) =>
        f.includes("/learning/")
      );
      expect(learningFiles.length).toBeGreaterThanOrEqual(1);
    },
    { timeout: 120_000 }
  );

  // ---------------------------------------------------------------------------
  // N1.4: Forget deletes the just-created memory
  // ---------------------------------------------------------------------------

  it(
    "N1.4: Forget deletes the just-created memory",
    async () => {
      const beforeForgetCount = countMemoryFiles(ws.root);

      const run = await sendWithRetry(
        agent,
        '/crux-forget "state continuity"'
      );
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const text = result.assistantText.toLowerCase();
      const confirmsAction =
        text.includes("delet") ||
        text.includes("remov") ||
        text.includes("forgot") ||
        text.includes("forget");
      expect(confirmsAction).toBe(true);

      const afterForgetCount = countMemoryFiles(ws.root);
      expect(afterForgetCount).toBeLessThan(beforeForgetCount);

      const index = readMemoryIndex(ws.root);
      expect(index.toLowerCase()).not.toContain("state continuity");
    },
    { timeout: 120_000 }
  );

  // ---------------------------------------------------------------------------
  // N1.5: Amnesia toggles correctly after full flow
  // ---------------------------------------------------------------------------

  it(
    "N1.5: Amnesia toggles correctly after full flow",
    async () => {
      const run = await sendWithRetry(agent, "/crux-amnesia on");
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const text = result.assistantText.toLowerCase();
      const confirmsActive =
        (text.includes("amnesia") &&
          (text.includes("on") ||
            text.includes("enabled") ||
            text.includes("active"))) ||
        text.includes("suppress");
      expect(confirmsActive).toBe(true);
    },
    { timeout: 120_000 }
  );
});
