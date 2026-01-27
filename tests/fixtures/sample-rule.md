---
crux: true
alwaysApply: true
---

# Comprehensive Team Coding Standards

This document defines the complete coding standards for our engineering team. All team members must follow these guidelines to ensure consistent, maintainable, secure, and high-quality code.

## Code Quality Guidelines

### Naming Conventions

#### JavaScript/TypeScript

1. **Variables and Functions**: Use camelCase
   - Good: `getUserById`, `isValidEmail`, `maxRetryCount`
   - Bad: `get_user_by_id`, `IsValidEmail`, `MAXRETRYCOUNT`

2. **Classes and Interfaces**: Use PascalCase
   - Good: `UserService`, `IAuthProvider`, `HttpClient`
   - Bad: `userService`, `iAuthProvider`, `httpClient`

3. **Constants**: Use SCREAMING_SNAKE_CASE for true constants
   - Good: `MAX_CONNECTIONS`, `API_BASE_URL`, `DEFAULT_TIMEOUT_MS`
   - Bad: `maxConnections`, `ApiBaseUrl`, `default_timeout_ms`

4. **Enums**: Use PascalCase for names, SCREAMING_SNAKE_CASE for values
   ```typescript
   enum HttpStatus {
       OK = 200,
       NOT_FOUND = 404,
       INTERNAL_SERVER_ERROR = 500
   }
   ```

5. **Type Parameters**: Use single uppercase letters or descriptive PascalCase
   - Good: `T`, `K`, `V`, `TRequest`, `TResponse`
   - Bad: `t`, `type`, `request_type`

#### Python

1. **Variables and Functions**: Use snake_case
   - Good: `get_user_by_id`, `is_valid_email`, `max_retry_count`
   - Bad: `getUserById`, `IsValidEmail`, `maxRetryCount`

2. **Classes**: Use PascalCase
   - Good: `UserService`, `AuthProvider`, `HttpClient`
   - Bad: `user_service`, `auth_provider`, `http_client`

3. **Constants**: Use SCREAMING_SNAKE_CASE
   - Good: `MAX_CONNECTIONS`, `API_BASE_URL`
   - Bad: `max_connections`, `api_base_url`

4. **Private Members**: Prefix with single underscore
   - Good: `_internal_method`, `_cache`
   - Bad: `internalMethod`, `__cache__`

#### Go

1. **Exported identifiers**: Use PascalCase (starts with uppercase)
   - Good: `GetUserByID`, `ValidateEmail`, `MaxConnections`

2. **Unexported identifiers**: Use camelCase (starts with lowercase)
   - Good: `getUserByID`, `validateEmail`, `maxConnections`

3. **Acronyms**: Keep consistent case
   - Good: `HTTPClient`, `userID`, `parseJSON`
   - Bad: `HttpClient`, `userId`, `parseJson`

### Code Style

#### General Principles

- Keep functions small and focused (20-30 lines maximum)
- Use early returns to avoid deep nesting
- Maximum nesting depth of 3 levels
- Write self-documenting code with clear variable names
- One concept per function
- Prefer composition over inheritance
- Follow the Single Responsibility Principle

#### Line Length and Formatting

| Language | Max Line Length | Indent |
|----------|-----------------|--------|
| JavaScript/TypeScript | 100 chars | 2 spaces |
| Python | 88 chars (Black) | 4 spaces |
| Go | 120 chars | tabs |
| Rust | 100 chars | 4 spaces |
| SQL | 80 chars | 2 spaces |

#### Function Complexity

| Metric | Threshold | Action |
|--------|-----------|--------|
| Cyclomatic complexity | ≤10 | Required |
| Cognitive complexity | ≤15 | Required |
| Parameters | ≤5 | Required, use object for more |
| Lines per function | ≤30 | Recommended |
| Nesting depth | ≤3 | Required |

### Documentation Standards

#### Public API Documentation

