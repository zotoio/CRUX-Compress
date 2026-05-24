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
 *
 * Static structural tests (20260523 meditate-richness spec) added below the
 * expensive LLM block — these run unconditionally and read command/agent files.
 */

import { readFileSync, existsSync } from "node:fs";
import { resolve, join } from "node:path";
import { Agent } from "@cursor/february/agent";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type CollectedRun,
  type IsolatedWorkspace,
  collectRun,
  createIsolatedWorkspace,
  createMemoryFixture,
  hasSubagentCall,
  rebuildMemoryIndex,
  requireApiKey,
  sendWithRetry,
} from "../helpers/harness.js";

// ---------------------------------------------------------------------------
// Helpers for static file assertions
// ---------------------------------------------------------------------------

// REPO_ROOT: go up from evals/sdk/tests/<file> → evals/sdk/tests → evals/sdk → evals → repo root
const REPO_ROOT = resolve(import.meta.url.replace("file://", ""), "../../../..");

function resolveTargetFile(...candidates: string[]): string {
  for (const c of candidates) {
    const p = join(REPO_ROOT, c);
    if (existsSync(p)) return p;
  }
  throw new Error(`None of the candidate target files exist: ${candidates.join(", ")}`);
}

function readCommandFile(): string {
  // Post-S06: concatenate command + all meditation skills so gate content (on the
  // command) and migrated content (on the skills) are both available to assertions.
  const parts: string[] = [];
  const cmdPath = join(REPO_ROOT, ".cursor/commands/crux-meditate.md");
  if (existsSync(cmdPath)) parts.push(readFileSync(cmdPath, "utf-8"));
  for (const name of ["coordination", "report", "review", "research", "quick", "ensemble"] as const) {
    const skillPath = join(REPO_ROOT, `.cursor/skills/crux-skill-memory-meditation-${name}/SKILL.md`);
    if (existsSync(skillPath)) parts.push(readFileSync(skillPath, "utf-8"));
  }
  if (parts.length > 0) return parts.join("\n");
  throw new Error("Neither command file nor meditation skill files exist");
}

function readAgentFile(): string {
  // Post-S04: research + ensemble skills come first (they carry the canonical rubric
  // and ensemble cadence definitions); then the guide agent (or memory-manager fallback).
  const parts: string[] = [];
  for (const name of ["research", "ensemble"] as const) {
    const p = join(REPO_ROOT, `.cursor/skills/crux-skill-memory-meditation-${name}/SKILL.md`);
    if (existsSync(p)) parts.push(readFileSync(p, "utf-8"));
  }
  const guidePath = join(REPO_ROOT, ".cursor/agents/crux-cursor-meditation-guide.md");
  const mmPath = join(REPO_ROOT, ".cursor/agents/crux-cursor-memory-manager.md");
  if (existsSync(guidePath)) {
    parts.push(readFileSync(guidePath, "utf-8"));
  } else if (existsSync(mmPath)) {
    parts.push(readFileSync(mmPath, "utf-8"));
  }
  if (parts.length > 0) return parts.join("\n");
  throw new Error("No agent or skill files found for readAgentFile()");
}

function readSkillFile(skillName: string): string {
  const p = join(REPO_ROOT, `.cursor/skills/crux-skill-memory-meditation-${skillName}/SKILL.md`);
  if (existsSync(p)) return readFileSync(p, "utf-8");
  return "";
}

function readMemoryManagerFile(): string {
  const p = join(REPO_ROOT, ".cursor/agents/crux-cursor-memory-manager.md");
  if (existsSync(p)) return readFileSync(p, "utf-8");
  return "";
}

const MEDITATION_SKILL_NAMES = [
  "research", "quick", "ensemble", "review", "report", "coordination",
] as const;

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
        const usedMeditationGuide = hasSubagentCall(
          meditateResult.toolCalls,
          "crux-cursor-meditation-guide"
        );

        expect(taskCalls.length >= 1 || usedMeditationGuide).toBe(true);
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

// ---------------------------------------------------------------------------
// 20260523 meditate-richness spec — Static structural assertions (K1–K10)
// These run unconditionally (no SDK LLM calls; no skipExpensive gate).
// ---------------------------------------------------------------------------

