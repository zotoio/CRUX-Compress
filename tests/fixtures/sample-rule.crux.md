---
generated: 2026-04-25 19:21
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6354
afterTokens: 2082
reducedBy: 67%
confidence: 95%
crux: true
---

> [!IMPORTANT]
> Generated file - do not edit!

# Comprehensive Team Coding Standards

```crux
⟦CRUX:sample-rule.md
Ρ{team coding standards; ∀team→follow}

Κ{fn=function; cls=class; var=variable; const=constant;
  cfg=config; env=environment; param=parameter;
  PII=personally identifiable info; PR=pull request}

R.naming.js/ts{
  var+fn=camelCase; cls+iface=PascalCase;
  const=SCREAMING_SNAKE; enum.name=PascalCase,enum.val=SCREAMING_SNAKE;
  type.param=[T|K|V|TRequest|TResponse]}

R.naming.py{
  var+fn=snake_case; cls=PascalCase; const=SCREAMING_SNAKE;
  private=_prefix}

R.naming.go{
  exported=PascalCase; unexported=camelCase;
  acronym=consistent[HTTPClient|userID|parseJSON]}

R.style{
  fn.lines≤20..30; early returns; nesting≤3; self-doc names;
  1concept/fn; composition≻inheritance; SRP}

R.format{
  js/ts:{line≤100ch;indent=2sp};
  py:{line≤88ch(Black);indent=4sp};
  go:{line≤120ch;indent=tabs};
  rust:{line≤100ch;indent=4sp};
  sql:{line≤80ch;indent=2sp}}

R.complexity{
  cyclomatic≤10!; cognitive≤15!; params≤5!;
  fn.lines≤30; nesting≤3!}

R.docs{
  ∀public.API→jsdoc[params+return+throws+examples];
  py→Google docstrings; go→godoc comments}

R.err{
  ¬swallow!; log+ctx!; custom types for domain;
  fail.fast on unrecoverable; actionable msgs}

E.err.hierarchy{
  BaseError∋[ValidationError{RequiredField|InvalidFormat|OutOfRange},
    BusinessError{InsufficientFunds|DuplicateEntity|StateTransition},
    IntegrationError{Network|Timeout|ServiceUnavailable},
    SystemError{Database|Cache|Configuration}]}

R.err.response{json:{error:{code,message,details,requestId,timestamp}}}

R.test.cov{line:≥80%⊕90%; branch:≥75%⊕85%; fn:≥85%⊕95%}

R.test.naming{"should [behavior] when [condition]"}

R.test.structure{AAA:[Arrange»Act»Assert]}

R.test.categories{
  unit→∀commit; integration→∀PR; e2e→nightly;
  perf→weekly; security→∀PR}

R.test.mock{
  mock.external.only[db,api,fs]; ¬mock.code.under.test;
  realistic.data; DI; reset.between.tests}

Π.arch{
  layers:[Presentation,Application,Domain,Infrastructure]→inward;
  domain=¬ext.deps; infra.impl←domain.iface}

Π.structure{
  src/{domain/[entities,value-objects,services,interfaces],
    application/[use-cases,services,dtos],
    infrastructure/[persistence,external-services,config],
    presentation/[controllers,middleware,validators]}}

R.api.rest{
  GET=retrieve; POST=create(¬idempotent); PUT=replace;
  PATCH=partial; DELETE=remove}

R.api.url{
  nouns¬verbs; plural; kebab-case;
  nest=relationships; query=filtering}

R.api.codes{
  200=OK; 201=Created; 204=NoContent;
  400=BadRequest; 401=Unauthorized; 403=Forbidden;
  404=NotFound; 409=Conflict; 422=Unprocessable;
  429=RateLimit; 500=ServerError; 503=Unavailable}

R.api.pagination{
  data+pagination{page,pageSize,totalPages,totalItems,hasNext,hasPrevious}
  +links{self,next,last}}

R.api.version{path:/api/v{n}/; v1=deprecated@2024-06-01; v2=current; v3=beta}

R.git.commit{
  format:"type(scope): desc\n\nBody\n\nFixes #N\nBREAKING CHANGE:"}

R.git.types{
  feat→minor; fix→patch; docs|style|refactor|test|chore|ci|build→none;
  perf→patch}

R.git.branch{
  feature/PROJ-{id}-{desc}; fix/PROJ-{id}-{desc};
  hotfix/PROJ-{id}-{desc}; release/v{M}.{m}.{p};
  experiment/{desc}}

R.git.protect{
  main:PR+2approvals+CI+¬force;
  develop:PR+1approval+CI;
  release/*:PR+2approvals+CI+CODEOWNERS}

R.pr{lines<400; desc+context; link.issues; screenshots@UI;
  upd.docs; +tests; req.codeowners}

R.security.auth{
  OAuth2.0|OIDC; session.mgmt; secure.storage[httpOnly,secure];
  rate.limit@auth; log.∀auth.events}

R.security.input{
  email=RFC5322+domain.verify; phone=E.164;
  url=protocol.whitelist[https]+domain.val;
  numbers=type+range+precision;
  strings=length+charset.whitelist;
  files=type+size+content.val}

R.security.data{
  rest:AES-256; transit:TLS1.3;
  pwd:bcrypt(cost≥12); PII:field.encrypt;
  db:parameterized.queries!; output:sanitize→¬XSS}

R.security.secrets{
  use:env.vars|secrets.mgr[Vault,AWS];
  rotate.regularly; audit.access;
  ¬commit; ¬log; ¬share.via.chat; ¬same.across.envs}

R.security.headers{
  CSP:default-src 'self';
  X-Content-Type-Options:nosniff;
  X-Frame-Options:DENY;
  X-XSS-Protection:1;mode=block;
  HSTS:max-age=31536000;includeSubDomains;
  Referrer-Policy:strict-origin-when-cross-origin}

R.db.query{
  idx→filtered/sorted cols; ¬SELECT *;
  EXPLAIN→analyze; paginate; conn.pool}

R.db.migrate{
  reversible[up/down]; ¬modify.existing;
  name=YYYYMMDD_desc; test@prod.like.data; backup.first}

R.db.naming{
  tables=snake_case.plural; cols=snake_case;
  pk=id; fk={table}_id;
  idx=idx_{table}_{cols}; constraint={type}_{table}_{cols}}

R.log.levels{
  ERROR=exceptions+failures; WARN=unexpected.handled;
  INFO=business.events; DEBUG=diagnostics;
  TRACE=dev.only}

R.log.format{json:{timestamp,level,service,traceId,spanId,message,context}}

R.metrics{
  app:[req.rate,err.rate,latency.p50.p95.p99];
  biz:[signups,conversions,txns];
  infra:[cpu,mem,disk,net];
  deps:[ext.api.latency,failure.rate]}

R.alerts{
  err.rate:warn>1%,crit>5%;
  p99.latency:warn>500ms,crit>2000ms;
  cpu:warn>70%,crit>90%;
  mem:warn>75%,crit>90%;
  disk:warn>80%,crit>95%}

R.perf.targets{
  api.read:p50=50ms,p95=150ms,p99=300ms;
  api.write:p50=100ms,p95=300ms,p99=500ms;
  bg.jobs:p50=1s,p95=5s,p99=30s;
  batch:p50=30s,p95=60s,p99=120s}

R.cache{
  browser:static@1yr; CDN:public.api@5min;
  app:session+computed@15min; db:query@1hr}

R.perf.checklist{
  compress[gzip,brotli]; keep-alive; cache;
  lazy.load; async.IO; batch.db; optimize.assets; paginate}

R.review.checklist{
  correctness; security; performance; readability;
  maintainability; tests; docs}

R.review.feedback{
  specific+actionable; explain.why; suggest.alternatives;
  ask.to.understand; acknowledge.good.work}

R.review.sla{
  P0:response=1hr,resolve=4hr;
  P1:response=4hr,resolve=1d;
  P2:response=1d,resolve=3d;
  P3:response=3d,resolve=1wk}

R.feature.flags{
  iface:{name,enabled,rolloutPct,allowedUsers,allowedGroups,metadata};
  check:flag.enabled→allowedUsers|rolloutPct}

R.feature.lifecycle{
  Created→Testing→Rollout→Enabled→Cleanup}

R.a11y.wcag{
  perceivable:[alt.text,captions,contrast≥4.5:1];
  operable:[keyboard,¬seizure,time];
  understandable:[clear.lang,consistent.nav,input.help];
  robust:[valid.HTML,ARIA,screen.reader]}

R.a11y.checklist{
  contrast:4.5:1.text,3:1.large; focus.indicators;
  alt.text; heading.hierarchy; form.labels;
  keyboard.access; ARIA.roles}

R.release.semver{MAJOR.MINOR.PATCH;
  MAJOR=breaking; MINOR=features.compat; PATCH=fixes.compat}

R.release.checklist{
  tests.pass; CHANGELOG; version.bump; docs.upd;
  security.scan; perf.bench; rollback.plan; notify.stakeholders}

R.deploy.strategy{
  blue-green:zero.downtime,risk=med;
  canary:high.risk.changes,risk=low;
  rolling:standard,risk=med;
  recreate:dev.only,risk=high}

Ω{consistency; quality; security; performance;
  maintainability; accessibility; reliability;
  ∀team→follow; deviations→discuss+document}
⟧
```