All public APIs must have comprehensive documentation:

```typescript
/**
 * Calculates the total price including tax and discounts.
 * 
 * This function applies the following rules:
 * 1. Base price is required and must be positive
 * 2. Tax rate is applied to the base price
 * 3. Discount is applied after tax calculation
 * 
 * @param basePrice - The price before tax (must be >= 0)
 * @param taxRate - The tax rate as a decimal (e.g., 0.1 for 10%)
 * @param discount - Optional discount amount to subtract
 * @returns The total price with tax minus any discount
 * @throws {ValidationError} When basePrice is negative
 * @throws {ValidationError} When taxRate is negative
 * 
 * @example
 * // Basic usage
 * const total = calculateTotalPrice(100, 0.1);
 * // Returns 110 (100 + 10% tax)
 * 
 * @example
 * // With discount
 * const discounted = calculateTotalPrice(100, 0.1, 15);
 * // Returns 95 (110 - 15 discount)
 */
function calculateTotalPrice(
    basePrice: number,
    taxRate: number,
    discount: number = 0
): number {
    if (basePrice < 0) {
        throw new ValidationError('Base price must be non-negative', 'basePrice');
    }
    if (taxRate < 0) {
        throw new ValidationError('Tax rate must be non-negative', 'taxRate');
    }
    return basePrice * (1 + taxRate) - discount;
}
```

#### Python Docstrings

Use Google-style docstrings for Python:

```python
def calculate_total_price(
    base_price: float,
    tax_rate: float,
    discount: float = 0.0
) -> float:
    """Calculate the total price including tax and discounts.

    This function applies tax to the base price and then subtracts
    any applicable discount.

    Args:
        base_price: The price before tax. Must be non-negative.
        tax_rate: The tax rate as a decimal (e.g., 0.1 for 10%).
        discount: Optional discount amount to subtract. Defaults to 0.

    Returns:
        The total price with tax minus any discount.

    Raises:
        ValueError: If base_price or tax_rate is negative.

    Examples:
        >>> calculate_total_price(100, 0.1)
        110.0
        >>> calculate_total_price(100, 0.1, 15)
        95.0
    """
    if base_price < 0:
        raise ValueError("base_price must be non-negative")
    if tax_rate < 0:
        raise ValueError("tax_rate must be non-negative")
    return base_price * (1 + tax_rate) - discount
```

#### Go Documentation

```go
// CalculateTotalPrice computes the final price including tax and discounts.
//
// The function applies the following calculation:
//   total = (basePrice * (1 + taxRate)) - discount
//
// Parameters:
//   - basePrice: The price before tax (must be >= 0)
//   - taxRate: The tax rate as a decimal (e.g., 0.1 for 10%)
//   - discount: The discount amount to subtract
//
// Returns the calculated total and an error if inputs are invalid.
func CalculateTotalPrice(basePrice, taxRate, discount float64) (float64, error) {
    if basePrice < 0 {
        return 0, ErrNegativeBasePrice
    }
    if taxRate < 0 {
        return 0, ErrNegativeTaxRate
    }
    return basePrice*(1+taxRate) - discount, nil
}
```

### Error Handling

#### Principles

1. Never swallow errors silently
2. Always log errors with sufficient context
3. Use custom error types for domain-specific errors
4. Fail fast on unrecoverable errors
5. Provide actionable error messages

#### Error Hierarchy

```
BaseError
├── ValidationError (user input problems)
│   ├── RequiredFieldError
│   ├── InvalidFormatError
│   └── OutOfRangeError
├── BusinessError (domain rule violations)
│   ├── InsufficientFundsError
│   ├── DuplicateEntityError
│   └── StateTransitionError
├── IntegrationError (external system failures)
│   ├── NetworkError
│   ├── TimeoutError
│   └── ServiceUnavailableError
└── SystemError (infrastructure failures)
    ├── DatabaseError
    ├── CacheError
    └── ConfigurationError
```

