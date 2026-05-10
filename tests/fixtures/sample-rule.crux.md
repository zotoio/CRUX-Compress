---
generated: 2026-05-10 19:01
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6354
afterTokens: 1309
reducedBy: 79%
confidence: 91%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Comprehensive Team Coding Standards

```crux
⟦CRUX:sample-rule.md
Ρ{team coding standards}
Κ{fn=function;cls=class;iface=interface;cov=coverage}

R.naming{
  JS/TS{var+fn=camelCase;cls+iface=PascalCase;
    const=SCREAMING_SNAKE;enum=Pascal+SCREAMING;typeParam=T|TName}
  Py{var+fn=snake_case;cls=PascalCase;const=SCREAMING_SNAKE;_=private}
  Go{exported=Pascal;unexported=camel;acronym=consistent}
}

R.style{
  fn≤30ln;early return;nest≤3!;1concept/fn;composition≻inheritance;SRP
  format{JS=100ch+2sp;Py=88ch+4sp;Go=120ch+tabs;Rust=100ch+4sp;SQL=80ch+2sp}
  complexity{cyclomatic≤10!;cognitive≤15!;params≤5!;nest≤3!}
}

R.docs{∀pub→jsdoc[params+return+throws+example];Py→Google docstrings;Go→comment}

R.errors{
  ¬swallow!;log+ctx;custom types;fail-fast;actionable msg
  hierarchy{Base→[Validation(Required|Format|Range),
    Business(Funds|Duplicate|StateTransition),
    Integration(Network|Timeout|Unavailable),
    System(DB|Cache|Config)]}
  Base∋{code,timestamp,ctx};API→{code,msg,details,reqId,ts}
}

R.test{
  cov{line≥80%⊕90%;branch≥75%⊕85%;fn≥85%⊕95%}
  naming="should [behavior] when [condition]";pattern=AAA
  categories{unit→∀commit;integration→∀PR;e2e→nightly;perf→weekly;SAST→∀PR}
  mock{ext only;¬SUT;realistic;DI;reset}
}

Π.arch{
  layers=[Presentation,Application,Domain,Infrastructure]
  deps→inward;domain=¬ext.deps;infra→impl iface
  src/[domain/[entities,value-objects,services,interfaces],
    application/[use-cases,services,dtos],
    infrastructure/[persistence,external-services,config],
    presentation/[controllers,middleware,validators]]
}

R.api{
  REST{GET=read;POST=create;PUT=replace;PATCH=partial;DELETE=remove}
  url{nouns;plural;kebab-case;/{id}/sub;?key=val}
  status{200;201;204;400;401;403;404;409;422;429;500;503}
  pagination∋{data,page,links};versioning=/api/v{n}/
}

R.git{
  commits=conventional{type(scope):desc}
  types{feat→minor;fix→patch;docs|style|refactor|test|chore→none}
  branches{feature|fix|hotfix/PROJ-{id}-{desc};release/v{M.m.p}}
  protection{main=PR+2approvals+CI+¬force;develop=PR+1+CI}
  PR{<400ln;desc+ctx;link issues;+tests;CODEOWNERS}
}

R.security{
  auth{OAuth2.0+OIDC;session mgmt;httpOnly;rate-limit;log events}
  input{email=RFC5322;phone=E.164;url=https;num=type+range;str=len+charset;file=type+size}
  data{AES-256@rest;TLS1.3@transit;bcrypt(≥12);PII→field encrypt;parameterized!;¬XSS}
  secrets{env vars;vault;rotate;audit;¬commit!;¬log!;¬share!}
  headers=[CSP,X-Content-Type-Options:nosniff,X-Frame-Options:DENY,HSTS,Referrer-Policy]
}

R.db{
  query{indexes;¬SELECT *;EXPLAIN;paginate;conn pool}
  migrations{reversible;¬modify existing;YYYYMMDD_desc;test prod-like;backup}
  naming{tables=snake+plural;cols=snake;PK=id;FK={t}_id;idx=idx_{t}_{c}}
}

R.logging{
  levels{ERROR=exceptions;WARN=handled;INFO=biz;DEBUG=diagnostic;TRACE=dev}
  format=JSON{ts,level,svc,traceId,spanId,msg,ctx}
  metrics{app=[req,err,latency(p50/95/99)];biz=[signups,txns];infra=[CPU,mem,disk]}
  alerts{err>1%w>5%c;p99>500ms.w>2s.c;CPU>70%w>90%c;mem>75%w>90%c;disk>80%w>95%c}
}

R.perf{
  targets{read=50/150/300ms;write=100/300/500ms;bg=1/5/30s;batch=30/60/120s}
  cache{browser=1yr;CDN=5min;app=15min;db=1hr}
  checklist=[compress,keep-alive,cache,lazy-load,async,batch,optimize,paginate]
}

R.review{
  checklist=[correctness,security,perf,readability,maintainability,tests,docs]
  feedback{specific;explain why;suggest alt;ask→understand;acknowledge}
  response{P0=1hr→4hr;P1=4hr→1d;P2=1d→3d;P3=3d→1wk}
}

R.flags{
  iface{name;enabled;rolloutPct;allowedUsers;allowedGroups;metadata}
  check{¬flag→⊥;¬enabled→⊥;allowed→⊤;hash%100<pct}
  lifecycle=[Created→Testing→Rollout→Enabled→Cleanup]
}

R.a11y{
  WCAG2.1.AA{perceivable=[alt,captions,contrast≥4.5:1];
    operable=[keyboard,¬seizure];understandable=[clear,consistent];
    robust=[valid HTML,ARIA,screen reader]}
  checklist{contrast≥4.5:1;focus=visible;alt;h1→h2→h3;forms=labels;keyboard=∀}
}

R.release{
  semver=M.m.p{M=breaking;m=feat;p=fix}
  checklist=[tests,CHANGELOG,ver,docs,security,perf,rollback,notify]
  deploy{blue-green=0-downtime;canary=low-risk;rolling=std;recreate=dev}
}

Ω{consistency;quality;security;perf;maintainability;a11y;reliability;
  ∀team→follow;deviation→discuss+document}
⟧
```
