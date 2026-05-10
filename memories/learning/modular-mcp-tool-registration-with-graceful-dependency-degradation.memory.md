---
id: "d51f57b"
title: "Modular MCP tool registration with graceful dependency degradation"
description: "MCP servers benefit from modular tool directories where each domain registers tools independently, combined with graceful degradation from heavy optional dependencies to stdlib fallbacks."
type: "learning"
strength: 1
created: 2026-05-10
modified: 2026-05-10
source: "20260403-crux-memories"
tags: [mcp, architecture, modularity, graceful-degradation, dependencies]
---

The `crux_mcp_server` uses modular tool directories (`tools/{domain}/`) where each tool module registers itself with the server on startup. Future CRUX tools (compression, validation) can be added as new subdirectories without modifying core server code.

The server also implements graceful dependency degradation: it attempts `sentence-transformers` for semantic search, falling back to a lightweight stdlib TF-IDF implementation (`collections.Counter` + `math.log`) when the heavy optional dependency is unavailable. This enables zero-extra-dependency deployment for basic functionality while supporting enhanced search when deps are present.

The combination of modular registration and graceful degradation means the server can grow in capability without increasing its minimum deployment footprint.