#### JavaScript/TypeScript Error Classes

```typescript
class BaseError extends Error {
    public readonly code: string;
    public readonly timestamp: Date;
    public readonly context: Record<string, unknown>;

    constructor(
        message: string,
        code: string,
        context: Record<string, unknown> = {}
    ) {
        super(message);
        this.name = this.constructor.name;
        this.code = code;
        this.timestamp = new Date();
        this.context = context;
        Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends BaseError {
    public readonly field: string;

    constructor(message: string, field: string) {
        super(message, 'VALIDATION_ERROR', { field });
        this.field = field;
    }
}

class IntegrationError extends BaseError {
    public readonly service: string;
    public readonly retryable: boolean;

    constructor(
        message: string,
        service: string,
        retryable: boolean = false
    ) {
        super(message, 'INTEGRATION_ERROR', { service, retryable });
        this.service = service;
        this.retryable = retryable;
    }
}
```

#### Error Response Format

All API errors must follow this format:

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Email address is invalid",
        "details": {
            "field": "email",
            "value": "not-an-email",
            "constraint": "email_format"
        },
        "requestId": "req_abc123",
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

## Testing Requirements

### Coverage Thresholds

| Metric | Minimum | Target |
|--------|---------|--------|
| Line coverage | 80% | 90% |
| Branch coverage | 75% | 85% |
| Function coverage | 85% | 95% |

### Test Naming

Use descriptive test names following the pattern: "should [behavior] when [condition]"

```typescript
describe('UserService', () => {
    describe('createUser', () => {
        it('should create user with valid data when all required fields provided', async () => {
            // test implementation
        });

        it('should throw ValidationError when email is invalid', async () => {
            // test implementation
        });

        it('should throw DuplicateEntityError when email already exists', async () => {
            // test implementation
        });

        it('should hash password before storing when password provided', async () => {
            // test implementation
        });
    });
});
```

### Test Structure (AAA Pattern)

```typescript
it('should calculate total with tax correctly', () => {
    // Arrange - Set up test data and dependencies
    const basePrice = 100;
    const taxRate = 0.1;
    const calculator = new PriceCalculator();

    // Act - Execute the code under test
    const result = calculator.calculateTotal(basePrice, taxRate);

    // Assert - Verify the results
    expect(result).toBe(110);
});
```

### Test Categories

| Category | Purpose | Execution |
|----------|---------|-----------|
| Unit | Test individual functions/classes in isolation | Every commit |
| Integration | Test component interactions | Every PR |
| E2E | Test complete user flows | Nightly |
| Performance | Verify response times and throughput | Weekly |
| Security | SAST/DAST scanning | Every PR |

### Mocking Guidelines

1. Mock external dependencies only (databases, APIs, file systems)
2. Never mock the code under test
3. Use realistic mock data
4. Prefer dependency injection for testability
5. Reset mocks between tests

```typescript
// Good - mocking external service
jest.mock('../services/EmailService');
const mockSendEmail = EmailService.send as jest.Mock;
mockSendEmail.mockResolvedValue({ messageId: 'msg_123' });

// Bad - mocking internal logic
jest.mock('../utils/validateEmail'); // Don't do this
```

## Architecture Patterns

### Layered Architecture

```
┌─────────────────────────────────────┐
│           Presentation              │  Controllers, Views, DTOs
├─────────────────────────────────────┤
│            Application              │  Use Cases, Services
├─────────────────────────────────────┤
│              Domain                 │  Entities, Value Objects, Domain Services
├─────────────────────────────────────┤
│          Infrastructure             │  Repositories, External Services
└─────────────────────────────────────┘
```

### Dependency Rules

1. Dependencies point inward (toward domain)
2. Domain layer has no external dependencies
3. Infrastructure implements domain interfaces
4. Application orchestrates domain logic

### File Structure

