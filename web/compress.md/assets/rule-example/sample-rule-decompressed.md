# Team Coding Standards (Decompressed from CRUX)

## 1) Naming conventions

### TypeScript

* **Variables & functions:** `camelCase`
* **Classes & interfaces:** `PascalCase`
* **Constants:** `SCREAMING_SNAKE_CASE`
* **Enums:**

  * Enum **name:** `PascalCase`
  * Enum **members:** `SCREAMING_SNAKE_CASE`

### Python

* **Variables & functions:** `snake_case`
* **Classes:** `PascalCase`
* **Private members:** prefix with `_` (single underscore)

### Go

* **Exported identifiers:** `PascalCase`
* **Unexported identifiers:** `camelCase`
* **Acronyms:** keep consistent casing (e.g., `HTTP`, `ID`) within identifiers

---

## 2) Code style rules

* **Function length:** ≤ 30 lines
* **Nesting depth:** ≤ 3 levels
* Prefer **early returns** over deep `if/else` blocks
* **One concept per function** (keep functions cohesive)
* Prefer **composition over inheritance**
* Follow **SRP (Single Responsibility Principle)**

---

## 3) Formatting standards

* **TypeScript:** 100 characters line length, 2-space indentation
* **Python:** 88 characters line length, 4-space indentation
* **Go:** 120 characters line length, tabs for indentation
* **Rust:** 100 characters line length, 4-space indentation
* **SQL:** 80 characters line length, 2-space indentation

---

## 4) Complexity limits

* **Cyclomatic complexity:** ≤ 10
* **Cognitive complexity:** ≤ 15
* **Parameter count:** ≤ 5 parameters per function
* **Nesting depth:** ≤ 3 levels (reinforces the style rule)

---

## 5) Documentation requirements

* **All public APIs must be documented.**
* For every **public** function/type/member, provide:

  * **TypeScript:** JSDoc
  * **Python:** docstring
  * **Go:** Go comment
* Documentation must include (as applicable):

  * Parameters
  * Return value
  * Throws/errors
  * Example usage

---

## 6) Error handling policy

### Policies

* **Do not swallow errors.**
* Log errors with **context**.
* Use **custom error types** (typed/structured errors).
* Prefer **fail-fast** behavior when correctness is at risk.
* Error messages must be **actionable** (tell the operator/dev what to do next).

### Error type hierarchy (example model)

Define a shared base error type containing:

* `code` (stable error code)
* `ts` (timestamp)
* `ctx` (structured context)

From the base type, derive:

* `ValidationError` (include `field`)
* `BusinessError`
* `IntegrationError` (include `svc` and `retry` semantics)
* `SystemError`

---

## 7) Testing standards

### Coverage targets

Set coverage thresholds with two “tiers” (baseline and stretch):

* **Line coverage:** ≥ 80% (target 90%)
* **Branch coverage:** ≥ 75% (target 85%)
* **Function coverage:** ≥ 85% (target 95%)

### Test naming + structure

* Test names must follow: **`"should [X] when [Y]"`**
* Use **AAA** structure: **Arrange → Act → Assert**

### Test cadence by type

* **Unit tests:** required per commit
* **Integration tests:** required per PR
* **End-to-end tests:** run nightly
* **Performance tests:** run weekly
* **Security tests:** required per PR

### Mocking policy

* Mock **external systems only**.
* **Do not** mock the thing you are explicitly testing.
* Mocks must be **realistic** (shape/behavior close to real dependencies).
* Prefer **DI (dependency injection)** to enable testability.
* Ensure mocks are **reset/cleaned** between tests.

---

## 8) Architecture

### Layering

Adopt a layered architecture:
**Presentation → Application → Domain → Infrastructure**

### Dependency rule

* Dependencies must flow **inward** only (outer layers can depend on inner layers; not vice versa).
* **Domain** must have **no external dependencies**.

### Source layout

Use the following directory structure:

* `domain/`

  * `entities/`
  * `values/`
  * `svc/`
  * `iface/`
* `app/`

  * `usecases/`
  * `svc/`
  * `dto/`
* `infra/`

  * `persist/`
  * `ext-svc/`
  * `cfg/`
* `presentation/`

  * `ctrl/`
  * `middleware/`
  * `validators/`

---

## 9) API standards (REST)

### HTTP semantics

* `GET` = read
* `POST` = create
* `PUT` = replace
* `PATCH` = partial update
* `DELETE` = remove

### URL conventions

* Use **nouns**, **plural**, **kebab-case**
* Support nesting where appropriate
* Prefer query parameters for filtering
* Pagination endpoints should be consistent
* API versioning via path: `/api/v{n}/`

### Status code conventions

* Success: `200`, `201`, `204`
* Client errors: `400`, `401`, `403`, `404`, `409`, `422`, `429`
* Server errors: `500`, `503`

### Pagination shape

Return:

* `data`
* `page`
* `total`
* `links`

---

## 10) Git standards

### Commit messages

Format: `type(scope): desc`

SemVer mapping guidance:

* `feat` → **minor**
* `fix` → **patch**
* `BREAKING` → **major**

### Branch naming

