/** RFC 5321 / common practice limits */
const MAX_EMAIL_LENGTH = 254;
const MAX_LOCAL_LENGTH = 64;

/**
 * Returns true if `value` looks like a syntactically plausible email address.
 * This checks shape only (single `@`, non-empty local and domain, domain has a dot);
 * it does not verify deliverability or DNS.
 */
export function isValidEmail(value: string): boolean {
  const email = value.trim();
  if (email.length === 0 || email.length > MAX_EMAIL_LENGTH) {
    return false;
  }

  const at = email.indexOf("@");
  if (at <= 0 || email.indexOf("@", at + 1) !== -1) {
    return false;
  }

  const local = email.slice(0, at);
  const domain = email.slice(at + 1);
  if (local.length > MAX_LOCAL_LENGTH || domain.length === 0) {
    return false;
  }
  if (
    domain.startsWith(".") ||
    domain.endsWith(".") ||
    domain.includes("..") ||
    !domain.includes(".")
  ) {
    return false;
  }

  for (const ch of email) {
    if (ch <= " " || ch === "\x7f") {
      return false;
    }
  }

  return true;
}