```
src/
├── domain/
│   ├── entities/
│   ├── value-objects/
│   ├── services/
│   └── interfaces/
├── application/
│   ├── use-cases/
│   ├── services/
│   └── dtos/
├── infrastructure/
│   ├── persistence/
│   ├── external-services/
│   └── config/
└── presentation/
    ├── controllers/
    ├── middleware/
    └── validators/
```

## API Design Standards

### RESTful Endpoints

| HTTP Method | Usage | Idempotent |
|-------------|-------|------------|
| GET | Retrieve resource(s) | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Remove resource | Yes |

### URL Naming

- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural forms: `/users` not `/user`
- Use kebab-case: `/user-profiles` not `/userProfiles`
- Nest for relationships: `/users/{id}/orders`
- Use query params for filtering: `/users?role=admin&active=true`

### Response Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST creating resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Semantic validation failure |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected errors |
| 503 | Service Unavailable | Maintenance/overload |

### Pagination

All list endpoints must support pagination:

```json
{
    "data": [...],
    "pagination": {
        "page": 1,
        "pageSize": 20,
        "totalPages": 5,
        "totalItems": 98,
        "hasNext": true,
        "hasPrevious": false
    },
    "links": {
        "self": "/users?page=1&pageSize=20",
        "next": "/users?page=2&pageSize=20",
        "last": "/users?page=5&pageSize=20"
    }
}
```

### Versioning

Use URL path versioning: `/api/v1/users`

| Version | Status | Sunset Date |
|---------|--------|-------------|
| v1 | Deprecated | 2024-06-01 |
| v2 | Current | - |
| v3 | Beta | - |

## Git Workflow

### Commit Messages

Use conventional commits format:

```
type(scope): description

Body explaining why (optional)

Fixes #123
BREAKING CHANGE: description of breaking change (if applicable)
```

#### Commit Types

| Type | Purpose | Version Bump |
|------|---------|--------------|
| feat | New feature | Minor |
| fix | Bug fix | Patch |
| docs | Documentation only | None |
| style | Formatting, semicolons | None |
| refactor | Code restructuring | None |
| perf | Performance improvement | Patch |
| test | Adding tests | None |
| chore | Maintenance | None |
| ci | CI/CD changes | None |
| build | Build system changes | None |

### Branch Naming

| Branch Type | Pattern | Example |
|-------------|---------|---------|
| Feature | `feature/PROJ-{id}-{description}` | `feature/PROJ-123-user-auth` |
| Bug Fix | `fix/PROJ-{id}-{description}` | `fix/PROJ-456-login-error` |
| Hotfix | `hotfix/PROJ-{id}-{description}` | `hotfix/PROJ-789-security-patch` |
| Release | `release/v{major}.{minor}.{patch}` | `release/v1.2.0` |
| Experiment | `experiment/{description}` | `experiment/new-caching-strategy` |

### Branch Protection

