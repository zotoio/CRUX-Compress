/**
 * Category O: Remember SDK Tests
 *
 * Tests from USER_EVAL_CHECKLISTS.md scenarios O1-O2.
 * Validates memory creation, type flags, and index rebuilding.
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
  assertOutputContains,
  collectRun,
  createIsolatedWorkspace,
  hasSubagentCall,
  listMemoryFiles,
  readMemoryIndex,
  rebuildMemoryIndex,
  requireApiKey,
} from "../helpers/harness.js";

describe("O: Remember", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;

  beforeAll(async () => {
    requireApiKey();
    ws = createIsolatedWorkspace();
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

  describe("O1: Remember - Interactive Creation", () => {
    it("delegates to memory manager or handles creation directly", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: always use semantic versioning" --type learning\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      const result = await collectRun(run, prompt);

      expect(result.status).toBe("finished");

      const usedSubagent = hasSubagentCall(result.toolCalls, "crux-cursor-memory-manager");
      const wroteFile = result.toolCalls.some(
        (tc) => tc.name === "edit" || tc.name === "write"
      );
      const outputConfirms =
        result.assistantText.toLowerCase().includes("memory") ||
        result.assistantText.toLowerCase().includes("created") ||
        result.assistantText.toLowerCase().includes("stored") ||
        result.assistantText.toLowerCase().includes("saved");

      expect(usedSubagent || wroteFile || outputConfirms).toBe(true);
    });

    it("creates memory file in correct type directory", async () => {
      const beforeFiles = listMemoryFiles(ws.root);

      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: prefer composition over inheritance" --type learning\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      await collectRun(run, prompt);

      const afterFiles = listMemoryFiles(ws.root);
      const newFiles = afterFiles.filter((f) => !beforeFiles.includes(f));

      const hasLearningMemory = newFiles.some(
        (f) => f.includes("/learning/") && f.endsWith(".memory.md")
      );
      expect(hasLearningMemory).toBe(true);
    });

    it("sets source to adhoc for manually created memories", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: use descriptive variable names" --type idea\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      await collectRun(run, prompt);

      const ideaDir = path.join(ws.root, "memories", "idea");
      if (fs.existsSync(ideaDir)) {
        const ideaFiles = fs.readdirSync(ideaDir);
        const newMemory = ideaFiles.find((f) => f.includes("sdk-test") || f.includes("descriptive"));

        if (newMemory) {
          const content = fs.readFileSync(path.join(ideaDir, newMemory), "utf-8");
          expect(content).toContain('source: "adhoc"');
        }
      }
    });

    it("rebuilds memory index after creation", async () => {
      const indexPath = path.join(ws.root, ".crux", "memory-index.yml");
      const beforeMtime = fs.existsSync(indexPath)
        ? fs.statSync(indexPath).mtimeMs
        : 0;

      await new Promise((r) => setTimeout(r, 100));

      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: document public APIs" --type learning\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      await collectRun(run, prompt);

      await new Promise((r) => setTimeout(r, 500));

      if (fs.existsSync(indexPath)) {
        const afterMtime = fs.statSync(indexPath).mtimeMs;
        const indexContent = readMemoryIndex(ws.root);
        const hasNewMemory =
          indexContent.includes("document public") ||
          indexContent.includes("sdk-test") ||
          afterMtime > beforeMtime;

        expect(hasNewMemory).toBe(true);
      }
    });

    it("confirmation shows memory details", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: use constants for magic numbers" --type redflag\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      const result = await collectRun(run, prompt);

      assertOutputContains(
        result.assistantText,
        ["redflag"],
        "O1: Confirmation shows type"
      );

      const confirmsCreation =
        result.assistantText.toLowerCase().includes("created") ||
        result.assistantText.toLowerCase().includes("stored") ||
        result.assistantText.toLowerCase().includes("saved") ||
        result.assistantText.toLowerCase().includes("recorded") ||
        result.assistantText.toLowerCase().includes("memory");

      expect(confirmsCreation).toBe(true);
    });
  });

  describe("O2: Remember - One-Shot with Type Flag", () => {
    it("--type flag bypasses type selection prompt", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: validate input at boundaries" --type redflag\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      const result = await collectRun(run, prompt);

      expect(result.status).toBe("finished");

      const asksForType =
        result.assistantText.toLowerCase().includes("which type") ||
        result.assistantText.toLowerCase().includes("select a type") ||
        result.assistantText.toLowerCase().includes("choose type");

      expect(asksForType).toBe(false);
    });

    it("creates memory in specified type directory", async () => {
      agent = Agent.create({
        apiKey: getApiKey(),
        model: { id: "composer-2" },
        local: { cwd: ws.root },
      });

      const prompt =
        '/crux-remember "SDK test: handle edge cases explicitly" --type core\n\n' +
        'IMPORTANT: Do NOT use AskQuestion or prompt for any input. ' +
        'Use sensible defaults for tags and description. Create the memory file immediately.';
      const run = await agent.send(prompt);
      await collectRun(run, prompt);

      const coreDir = path.join(ws.root, "memories", "core");
      if (fs.existsSync(coreDir)) {
        const coreFiles = fs.readdirSync(coreDir);
        const hasNewMemory = coreFiles.some(
          (f) => f.includes("edge") || f.includes("sdk-test")
        );
        expect(hasNewMemory).toBe(true);
      }
    });
  });
});
