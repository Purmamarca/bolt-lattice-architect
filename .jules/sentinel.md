# Sentinel Journal - Bolt-Lattice-Architect

## 2026-02-24 - Initial Security Assessment

Vulnerability: Insecure IP normalization logic in `src/lib/security-policy.ts`.
Learning: Simple regex and `parseInt` without bounds checking or `NaN` validation can lead to ambiguous IP resolutions, potentially bypassing whitelists or causing logic errors in security enforcement.
Fix: Refactored `normalizeIp` to use strict regex validation for each octet (hex, octal, decimal), ensured octets are within 0-255 range, and prevented `NaN` leaks.
Prevention: Always validate input ranges (0-255 for IP octets) and check for `NaN` after parsing numeric strings. Use robust IP parsing libraries if possible, or implement strict validation.