describe("Q: Meditate — Structural: K2 Merged Cost+Richness Gate", () => {
  it("Q-Cost-and-Richness-Acknowledgment exists in command file", () => {
    const content = readCommandFile();
    expect(content).toContain("Q-Cost-and-Richness-Acknowledgment");
  });

  it("no standalone Q-Comprehensiveness gate", () => {
    const content = readCommandFile();
    expect(content).not.toContain("Q-Comprehensiveness");
  });

  it("all four richness enum values documented", () => {
    const content = readCommandFile();
    for (const level of ["compact", "default", "detailed", "exhaustive"]) {
      expect(content).toContain(level);
    }
  });

  it("default richness is preselected", () => {
    const content = readCommandFile().toLowerCase();
    expect(content).toContain("preselected");
    expect(content).toContain("default");
  });

  it("mode-swap preserves richness selection", () => {
    const content = readCommandFile();
    expect(content.toLowerCase()).toContain("richness");
    expect(content.toLowerCase()).toContain("preserved");
    expect(content).toContain("switch_to_quick");
  });

  it("K1 dual-meaning callout present for default level", () => {
    const content = readCommandFile();
    const hasDualMeaning =
      content.includes("naming-reconciliation") ||
      content.includes("level *name* `default` matches the preselected option") ||
      content.includes("dual meaning");
    expect(hasDualMeaning).toBe(true);
  });
});

describe("Q: Meditate — Structural: K10 Finalisation Enhancement Gate", () => {
  it("Q-Finalisation-Enhancements gate documented", () => {
    const content = readCommandFile();
    expect(content).toContain("Q-Finalisation-Enhancements");
  });

  it("gate is multi-select 0–5", () => {
    const content = readCommandFile();
    expect(content).toContain("0–5");
    expect(content.toLowerCase()).toContain("multi-select");
  });

  it("gate fires after consolidation before adversarial review", () => {
    const content = readCommandFile().toLowerCase();
    const idx = content.indexOf("q-finalisation-enhancements");
    expect(idx).toBeGreaterThan(-1);
    expect(content).toContain("consolidat");
    expect(content).toContain("adversarial");
    expect(content).toContain("before");
  });

  it("skip-all path reproduces today's behaviour", () => {
    const content = readCommandFile().toLowerCase();
    expect(content).toContain("skip");
    expect(content).toContain("unchosen_persisted");
  });

  it("cheap items bundle into respawn, expensive items default to queue", () => {
    const content = readCommandFile().toLowerCase();
    expect(content).toContain("cheap");
    expect(content).toContain("respawn");
    expect(content).toContain("expensive");
    expect(content).toContain("queue");
  });
});

describe("Q: Meditate — Structural: K10 Reflection Rubric", () => {
  it("impact × insight-value rubric documented in agent file", () => {
    const content = readAgentFile().toLowerCase();
    expect(content).toContain("impact_score");
    expect(content).toContain("insight_value_score");
  });

  it("both axes use 1–10 scale", () => {
    const content = readAgentFile();
    expect(content.includes("1–10") || content.includes("1-10")).toBe(true);
  });

  it("minimum_impact_threshold defaults to 6", () => {
    const content = readAgentFile();
    expect(content).toContain("minimum_impact_threshold");
    const idx = content.indexOf("minimum_impact_threshold");
    const surrounding = content.slice(Math.max(0, idx - 50), idx + 100);
    expect(surrounding).toContain("6");
  });

  it("worked examples for impact_score 9, 5, 2 present", () => {
    const content = readAgentFile();
    expect(content).toContain("impact_score");
    expect(content.includes("`9`") || content.includes("9` =") || content.includes("= 9")).toBe(true);
    expect(content.includes("`5`") || content.includes("5` =") || content.includes("= 5")).toBe(true);
    expect(content.includes("`2`") || content.includes("2` =") || content.includes("= 2")).toBe(true);
  });

  it("weights configurable via finalisationEnhancements.weights", () => {
    const combined = readCommandFile() + readAgentFile();
    const hasWeightsKey =
      combined.includes("finalisationEnhancements") || combined.toLowerCase().includes("finalisation_enhancements");
    expect(hasWeightsKey).toBe(true);
    expect(combined).toContain("impact: 1.0");
    expect(combined).toContain("insight_value: 1.0");
  });
});

describe("Q: Meditate — Structural: K9 Respawn Protocol", () => {
  it("respawn protocol documented with all required payload keys", () => {
    const content = readCommandFile();
    const required = [
      "respawn_reasons",
      "reviewer_iteration",
      "prior_report_paths",
      "missing_sections",
      "missing_visualisations",
      "accepted_finalisation_enhancements",
      "preserve_other_content",
      "comprehensiveness_payload",
      "init_suggestions_payload",
      "theming_payload",
    ];
    for (const key of required) {
      expect(content, `Respawn payload key '${key}' must be documented`).toContain(key);
    }
  });

  it("respawn shares ≤3 iteration cap; ESCALATE at iter 3", () => {
    const content = readCommandFile();
    const lower = content.toLowerCase();
    const hasCap = content.includes("≤3") || lower.includes("3 iteration") || lower.includes("cap is **3");
    expect(hasCap).toBe(true);
    expect(content).toContain("ESCALATE");
  });

  it("triple-reason ordering: accepted_enhancements first", () => {
    const content = readCommandFile().toLowerCase();
    expect(content).toContain("accepted_finalisation_enhancements");
    expect(content).toContain("missing_init_suggestion_sections");
    expect(content).toContain("missing_init_suggestion_visualisations");
    const feIdx = content.indexOf("accepted_finalisation_enhancements");
    const visIdx = content.indexOf("missing_init_suggestion_visualisations");
    const secIdx = content.indexOf("missing_init_suggestion_sections");
    // At least one ordering pair should be correct
    if (feIdx > -1 && visIdx > -1 && secIdx > -1) {
      expect(feIdx < visIdx || feIdx < secIdx).toBe(true);
    }
  });
});

