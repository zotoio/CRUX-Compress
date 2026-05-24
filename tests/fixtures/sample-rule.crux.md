---
generated: 2026-05-24 19:28
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6354
afterTokens: 1122
reducedBy: 82%
confidence: 89%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Comprehensive Team Coding Standards

```crux
⟦CRUX:tests/fixtures/sample-rule.md
Ρ{team coding standards; multi-lang}
Κ{fn=function;cls=class;iface=interface;cov=coverage;pr=pull request}

R.naming{
  JS/TS{var+fn=camelCase;cls+iface=PascalCase;const=UPPER_SNAKE;enum=Pascal:UPPER_SNAKE;typeParam=T|Pascal}
  Py{var+fn=snake_case;cls=PascalCase;const=UPPER_SNAKE;private=_prefix}
  Go{exported=Pascal;unexported=camel;acronym=consistent}
}

R.style{
  fn≤30ln;early return;nest≤3;SRP;composition≻inheritance
  format{JS:100ch/2sp;Py:88ch/4sp;Go:120ch/tabs;Rust:100ch/4sp;SQL:80ch/2sp}
  limits{cyclomatic≤10!;cognitive≤15!;params≤5!;nest≤3!}
}

R.docs{∀public→jsdoc|docstring|godoc[params+return+throws+example]}

R.errors{
  ¬swallow!;log+ctx!;custom types!;fail fast!;actionable msg!
  hierarchy{Base→[Validation,Business,Integration,System]→subtypes}
  response=JSON{code,msg,details,requestId,timestamp}
}

R.testing{
  cov{line≥80%⊕90%;branch≥75%⊕85%;fn≥85%⊕95%}
  name="should [X] when [Y]";pattern=AAA
  run{unit→∀commit;integration→∀PR;e2e→nightly;perf→weekly;security→∀PR}
  mock{external only!;¬mock SUT;realistic;DI;reset}
}

Π.arch{
  layers=[Presentation,Application,Domain,Infrastructure]→inward deps
  domain=¬ext.deps;infra.impl→domain.iface
  src/[domain/,application/,infrastructure/,presentation/]
}

R.api{
  REST{GET;POST;PUT;PATCH;DELETE}→standard semantics
  URL{nouns;plural;kebab-case;nest=rels;query=filter}
  codes{2xx=[200,201,204];4xx=[400,401,403,404,409,422,429];5xx=[500,503]}
  pagination{data+meta[page,size,total,hasNext]+links}
  ver=URL /api/v{n}/
}

R.git{
  commits=conventional{type(scope):desc}
  types{feat→minor;fix→patch;docs|style|refactor|test|chore→none}
  branch{feature|fix|hotfix/PROJ-{id}-{desc};release/v{semver};experiment/{desc}}
  protect{main:PR+2approvals+CI+¬force;develop:PR+1+CI;release:+CODEOWNERS}
  PR{<400ln;desc;link issues;+tests;screenshots(UI)}
}

R.security{
  auth=OAuth2/OIDC;session;httpOnly;rate limit;log
  input{email=RFC5322;phone=E.164;url=https;num=range;str=len;file=type+size}
  data{rest=AES-256;transit=TLS1.3;pw=bcrypt≥12;PII=encrypt;DB=parameterized;¬XSS}
  secrets{env|vault;¬git!;¬log!;rotate;¬share;¬reuse}
  headers=[CSP,X-Content-Type-Options,X-Frame-Options,HSTS,Referrer-Policy]
}

R.db{
  query{idx!;¬SELECT*;EXPLAIN;paginate;pool}
  migrations{reversible;¬modify existing;test prod-like;backup}
  naming{tables=snake_plural;cols=snake;PK=id;FK={t}_id;idx=idx_{t}_{c}}
}

R.logging{
  levels=[ERROR,WARN,INFO,DEBUG,TRACE]
  format=JSON{timestamp,level,svc,traceId,msg,ctx}
  metrics{app=[rate,err,latency];biz=[signups,txns];infra=[CPU,mem,disk]}
  alerts{err:>1%warn/>5%crit;p99:>500ms/>2s;CPU:>70%/>90%;mem:>75%/>90%;disk:>80%/>95%}
}

R.perf{
  targets{read:50/150/300ms;write:100/300/500ms;bg:1/5/30s;batch:30/60/120s}
  cache{browser:1yr;CDN:5min;app:15min;DB:1hr}
  optimize=[compress,keep-alive,cache,lazy-load,async,batch,pagination]
}

R.review{
  check=[correctness,security,perf,readability,maintainability,tests,docs]
  feedback{specific;explain why;suggest alt;acknowledge good}
  SLA{P0:1hr→4hr;P1:4hr→1d;P2:1d→3d;P3:3d→1wk}
}

R.flags{lifecycle=[Created→Testing→Rollout→Enabled→Cleanup];rollout=hash%<pct}

R.a11y{
  WCAG2.1.AA{perceivable;operable;understandable;robust}
  checks{contrast≥4.5:1;focus:visible;alt:∀img;headings:logical;keyboard:∀fn;ARIA}
}

R.release{
  semver{M=breaking;m=feat;p=fix}
  checklist=[tests,CHANGELOG,ver,docs,security,perf,rollback,notify]
  deploy{blue-green|canary|rolling|recreate}
}

Ω{consistency;quality;security;perf;maintainability;a11y;reliability;∀team→follow}
⟧
```
