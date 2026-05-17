---
generated: 2026-05-17 16:36
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6354
afterTokens: 1442
reducedBy: 77%
confidence: 93%
crux: true
---

> [!IMPORTANT]
> Generated file - do not edit!

# Comprehensive Team Coding Standards

```crux
⟦CRUX:sample-rule.md
Ρ{team coding standards; ∀members!}
Κ{fn=function; cls=class; iface=interface; cov=coverage; svc=service}

R.naming{
  JS/TS{var+fn=camelCase; cls+iface=PascalCase; const=UPPER_SNAKE;
    enum=PascalCase+UPPER_SNAKE vals; type.param=[T,K,V]|PascalCase}
  PY{var+fn=snake_case; cls=PascalCase; const=UPPER_SNAKE; private=_prefix}
  GO{exported=PascalCase; unexported=camelCase; acronyms=consistent}
}

R.style{fn.len≤30; early return; nesting≤3!; 1concept/fn;
  composition≻inheritance; SRP}

R.format{JS/TS=100ch+2sp; PY=88ch(Black)+4sp; GO=120ch+tabs;
  Rust=100ch+4sp; SQL=80ch+2sp}

R.complexity{cyclomatic≤10!; cognitive≤15!; params≤5!(→obj); nesting≤3!}

R.docs{∀public→JSDoc[params+return+throws+example]; PY→Google; GO→godoc}

R.err{¬swallow!; log+ctx; custom types; fail-fast; actionable msg;
  hierarchy{Base→[Validation(Required|InvalidFormat|OutOfRange),
    Business(InsufficientFunds|Duplicate|StateTransition),
    Integration(Network|Timeout|Unavailable),
    System(DB|Cache|Config)]};
  Base∋{code,timestamp,ctx}; Validation∋{field};
  Integration∋{svc,retryable};
  API.err→{code,message,details,requestId,timestamp}}

R.test{cov{line≥80%⊕90%; branch≥75%⊕85%; fn≥85%⊕95%};
  naming="should [behavior] when [condition]"; AAA pattern;
  unit=∀commit; integration=∀PR; e2e=nightly; perf=weekly; security=∀PR;
  mock external only!; ¬mock SUT; realistic data; DI; reset}

Π.arch{layers=[Presentation,Application,Domain,Infrastructure];
  deps→inward; domain=¬ext deps; infra→impl domain ifaces;
  src/[domain/[entities,value-objects,services,interfaces],
    application/[use-cases,services,dtos],
    infrastructure/[persistence,external-services,config],
    presentation/[controllers,middleware,validators]]}

R.api{REST{GET=read;POST=create;PUT=replace;PATCH=partial;DELETE=remove};
  url{nouns¬verbs; plural; kebab-case; /{id}/sub; ?key=val};
  codes{200=OK;201=Created;204=NoContent;400=BadReq;401=Unauth;
    403=Forbidden;404=NotFound;409=Conflict;422=Unprocessable;
    429=RateLimit;500=ServerErr;503=Unavailable};
  pagination!{data+{page,pageSize,totals,hasNext/Prev}+links};
  versioning=URL(/api/v1/)}

R.git{conventional commits{type(scope):desc};
  feat→minor; fix→patch; docs|style|refactor|test|chore|ci|build→none;
  branch{feature|fix|hotfix/PROJ-{id}-{desc}; release/v{M}.{m}.{p};
    experiment/{desc}};
  main=PR+2approvals+CI+¬force-push; develop=PR+1+CI;
  release=PR+2+CI+CODEOWNERS;
  PR{<400ln; +desc; link issues; +screenshots(UI); +docs+tests}}

R.security{auth{OAuth2.0+OIDC; session mgmt; httpOnly; rate-limit; log};
  input{email=RFC5322; phone=E.164; url=https; num=type+range;
    str=len+charset; files=type+size+content};
  data{AES-256@rest; TLS1.3@transit; bcrypt≥12; encrypt PII;
    parameterized queries!; sanitize→¬XSS};
  secrets{env vars!; mgr(Vault|AWS); rotate!;
    ¬commit!; ¬log!; ¬share!; ¬reuse envs!};
  headers!{CSP; X-Content-Type-Options:nosniff; X-Frame-Options:DENY;
    HSTS:31536000; Referrer-Policy:strict-origin-when-cross-origin}}

R.db{indexes∀filter/sort; ¬SELECT*; EXPLAIN; paginate; conn pool;
  migrations{reversible!; ¬modify!; descriptive names; test prod-like; backup};
  naming{tables=snake_case+plural; cols=snake_case; PK=id;
    FK={table}_id; idx=idx_{t}_{c}; constraint={type}_{t}_{c}}}

R.logging{ERROR=exceptions; WARN=handled; INFO=biz; DEBUG=diag; TRACE=dev;
  format=JSON{timestamp,level,service,traceId,spanId,msg,ctx};
  metrics{app=[req,err,latency p50/95/99]; biz=[signups,conversions,txns];
    infra=[CPU,mem,disk,net]; deps=[latency,fail rate]};
  alerts{err>1%→warn,>5%→crit; p99>500ms→warn,>2s→crit;
    CPU>70/90; mem>75/90; disk>80/95}}

R.perf{targets{read=50/150/300ms; write=100/300/500ms;
    bg=1/5/30s; batch=30/60/120s};
  cache{browser=1yr; CDN=5min; app=15min; db=1hr};
  optimize[compression,keep-alive,caching,lazy-load,
    async IO,batch DB,optimize assets,paginate]}

R.review{checklist=[correctness,security,perf,readability,
    maintainability,tests,docs];
  feedback{specific; explain why; suggest alt; ¬vague; ¬dismissive};
  P0=1hr→4hr; P1=4hr→1d; P2=1d→3d; P3=3d→1wk}

R.flags{FeatureFlag{name,enabled,rollout%,allowedUsers,allowedGroups,meta};
  lifecycle=[Created→Testing→Rollout→Enabled→Cleanup]}

R.a11y{WCAG2.1.AA!; contrast≥4.5:1; keyboard!; alt∀imgs;
  heading hierarchy; form labels; ARIA; screen reader;
  ¬seizure; valid HTML}

R.release{semver; checklist=[tests,CHANGELOG,ver,docs,security,
    perf,rollback plan,notify];
  deploy{blue-green|canary|rolling|recreate}}

Ω{consistent+quality+secure+performant+maintainable+accessible+reliable;
  ∀team→follow!; deviation→discussion+exception}
⟧
```