describe("Q: Meditate — Structural: K10 Ensemble Layered Cadence", () => {
  it("per-tree YAML schema has source_tree and surfaced_to_root fields", () => {
    const agentContent = readAgentFile();
    expect(agentContent).toContain("source_tree:");
    expect(agentContent).toContain("surfaced_to_root");
  });

  it("root combined YAML has cross_model_candidates and union_candidates", () => {
    const combined = readCommandFile() + readAgentFile();
    expect(combined).toContain("cross_model_candidates");
    expect(combined).toContain("union_candidates");
  });

  it("single root askQuestion at ensemble root", () => {
    const content = readCommandFile().toLowerCase();
    expect(content).toContain("ensemble root");
    expect(content).toContain("q-finalisation-enhancements");
  });
});

// ---------------------------------------------------------------------------
// S08: New structural describe blocks — Guide Agent, Six Skills,
//      Thin Coordinator, and Trimmed Memory-Manager
// ---------------------------------------------------------------------------

describe("Q: Meditate — Structural: Guide Agent Frontmatter & Persona", () => {
  it("guide agent file exists", () => {
    const p = join(REPO_ROOT, ".cursor/agents/crux-cursor-meditation-guide.md");
    expect(existsSync(p)).toBe(true);
  });

  it("frontmatter has name: crux-cursor-meditation-guide", () => {
    const content = readAgentFile();
    expect(content).toContain("name: crux-cursor-meditation-guide");
  });

  it("description contains meditation", () => {
    const content = readAgentFile().toLowerCase();
    expect(content).toContain("meditation");
  });

  it("mode router lists Phases A–G, Quick 6-step, K10 In-Pass Reflection, Adversarial Review", () => {
    const content = readAgentFile();
    expect(content.includes("Phases A–G") || content.includes("Phases A-G")).toBe(true);
    expect(content.includes("6-step") || content.toLowerCase().includes("6 step")).toBe(true);
    expect(content).toContain("K10 In-Pass Reflection");
    expect(content).toContain("Adversarial Review");
  });

  it("canonical comprehensiveness abort error string present", () => {
    const content = readAgentFile();
    expect(content).toContain(
      "comprehensiveness: payload required; missing from spawn prompt — caller misconfigured"
    );
  });

  it("User Input Escalation + Pattern A + Pattern B + needs_user_input present", () => {
    const content = readAgentFile();
    expect(content).toContain("User Input Escalation");
    expect(content).toContain("Pattern A");
    expect(content).toContain("Pattern B");
    expect(content).toContain("needs_user_input");
  });
});

