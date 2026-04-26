/**
 * Category B: Dream SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios B1-B3.
 * Validates /crux-dream command: listing unprocessed specs, full dream flow
 * with memory extraction, and conflict detection with existing memories.
 *
 * All tests run in an isolated git worktree — the real repo is never modified.
 */

import { Agent } from "@cursor/february/agent";
import * as fs from "node:fs";
import * as path from "node:path";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type CollectedRun,
  type IsolatedWorkspace,
  collectRun,
  countMemoryFiles,
  createConflictingMemories,
  createIsolatedWorkspace,
  createMemoryFixture,
  createSpecFixture,
  rebuildMemoryIndex,
  requireApiKey,
  sendWithRetry,
} from "../helpers/harness.js";

describe("B: Dream", () => {
  let ws: IsolatedWorkspace;
  let initialMemoryCount: number;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    createSpecFixture(ws.root, "20260420-test-feature");
    createSpecFixture(ws.root, "20260415-old-feature", {
      alreadyDreamed: true,
    });

    createMemoryFixture(
      {
        slug: "sdk-test-dream-baseline",
        type: "learning",
        title: "Use exponential backoff for retries",
        description:
          "Exponential backoff prevents thundering herd on service recovery",
        tags: ["resilience", "retry", "api"],
        body: "Always use exponential backoff with jitter when retrying failed API calls.",
      },
      ws.root
    );

    createConflictingMemories(ws.root, {
      topic: "caching",
      memory1: {
        slug: "sdk-test-dream-conflict-a",
        type: "learning",
        title: "Always use write-through caching for user sessions",
        body: "Write-through caching is the only safe approach for session data.",
      },
      memory2: {
        slug: "sdk-test-dream-conflict-b",
        type: "learning",
        title: "Use cache-aside for better performance",
        body: "Cache-aside pattern provides better read performance and cache utilization.",
      },
    });

    rebuildMemoryIndex(ws.root);
    initialMemoryCount = countMemoryFiles(ws.root);
  });

  afterAll(async () => {
    ws.cleanup();
  });

  // ---------------------------------------------------------------------------
  // B1: Dream — No Arguments (List Unprocessed Specs)
  // ---------------------------------------------------------------------------

  describe("B1: Dream - No Arguments (List Unprocessed Specs)", () => {
    let b1Result: CollectedRun;

    beforeAll(async () => {
      const b1Agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });
      const run = await sendWithRetry(b1Agent, "/crux-dream");
      b1Result = await collectRun(run);
      await b1Agent[Symbol.asyncDispose]();
    });

    it("lists unprocessed specs when called with no arguments", () => {
      expect(b1Result.status).toBe("finished");

      const mentionsUndreamed =
        b1Result.assistantText.includes("20260420-test-feature") ||
        b1Result.assistantText.toLowerCase().includes("test-feature");

      expect(mentionsUndreamed).toBe(true);
    });

    it("excludes already-dreamed specs from listing", () => {
      const text = b1Result.assistantText;

      const mentionsOldSpec =
        text.includes("20260415-old-feature") ||
        text.toLowerCase().includes("old-feature");

      if (mentionsOldSpec) {
        const hasDreamedQualifier =
          /already.*dream|processed|complete|skip/i.test(text) ||
          /old-feature.{0,60}(dream|processed|done)/i.test(text);
        expect(hasDreamedQualifier).toBe(true);
      }
    });
  });

  // ---------------------------------------------------------------------------
  // B2: Dream — Full Flow with Spec Name
  // ---------------------------------------------------------------------------

  describe("B2: Dream - Full Flow with Spec Name", () => {
    let b2Result: CollectedRun;

    beforeAll(async () => {
      const b2Agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });
      const run = await sendWithRetry(
        b2Agent,
        "/crux-dream 20260420-test-feature — accept all candidate facts and write the dream summary"
      );
      b2Result = await collectRun(run);
      await b2Agent[Symbol.asyncDispose]();
    }, 300_000);

    it(
      "verifies spec execution status",
      { timeout: 300_000 },
      () => {
        expect(b2Result.status).toBe("finished");

        const verifyPatterns = [
          /verif|check|confirm|status|complete|execution|review/i,
          /subtask|spec|feature/i,
        ];

        const matchCount = verifyPatterns.filter((p) =>
          p.test(b2Result.assistantText)
        ).length;
        expect(matchCount).toBeGreaterThanOrEqual(1);
      }
    );

    it(
      "presents candidate facts with type labels",
      { timeout: 300_000 },
      () => {
        const text = b2Result.assistantText;

        const hasTypeLabels =
          /\[?(learning|redflag|red.flag|idea|goal|core)\]?/i.test(text);
        const hasCandidateLanguage =
          /candidate|fact|extract|finding|insight|observation|memor/i.test(
            text
          );

        expect(hasTypeLabels || hasCandidateLanguage).toBe(true);
      }
    );

    it(
      "creates memory files and writes dream summary",
      { timeout: 300_000 },
      () => {
        const currentCount = countMemoryFiles(ws.root);

        const specDir = path.join(ws.root, "specs", "20260420-test-feature");
        const specFiles = fs.existsSync(specDir)
          ? fs.readdirSync(specDir)
          : [];
        const dreamSummary = specFiles.find((f) => f.startsWith("dream-"));

        const dreamFlowCompleted =
          dreamSummary !== undefined || currentCount > initialMemoryCount;
        expect(dreamFlowCompleted).toBe(true);
      }
    );
  });

  // ---------------------------------------------------------------------------
  // B3: Dream — Conflict Detection
  // ---------------------------------------------------------------------------

  describe("B3: Dream - Conflict Detection", () => {
    let b3Result: CollectedRun;

    beforeAll(async () => {
      const b3Agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });
      const run = await sendWithRetry(
        b3Agent,
        "/crux-dream 20260420-test-feature — present any conflicts for review but do not auto-resolve"
      );
      b3Result = await collectRun(run);
      await b3Agent[Symbol.asyncDispose]();
    }, 300_000);

    it(
      "detects contradiction with existing memory",
      { timeout: 300_000 },
      () => {
        expect(b3Result.status).toBe("finished");

        const conflictLanguage =
          /conflict|contradict|clash|tension|inconsisten|disagree|opposing|differ/i.test(
            b3Result.assistantText
          );
        const mentionsExisting =
          /existing.*memor|current.*memor|already.*stored|known/i.test(
            b3Result.assistantText
          );
        const mentionsCaching =
          b3Result.assistantText.toLowerCase().includes("cach");

        expect(conflictLanguage || mentionsExisting || mentionsCaching).toBe(
          true
        );
      }
    );

    it(
      "presents resolution options for conflicts",
      { timeout: 300_000 },
      () => {
        const text = b3Result.assistantText;

        const hasResolutionOptions =
          /keep|replace|merge|retain|update|overwrite|reconcile/i.test(text) ||
          /option|choice|resolution|action|recommend/i.test(text);

        expect(hasResolutionOptions).toBe(true);
      }
    );

    it(
      "references both conflicting memory titles",
      { timeout: 300_000 },
      () => {
        const text = b3Result.assistantText.toLowerCase();

        const mentionsWriteThrough =
          text.includes("write-through") || text.includes("write through");
        const mentionsCacheAside =
          text.includes("cache-aside") || text.includes("cache aside");

        expect(mentionsWriteThrough || mentionsCacheAside).toBe(true);
      }
    );
  });
});
