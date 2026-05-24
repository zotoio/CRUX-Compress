---
id: "201a643"
title: "Mandatory multi-iteration adversarial review must gate all published artifacts"
description: "Any workflow that produces published artifacts should gate generation behind a mandatory adversarial review cycle: fresh reviewer context, multi-dimensional audit, severity classification, iteration cap, ESCALATE semantics, and Pattern-B escalation for ambiguity."
type: "learning"
strength: 2
created: 2026-05-24
modified: 2026-05-24
source: "20260516-meditate-research-mode-overhaul"
tags: [quality-gates, adversarial-review, iteration-cap, report-generation, escalation, agent-coordination]
---

Any workflow that produces published artifacts (reports, documentation, released packages) should gate generation behind a mandatory adversarial review cycle with these properties:

1. **Fresh reviewer context**: the reviewer is a separate subagent with no prior involvement in producing the content being reviewed — eliminates confirmation bias
2. **Multi-dimensional audit**: review across orthogonal dimensions (e.g. citation integrity, cross-file consistency, substance, calibration, anti-homogenisation drift) — prevents tunnel-vision reviews
3. **Severity classification**: MUST_FIX (blocks publication), SHOULD_FIX (applied if unambiguous), ADVISORY (logged) — focuses iteration effort on blocking issues
4. **Iteration cap** (default 3): prevents infinite review loops while giving enough passes for convergent fix-and-recheck
5. **ESCALATE semantics**: when the cap is reached with unresolved MUST_FIX findings, abort the publication step entirely and surface findings to the user — never publish over known quality failures
6. **Pattern-B escalation for ambiguity**: when a MUST_FIX finding is ambiguous (multiple valid resolutions), the reviewer escalates to the user via Pattern B with mandatory context/decision-guidance — never auto-resolves subjective decisions

This pattern was validated in the Meditate Research-Mode Overhaul where 11-dimension adversarial review gates every HTML+PDF report. The same pattern applies to any multi-agent output pipeline.
