---
generated: 2026-04-26 00:49
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6354
afterTokens: 1502
reducedBy: 76%
confidence: 93%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Comprehensive Team Coding Standards

```crux
⟦CRUX:sample-rule.md
Ρ{team coding standards; all langs; quality+security+perf}

Κ{fn=function; cls=class; iface=interface; cfg=config;
  var=variable; param=parameter; ctx=context; svc=service}

R.naming.js{
  var+fn=camelCase; cls+iface=PascalCase; const=SCREAMING_SNAKE;
  enum.name=PascalCase; enum.val=SCREAMING_SNAKE; typeParam=T|TName
}
R.naming.py{
  var+fn=snake_case; cls=PascalCase; const=SCREAMING_SNAKE;
  private=_prefix
}
R.naming.go{
  exported=PascalCase; unexported=camelCase; acronyms=consistent(HTTP|ID)
}

R.style{
  fn.len≤30ln; early return; nest≤3; composition≻inheritance; SRP;
  JS/TS:100ch,2sp; Py:88ch,4sp; Go:120ch,tabs; Rust:100ch,4sp; SQL:80ch,2sp
}
R.complexity{cyclomatic≤10; cognitive≤15; params≤5; nest≤3}

R.docs{
  ∀public.API→jsdoc[params+return+throws+examples];
  Py=Google docstrings; Go=// fn comment
}

R.err{
  ¬swallow; log+ctx; custom types; fail fast; actionable msgs;
  hierarchy: Base→[Validation,Business,Integration,System]→subtypes;
  API.err.format{code,message,details,requestId,timestamp}
}

R.test{
  cov{line≥80%⊕90%; branch≥75%⊕85%; fn≥85%⊕95%};
  naming="should [behavior] when [condition]"; AAA pattern;
  categories{Unit@commit; Integration@PR; E2E@nightly; Perf@weekly; Security@PR};
  mock ext only; ¬mock code under test; DI for testability; reset mocks
}

Π.arch{
  layers[Presentation→Application→Domain→Infrastructure];
  deps→inward; Domain=¬ext deps; Infra impl Domain ifaces
}
Π.files{
  src/[domain/[entities,value-objects,services,interfaces],
       application/[use-cases,services,dtos],
       infrastructure/[persistence,external-services,config],
       presentation/[controllers,middleware,validators]]
}

R.api{
  REST{GET=read; POST=create; PUT=replace; PATCH=partial; DELETE=remove};
  URL{nouns; plural; kebab-case; nest=/parent/{id}/child; query=filter};
  codes{200=OK; 201=Created; 204=NoContent; 400=Bad; 401=Unauth;
        403=Forbidden; 404=NotFound; 409=Conflict; 422=Semantic;
        429=RateLimit; 500=Internal; 503=Unavail};
  ∀list→paginate{page,pageSize,total,hasNext,links};
  version=/api/v{n}/
}

R.git{
  commit=type(scope):desc; types[feat→minor;fix→patch;
    docs|style|refactor|test|chore|ci|build→none];
  branch{feature/PROJ-{id}-{desc}; fix/; hotfix/; release/v{sem}; experiment/};
  main=PR+2approvals+CI+¬force; develop=PR+1approval+CI;
  PR{<400ln; desc+ctx; link issues; screenshots@UI; +docs; +tests; request CODEOWNERS}
}

P.security{
  auth{OAuth2.0|OIDC; session mgmt; secure token storage; rate limit; log all};
  input.val{email=RFC5322; phone=E.164; URL=https whitelist;
            num=type+range; str=len+whitelist; file=type+size+content};
  data{AES-256@rest; TLS1.3@transit; bcrypt≥12; field-level PII;
       parameterized queries; sanitize output→¬XSS};
  secrets{env vars; secrets mgr(Vault|AWS); rotate; audit; ¬git; ¬logs; ¬chat};
  headers{CSP; X-Content-Type-Options:nosniff; X-Frame:DENY;
          HSTS:31536000; Referrer-Policy}
}

R.db{
  query{∀filter|sort→index; ¬SELECT*; EXPLAIN; paginate; pool};
  migrations{reversible; ¬modify existing; desc name; test prod-like; backup};
  naming{tables=snake_plural; cols=snake; pk=id; fk={table}_id;
         idx=idx_{t}_{c}; constraint={type}_{t}_{c}}
}

R.logging{
  levels{ERROR=exceptions; WARN=handled; INFO=biz events; DEBUG=diag; TRACE=dev};
  format=JSON{timestamp,level,service,traceId,spanId,message,context};
  metrics{app=[req rate,err rate,latency p50/95/99]; biz=[signups,txn];
          infra=[cpu,mem,disk,net]; deps=[api latency,fail rate]};
  alerts{err>1%→warn,>5%→crit; p99>500ms→warn,>2s→crit;
         cpu>70%→warn,>90%→crit; mem>75%→warn,>90%→crit}
}

R.perf{
  latency{API.read:50/150/300ms; API.write:100/300/500ms;
          bg:1/5/30s; batch:30/60/120s};
  cache{browser=1yr static; CDN=5min API; app=15min session;
        db=1hr query};
  optimize[gzip,keep-alive,cache,lazy load,async IO,batch DB,
           compress images,paginate]
}

R.review{
  checklist[correct,secure,perf,readable,maintainable,tested,documented];
  feedback{specific+actionable; explain why; suggest alt; ask→understand};
  response{P0:1h→4h; P1:4h→1d; P2:1d→3d; P3:3d→1w}
}

R.flags{
  iface{name,enabled,rollout%,allowedUsers,allowedGroups,metadata};
  lifecycle[Created→Testing→Rollout→Enabled→Cleanup]
}

R.a11y{
  WCAG2.1AA; perceivable[alt,captions,contrast≥4.5:1];
  operable[keyboard,¬seizure,time]; understandable[clear,consistent,input help];
  robust[valid HTML,ARIA,screen reader];
  checks{contrast,focus,alt,heading hierarchy,form labels,keyboard,ARIA}
}

R.release{
  semver=MAJOR.MINOR.PATCH; checklist[tests,CHANGELOG,version,docs,
    security scan,perf bench,rollback plan,notify];
  deploy{Blue-Green=0 downtime; Canary=low risk; Rolling=standard; Recreate=dev}
}

Ω{consistency; quality; security; perf; maintainability; a11y; reliability;
  ∀team→follow; deviation→discuss+doc exception}
⟧
```
