---
description: Team coding standards and best practices
alwaysApply: false
crux: true
---

# Team Coding Standards and Best Practices

This document outlines our team's coding standards, conventions, and best practices that have been developed over time. All team members should follow these guidelines to maintain consistency across our codebase.

## General Principles

### Code Quality Philosophy

We believe that code should be written for humans first and computers second. This means that readability and maintainability are our top priorities. When in doubt, always choose the more readable option over the clever one.

Every piece of code you write will be read many more times than it was written. Keep this in mind when making decisions about naming, structure, and documentation.

### The Boy Scout Rule

Always leave the code better than you found it. If you touch a file to make a change, take a moment to clean up any minor issues you notice - fix typos, improve variable names, add missing documentation, or refactor confusing logic.

However, be careful not to scope-creep your changes. If you find something that requires significant refactoring, create a separate ticket for it rather than bundling it with your current work.

## Naming Conventions

### Variables and Functions

Variable names should be descriptive and self-documenting. Avoid single-letter variables except in very short loops or well-understood mathematical contexts.

- Use camelCase for variables and functions in JavaScript and TypeScript
- Use snake_case for variables and functions in Python
- Use PascalCase for class names in all languages
- Use SCREAMING_SNAKE_CASE for constants

Bad examples:
- `x` - What does this represent?
- `data` - Too generic, what kind of data?
- `temp` - Temporary what?
- `handleClick` - Handle click of what?

Good examples:
- `userEmailAddress` - Clear and specific
- `orderLineItems` - Describes the contents
- `calculateMonthlyRevenue` - Describes the action and scope
- `handleSubmitButtonClick` - Specific to the element

### Boolean Variables

Boolean variables should be named as questions that can be answered with yes or no. They should typically start with `is`, `has`, `can`, `should`, or similar prefixes.

Good examples:
- `isUserLoggedIn`
- `hasPermission`
- `canEditDocument`
- `shouldRefreshCache`

Bad examples:
- `loggedIn` - Is this a boolean or a timestamp?
- `permission` - The permission itself or whether they have it?
- `refresh` - A command or a state?

### File and Directory Names

Use kebab-case for file names in JavaScript and TypeScript projects. Use snake_case for Python files. Directory names should be lowercase with hyphens.

Each file should have a single responsibility. If a file contains multiple unrelated concerns, split it into separate files.

## Code Structure

### Function Length

Functions should generally be no longer than 20-30 lines. If a function is longer than this, it's usually doing too much and should be broken down into smaller, more focused functions.

Each function should do one thing and do it well. If you find yourself writing comments to separate different sections of a function, that's a sign it should be split.

### Nesting Depth

Avoid deeply nested code. If you find yourself with more than 3 levels of nesting, consider using early returns, extracting functions, or restructuring the logic.

Bad example with deep nesting:
```javascript
function processOrder(order) {
  if (order) {
    if (order.items) {
      if (order.items.length > 0) {
        if (order.customer) {
          if (order.customer.isActive) {
            // Finally do something
          }
        }
      }
    }
  }
}
```

Good example with early returns:
```javascript
function processOrder(order) {
  if (!order) return;
  if (!order.items?.length) return;
  if (!order.customer?.isActive) return;
  
  // Do the actual work
}
```

### Comments

Write code that is self-documenting. Comments should explain "why" not "what". The code itself should make the "what" obvious.

Bad comments:
```javascript
// Increment i by 1
i++;

// Loop through the array
for (const item of items) {
```

Good comments:
```javascript
// We need to retry 3 times because the external API has intermittent failures
const MAX_RETRIES = 3;

// Using a Set here instead of Array for O(1) lookup performance
const processedIds = new Set();
```

### Documentation

All public APIs, classes, and functions should have documentation comments (JSDoc for JavaScript/TypeScript, docstrings for Python). Include:

- A brief description of what the function does
- Parameter descriptions with types
- Return value description
- Examples for complex functions
- Any exceptions that might be thrown

```javascript
/**
 * Calculates the total price of an order including tax and discounts.
 * 
 * @param {Order} order - The order to calculate the price for
 * @param {number} taxRate - The tax rate as a decimal (e.g., 0.08 for 8%)
 * @param {Discount[]} discounts - Array of applicable discounts
 * @returns {number} The total price in cents
 * @throws {InvalidOrderError} If the order has no line items
 * 
 * @example
 * const total = calculateOrderTotal(order, 0.08, [tenPercentOff]);
 */
function calculateOrderTotal(order, taxRate, discounts) {
  // ...
}
```

## Error Handling

### Never Swallow Errors

Never catch an error and do nothing with it. At minimum, log the error. Better yet, handle it appropriately or re-throw it.

Bad:
```javascript
try {
  doSomething();
} catch (e) {
  // Silently ignored - this is terrible!
}
```

Good:
```javascript
try {
  doSomething();
} catch (error) {
  logger.error('Failed to do something', { error, context: relevantData });
  throw new ApplicationError('Operation failed', { cause: error });
}
```

### Use Custom Error Types

Create custom error types for different categories of errors in your application. This makes error handling more precise and debugging easier.

