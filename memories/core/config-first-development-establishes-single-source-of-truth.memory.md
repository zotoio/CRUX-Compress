---
id: "04fae67"
title: "Config-first development establishes single source of truth for multi-component features"
description: "Define the complete configuration schema as the first subtask of any multi-component feature, then make all components consume it. This eliminates cross-component drift and provides a single authoritative source for all configurable behavior."
type: "core"
strength: 1
created: 2026-05-10
modified: 2026-05-10
source: "20260403-crux-memories"
tags: [architecture, configuration, multi-component, single-source-of-truth]
---

Subtask 01 of the CRUX Memories spec established the full `.crux/crux-memories.json` config schema — flags, storage paths, type priorities, thresholds, hook settings, scope rules — before any of the 13 implementation subtasks began. Every subsequent subtask (skills, agent, MCP server, hooks, evals) referenced this config rather than hardcoding values. This eliminated cross-component drift and provided a single authoritative source for all configurable behavior.

The pattern: define the complete configuration schema as the first subtask of any multi-component feature, then make all components consume it. When 13+ components all read from one config file, changes propagate automatically and inconsistencies surface immediately as config parse errors rather than silent behavioral mismatches discovered later.