| Branch | Rules |
|--------|-------|
| main | Require PR, 2 approvals, CI pass, no force push |
| develop | Require PR, 1 approval, CI pass |
| release/* | Require PR, 2 approvals, CI pass, CODEOWNERS |

### Pull Request Guidelines

1. Keep PRs small (< 400 lines changed)
2. Include description with context
3. Link related issues
4. Add screenshots for UI changes
5. Update documentation if needed
6. Add tests for new functionality
7. Request review from relevant code owners

## Security Guidelines

### Authentication & Authorization

1. Use industry-standard protocols (OAuth 2.0, OpenID Connect)
2. Implement proper session management
3. Use secure token storage (httpOnly cookies, secure storage)
4. Implement rate limiting on auth endpoints
5. Log all authentication events

### Input Validation

| Input Type | Validation |
|------------|------------|
| Email | RFC 5322 format, domain verification |
| Phone | E.164 format |
| URL | Protocol whitelist (https), domain validation |
| Numbers | Type, range, precision |
| Strings | Length limits, character whitelist |
| Files | Type, size, content validation |

### Data Protection

1. Encrypt sensitive data at rest (AES-256)
2. Use TLS 1.3 for data in transit
3. Hash passwords with bcrypt (cost factor ≥ 12)
4. Implement field-level encryption for PII
5. Use parameterized queries for all database operations
6. Sanitize output to prevent XSS

### Secrets Management

| DO | DON'T |
|----|-------|
| Use environment variables | Commit secrets to git |
| Use secrets manager (Vault, AWS Secrets) | Log sensitive data |
| Rotate credentials regularly | Share credentials via chat |
| Audit secret access | Use same secret across environments |

### Security Headers

Required headers for all HTTP responses:

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
```

## Database Standards

### Query Optimization

1. Always use indexes for filtered/sorted columns
2. Avoid SELECT * - specify needed columns
3. Use EXPLAIN to analyze query plans
4. Limit result sets with pagination
5. Use connection pooling

### Migrations

1. Migrations must be reversible (up/down)
2. Never modify existing migrations
3. Use descriptive migration names: `20240115_add_user_preferences_table`
4. Test migrations on production-like data
5. Backup before running migrations

### Naming Conventions

| Object | Convention | Example |
|--------|------------|---------|
| Tables | snake_case, plural | `user_profiles` |
| Columns | snake_case | `created_at` |
| Primary Keys | `id` | `id` |
| Foreign Keys | `{table}_id` | `user_id` |
| Indexes | `idx_{table}_{columns}` | `idx_users_email` |
| Constraints | `{type}_{table}_{columns}` | `uq_users_email` |

## Logging & Monitoring

### Log Levels

| Level | Usage |
|-------|-------|
| ERROR | Exceptions, failures requiring attention |
| WARN | Unexpected but handled situations |
| INFO | Significant business events |
| DEBUG | Detailed diagnostic information |
| TRACE | Very detailed debugging (development only) |

### Structured Logging Format

```json
{
    "timestamp": "2024-01-15T10:30:00.000Z",
    "level": "INFO",
    "service": "user-service",
    "traceId": "abc123",
    "spanId": "def456",
    "message": "User created successfully",
    "context": {
        "userId": "usr_123",
        "action": "CREATE_USER",
        "duration": 150
    }
}
```

### Metrics to Track

| Category | Metrics |
|----------|---------|
| Application | Request rate, error rate, latency (p50, p95, p99) |
| Business | Signups, conversions, transactions |
| Infrastructure | CPU, memory, disk, network |
| Dependencies | External API latency, failure rate |

### Alerting Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | > 1% | > 5% |
| P99 latency | > 500ms | > 2000ms |
| CPU usage | > 70% | > 90% |
| Memory usage | > 75% | > 90% |
| Disk usage | > 80% | > 95% |

## Performance Guidelines

### Response Time Targets

| Endpoint Type | P50 | P95 | P99 |
|---------------|-----|-----|-----|
| API reads | 50ms | 150ms | 300ms |
| API writes | 100ms | 300ms | 500ms |
| Background jobs | 1s | 5s | 30s |
| Batch operations | 30s | 60s | 120s |

### Caching Strategy

| Cache Layer | Use Case | TTL |
|-------------|----------|-----|
| Browser | Static assets | 1 year |
| CDN | Public API responses | 5 min |
| Application | Session data, computed results | 15 min |
| Database | Query results | 1 hour |

### Optimization Checklist

1. Enable compression (gzip, brotli)
2. Use connection keep-alive
3. Implement request/response caching
4. Lazy load non-critical resources
5. Use async operations for I/O
6. Batch database operations
7. Optimize images and assets
8. Use pagination for large datasets

## Code Review Guidelines

### Review Checklist

1. **Correctness**: Does the code do what it's supposed to?
2. **Security**: Are there any security vulnerabilities?
3. **Performance**: Are there any performance issues?
4. **Readability**: Is the code easy to understand?
5. **Maintainability**: Will this be easy to modify later?
6. **Tests**: Are tests adequate and passing?
7. **Documentation**: Is the code properly documented?

### Feedback Guidelines

| DO | DON'T |
|----|-------|
| Be specific and actionable | Be vague or dismissive |
| Explain the "why" | Just say "change this" |
| Suggest alternatives | Only criticize |
| Ask questions to understand | Assume bad intent |
| Acknowledge good work | Focus only on negatives |

### Review Response Times

| Priority | Initial Response | Resolution |
|----------|------------------|------------|
| Critical (P0) | 1 hour | 4 hours |
| High (P1) | 4 hours | 1 day |
| Normal (P2) | 1 day | 3 days |
| Low (P3) | 3 days | 1 week |

## Feature Flags

### Implementation

```typescript
interface FeatureFlag {
    name: string;
    enabled: boolean;
    rolloutPercentage: number;
    allowedUsers: string[];
    allowedGroups: string[];
    metadata: Record<string, unknown>;
}

function isFeatureEnabled(
    flagName: string,
    userId?: string,
    context?: Record<string, unknown>
): boolean {
    const flag = getFeatureFlag(flagName);
    if (!flag) return false;
    if (!flag.enabled) return false;
    if (flag.allowedUsers.includes(userId)) return true;
    if (flag.rolloutPercentage === 100) return true;
    return hashUser(userId) % 100 < flag.rolloutPercentage;
}
```

### Lifecycle

| State | Description | Action |
|-------|-------------|--------|
| Created | Flag defined, not enabled | Development |
| Testing | Enabled for internal users | QA validation |
| Rollout | Gradual percentage increase | Monitor metrics |
| Enabled | 100% rollout | Monitor for issues |
| Cleanup | Remove flag, hardcode behavior | Code cleanup |

## Accessibility Standards

### WCAG 2.1 AA Compliance

1. **Perceivable**: Content is presentable in different ways
   - Alt text for images
   - Captions for video
   - Sufficient color contrast (4.5:1 for text)

2. **Operable**: UI components are navigable
   - Keyboard accessible
   - No seizure-inducing content
   - Sufficient time to interact

3. **Understandable**: Content is readable and predictable
   - Clear language
   - Consistent navigation
   - Input assistance

4. **Robust**: Content works with assistive technologies
   - Valid HTML
   - ARIA labels where needed
   - Compatible with screen readers

### Accessibility Checklist

| Check | Requirement |
|-------|-------------|
| Color contrast | 4.5:1 for normal text, 3:1 for large text |
| Focus indicators | Visible focus state for all interactive elements |
| Alt text | All meaningful images have descriptive alt text |
| Headings | Logical heading hierarchy (h1 → h2 → h3) |
| Forms | Labels associated with inputs, error messages clear |
| Keyboard | All functionality accessible via keyboard |
| ARIA | Proper ARIA roles and labels |

## Release Management

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking API changes
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

### Release Checklist

1. All tests passing
2. CHANGELOG updated
3. Version bumped
4. Documentation updated
5. Security scan passed
6. Performance benchmarks met
7. Rollback plan documented
8. Stakeholders notified

### Deployment Strategy

| Strategy | Use Case | Risk |
|----------|----------|------|
| Blue-Green | Zero downtime required | Medium |
| Canary | High-risk changes | Low |
| Rolling | Standard updates | Medium |
| Recreate | Development only | High |

## Summary

Following these comprehensive standards ensures:

1. **Consistency**: Uniform code style and patterns across the team
2. **Quality**: High-quality, well-tested, and documented code
3. **Security**: Protected systems and data
4. **Performance**: Fast and efficient applications
5. **Maintainability**: Code that's easy to understand and modify
6. **Accessibility**: Inclusive applications for all users
7. **Reliability**: Stable and predictable systems

All team members are expected to follow these guidelines. Deviations require team discussion and documented exceptions.
