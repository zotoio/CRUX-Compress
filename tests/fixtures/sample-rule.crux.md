---
generated: 2026-03-11 14:30
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6278
afterTokens: 1827
reducedBy: 71%
confidence: 93%
---

# Comprehensive Team Coding Standards

```crux
⟦CRUX:sample-rule.md
Ρ{team coding standards; comprehensive eng guidelines}

Κ{var=variable; fn=function; cls=class; const=constant; param=parameter;
  iface=interface; svc=service; cfg=config; env=environment; 
  PII=personally identifiable info}

R.naming{
  JS/TS{var+fn=camelCase; cls+iface=PascalCase; const=SCREAMING_SNAKE_CASE;
        enum.name=PascalCase; enum.val=SCREAMING_SNAKE_CASE; typeParam=T|K|V|TFoo}
  Py{var+fn=snake_case; cls=PascalCase; const=SCREAMING_SNAKE_CASE; _private}
  Go{export=PascalCase; unexport=camelCase; acronym=consistent_case}
}

R.style{
  fn.lines≤30; early_return; nest≤3; self_doc; 1_concept/fn;
  composition≻inheritance; SRP!
}

R.formatting{
  JS/TS{line≤100ch; indent=2sp}
  Py{line≤88ch; indent=4sp}
  Go{line≤120ch; indent=tab}
  Rust{line≤100ch; indent=4sp}
  SQL{line≤80ch; indent=2sp}
}

R.complexity{
  cyclomatic≤10!; cognitive≤15!; param≤5→obj!;
  fn.lines≤30; nest≤3!
}

R.docs{
  ∀pub.API→JSDoc|docstring[params+return+throws+examples]
  TS=JSDoc; Py=Google_docstring; Go=comment_blocks
}

R.error{
  ¬swallow!; log+ctx!; custom_err_types; fail_fast; actionable_msg
  hierarchy{BaseError→[ValidationError,BusinessError,IntegrationError,SystemError]}
  ValidationError∋[RequiredField,InvalidFormat,OutOfRange]
  BusinessError∋[InsufficientFunds,DuplicateEntity,StateTransition]
  IntegrationError∋[Network,Timeout,ServiceUnavailable]
  SystemError∋[Database,Cache,Configuration]
  API.err.format{code;message;details;requestId;timestamp}
}

R.test{
  cov.line{min=80%⊕90%}; cov.branch{min=75%⊕85%}; cov.fn{min=85%⊕95%}
  naming="should [behavior] when [condition]"
  pattern=AAA[Arrange,Act,Assert]
  types{unit=∀commit; integration=∀PR; E2E=nightly; perf=weekly; security=∀PR}
  mock{ext_deps_only; ¬mock_under_test; realistic_data; inject_deps; reset_between}
}

R.arch{
  layers[Presentation,Application,Domain,Infrastructure]
  deps→inward; Domain.deps=∅; Infra.impl→Domain.iface
  structure{
    src/domain/[entities,value-objects,services,interfaces]
    src/application/[use-cases,services,dtos]
    src/infrastructure/[persistence,external-services,config]
    src/presentation/[controllers,middleware,validators]
  }
}

R.API{
  REST{GET=read; POST=create; PUT=replace; PATCH=partial; DELETE=remove}
  URL{nouns; plural; kebab-case; nest→relations; query→filter}
  codes{200=OK; 201=Created; 204=NoContent; 
        400=BadRequest; 401=Unauth; 403=Forbidden; 404=NotFound;
        409=Conflict; 422=Unprocessable; 429=RateLimit;
        500=ServerError; 503=Unavailable}
  pagination{data;page;pageSize;totalPages;totalItems;hasNext;hasPrevious;links}
  versioning=URL_path[/api/v{n}/]
}

R.git{
  commit="type(scope): desc"; types[feat→m; fix→p; docs|style|refactor|perf|test|chore|ci|build→∅]
  branch{feature/PROJ-{id}-{desc}; fix/PROJ-{id}-{desc}; 
         hotfix/PROJ-{id}-{desc}; release/v{M}.{m}.{p}; experiment/{desc}}
  protect{main[PR+2approval+CI+¬force]; develop[PR+1approval+CI]; 
          release/*[PR+2approval+CI+CODEOWNERS]}
  PR{lines<400; desc+ctx; link_issues; screenshots@UI; upd_docs; +tests; req_owners}
}

R.security{
  auth{OAuth2.0|OIDC; session_mgmt; secure_storage[httpOnly,secure]; ratelimit; log_events}
  validation{email=RFC5322+domain; phone=E.164; URL=https+domain; 
             num=type+range+precision; str=len+whitelist; file=type+size+content}
  data{rest=AES-256; transit=TLS1.3; pwd=bcrypt[cost≥12]; 
       PII=field_encrypt; query=parameterized; output=sanitize_XSS}
  secrets{env_vars; secrets_mgr[Vault,AWS]; rotate!; audit; 
          ¬commit_git!; ¬log!; ¬share_chat!; ¬reuse_env!}
  headers{CSP="default-src 'self'"; X-Content-Type-Options=nosniff;
          X-Frame-Options=DENY; X-XSS-Protection="1; mode=block";
          HSTS="max-age=31536000; includeSubDomains";
          Referrer-Policy=strict-origin-when-cross-origin}
}

R.db{
  query{idx→filter/sort; ¬SELECT_*; EXPLAIN; pagination; conn_pool}
  migration{reversible; ¬modify_existing; name=YYYYMMDD_desc; test_prod_data; backup!}
  naming{table=snake_case_plural; col=snake_case; PK=id; 
         FK={table}_id; idx=idx_{table}_{cols}; constraint={type}_{table}_{cols}}
}

R.logging{
  levels{ERROR=exceptions; WARN=handled; INFO=biz_events; DEBUG=diagnostic; TRACE=dev_only}
  format{timestamp;level;service;traceId;spanId;message;context}
  metrics{app[req_rate,err_rate,latency]; biz[signups,conversions,txn];
          infra[CPU,memory,disk,network]; deps[API_latency,fail_rate]}
  alerts{err_rate{warn>1%; crit>5%}; P99{warn>500ms; crit>2s};
         CPU{warn>70%; crit>90%}; mem{warn>75%; crit>90%}; disk{warn>80%; crit>95%}}
}

R.perf{
  latency{API.read[P50≤50ms;P95≤150ms;P99≤300ms];
          API.write[P50≤100ms;P95≤300ms;P99≤500ms];
          bg_job[P50≤1s;P95≤5s;P99≤30s]; batch[P50≤30s;P95≤60s;P99≤120s]}
  cache{browser[static=1yr]; CDN[pub_API=5m]; app[session=15m]; db[query=1hr]}
  optimize[compress;keepalive;caching;lazy_load;async_IO;batch_db;optimize_assets;pagination]
}

R.review{
  checklist[correctness;security;perf;readability;maintainability;tests;docs]
  feedback{specific; explain_why; suggest_alt; ask_?; ack_good}
  response{P0[1hr→4hr]; P1[4hr→1d]; P2[1d→3d]; P3[3d→1wk]}
}

R.flags{
  iface{name;enabled;rolloutPct;allowedUsers;allowedGroups;metadata}
  lifecycle[Created→Testing→Rollout→Enabled→Cleanup]
}

R.a11y{
  WCAG2.1_AA; perceivable[alt_text;captions;contrast≥4.5:1]
  operable[keyboard;¬seizure;sufficient_time]
  understandable[clear_lang;consistent_nav;input_assist]
  robust[valid_HTML;ARIA;screen_reader]
  checks{contrast[text=4.5:1;large=3:1]; focus_visible; alt_text; 
         heading_hierarchy; form_labels; keyboard_accessible; ARIA_roles}
}

R.release{
  semver=MAJOR.MINOR.PATCH[breaking.feat.fix]
  checklist[tests_pass;CHANGELOG;ver_bump;docs_upd;security_scan;perf_bench;rollback_plan;notify]
  deploy{blue_green=zero_downtime; canary=low_risk; rolling=standard; recreate=dev_only}
}

Ω{consistency; quality; security; perf; maintainability; a11y; reliability;
  ∀team→follow; deviation→discuss+doc_exception}
⟧
```