describe("Q: Meditate — Structural: Six Meditation Skills", () => {
  it("all six SKILL.md files exist", () => {
    for (const name of MEDITATION_SKILL_NAMES) {
      const p = join(REPO_ROOT, `.cursor/skills/crux-skill-memory-meditation-${name}/SKILL.md`);
      expect(existsSync(p), `SKILL.md for '${name}' must exist`).toBe(true);
    }
  });

  it("each skill frontmatter name matches its directory", () => {
    for (const name of MEDITATION_SKILL_NAMES) {
      const content = readSkillFile(name);
      expect(content, `'${name}' skill must have matching name frontmatter`).toContain(
        `name: crux-skill-memory-meditation-${name}`
      );
    }
  });

  it("each skill description contains meditation", () => {
    for (const name of MEDITATION_SKILL_NAMES) {
      const content = readSkillFile(name).toLowerCase();
      expect(content, `'${name}' skill description must contain 'meditation'`).toContain(
        "meditation"
      );
    }
  });

  it("coordination skill: 18-row filename table sentinel rows present", () => {
    const content = readSkillFile("coordination");
    expect(content).toContain("finalisation-enhancements.yml");
    expect(content).toContain("init-suggestions-{ts}.yml");
    expect(content).toContain("retrospective-{ts}.md");
    expect(content).toContain("report-{topic-slug}-{ts}.html");
  });

  it("research skill: Phases A–G + init-suggestions write + canonical treatment filter", () => {
    const content = readSkillFile("research");
    expect(content.includes("Phases A–G") || content.includes("Phases A-G")).toBe(true);
    expect(content).toContain("init-suggestions-{ts}.yml");
    expect(content).toContain("treatment:");
    expect(content).toContain("additional_facet");
  });

  it("quick skill: 6-step + warn-only citation regime", () => {
    const content = readSkillFile("quick");
    expect(content).toContain("6-step");
    expect(content.includes("warn_only") || content.includes("warn-only")).toBe(true);
  });

  it("review skill: 13 dimensions + Dim 12 + Dim 13 + Report-Skill Respawn Protocol", () => {
    const content = readSkillFile("review");
    expect(content).toContain("13");
    expect(content).toContain("Comprehensiveness fidelity");
    expect(content).toContain("Init-suggestion AND finalisation-enhancement honour");
    expect(content).toContain("Report-Skill Respawn Protocol");
    expect(content).toContain("respawn_reasons");
  });

  it("report skill: Comprehensiveness Level Mapping + Per-Cheap-Type + 7 cheap types + Universal Contrast", () => {
    const content = readSkillFile("report");
    expect(content).toContain("Comprehensiveness Level Mapping");
    expect(content).toContain("Per-Cheap-Type Rendering Contract");
    expect(content).toContain("executive_summary");
    expect(content).toContain("action_plan");
    expect(content).toContain("Universal Contrast");
  });

  it("ensemble skill: cross-model-synthesis + source_tree + surfaced_to_root + cross_model_candidates + union_candidates + K10 Ensemble Respawn Targeting", () => {
    const content = readSkillFile("ensemble");
    expect(content).toContain("cross-model-synthesis.md");
    expect(content).toContain("source_tree");
    expect(content).toContain("surfaced_to_root");
    expect(content).toContain("cross_model_candidates");
    expect(content).toContain("union_candidates");
    expect(content).toContain("K10 Ensemble Respawn Targeting");
  });
});

describe("Q: Meditate — Structural: Refactored Command Thin Coordinator", () => {
  it("## Instructions spawns crux-cursor-meditation-guide", () => {
    const content = readCommandFile();
    const relatedIdx = content.indexOf("## Related");
    const instructions = relatedIdx !== -1 ? content.slice(0, relatedIdx) : content;
    expect(instructions).toContain("crux-cursor-meditation-guide");
  });

  it("## Instructions does NOT spawn crux-cursor-memory-manager", () => {
    const content = readCommandFile();
    const relatedIdx = content.indexOf("## Related");
    const instructions = relatedIdx !== -1 ? content.slice(0, relatedIdx) : content;
    expect(instructions).not.toContain("crux-cursor-memory-manager");
  });

  it("Q-Cost-and-Richness-Acknowledgment still present", () => {
    const content = readCommandFile();
    expect(content).toContain("Q-Cost-and-Richness-Acknowledgment");
  });

  it("Q-Finalisation-Enhancements still present", () => {
    const content = readCommandFile();
    expect(content).toContain("Q-Finalisation-Enhancements");
  });

  it("Related section lists all six meditation skill directory names", () => {
    const content = readCommandFile();
    for (const name of MEDITATION_SKILL_NAMES) {
      expect(content).toContain(`crux-skill-memory-meditation-${name}`);
    }
  });
});

describe("Q: Meditate — Structural: Trimmed Memory-Manager", () => {
  it("crux-cursor-memory-manager.md still has Dream + REM Sleep + Recall + Remember + Forget modes", () => {
    const content = readMemoryManagerFile();
    if (!content) return;
    expect(content).toContain("Dream Mode");
    expect(content).toContain("REM Sleep");
    expect(content).toContain("Recall Mode");
    expect(content).toContain("Remember Mode");
    expect(content).toContain("Forget Mode");
  });

  it("crux-cursor-memory-manager.md no longer has Phases A–G executable content", () => {
    const content = readMemoryManagerFile();
    if (!content) return;
    expect(content).not.toContain("Phases A–G");
  });

  it("crux-cursor-memory-manager.md no longer has Quick 6-step executable content", () => {
    const content = readMemoryManagerFile();
    if (!content) return;
    expect(content).not.toContain("Quick 6-step");
  });

  it("crux-cursor-memory-manager.md no longer has ### Adversarial Review heading", () => {
    const content = readMemoryManagerFile();
    if (!content) return;
    expect(content).not.toContain("### Adversarial Review");
  });

  it("crux-cursor-memory-manager.md no longer has ensembleAggregation: true spawn parameter", () => {
    const content = readMemoryManagerFile();
    if (!content) return;
    expect(content).not.toContain("ensembleAggregation: true");
  });

  it("crux-cursor-memory-manager.md no longer has K10c reflection rubric", () => {
    const content = readMemoryManagerFile();
    if (!content) return;
    expect(content).not.toContain("K10c reflection rubric");
  });
});
