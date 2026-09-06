---
generated: 2026-07-13 19:40
sourceChecksum: "2429874930"
cruxLevel: 25
beforeTokens: 25499
afterTokens: 5478
reducedBy: 79%
confidence: 92%
---

If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

> [!IMPORTANT]
> Generated file - do not edit!

# crux-meditate

```crux
⟦CRUX:crux-meditate.source.mdx
Κ{cmd=/crux-meditate; guide=crux-cursor-meditation-guide;
  cfg=.crux/crux-memories.json; wdir=meditations/{yyyymmdd}-{topic-slug}/;
  RQ=Q-Cost-and-Richness-Acknowledgment; FE=Q-Finalisation-Enhancements;
  init=init-suggestions-{ts}.yml; fenh=finalisation-enhancements.yml}

Λ.usage{
  /crux-meditate→explore facets from chat ctx
  /crux-meditate "topic"→explore specific theme
  /crux-meditate @file @folder/→explore referenced code
  /crux-meditate --quick "topic"→fast parallel-fanout(legacy)
  /crux-meditate --random-model "topic"→1 tree,random pool model
  /crux-meditate --model-per-branch "topic"→1 tree,branch=distinct model
  /crux-meditate --ensemble "topic"→N parallel trees+aggregate
  /crux-meditate --ensemble --quick "topic"→ensemble of Quick trees
  flags=[--quick,--random-model,--model-per-branch,--ensemble] anywhere in $ARGUMENTS
  --random-model|--model-per-branch|--ensemble=mutually exclusive!
}

Φ.modes{
  recursion:[Research(default;serial depth-first;citations mandatory;peer review),
    Quick(--quick;parallel fan-out;citations warn-only;¬peer review)]
  modelStrategy:[
    none(default;caller model),
    random(--random-model;1 tree;pool pick;same agent count),
    per_branch(--model-per-branch;1 tree;each top-level branch=distinct pool model;
      descendants inherit;peer+adversarial→caller model;same agent count),
    ensemble_max(--ensemble;N trees parallel+1 aggregator;cross-model-synthesis.md+
      ensemble-report pair;poolSize≥2!)]
  common_ground: ∀strategy→same safeguards[cost ack w/ richness,theme preflight,
    combined facet/sections/viz/focus confirm,FE gate,Branch&Leaf Index,
    adversarial review-and-fix,mandatory paired HTML+PDF report]
}

Γ.instructions{
  invoke→spawn `crux-cursor-meditation-guide` subagent
  escalation=Pattern B(work first then escalate)!
  subagents NEVER AskQuestion→parent owns all pre-spawn+post-consolidation gates
  shared_memory_file=.cursor/skills/_memory-shared.md#user-input-escalation
  coordination→md files in wdir; ¬in-context return vals; ¬JSONL polling
  subagent→steps 1–8(mode-specific); calling agent→steps 9–12
  mandatory_gates_order: Q-Depth-Selection→RQ→Theme Preflight→
    combined Facet/Sections/Viz/Focus Confirmation(mid-flow)→FE(post-consolidation)
}

Λ.arg_handling{
  1.mode_select: --quick→meditateMode:"quick"; else→"research"
  2.model_strategy_select: >1 flag→abort "mutually exclusive"
    --random-model→mode:"random"; read cfg.meditate.modelPool; pool empty→abort
    --model-per-branch→mode:"per_branch"; pool empty→abort;
      branch_assignments deferred to step 4b
    --ensemble→mode:"ensemble_max"; pool<2→abort
    none→mode:"none"
  3.strip flags from $ARGUMENTS before topic-slug derivation!
  4.remaining: no args→derive from chat ctx; "quoted"→seed topic;
    @file/@folder→examine code; mixed→synthesize all
  propagate meditateMode+modelStrategy to depth-0 subagent unchanged
}

Γ.Q-Depth-Selection{⊛mandatory; calling agent's first action
  controls recursion levels; deeper=more agents+time
  agent_count_table:
    D1: Research~8(1+3+3peer+1adv); Quick~5(1+3+1adv); broad survey
    D2: Research~17(1+3+9+3peer+1adv); Quick~14; detailed analysis
    D3(default): Research~45(1+3+9+27+3peer+1adv); Quick~42; deep research
  ensemble multiplies per-tree×N+1 aggregator
  prompt: single-select[depth_1,depth_2,depth_3(preselected)]
  store→maxDepth(1|2|3); propagate unchanged to all children
  expansion-continuation: reuse prev maxDepth; ¬re-run full gate
  non-interactive: default depth 3 w/o prompt
}

Γ.Q-Cost-and-Richness-Acknowledgment{⊛mandatory; calling agent's second action
  purpose: surface cost tradeoff+richness selection in single askQuestion
  preamble shows: agent count,report tokens,4 richness rows,mode+strategy context

  Sub-Q1(richness;single-select;preselected=default;
    level *name* `default` matches the preselected option—dual meaning per K1):
    compact→pre-richness behaviour;~25k tokens;≥4 charts/≥3 infographics/≥1 calc
    `default` **[preselected]**→new default;~40k;5/4/1;branch_summary sections
    detailed→substantial bump;~60k;7/6/2;per_leaf_detail;verbatim_quotes;named_section peer review
    exhaustive→~90k;10/8/3;per-finding citation cols;+27 leaf-builder agents(Research D3)
      Quick=warn-only per OQ#5

  Sub-Q2(proceed/swap/cancel;no preselection;non-interactive→abort!):
    proceed→continue current mode+strategy
    switch_to_quick→offered when mode=Research; richness+strategy preserved
    switch_to_research→offered when mode=Quick; richness+strategy preserved
    switch_to_single→offered when mode≠"none"
    switch_to_random_model→offered when mode≠"random" ∧ poolSize≥1
    switch_to_model_per_branch→offered when mode≠"per_branch" ∧ poolSize≥1
    switch_to_ensemble→offered when mode≠"ensemble_max" ∧ poolSize≥2
    cancel→acknowledge+stop; ¬spawn; ¬Theme Preflight; ¬create wdir

  behaviour:
    always run first invocation; mode-swap preserves richness!
    richness set-once-per-invocation(K6)→stored selectedRichness;
      propagated as comprehensiveness: payload; ¬change after gate closes;
      cancel and re-invoke /crux-meditate to change
    expansion-continuation→Q-Cost-Acknowledgment-Expansion(read-only-richness variant;
      locked richness; ¬mode/depth re-offered; Sub-Q2 only[proceed_expansion|cancel])
    non-interactive→abort; ¬default to proceed silently
}

Γ.read-only-richness-variant{
  used when gate re-fires after richness locked
  Sub-Q1→locked display row: "Richness: {level} (locked — set at start; cancel and re-invoke /crux-meditate to change)"
  Sub-Q2→fully interactive
  trigger preambles:
    expansion→"continuing by expanding direction(s)"
    additional-facet→"Cost has changed because you accepted {N} additional facets"
    spawn_now(K10b)→"accepted spawning {N} follow-up agent(s) for finalisation enhancements ({types})"
  no re-presentation loop: each trigger fires ≤1× per cause
}

Γ.Theme-Preflight{⊛mandatory; Pattern A(pre-collect before spawn)
  purpose: ensure visually distinct report; ¬homogenised AI default!
  Anti-Homogenization Rules→`crux-skill-memory-meditation-report` §6.3
  forbid_homogenised_defaults: true in theming payload!

  when: always first invocation; skip+reuse on expansion; re-run on --retheme

  Q1(theme source;single-select):
    match_repo→scan pkg.json/tailwind/css/tokens→Q1b confirm
    preset→go to Q2
    custom→user describes
    surprise_me→deliberately different from default

  Q2(style direction;single-select;if Q1≠match_repo|Q1b=no):
    [editorial,scientific,minimal_typographic,bold_maximalist,
     retro_print,brutalist,terminal_dossier,architectural_blueprint,surprise_me]

  Q3(colour scheme;single-select):
    [cool_default,warm_palette,monochrome,high_contrast_minimal,
     repo_inferred(match_repo only),custom_hex]

  Q4(typography;single-select;if source≠match_repo):
    [serif_headings_sans_body,sans_headings_sans_body,
     mono_headings_mono_body,serif_throughout,mixed_distinctive]

  Q5(confirmation;single-select): [confirm,restart_preflight,cancel_meditation]

  non-interactive→surprise_me seeded by topic-slug; proceed w/o confirm;
    ¬silent homogenised default!

  theming payload→{source,matched_repo_signals?,preset?,custom?,
    default_color_mode:"dark",enable_color_toggle:true,
    pdf_color_mode:"light_high_contrast",forbid_homogenised_defaults:true}
}

Φ.comprehensiveness_payload{⊛propagate unchanged to all children; abort if missing!
  canonical error: "comprehensiveness: payload required; missing from spawn prompt — caller misconfigured"
  schema: {level,minima:{charts:{count,types_required},infographics:{count,types_required},
    calculators:{count,scenarios_per}},depth3_leaf_inclusion,per_branch_section_depth,
    citation_density,peer_review_surfacing,section_length_budget_tokens:{hero,per_facet,citations},
    ensemble_cross_model_depth}
}

Φ.modelStrategy_payload{⊛propagate unchanged; abort if missing!
  schema: {mode,pool:[{slug,label}],resolved_model_slug?,resolved_model_label?,
    branch_assignments:[{branch_index,slug,label}],assignment_policy_note?}
  per-spawn model: dispatch:
    none→omit model:; random→model:resolved_model_slug ∀spawns;
    per_branch→step 4b resolves assignments; depth-1 spawn=assignments[i].slug;
      peer+adversarial→omit model:(caller's model);
    ensemble_max→per-tree pinned via Ensemble Protocol
}

Γ.Facet-Confirmation{⊛mandatory@depth-0; Pattern B(combined askQuestion)
  depth-0 derives 3 facets+3–8 sections+5–10 viz+0–5 focus areas→
    writes facets-pending-{ts}.yml→returns needs_user_input(reason:"facets-and-init-suggestions-confirmation")
  calling agent→single askQuestion(5 sub-questions):

  sub-q1(facets;single-select): confirm_all|modify_one|modify_multiple|regenerate(≤3)|cancel
  sub-q2(sections;multi-select;all preselected): per section[id,title,rationale,source_signals]
  sub-q3(visualisations;multi-select;all preselected): per viz[id,type,rationale,what_it_would_show]
  sub-q4(additional_focus_areas;per-item single-select;default=skip):
    skip→zero cost; additional_facet→+~14 agents D3;triggers cost-ack re-presentation!
    report_section_only→no agent cost; additional_facet_AND_section→both+custom title+cost-ack!
  sub-q5(deep_confirm;single-select;preselected=none):
    none(default)→auto-derive D2+D3; depth_2_only→+≤9 prompts; all_levels→+≤36 prompts

  cost-ack re-presentation: any additional_facet|additional_facet_AND_section→
    read-only-richness variant before tree spawns; cancel→abort+delete pending

  resume-handler: calling agent resumes depth-0 w/ confirmed payload→
    depth-0 writes facets.md+deletes pending+writes init-suggestions-{ts}.yml→spawn tree
    regenerate→re-derive(≤3 attempts); modify→apply overrides then resolve
}

Γ.deep-confirm-flow{when confirmDeepFacets≠none; file-based escalation
  child: derive 3 children→write pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml(status:pending)
    →poll confirmed-facets-{same-path-id}-{ts}.yml→apply decisions[confirmed|modified|regenerate(≤3)]
    →acquire registry lock→proceed
  depth-0: poll pending-facets-*.yml alongside branch outputs→batch into needs_user_input→
    calling agent askQuestion→write confirmed-facets→child proceeds
}

Γ.what-happens{
  Research(default):
    steps 1–8 by subagent tree; steps 9–12 by calling agent
    protocol: `crux-skill-memory-meditation-research`(Phases A–G,registry lock,citations idx,
      peer review,init-suggestions-{ts}.yml write,K10c reflection→fenh)
    spawn: pass meditateMode,maxDepth,theming:,comprehensiveness:(REQUIRED!),
      parentContext,stripped $ARGUMENTS

  Quick(--quick):
    `crux-skill-memory-meditation-quick`(6-step parallel fan-out,warn-only citations,
      ¬peer review,init-suggestions-{ts}.yml write,K10c reflection)
    spawn: same fields as Research

  single-tree model strategies(--random-model|--model-per-branch):
    single tree; standard Research|Quick workflow; 1 wdir,1 consolidation.md,
    1 report pair; ¬cross-model-synthesis.md; ¬model-{slug}/ subdirs
    only changes which model executes which agent(per modelStrategy payload dispatch)
    facets.md+report footer record strategy; per_branch→[branch model: {label}] in report

  Ensemble Max(--ensemble; modelStrategy.mode=="ensemble_max"):
    Ensemble Protocol replaces steps 1–8:
    1.read pool from cfg→N=poolSize; pool<2→abort
    2.Q-Depth-Selection(shared)
    3.RQ(ensemble variant;total~N×perModelCount+1)
    4.Theme Preflight(shared)
    5.create meditations/{slug}-ensemble/
    6.derive+confirm facets ONCE(caller model;shared)→extract confirmed facets
    7.spawn N trees parallel: each→model-{label-slug}/ subdir;
      model:slug on Task; pass preConfirmedFacets+confirmDeepFacets+shared theming/comprehensiveness
    8.poll N completions; deep-confirm hook polls all N subdirs
    9.spawn cross-model aggregator(ensembleAggregatorModel|caller model):
      `crux-skill-memory-meditation-ensemble`→cross-model-synthesis.md+ensemble-report pair
    10.verify ensemble artifacts
}

Γ.calling-agent-steps-9-12{
  9.verify report: prefix-glob report-{topic-slug}-*.html/*.pdf; both non-empty!
    missing→regenerate; PDF missing(no chromium)→surface install hint prominently
    ESCALATE→no-op

  10.present: read consolidation.md; display by facet theme(Subject-Matter Focus!);
    include paths[wdir,facets.md,retrospective-{ts}.md,report HTML+PDF]
    ESCALATE→show review paths+unresolved MUST_FIX instead
    end w/ reminder: further edits in new session pointed at wdir

  11.interactive continuation(AskQuestion multi-select):
    group1(expansion directions): per tangent→full new tree+adversarial+report
    group2(reapply unchosen enhancements): per unchosen_persisted item in fenh→
      re-trigger FE w/ single item pre-checked; fresh ≤3 cap
    group3(spawn queued follow-ups): per follow-up-{type}-{ts}.yml→
      cost-ack re-presentation(spawn_now variant)→spawn immediately
    other: save_spec→draft spec outline; end_meditation→complete session
    ¬offer "Save as HTML"/"Save as PDF"(already produced!)

  12.handle selection:
    expansion→Q-Cost-Acknowledgment-Expansion(read-only-richness;locked)→
      re-run facet confirm; reuse maxDepth+mode+richness; ¬re-ask depth/mode
    reapply_enhancement_{id}→re-run FE w/ item pre-checked; fresh ≤3 cap
    spawn_queued_{id}→cost-ack(spawn_now variant)→spawn
    save_spec→write outline to specsDir
    end_meditation→remind user about new-session adjustments

  ensemble steps 9–12:
    10.verify all N per-model reports+ensemble synthesis+ensemble report pair
    11.present cross-model-synthesis.md; paths to all per-model+ensemble artifacts
    12.continuation: per-model expansion options+"Explore deeper using {model-label}";
      save_spec; end_meditation; expansions→single-model(¬re-ensemble unless --ensemble)
}

Γ.coordination{
  artefact filename grammar(18 rows), placeholders, prefix-glob polling, retrospective template,
  Branch & Leaf Index template→all in `crux-skill-memory-meditation-coordination`
  calling agent ¬reads wdir artefacts directly; depth-0 owns coordination
  step 9 verifies report pair by prefix-glob before step 10
}

Γ.Q-Finalisation-Enhancements{⊛K10a; mandatory post-consolidation before adversarial review
  depth-0 writes fenh via in-pass reflection→returns needs_user_input
  calling agent fires gate; both Research+Quick; at ensemble root after aggregator

  skip-all(0 items)→pre-K10 behaviour unchanged
  graceful_degradation: <5 candidates→present whatever; 0 passed threshold→skip gate

  multi-select 0–5; options per candidate: {id,title,cost_class[cheap|expensive],
    description,impact_score,insight_value_score,composite_score}
  cheap=bundled into first adversarial iteration respawn; 0 extra spawns
  expensive→per-item treatment sub-question:
    queue[default]→write follow-up-{type}-{ts}.yml; surface in continuation
    spawn_now→cost-ack re-presentation(spawn_now variant)→spawn after adversarial

  update flow(K10c): update fenh in-place[accepted,treatment,decided_at_utc]→
    write follow-up files→resume depth-0 w/ path→
    depth-0: cheap→accepted_finalisation_enhancements list for reviewer;
    expensive spawn_now→pending_spawn_now returned step 13

  K10b: 7 cheap types[executive_summary,action_plan,risks_section,glossary,
    decision_tree_infographic,reader_persona_tldrs,cross_branch_synthesis_section]
    report skill processes in per-reason ordering; contract in `crux-skill-memory-meditation-report` §6.9
  ensemble K10: layered cadence in `crux-skill-memory-meditation-ensemble`
}

Γ.adversarial-review{⊛mandatory; 13 dimensions; ≤3 iterations
  spawns fresh guide in Review function; clean context
  dims include: Dim 9 peer-review thoroughness(Research only),
    Dim 12 Comprehensiveness fidelity, Dim 13 init-suggestion+finalisation-enhancement honour
  Dim 13: respawn_required: true; bypasses user input; structured respawn_reasons list
    [missing_init_suggestion_sections,missing_init_suggestion_visualisations,
     accepted_finalisation_enhancements]
  MUST_FIX w/ mandatory context; ambiguous→escalate via Pattern B
  iter 3 unresolved→ESCALATE(abort report)
  Quick relaxations: missing-citation→SHOULD_FIX; peer-review dim N/A
  contract in `crux-skill-memory-meditation-review`
}

R.Subject-Matter-Focus{⊛mandatory; consolidation.md+reports
  forbidden: branch N labels,depth/agent counts,raw [child:] citations,process framing
  required: facet titles as headings,topic-name xrefs,[research: subfocus-slug],
    conclusion-first exec summaries
  contract in `crux-skill-memory-meditation-report`
}

R.report-generation{⊛mandatory; paired HTML+PDF; both modes
  non-optional; non-user-selectable; not deferred
  ¬generated over failing review(ESCALATE aborts)
  comprehensiveness minima driven by level; init-suggestions honoured(floor-not-ceiling)
  contract in `crux-skill-memory-meditation-report`
}

R.retrospective{always-written(incl ESCALATE); retrospective-{yyyymmddHHMMSS}.md
  template in `crux-skill-memory-meditation-coordination`
}

R.ensemble-report{when ensemble_max; cross-model-synthesis.md(8 sections)+
  ensemble-report pair; model comparison hero,agreement heatmap,divergence deep-dives
  contract in `crux-skill-memory-meditation-ensemble`
}

M.related{
  `crux-cursor-meditation-guide`→orchestrate recursive tree
    (Phases A–G,Quick 6-step,Adversarial Review,Ensemble Aggregation)
  skills:[`crux-skill-memory-meditation-research`(Phases A–G,registry,citations,peer review,K10c),
    `crux-skill-memory-meditation-quick`(6-step,warn-only,K10c),
    `crux-skill-memory-meditation-ensemble`(cross-model synthesis,K10 cadence+targeting),
    `crux-skill-memory-meditation-review`(13 dims,Respawn Protocol),
    `crux-skill-memory-meditation-report`(Comprehensiveness,K10b,Init-Suggestions,Subject-Matter Focus),
    `crux-skill-memory-meditation-coordination`(filenames,polling,retrospective,Branch&Leaf Index)]
  thin_agents:[`crux-memory-dream`,`crux-memory-rem`,`crux-memory-recall`,
    `crux-memory-remember`,`crux-memory-forget`]→mode-scoped Dream/REM/Recall/Remember/Forget;
    ≻deprecated umbrella dispatcher
  cmds: /crux-dream→extract+create mems; /crux-recall→query mems;
    /crux-remember→ad-hoc create; /crux-forget→remove mems
}
⟧
```
