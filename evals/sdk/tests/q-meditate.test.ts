/**
 * Category Q: Meditate SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios Q1-Q3.
 * Validates /crux-meditate facet derivation, subagent spawning,
 * memory-referencing output, and clean session completion.
 *
 * GATED behind SDK_EVAL_SKIP_EXPENSIVE (default: skip).
 * Run explicitly: SDK_EVAL_SKIP_EXPENSIVE=false pnpm test:meditate
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
  createIsolatedWorkspace,
  createMemoryFixture,
  hasSubagentCall,
  rebuildMemoryIndex,
  requireApiKey,
  sendWithRetry,
} from "../helpers/harness.js";

const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";

describe.skipIf(skipExpensive)("Q: Meditate", () => {
  let ws: IsolatedWorkspace;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    // Performance / optimization memories
    createMemoryFixture(
      {
        slug: "sdk-test-meditate-memoization",
        type: "learning",
        title: "Memoize expensive computations in render paths",
        description:
          "React.memo and useMemo prevent unnecessary re-renders of heavy components",
        tags: ["performance", "react", "memoization"],
        body: "Wrap pure components with React.memo and derive expensive values with useMemo to avoid redundant work during re-renders.",
        strength: 4,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-meditate-caching",
        type: "core",
        title: "Cache invalidation requires careful TTL management",
        description:
          "TTL should match data freshness requirements; stale-while-revalidate improves perceived performance",
        tags: ["caching", "performance", "ttl", "invalidation"],
        body: "Choose cache TTL based on data change frequency. Use stale-while-revalidate to serve cached content while refreshing in the background.",
        strength: 5,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-meditate-lazy-loading",
        type: "idea",
        title: "Lazy-load below-the-fold content for faster initial paint",
        description:
          "Dynamic imports and IntersectionObserver defer non-critical resources",
        tags: ["performance", "lazy-loading", "ux"],
        body: "Use React.lazy with Suspense for route-level splitting. Apply IntersectionObserver for images and heavy widgets below the fold.",
        strength: 2,
      },
      ws.root
    );

    // Security memories
    createMemoryFixture(
      {
        slug: "sdk-test-meditate-input-validation",
        type: "redflag",
        title: "Always validate and sanitize user input at API boundaries",
        description:
          "Unvalidated input enables injection, XSS, and data corruption",
        tags: ["security", "validation", "input-sanitization"],
        body: "Validate all user-supplied data with schema validation (e.g. zod) at API boundaries. Never trust client-side validation alone.",
        strength: 4,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-meditate-auth-tokens",
        type: "learning",
        title: "Rotate auth tokens periodically and use short-lived JWTs",
        description:
          "Long-lived tokens increase blast radius of credential theft",
        tags: ["security", "auth", "jwt", "tokens"],
        body: "Issue short-lived JWTs (15-30 min) with refresh tokens. Implement token rotation so compromised refresh tokens are single-use.",
        strength: 3,
      },
      ws.root
    );

    // Architecture / design memories
    createMemoryFixture(
      {
        slug: "sdk-test-meditate-singleton",
        type: "learning",
        title: "Use singleton pattern for shared stateful services",
        description:
          "Database pools and config managers should be singletons to prevent resource leaks",
        tags: ["architecture", "singleton", "design-pattern"],
        body: "Implement singletons for connection pools, config managers, and event buses. Ensure thread-safe lazy initialization.",
        strength: 3,
      },
      ws.root
    );

    createMemoryFixture(
      {
        slug: "sdk-test-meditate-dependency-injection",
        type: "idea",
        title: "Adopt dependency injection for testable architecture",
        description:
          "DI decouples components and enables mocking in unit tests",
        tags: ["architecture", "dependency-injection", "testing"],
        body: "Use constructor injection for services. Leverage DI containers in larger codebases. This enables straightforward mocking and improves modularity.",
        strength: 2,
      },
      ws.root
    );

    // Testing / quality memory
    createMemoryFixture(
      {
        slug: "sdk-test-meditate-test-isolation",
        type: "core",
        title: "Ensure test isolation with independent fixtures",
        description:
          "Shared mutable state between tests causes flaky failures",
        tags: ["testing", "isolation", "quality"],
        body: "Each test should create its own fixtures and clean up after itself. Never rely on test execution order or shared mutable state.",
        strength: 4,
      },
      ws.root
    );

    rebuildMemoryIndex(ws.root);
  }, 60_000);

  afterAll(async () => {
    ws.cleanup();
  });

  // -----------------------------------------------------------------------
  // Q1: Meditate — No Arguments (Context-Derived Facets)
  // -----------------------------------------------------------------------

  describe("Q1: Meditate - No Arguments (Context-Derived Facets)", () => {
    let agent: Agent;
    let meditateResult: CollectedRun;

    beforeAll(async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      // Turn 1: establish performance optimization context
      const setupRun = await sendWithRetry(
        agent,
        "I'm working on optimizing a React app that has slow list rendering and excessive API calls. What patterns should I consider?"
      );
      await collectRun(setupRun);

      // Turn 2: invoke meditate with no args — should derive facets from context
      const meditateRun = await sendWithRetry(agent, "/crux-meditate");
      meditateResult = await collectRun(meditateRun);
    }, 480_000);

    afterAll(async () => {
      if (agent) {
        await agent[Symbol.asyncDispose]();
      }
    });

    it(
      "derives exploration facets from context",
      { timeout: 480_000 },
      () => {
        const hasFacets =
          /facet|theme|dimension|branch|direction|aspect|exploration/i.test(
            meditateResult.assistantText
          ) ||
          /(1\.|2\.|3\.|\(1\)|\(2\)|\(3\)|first|second|third)/i.test(
            meditateResult.assistantText
          );

        expect(hasFacets).toBe(true);
      }
    );

    it(
      "spawns subagents for recursive exploration",
      { timeout: 480_000 },
      () => {
        const taskCalls = meditateResult.toolCalls.filter(
          (tc) => tc.name === "Task"
        );
        const usedMemoryManager = hasSubagentCall(
          meditateResult.toolCalls,
          "crux-cursor-memory-manager"
        );

        expect(taskCalls.length >= 1 || usedMemoryManager).toBe(true);
      }
    );

    it(
      "references memories in consolidated output",
      { timeout: 480_000 },
      () => {
        const text = meditateResult.assistantText.toLowerCase();

        const referencesMemory =
          text.includes("memory") ||
          text.includes("memoiz") ||
          text.includes("cache") ||
          text.includes("lazy") ||
          text.includes("singleton");

        const hasConsolidation =
          /insight|finding|pattern|connection|theme|synthesis|consolidat/i.test(
            meditateResult.assistantText
          );

        expect(referencesMemory).toBe(true);
        expect(hasConsolidation).toBe(true);
      }
    );
  });

  // -----------------------------------------------------------------------
  // Q2: Meditate — Topic Argument
  // -----------------------------------------------------------------------

  describe("Q2: Meditate - Topic Argument", () => {
    let agent: Agent;
    let meditateResult: CollectedRun;

    beforeAll(async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await sendWithRetry(
        agent,
        '/crux-meditate "how should we approach caching strategies"'
      );
      meditateResult = await collectRun(run);
    }, 480_000);

    afterAll(async () => {
      if (agent) {
        await agent[Symbol.asyncDispose]();
      }
    });

    it(
      "derives facets from provided topic",
      { timeout: 480_000 },
      () => {
        const text = meditateResult.assistantText.toLowerCase();
        const hasCachingFacets =
          text.includes("cache") ||
          text.includes("caching") ||
          text.includes("strategy") ||
          text.includes("ttl") ||
          text.includes("invalidation");

        expect(hasCachingFacets).toBe(true);
      }
    );

    it(
      "produces consolidated insights referencing memories",
      { timeout: 480_000 },
      () => {
        const text = meditateResult.assistantText.toLowerCase();

        const referencesMemoryContent =
          text.includes("memory") ||
          text.includes("stale-while-revalidate") ||
          text.includes("ttl") ||
          text.includes("cache invalidation");

        const hasInsightLanguage =
          /connection|pattern|across|relate|link|insight|consolidat|synthesis/i.test(
            meditateResult.assistantText
          );

        expect(referencesMemoryContent).toBe(true);
        expect(hasInsightLanguage).toBe(true);
      }
    );
  });

  // -----------------------------------------------------------------------
  // Q3: Meditate — File/Folder References
  // -----------------------------------------------------------------------

  describe("Q3: Meditate - File/Folder References", () => {
    it(
      "derives facets from file/folder reference",
      { timeout: 480_000 },
      async () => {
        const agent = Agent.create({
          apiKey: getApiKey(),
          model: { id: "composer-2" },
          local: { cwd: ws.root },
        });

        try {
          const run = await sendWithRetry(
            agent,
            '/crux-meditate "Explore the patterns in .cursor/skills/"'
          );
          const result = await collectRun(run);

          expect(result.status).toBe("finished");

          const text = result.assistantText.toLowerCase();
          const hasFacetDerivation =
            /facet|theme|dimension|branch|direction|aspect|exploration/i.test(
              result.assistantText
            ) ||
            text.includes("skill") ||
            text.includes("pattern") ||
            text.includes("memory");

          expect(hasFacetDerivation).toBe(true);
        } finally {
          await agent[Symbol.asyncDispose]();
        }
      }
    );
  });
});
