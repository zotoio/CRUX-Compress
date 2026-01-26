---
crux: true
alwaysApply: true
---

# Sample Coding Standards

This is a sample rule file used for testing CRUX compression. It contains typical content found in a team coding standards document.

## Code Quality Guidelines

### Naming Conventions

1. **Variables and Functions**: Use camelCase for JavaScript/TypeScript, snake_case for Python
2. **Classes**: Use PascalCase for all languages
3. **Constants**: Use SCREAMING_SNAKE_CASE for true constants

### Code Style

- Keep functions small and focused (20-30 lines maximum)
- Use early returns to avoid deep nesting
- Maximum nesting depth of 3 levels
- Write self-documenting code

### Documentation

All public APIs should have documentation:

```javascript
/**
 * Calculates the total price including tax
 * @param {number} basePrice - The price before tax
 * @param {number} taxRate - The tax rate as a decimal
 * @returns {number} The total price with tax
 */
function calculateTotalPrice(basePrice, taxRate) {
    return basePrice * (1 + taxRate);
}
```

### Error Handling

- Never swallow errors silently
- Always log errors with context
- Use custom error types for domain-specific errors

```javascript
class ValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
    }
}
```

## Testing Requirements

- Minimum 80% code coverage
- Use descriptive test names: "should [behavior] when [condition]"
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies only

## Git Workflow

### Commit Messages

Use conventional commits format:

```
type(scope): description

Body explaining why (optional)

Fixes #123
```

Types: feat, fix, docs, style, refactor, test, chore

### Branch Naming

- Features: `feature/short-description`
- Fixes: `fix/short-description`
- With ticket: `feature/PROJ-123-description`

## Security Guidelines

- Never commit secrets or API keys
- Validate all user input
- Use parameterized queries for database operations
- Encode output to prevent XSS

## Summary

Following these standards ensures consistent, maintainable, and secure code across the team.
