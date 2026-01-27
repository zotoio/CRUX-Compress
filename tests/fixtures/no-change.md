---
crux: true
alwaysApply: true
---

# Testing Standards

This document defines the testing standards for our engineering team. All team members must follow these guidelines to ensure reliable, maintainable test suites.

## Test Coverage Requirements

### Coverage Thresholds

| Metric | Minimum | Target |
|--------|---------|--------|
| Line coverage | 80% | 90% |
| Branch coverage | 75% | 85% |
| Function coverage | 85% | 95% |

### Critical Path Coverage

All critical business logic paths must have 100% coverage:
- Payment processing
- Authentication flows
- Data validation
- Error handling

## Test Naming Conventions

Use descriptive test names following the pattern: "should [behavior] when [condition]"

```typescript
describe('PaymentService', () => {
    describe('processPayment', () => {
        it('should succeed when valid card details provided', async () => {
            // test implementation
        });

        it('should throw InsufficientFundsError when balance too low', async () => {
            // test implementation
        });

        it('should retry on network timeout up to 3 times', async () => {
            // test implementation
        });
    });
});
```

## Test Structure

### AAA Pattern

All tests must follow the Arrange-Act-Assert pattern:

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

### Test Independence

Each test must:
- Run in isolation without depending on other tests
- Clean up any state it creates
- Not rely on test execution order
- Use fresh fixtures for each test

## Test Categories

| Category | Purpose | When to Run |
|----------|---------|-------------|
| Unit | Test individual functions in isolation | Every commit |
| Integration | Test component interactions | Every PR |
| E2E | Test complete user flows | Nightly |
| Performance | Verify response times | Weekly |
| Security | SAST/DAST scanning | Every PR |

## Mocking Guidelines

### What to Mock

1. External services (APIs, databases, file systems)
2. Time-dependent operations
3. Random number generators
4. Network requests

### What NOT to Mock

1. The code under test
2. Simple utility functions
3. Value objects
4. Pure functions without side effects

### Mock Best Practices

```typescript
// Good - mocking external service
jest.mock('../services/PaymentGateway');
const mockCharge = PaymentGateway.charge as jest.Mock;
mockCharge.mockResolvedValue({ transactionId: 'txn_123' });

// Bad - mocking internal logic
jest.mock('../utils/calculateTax'); // Don't do this
```

## Test Data Management

### Fixtures

- Store reusable test data in `tests/fixtures/` directory
- Use factories for generating test objects
- Never use production data in tests
- Anonymize any real data used as templates

### Database State

- Use transactions that rollback after each test
- Seed minimal required data per test
- Avoid shared database state between tests

## Assertion Guidelines

### Be Specific

```typescript
// Good - specific assertion
expect(user.email).toBe('test@example.com');
expect(user.role).toBe('admin');

// Bad - vague assertion
expect(user).toBeTruthy();
```

### Test One Thing

Each test should verify one specific behavior. If you need multiple assertions, they should all relate to the same behavior.

### Error Assertions

Always verify error types and messages:

```typescript
await expect(service.process(invalidData))
    .rejects
    .toThrow(new ValidationError('Email is required'));
```

## Continuous Integration

### Required Checks

All PRs must pass:
- Unit tests (100% pass rate)
- Integration tests (100% pass rate)
- Coverage thresholds met
- No flaky test failures

### Flaky Test Policy

- Flaky tests must be fixed within 48 hours
- If not fixable, quarantine and create tracking issue
- Never skip flaky tests without documentation

## Summary

Following these testing standards ensures:
- Reliable test suites that catch real bugs
- Maintainable tests that are easy to update
- Fast feedback loops for developers
- Confidence in code changes
