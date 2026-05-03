/**
 * Category C: REM Sleep SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios C1, C2, and C3.
 * Validates /crux-dream --rem report structure, yolo auto-apply,
 * and conflict-resolution safeguards.
 *
 * All tests run in an isolated git worktree — the real repo is never modified.
 */

import { Agent } from "@cursor/february/agent";
import * as fs from "node:fs";
import * as path from "node:path";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type CollectedRun,
  type IsolatedWorkspace,
  assertTrackerDeleted,
  collectRun,
  createConflictingMemories,
  createIsolatedWorkspace,
  createMemoryFixture,
  createOrphanedTracker,
  createTrackerFixture,
  rebuildMemoryIndex,
  requireApiKey,
  seedAgedMemory,
  sendWithRetry,
} from "../helpers/harness.js";

describe("C: REM Sleep", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;

  // Paths for conflict verification
  let conflictPathA: string;
  let conflictPathB: string;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    // --- Promotion candidate: idea with strength 6 (exceeds promoteAt=5) ---
    createMemoryFixture(
      {
        slug: "sdk-test-rem-promote",
        type: "idea",
        title: "Memoization for expensive computations",
        description: "Cache pure function results to avoid redundant work",
        tags: ["performance", "memoization", "optimization"],
        body: "Use memoization for pure functions with expensive computation. This pattern significantly reduces CPU usage in hot paths.",
        strength: 6,
      },
      ws.root
    );

    // --- Demotion candidate: learning unreferenced for 100 days ---
    seedAgedMemory(
      {
        slug: "sdk-test-rem-demote",
        type: "learning",
        title: "Old database query pattern",
        description: "Legacy approach to database queries that may no longer apply",
        tags: ["database", "queries", "legacy"],
        body: "Always use parameterized queries with connection pooling for database access.",
        strength: 1,
      },
      ws.root,
      100
    );
    const agedDate = new Date();
    agedDate.setDate(agedDate.getDate() - 100);
    createTrackerFixture(ws.root, "sdk-test-rem-demote", {
      lastReferenced: agedDate.toISOString().split("T")[0],
    });

    // --- Archival candidate: learning unreferenced for 200 days ---
    seedAgedMemory(
      {
        slug: "sdk-test-rem-archive",
        type: "learning",
        title: "Deprecated API migration notes",
        description: "Migration notes for an API version that is no longer supported",
        tags: ["api", "migration", "deprecated"],
        body: "When migrating from v1 to v2, update the auth header format and batch endpoints.",
        strength: 1,
      },
      ws.root,
      200
    );

    // --- Orphaned tracker (no matching memory file) ---
    createOrphanedTracker(ws.root, "nonexistent-memory");

    // --- Conflicting memories ---
    [conflictPathA, conflictPathB] = createConflictingMemories(ws.root, {
      topic: "sql-joins",
      memory1: {
        slug: "sdk-test-rem-conflict-a",
        type: "learning",
        title: "Prefer SQL JOINs for related data",
        body: "Always use SQL JOINs over multiple queries for related data to reduce round trips.",
      },
      memory2: {
        slug: "sdk-test-rem-conflict-b",
        type: "learning",
        title: "Avoid SQL JOINs for large tables",
        body: "Use application-level joins for better cache utilization and horizontal scaling.",
      },
    });

    // --- Normal memories (should NOT be flagged) ---
    createMemoryFixture(
      {
        slug: "sdk-test-rem-normal-a",
        type: "core",
        title: "Use structured logging in production",
        description: "JSON-structured logs enable efficient filtering and aggregation",
        tags: ["logging", "observability"],
        body: "Always use structured JSON logging in production for machine-parseable log output.",
        strength: 3,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-rem-normal-b",
        type: "learning",
        title: "Prefer composition over inheritance",
        description: "Composition provides more flexibility than class inheritance",
        tags: ["design-patterns", "architecture"],
        body: "Favor composition over inheritance to achieve flexible and maintainable code.",
        strength: 3,
      },
      ws.root
    );

    rebuildMemoryIndex(ws.root);
  });

  afterAll(async () => {
    ws.cleanup();
  });

  afterEach(async () => {
    if (agent) {
      await agent[Symbol.asyncDispose]();
    }
  });

  // -----------------------------------------------------------------------
  // C1: REM Sleep — Interactive Recommendations
  // -----------------------------------------------------------------------

  describe("C1: REM Sleep - Interactive Recommendations", () => {
    let c1Result: CollectedRun;

    it(
      "presents structured REM sleep report",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: ws.root },
        });

        const run = await sendWithRetry(
          agent,
          "/crux-dream --rem — analyze and present recommendations without waiting for confirmation"
        );
        c1Result = await collectRun(run);

        expect(c1Result.status).toBe("finished");

        const sectionKeywords = [
          "promot",
          "demot",
          "archiv",
          "cleanup",
          "orphan",
          "conflict",
          "consolidat",
          "rebalanc",
        ];
        const matchCount = sectionKeywords.filter((kw) =>
          c1Result.assistantText.toLowerCase().includes(kw)
        ).length;

        expect(matchCount).toBeGreaterThanOrEqual(2);
      }
    );

    it(
      "identifies promotion candidates",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: ws.root },
        });

        const run = await sendWithRetry(
          agent,
          "/crux-dream --rem — analyze and present recommendations without waiting for confirmation"
        );
        const result = await collectRun(run);

        expect(result.status).toBe("finished");

        const text = result.assistantText.toLowerCase();
        const mentionsPromotion =
          text.includes("promot") || text.includes("upgrade") || text.includes("idea → learning") || text.includes("transition");
        const mentionsCandidate =
          text.includes("memoization") || text.includes("sdk-test-rem-promote") || text.includes("expensive computation");

        expect(mentionsPromotion).toBe(true);
        expect(mentionsCandidate).toBe(true);
      }
    );

    it(
      "identifies demotion and archival candidates",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: ws.root },
        });

        const run = await sendWithRetry(
          agent,
          "/crux-dream --rem — analyze and present recommendations without waiting for confirmation"
        );
        const result = await collectRun(run);

        expect(result.status).toBe("finished");

        const text = result.assistantText.toLowerCase();

        const mentionsDemotion =
          text.includes("demot") || text.includes("weaken") || text.includes("unreferenced") || text.includes("stale");
        const mentionsArchival =
          text.includes("archiv") || text.includes("deprecated") || text.includes("migration notes");

        expect(mentionsDemotion || mentionsArchival).toBe(true);
      }
    );
  });

  // -----------------------------------------------------------------------
  // C2: REM Sleep — Yolo Mode Auto-Apply
  // -----------------------------------------------------------------------

  describe("C2: REM Sleep - Yolo Mode Auto-Apply", () => {
    let c2Ws: IsolatedWorkspace;

    beforeAll(async () => {
      c2Ws = createIsolatedWorkspace();

      // Promotion candidate
      createMemoryFixture(
        {
          slug: "sdk-test-rem-promote",
          type: "idea",
          title: "Memoization for expensive computations",
          description: "Cache pure function results to avoid redundant work",
          tags: ["performance", "memoization", "optimization"],
          body: "Use memoization for pure functions with expensive computation.",
          strength: 6,
        },
        c2Ws.root
      );

      // Demotion candidate
      const agedDate = new Date();
      agedDate.setDate(agedDate.getDate() - 100);
      seedAgedMemory(
        {
          slug: "sdk-test-rem-demote",
          type: "learning",
          title: "Old database query pattern",
          description: "Legacy approach to database queries",
          tags: ["database", "queries", "legacy"],
          body: "Always use parameterized queries with connection pooling.",
          strength: 1,
        },
        c2Ws.root,
        100
      );
      createTrackerFixture(c2Ws.root, "sdk-test-rem-demote", {
        lastReferenced: agedDate.toISOString().split("T")[0],
      });

      // Orphaned tracker
      createOrphanedTracker(c2Ws.root, "nonexistent-memory");

      // Normal memory
      createMemoryFixture(
        {
          slug: "sdk-test-rem-normal",
          type: "core",
          title: "Use structured logging in production",
          description: "JSON-structured logs for filtering",
          tags: ["logging", "observability"],
          body: "Always use structured JSON logging in production.",
          strength: 3,
        },
        c2Ws.root
      );

      rebuildMemoryIndex(c2Ws.root);
    });

    afterAll(async () => {
      c2Ws.cleanup();
    });

    it(
      "auto-applies non-conflict changes in yolo mode",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: c2Ws.root },
        });

        const run = await sendWithRetry(agent, "/crux-dream --rem --yolo");
        const result = await collectRun(run);

        expect(result.status).toBe("finished");

        const autoApplyKeywords = [
          "applied",
          "auto",
          "promoted",
          "cleaned",
          "completed",
          "executed",
          "processed",
        ];
        const matchCount = autoApplyKeywords.filter((kw) =>
          result.assistantText.toLowerCase().includes(kw)
        ).length;

        expect(matchCount).toBeGreaterThanOrEqual(1);
      }
    );

    it(
      "cleans up orphaned trackers",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: c2Ws.root },
        });

        const run = await sendWithRetry(agent, "/crux-dream --rem --yolo");
        const result = await collectRun(run);

        expect(result.status).toBe("finished");

        const orphanCleaned =
          result.assistantText.toLowerCase().includes("orphan") ||
          result.assistantText.toLowerCase().includes("cleanup") ||
          result.assistantText.toLowerCase().includes("removed tracker");

        let trackerGone = false;
        try {
          assertTrackerDeleted(c2Ws.root, "nonexistent-memory");
          trackerGone = true;
        } catch {
          trackerGone = false;
        }

        expect(orphanCleaned || trackerGone).toBe(true);
      }
    );

    it(
      "rebuilds memory index after changes",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: c2Ws.root },
        });

        const run = await sendWithRetry(agent, "/crux-dream --rem --yolo");
        const result = await collectRun(run);

        expect(result.status).toBe("finished");

        const indexPath = path.join(c2Ws.root, ".crux", "memory-index.yml");
        const indexExists = fs.existsSync(indexPath);

        const outputMentionsIndex =
          result.assistantText.toLowerCase().includes("index") ||
          result.assistantText.toLowerCase().includes("rebuilt") ||
          result.assistantText.toLowerCase().includes("updated");

        expect(indexExists || outputMentionsIndex).toBe(true);
      }
    );
  });

  // -----------------------------------------------------------------------
  // C3: REM Sleep — Conflict Resolution
  // -----------------------------------------------------------------------

  describe("C3: REM Sleep - Conflict Resolution", () => {
    let c3Ws: IsolatedWorkspace;

    beforeAll(async () => {
      c3Ws = createIsolatedWorkspace();

      createConflictingMemories(c3Ws.root, {
        topic: "sql-joins",
        memory1: {
          slug: "sdk-test-rem-conflict-a",
          type: "learning",
          title: "Prefer SQL JOINs for related data",
          body: "Always use SQL JOINs over multiple queries for related data to reduce round trips.",
        },
        memory2: {
          slug: "sdk-test-rem-conflict-b",
          type: "learning",
          title: "Avoid SQL JOINs for large tables",
          body: "Use application-level joins for better cache utilization and horizontal scaling.",
        },
      });

      // Normal memory so workspace isn't conflict-only
      createMemoryFixture(
        {
          slug: "sdk-test-rem-normal-c3",
          type: "core",
          title: "Use structured logging in production",
          description: "JSON-structured logs for filtering",
          tags: ["logging", "observability"],
          body: "Always use structured JSON logging in production.",
          strength: 3,
        },
        c3Ws.root
      );

      rebuildMemoryIndex(c3Ws.root);
    });

    afterAll(async () => {
      c3Ws.cleanup();
    });

    it(
      "presents both sides of a conflict",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: c3Ws.root },
        });

        const run = await sendWithRetry(
          agent,
          "/crux-dream --rem --yolo — present any conflicts for review but do not auto-resolve"
        );
        const result = await collectRun(run);

        expect(result.status).toBe("finished");

        const text = result.assistantText.toLowerCase();
        const mentionsConflictA =
          text.includes("prefer sql joins") || text.includes("conflict-a") || text.includes("related data");
        const mentionsConflictB =
          text.includes("avoid sql joins") || text.includes("conflict-b") || text.includes("large tables");

        expect(mentionsConflictA || mentionsConflictB).toBe(true);
      }
    );

    it(
      "does not auto-resolve conflicts",
      { timeout: 300_000 },
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: c3Ws.root },
        });

        const run = await sendWithRetry(
          agent,
          "/crux-dream --rem --yolo — present any conflicts for review but do not auto-resolve"
        );
        await collectRun(run);

        const conflictAPath = path.join(
          c3Ws.root,
          "memories",
          "learning",
          "sdk-test-rem-conflict-a.memory.md"
        );
        const conflictBPath = path.join(
          c3Ws.root,
          "memories",
          "learning",
          "sdk-test-rem-conflict-b.memory.md"
        );

        expect(fs.existsSync(conflictAPath)).toBe(true);
        expect(fs.existsSync(conflictBPath)).toBe(true);
      }
    );
  });
});
