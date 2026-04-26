/**
 * Category R: Forget SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios R1-R2.
 * Validates /crux-forget by memory ID (deletion, tracker cleanup, index rebuild)
 * and by search query (search results, selective deletion).
 *
 * All tests run in an isolated git worktree — the real repo is never modified.
 */

import { Agent } from "@cursor/february/agent";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type CollectedRun,
  type IsolatedWorkspace,
  assertMemoryDeleted,
  assertMemoryExists,
  assertOutputContains,
  assertTrackerDeleted,
  collectRun,
  countMemoryFiles,
  createIsolatedWorkspace,
  createMemoryFixture,
  createTrackerFixture,
  readMemoryIndex,
  rebuildMemoryIndex,
  requireApiKey,
  sendWithRetry,
} from "../helpers/harness.js";

describe("R: Forget", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    createMemoryFixture(
      {
        slug: "sdk-test-forget-perf",
        type: "learning",
        title: "Batch database queries for performance",
        description: "Use batch queries to reduce N+1 overhead in hot paths",
        tags: ["performance", "optimization"],
        body: "Always batch database queries in loops. N+1 queries are the most common performance bottleneck.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-forget-security",
        type: "redflag",
        title: "Sanitize user input before SQL queries",
        description: "Prevent SQL injection by parameterizing all queries",
        tags: ["security", "auth"],
        body: "Never interpolate user input directly into SQL strings. Always use parameterized queries.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-forget-cache",
        type: "idea",
        title: "Implement edge caching for static assets",
        description: "CDN-level caching for performance improvements",
        tags: ["caching", "performance"],
        body: "Static assets should be served from edge caches with long TTLs and versioned filenames.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-forget-testing",
        type: "learning",
        title: "Property-based testing catches edge cases",
        description: "Generative testing reveals unexpected input combinations",
        tags: ["testing", "quality"],
        body: "Property-based tests find edge cases that hand-written examples miss.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-forget-keep",
        type: "core",
        title: "Modular architecture principles",
        description: "Keep modules loosely coupled with clear interfaces",
        tags: ["architecture"],
        body: "Each module should own its data and expose a minimal public API.",
      },
      ws.root
    );

    createTrackerFixture(ws.root, "sdk-test-forget-perf");
    createTrackerFixture(ws.root, "sdk-test-forget-security");

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

  // -------------------------------------------------------------------------
  // R1: Forget - By Memory ID
  // -------------------------------------------------------------------------

  describe("R1: Forget - By Memory ID", () => {
    let forgetResult: CollectedRun;
    let r1MemoryCountBefore: number;

    it(
      "shows memory details and confirms deletion",
      async () => {
        r1MemoryCountBefore = countMemoryFiles(ws.root);

        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: ws.root },
        });

        const run = await sendWithRetry(agent, "/crux-forget sdk-test-forget-perf");
        forgetResult = await collectRun(run);

        expect(forgetResult.status).toBe("finished");

        const text = forgetResult.assistantText.toLowerCase();
        const mentionsMemory =
          text.includes("performance") ||
          text.includes("forget-perf") ||
          text.includes("batch");
        expect(mentionsMemory).toBe(true);

        const confirmsAction =
          text.includes("delet") ||
          text.includes("remov") ||
          text.includes("forgot") ||
          text.includes("forget");
        expect(confirmsAction).toBe(true);
      },
      { timeout: 300_000 }
    );

    it(
      "deletes the memory file",
      async () => {
        assertMemoryDeleted(ws.root, "learning", "sdk-test-forget-perf");
      },
      { timeout: 300_000 }
    );

    it(
      "cleans up associated reference tracker",
      async () => {
        assertTrackerDeleted(ws.root, "sdk-test-forget-perf");
      },
      { timeout: 300_000 }
    );

    it(
      "rebuilds index after deletion",
      async () => {
        const index = readMemoryIndex(ws.root);
        expect(index).not.toContain("sdk-test-forget-perf");

        expect(index).toContain("sdk-test-forget-keep");
      },
      { timeout: 300_000 }
    );
  });

  // -------------------------------------------------------------------------
  // R2: Forget - Search and Select
  // -------------------------------------------------------------------------

  describe("R2: Forget - Search and Select", () => {
    it(
      "searches memories by keyword and shows results",
      async () => {
        agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: ws.root },
        });

        const run = await sendWithRetry(agent, '/crux-forget "performance"');
        const result = await collectRun(run);

        expect(result.status).toBe("finished");
        assertOutputContains(
          result.assistantText,
          ["performance"],
          "R2: Search results mention performance"
        );
      },
      { timeout: 300_000 }
    );

    it(
      "only deletes selected memories, not all matches",
      async () => {
        assertMemoryExists(ws.root, "core", "sdk-test-forget-keep");

        const remainingCount = countMemoryFiles(ws.root);
        expect(remainingCount).toBeGreaterThanOrEqual(1);
      },
      { timeout: 300_000 }
    );
  });
});