```javascript
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

class NotFoundError extends Error {
  constructor(resourceType, resourceId) {
    super(`${resourceType} with id ${resourceId} not found`);
    this.name = 'NotFoundError';
    this.resourceType = resourceType;
    this.resourceId = resourceId;
  }
}
```

### Error Messages

Error messages should be helpful to developers debugging issues. Include:

- What operation failed
- What the expected state was
- What the actual state was
- Any relevant IDs or context

Bad: "Error occurred"
Good: "Failed to update user profile: user 12345 not found in database"

## Testing

### Test Coverage Requirements

All new code should have tests. We aim for a minimum of 80% code coverage, but coverage alone is not sufficient - tests must be meaningful.

### Test Naming

Test names should describe the scenario being tested and the expected outcome. Use the format: "should [expected behavior] when [condition]"

```javascript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a new user when valid data is provided', () => {});
    it('should throw ValidationError when email is invalid', () => {});
    it('should throw DuplicateError when email already exists', () => {});
  });
});
```

### Test Structure

Follow the Arrange-Act-Assert (AAA) pattern in your tests:

```javascript
it('should calculate correct total with discount', () => {
  // Arrange
  const order = createTestOrder({ subtotal: 100 });
  const discount = createDiscount({ percentage: 10 });
  
  // Act
  const result = calculateTotal(order, discount);
  
  // Assert
  expect(result).toBe(90);
});
```

### Mocking Guidelines

Mock external dependencies, not internal implementation details. Tests should verify behavior, not implementation.

Don't mock:
- The unit you're testing
- Simple utility functions
- Data structures

Do mock:
- External APIs and services
- Database connections
- File system operations
- Time-dependent operations

## Git Workflow

### Commit Messages

Write clear, descriptive commit messages. Use the conventional commits format:

```
type(scope): short description

Longer description if needed. Explain the "why" behind the change,
not just the "what" (the code shows the what).

Fixes #123
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Branch Naming

Use descriptive branch names with the following format:

- `feature/short-description` - For new features
- `fix/short-description` - For bug fixes
- `refactor/short-description` - For refactoring
- `docs/short-description` - For documentation updates

Include the ticket number when applicable: `feature/PROJ-123-user-authentication`

### Pull Requests

Every pull request should:

- Have a clear title that summarizes the change
- Include a description explaining what and why
- Reference any related issues or tickets
- Be as small as possible while still being complete
- Include tests for any new functionality
- Pass all CI checks before requesting review

## Security

### Sensitive Data

Never commit sensitive data to the repository:
- API keys and secrets
- Passwords and credentials
- Private keys and certificates
- Personal identifying information (PII)

Use environment variables for configuration. Use secret management tools for production credentials.

### Input Validation

Always validate and sanitize user input. Never trust data from external sources.

- Validate type, format, and range
- Sanitize strings to prevent injection attacks
- Use parameterized queries for database operations
- Encode output to prevent XSS attacks

### Authentication and Authorization

- Always check authorization before performing operations
- Use established libraries for authentication - don't roll your own
- Implement rate limiting on authentication endpoints
- Use secure session management

## Performance

### Database Queries

- Avoid N+1 queries - use eager loading when appropriate
- Add indexes for frequently queried columns
- Use pagination for large result sets
- Profile slow queries and optimize as needed

### Caching

- Cache expensive computations and external API responses
- Set appropriate TTLs based on data volatility
- Implement cache invalidation strategies
- Use cache warming for critical paths

### Frontend Performance

- Lazy load components and routes
- Optimize images and assets
- Minimize bundle size
- Use code splitting for large applications

## Dependency Management

### Adding Dependencies

Before adding a new dependency, consider:

- Is it actively maintained?
- What is the bundle size impact?
- Are there security vulnerabilities?
- Can we achieve the same result with existing dependencies or minimal custom code?

Document why each major dependency was chosen in the project README.

### Version Pinning

- Pin exact versions in production applications
- Use version ranges only in libraries
- Regularly update dependencies and test thoroughly
- Monitor for security vulnerabilities with automated tools

## Code Review

### As an Author

- Self-review your code before requesting review
- Keep PRs small and focused
- Provide context in the PR description
- Respond to feedback constructively

### As a Reviewer

- Be respectful and constructive in feedback
- Explain the reasoning behind suggestions
- Distinguish between required changes and suggestions
- Approve when the code is good enough, not perfect

## Logging

### What to Log

- Application startup and shutdown
- Authentication events (login, logout, failures)
- Business-critical operations
- Errors and exceptions with context
- Performance metrics for critical paths

### What Not to Log

- Sensitive data (passwords, tokens, PII)
- High-frequency events that would flood logs
- Redundant information

### Log Levels

- ERROR: Something failed and needs attention
- WARN: Something unexpected but recoverable
- INFO: Normal business events
- DEBUG: Detailed information for debugging
- TRACE: Very detailed tracing information

## Conclusion

These standards are living documentation. As our team grows and technology evolves, these guidelines should be updated to reflect our current best practices. If you have suggestions for improvements, bring them up in the team meeting or submit a PR to this document.

Remember: the goal of these standards is to help us write better code together, not to create bureaucracy. Use good judgment, and when in doubt, ask a colleague.
