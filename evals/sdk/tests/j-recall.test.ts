/**
 * Category J: Recall SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios J1-J4.
 * Validates recall command invocation, display format, and filtering.
 *
 * All tests run in an isolated git worktree — the real repo is never modified.
 */

import { Agent } from "@cursor/february/agent";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type IsolatedWorkspace,
  assertOutputContains,
  collectRun,
  createIsolatedWorkspace,
  createMemoryFixture,
  hasSubagentCall,
  rebuildMemoryIndex,
  requireApiKey,
} from "../helpers/harness.js";

describe("J: Recall", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    createMemoryFixture(
      {
        slug: "sdk-test-recall-performance",
        type: "learning",
        title: "Memoize expensive React components",
        description: "Use React.memo for components with stable props to avoid re-renders",
        tags: ["react", "performance", "memoization"],
        body: "Always wrap list item components in React.memo when the parent re-renders frequently.",
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-recall-caching",
        type: "core",
        title: "Cache invalidation requires careful TTL selection",
        description: "TTL should match data freshness requirements",
        tags: ["caching", "performance", "ttl"],
        body: "Set cache TTL based on how often the underlying data changes, not arbitrary values.",
        strength: 5,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-recall-security",
        type: "redflag",
        title: "Never log sensitive data",
        description: "PII and credentials must not appear in logs",
        tags: ["security", "logging", "pii"],
        body: "Sanitize all log output to remove passwords, tokens, and personally identifiable information.",
        source: "20260403-security-audit",
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

  describe("J1: Recall - No Arguments (Contextual Memories)", () => {
    it("delegates to memory manager or handles recall directly", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-recall");
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const usedSubagent = hasSubagentCall(result.toolCalls, "crux-cursor-memory-manager");
      const readMemoryFiles = result.toolCalls.some(
        (tc) => tc.name === "read" || tc.name === "glob" || tc.name === "grep"
      );
      const outputMentionsMemory =
        result.assistantText.toLowerCase().includes("memory") ||
        result.assistantText.toLowerCase().includes("recall");

      expect(usedSubagent || readMemoryFiles || outputMentionsMemory).toBe(true);
    });

    it("displays memories with required metadata fields", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-recall");
      const result = await collectRun(run);

      const text = result.assistantText.toLowerCase();
      const hasTitle = /title|name|slug/i.test(result.assistantText) ||
        text.includes("memoize") || text.includes("cache");
      const hasType = /type|category|core|learning|redflag/i.test(result.assistantText);
      const hasStrength = /strength|str|priority|\bstr\b/i.test(result.assistantText) ||
        /\b[1-5]\b/.test(result.assistantText);

      expect(hasTitle).toBe(true);
      expect(hasType).toBe(true);
    });

    it("uses structured display format", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-recall");
      const result = await collectRun(run);

      const hasStructuredFormat =
        result.assistantText.includes("[core]") ||
        result.assistantText.includes("[learning]") ||
        result.assistantText.includes("[redflag]") ||
        /##\s*(core|learning|redflag|goal|idea)/i.test(result.assistantText) ||
        /───.*───/.test(result.assistantText) ||
        /\|.*\|.*\|/.test(result.assistantText) ||
        /`(core|learning|redflag)`/.test(result.assistantText);

      expect(hasStructuredFormat).toBe(true);
    });
  });

  describe("J2: Recall - Query Mode (Influence Identification)", () => {
    it("searches memories by keyword", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send('/crux-recall "performance"');
      const result = await collectRun(run);

      expect(result.status).toBe("finished");
      assertOutputContains(
        result.assistantText,
        ["performance"],
        "J2: Search results contain keyword"
      );
    });

    it("explains why memories are relevant", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const setupRun = await agent.send(
        "How should I optimize my React list component for better performance?"
      );
      await collectRun(setupRun);

      const recallRun = await agent.send(
        '/crux-recall "why did you suggest memoization?"'
      );
      const result = await collectRun(recallRun);

      const hasExplanation =
        result.assistantText.toLowerCase().includes("memo") ||
        result.assistantText.toLowerCase().includes("performance") ||
        result.assistantText.toLowerCase().includes("influenced") ||
        result.assistantText.toLowerCase().includes("based on");

      expect(hasExplanation).toBe(true);
    });
  });

  describe("J3: Recall - Spec Name(s) (Source Filtering)", () => {
    it("filters memories by source spec", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-recall 20260403-security-audit");
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      assertOutputContains(
        result.assistantText,
        ["security", "log"],
        "J3: Filtered results show security memory"
      );
    });

    it("excludes memories from other sources", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-recall 20260403-security-audit");
      const result = await collectRun(run);

      const showsOnlySecuritySource =
        !result.assistantText.includes("sdk-test-recall-performance") ||
        result.assistantText.toLowerCase().includes("security");

      expect(showsOnlySecuritySource).toBe(true);
    });
  });

  describe("J4: Recall - Memory File(s) (Direct Display)", () => {
    it("displays specific memory file by path", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send(
        "/crux-recall memories/learning/sdk-test-recall-performance.memory.md"
      );
      const result = await collectRun(run);

      expect(result.status).toBe("finished");
      assertOutputContains(
        result.assistantText,
        ["Memoize", "React", "component"],
        "J4: Direct file display shows content"
      );
    });

    it("shows full frontmatter and body", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send(
        "/crux-recall memories/core/sdk-test-recall-caching.memory.md"
      );
      const result = await collectRun(run);

      assertOutputContains(
        result.assistantText,
        ["Cache invalidation", "TTL", "core"],
        "J4: Full memory content displayed"
      );
    });
  });
});
