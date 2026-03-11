---
generated: 2026-02-08 10:15
sourceChecksum: "2253728265"
beforeTokens: 6278
afterTokens: 1059
reducedBy: 83%
confidence: 95%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Comprehensive Team Coding Standards

```crux
⟦CRUX:sample-rule.md
Ρ{team coding standards}
Κ{fn=function;cls=class;iface=interface;cov=coverage;PR=pull request}

R.naming{
  ts:var+fn=camelCase;cls+iface=PascalCase;const=SCREAMING_SNAKE;enum=Pascal:SCREAMING;
  py:var+fn=snake_case;cls=PascalCase;private=_prefix;
  go:exported=Pascal;unexported=camel;acronym=consistent(HTTP|ID)
}
R.style{fn≤30ln;nest≤3;early_return;1concept/fn;composition≻inherit;SRP}
R.format{ts:100ch/2sp;py:88ch/4sp;go:120ch/tab;rust:100ch/4sp;sql:80ch/2sp}
R.complexity{cyclomatic≤10;cognitive≤15;params≤5;nest≤3}
R.docs{∀public→jsdoc|docstring|gocomment[params+return+throws+example]}

P.err{¬swallow;log+ctx;custom_types;fail_fast;actionable_msg}
E.err{Base{code;ts;ctx}→[Validation{field},Business,Integration{svc;retry},System]}

R.test{
  cov:line≥80%⊕90%;branch≥75%⊕85%;fn≥85%⊕95%;
  name="should [X] when [Y]";AAA=Arrange»Act»Assert;
  unit→commit;integration→PR;e2e→nightly;perf→weekly;security→PR;
  mock:external_only;¬mock_tested;realistic;DI;reset
}

Π.arch{Presentation→Application→Domain→Infrastructure;deps_inward;Domain=no_ext_deps}
Π.src{domain/[entities,values,svc,iface];app/[usecases,svc,dto];
  infra/[persist,ext-svc,cfg];presentation/[ctrl,middleware,validators]}

R.api{
  rest:GET=read;POST=create;PUT=replace;PATCH=partial;DELETE=remove;
  url:nouns+plural+kebab+nest+query_filter;
  status:200|201|204=ok;400|401|403|404|409|422|429=client;500|503=server;
  pagination:{data,page,total,links};version:/api/v{n}/
}

R.git{
  commit:type(scope):desc;feat→minor;fix→patch;BREAKING→major;
  branch:feature|fix|hotfix/PROJ-{id}-{desc};release/v{ver};
  protect:main=PR+2+CI+¬force;develop=PR+1+CI;release=+CODEOWNERS;
  PR:<400ln;+desc+issues+tests;screenshots_if_UI
}

P.security{
  auth:OAuth2|OIDC;session;httpOnly;rate_limit;log_events;
  input:email=RFC5322;phone=E.164;url=https;validate_all;
  data:rest=AES256;transit=TLS1.3;pwd=bcrypt≥12;param_queries;sanitize;
  secrets:env|vault;rotate;audit;¬commit|log|share;
  headers:CSP+X-Content-Type+X-Frame+HSTS+Referrer
}

R.db{query:idx;¬SELECT*;EXPLAIN;paginate;pool;
  migrate:reversible;¬modify_existing;YYYYMMDD_name;test+backup;
  naming:table=snake_plural;col=snake;pk=id;fk={t}_id;idx=idx_{t}_{c}}

R.log{levels:ERROR|WARN|INFO|DEBUG|TRACE;
  format:json{ts,level,svc,traceId,msg,ctx};
  metrics:req_rate+err_rate+latency(p50/95/99)+biz+infra+deps;
  alerts:err>1%warn>5%crit;p99>500ms|2s;cpu>70|90;mem>75|90;disk>80|95}

R.perf{latency:read≤50/150/300ms;write≤100/300/500ms;bg≤1/5/30s;
  cache:browser=1yr;cdn=5m;app=15m;db=1hr;
  optimize:gzip|brotli;keepalive;cache;lazy;async;batch;paginate}

R.review{check:correct+secure+perf+readable+maintainable+tested+documented;
  feedback:specific+why+suggest+ask;¬vague|criticize_only;
  response:P0=1→4hr;P1=4hr→1d;P2=1d→3d;P3=3d→1wk}

E.feature_flag{name;enabled;rollout%;users[];groups[];
  lifecycle:Created→Testing→Rollout→Enabled→Cleanup}

R.a11y{wcag:perceivable(alt+caption+contrast4.5:1);operable(kbd+time);
  understandable(clear+consistent);robust(html+aria+screenreader);
  check:contrast+focus+alt+headings+forms+kbd+aria}

R.release{semver:MAJOR=break;MINOR=feat;PATCH=fix;
  checklist:tests+changelog+version+docs+security+perf+rollback+notify;
  deploy:blue_green|canary|rolling|recreate}

Ω{∀team→follow;deviation→discuss+document;
  goals=[consistency,quality,security,perf,maintainability,a11y,reliability]}
⟧
```
