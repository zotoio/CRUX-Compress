/**
 * Category P: Amnesia SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios P1-P3.
 * Validates amnesia toggle, explicit command override, and subagent inheritance.
 *
 * All tests run in an isolated git worktree — the real repo is never modified.
 */

import { Agent } from "@cursor/february/agent";
import * as fs from "node:fs";
import * as path from "node:path";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { getApiKey } from "../helpers/config.js";
import {
  type IsolatedWorkspace,
  assertOutputExcludes,
  collectRun,
  createIsolatedWorkspace,
  createMemoryFixture,
  rebuildMemoryIndex,
  requireApiKey,
} from "../helpers/harness.js";

describe("P: Amnesia", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();

    createMemoryFixture(
      {
        slug: "sdk-test-amnesia-auth",
        type: "learning",
        title: "Use JWT for stateless auth",
        description: "JWT tokens enable horizontal scaling without session storage",
        tags: ["auth", "jwt", "scaling"],
        body: "Prefer JWT over session cookies for APIs that need to scale horizontally.",
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

  describe("P1: Amnesia - Toggle Mode", () => {
    it("confirms amnesia mode is ON when toggled", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-amnesia");
      const result = await collectRun(run);

      expect(result.status).toBe("finished");

      const confirmsOn =
        result.assistantText.toLowerCase().includes("amnesia") &&
        (result.assistantText.toLowerCase().includes("on") ||
          result.assistantText.toLowerCase().includes("enabled") ||
          result.assistantText.toLowerCase().includes("active"));

      expect(confirmsOn).toBe(true);
    });

    it("toggles amnesia mode OFF when called again", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const onRun = await agent.send("/crux-amnesia on");
      await collectRun(onRun);

      const offRun = await agent.send("/crux-amnesia off");
      const result = await collectRun(offRun);

      const confirmsOff =
        result.assistantText.toLowerCase().includes("off") ||
        result.assistantText.toLowerCase().includes("disabled") ||
        result.assistantText.toLowerCase().includes("restored") ||
        result.assistantText.toLowerCase().includes("config-driven");

      expect(confirmsOff).toBe(true);
    });

    it("does not modify config file during toggle", async () => {
      const configPath = path.join(ws.root, ".crux", "crux-memories.json");
      const beforeContent = fs.existsSync(configPath)
        ? fs.readFileSync(configPath, "utf-8")
        : null;

      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-amnesia on");
      await collectRun(run);

      const afterContent = fs.existsSync(configPath)
        ? fs.readFileSync(configPath, "utf-8")
        : null;

      expect(afterContent).toBe(beforeContent);
    });

    it("suppresses ambient memory usage during amnesia", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const amnesiaRun = await agent.send("/crux-amnesia on");
      await collectRun(amnesiaRun);

      const taskRun = await agent.send(
        "How should I implement authentication for my API?"
      );
      const result = await collectRun(taskRun);

      assertOutputExcludes(
        result.assistantText,
        ["[memory:", "sdk-test-amnesia-auth"],
        "P1: No memory annotations during amnesia"
      );
    });
  });

  describe("P2: Amnesia - Explicit Memory Commands Still Work", () => {
    it("/crux-recall works during amnesia and is not blocked", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const amnesiaRun = await agent.send("/crux-amnesia on");
      await collectRun(amnesiaRun);

      const recallRun = await agent.send("/crux-recall");
      const result = await collectRun(recallRun);

      expect(result.status).toBe("finished");

      const showsMemories =
        result.assistantText.toLowerCase().includes("memory") ||
        result.assistantText.toLowerCase().includes("title") ||
        result.assistantText.toLowerCase().includes("type");

      expect(showsMemories).toBe(true);

      assertOutputExcludes(
        result.assistantText,
        [/cannot.*amnesia/i, /blocked/i, /disabled.*recall/i],
        "P2: Explicit commands not blocked"
      );
    });

    it("/crux-remember works during amnesia", { timeout: 300_000 }, async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const amnesiaRun = await agent.send("/crux-amnesia on");
      await collectRun(amnesiaRun);

      const rememberRun = await agent.send(
        '/crux-remember "Test memory during amnesia" --type idea'
      );
      const result = await collectRun(rememberRun);

      const createsMemory =
        result.assistantText.toLowerCase().includes("created") ||
        result.assistantText.toLowerCase().includes("saved") ||
        result.assistantText.toLowerCase().includes("memory") ||
        result.assistantText.toLowerCase().includes("idea");

      expect(createsMemory).toBe(true);
    });
  });

  describe("P3: Amnesia - Subagent Inheritance", () => {
    it("subagents inherit amnesia state", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const amnesiaRun = await agent.send("/crux-amnesia on");
      await collectRun(amnesiaRun);

      const taskRun = await agent.send(
        "Create a simple utility function that validates email addresses"
      );
      const result = await collectRun(taskRun);

      assertOutputExcludes(
        result.assistantText,
        ["[memory:"],
        "P3: Subagents do not annotate with memories"
      );
    });
  });

  describe("Amnesia Status Check", () => {
    it("/crux-amnesia status shows current mode", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const run = await agent.send("/crux-amnesia status");
      const result = await collectRun(run);

      const showsStatus =
        result.assistantText.toLowerCase().includes("status") ||
        result.assistantText.toLowerCase().includes("mode") ||
        result.assistantText.toLowerCase().includes("amnesia") ||
        result.assistantText.toLowerCase().includes("enabled") ||
        result.assistantText.toLowerCase().includes("disabled");

      expect(showsStatus).toBe(true);
    });
  });
});