* `feature/PROJ-{id}-{desc}`
* `fix/PROJ-{id}-{desc}`
* `hotfix/PROJ-{id}-{desc}`
* `release/v{ver}`

### Branch protection

* `main`: PR required, **2 approvals**, CI required, **no force push**
* `develop`: PR required, **1 approval**, CI required
* `release`: requires **CODEOWNERS** enforcement

### Pull request hygiene

* PR should be **< 400 lines** (diff size guideline)
* Must include:

  * Description
  * Linked issues
  * Tests
  * Screenshots if UI changes

---

## 11) Security policies

### Auth/session

* OAuth2 or OIDC
* Use sessions where appropriate
* Cookies must be `httpOnly`
* Rate limiting enabled
* Log security-relevant events

### Input validation

* Validate everything
* Email: RFC 5322 compliant
* Phone: E.164 compliant
* URLs must be `https`
* Centralize and consistently apply validators

### Data protection

* At rest: AES-256
* In transit: TLS 1.3
* Password hashing: bcrypt cost ≥ 12
* Use parameterized queries
* Sanitize inputs/outputs as appropriate

### Secrets management

* Store secrets in environment variables or a vault
* Rotate secrets
* Audit access/use
* Never commit, log, or share secrets

### Security headers

Set:

* CSP
* `X-Content-Type-Options`
* `X-Frame-Options`
* HSTS
* Referrer-Policy

---

## 12) Database standards

### Querying

* Use indexes appropriately
* **No `SELECT *`**
* Use `EXPLAIN` for non-trivial queries
* Paginate results
* Use connection pooling

### Migrations

* Migrations must be **reversible**
* Do **not** modify existing migrations (append-only)
* Naming: `YYYYMMDD_name`
* Test migrations
* Ensure backups exist and are validated before risky changes

### Naming conventions

* Tables: `snake_case`, plural
* Columns: `snake_case`
* Primary key: `id`
* Foreign key: `{table}_id`
* Index: `idx_{table}_{column}`

---

## 13) Logging, metrics, and alerts

### Log levels

Use: `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`

### Log format

Structured JSON with:

* `ts`
* `level`
* `svc`
* `traceId`
* `msg`
* `ctx`

### Metrics

Track:

* Request rate
* Error rate
* Latency p50 / p95 / p99
* Business metrics
* Infrastructure metrics
* Dependency metrics

### Alert thresholds (warn/critical)

* Error rate: warn > 1%, critical > 5%
* p99 latency: warn > 500 ms, critical > 2 s
* CPU: warn > 70%, critical > 90%
* Memory: warn > 75%, critical > 90%
* Disk: warn > 80%, critical > 95%

---

## 14) Performance standards

### Latency SLOs (p50 / p95 / p99 guidance)

* **Reads:** ≤ 50 / 150 / 300 ms
* **Writes:** ≤ 100 / 300 / 500 ms
* **Background jobs:** ≤ 1 / 5 / 30 s

### Caching policy (typical TTLs)

* Browser: 1 year
* CDN: 5 minutes
* App cache: 15 minutes
* DB cache: 1 hour

### Optimization checklist

Use as applicable:

* gzip or brotli compression
* Keep-alive connections
* Effective caching
* Lazy loading
* Async processing
* Batching
* Pagination

---

## 15) Code review standards

### What to check

Review for:

* Correctness
* Security
* Performance
* Readability
* Maintainability
* Tests
* Documentation

### Feedback quality

Feedback must be:

* Specific
* Explain **why**
* Include a suggestion or ask a targeted question
  Avoid:
* Vague feedback
* Criticism without guidance

### Response expectations (SLA)

* **P0:** respond within 1–4 hours
* **P1:** within 4 hours–1 day
* **P2:** within 1–3 days
* **P3:** within 3 days–1 week

---

## 16) Feature flags (entity model)

A feature flag includes:

* `name`
* `enabled`
* `rollout%`
* `users[]`
* `groups[]`

Lifecycle:
**Created → Testing → Rollout → Enabled → Cleanup**

---

## 17) Accessibility (a11y)

Follow WCAG principles:

* **Perceivable:** alt text, captions, contrast ≥ 4.5:1
* **Operable:** keyboard support, time-based media controls
* **Understandable:** clear and consistent UI/content
* **Robust:** valid HTML, ARIA as needed, screen reader support

Checklist:

* Contrast
* Focus states
* Alt text
* Headings
* Forms
* Keyboard navigation
* ARIA usage

---

## 18) Release standards

### Versioning

Use SemVer:

* MAJOR = breaking change
* MINOR = feature
* PATCH = fix

### Release checklist

Must include:

* Tests passing
* Changelog updated
* Version bumped
* Docs updated
* Security review complete
* Performance checks complete
* Rollback plan ready
* Stakeholders notified

### Deployment strategies

Use one of:

* Blue/green
* Canary
* Rolling
* Recreate

---

## 19) Quality gates (team-wide)

* Everyone on the team must follow these standards.
* If deviation is needed: **discuss it and document it**.
* Goals:

  * Consistency
  * Quality
  * Security
  * Performance
  * Maintainability
  * Accessibility
  * Reliability
