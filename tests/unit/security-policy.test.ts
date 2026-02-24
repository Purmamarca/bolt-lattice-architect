/**
 * TDD Test Suite: Security Policy Module
 * Tests for: src/lib/security-policy.ts
 *
 * Follows Red → Green → Refactor cycle.
 * All tests were written BEFORE fixes were applied where applicable.
 */

import {
  CFGPolicyEngine,
  DEFAULT_POLICY,
  ViolationType,
  SecurityPolicy,
  normalizeIp,
  isIpApproved,
} from '../../src/lib/security-policy';

// ============================================================================
// normalizeIp — standalone exported function
// ============================================================================

describe('normalizeIp()', () => {
  describe('canonical dotted-decimal input', () => {
    it('returns the IP unchanged when already in dotted-decimal form', () => {
      expect(normalizeIp('10.0.0.5')).toBe('10.0.0.5');
    });

    it('strips surrounding whitespace', () => {
      expect(normalizeIp('  10.0.0.5')).toBe('10.0.0.5');
      expect(normalizeIp('192.168.1.50  ')).toBe('192.168.1.50');
      expect(normalizeIp(' 192.168.1.50 ')).toBe('192.168.1.50');
    });
  });

  describe('decimal (integer) representation', () => {
    it('converts 167772165 → 10.0.0.5', () => {
      expect(normalizeIp('167772165')).toBe('10.0.0.5');
    });

    it('converts 3232235826 → 192.168.1.50', () => {
      expect(normalizeIp('3232235826')).toBe('192.168.1.50');
    });

    it('converts 3232235875 → 192.168.1.99 (rogue)', () => {
      expect(normalizeIp('3232235875')).toBe('192.168.1.99');
    });
  });

  describe('hex representation', () => {
    it('converts 0x0a000005 → 10.0.0.5', () => {
      expect(normalizeIp('0x0a000005')).toBe('10.0.0.5');
    });

    it('converts 0xA000005 → 10.0.0.5', () => {
      expect(normalizeIp('0xA000005')).toBe('10.0.0.5');
    });

    it('converts 0xC0A80132 → 192.168.1.50', () => {
      expect(normalizeIp('0xC0A80132')).toBe('192.168.1.50');
    });

    it('converts 0xC0A80163 → 192.168.1.99 (rogue)', () => {
      expect(normalizeIp('0xC0A80163')).toBe('192.168.1.99');
    });
  });

  describe('octal dotted notation', () => {
    it('converts 012.0.0.05 → 10.0.0.5', () => {
      expect(normalizeIp('012.0.0.05')).toBe('10.0.0.5');
    });

    it('converts 0300.0250.01.062 → 192.168.1.50', () => {
      expect(normalizeIp('0300.0250.01.062')).toBe('192.168.1.50');
    });
  });

  describe('malformed / unrecognized inputs — must not crash', () => {
    it('returns non-IP strings as-is (cannot normalize)', () => {
      expect(normalizeIp('abc.def.ghi.jkl')).toBe('abc.def.ghi.jkl');
    });

    it('handles empty string without throwing', () => {
      expect(() => normalizeIp('')).not.toThrow();
    });

    it('handles IPv6 loopback without throwing', () => {
      expect(() => normalizeIp('::1')).not.toThrow();
    });

    it('returns hostname as-is (no dots matching IPv4 pattern)', () => {
      expect(normalizeIp('localhost')).toBe('localhost');
    });
  });
});

// ============================================================================
// isIpApproved — standalone exported function
// ============================================================================

describe('isIpApproved()', () => {
  describe('directly approved IPs', () => {
    it('approves 10.0.0.5', () => {
      expect(isIpApproved('10.0.0.5')).toBe(true);
    });

    it('approves 192.168.1.50', () => {
      expect(isIpApproved('192.168.1.50')).toBe(true);
    });
  });

  describe('obfuscated approved IPs', () => {
    it('approves decimal representation of 10.0.0.5', () => {
      expect(isIpApproved('167772165')).toBe(true);
    });

    it('approves hex representation of 192.168.1.50', () => {
      expect(isIpApproved('0xC0A80132')).toBe(true);
    });

    it('approves whitespace-padded whitelisted IPs', () => {
      expect(isIpApproved('  10.0.0.5')).toBe(true);
      expect(isIpApproved('192.168.1.50  ')).toBe(true);
    });

    it('approves octal dotted 10.0.0.5', () => {
      expect(isIpApproved('012.0.0.05')).toBe(true);
    });
  });

  describe('unauthorized IPs', () => {
    it('rejects 8.8.8.8 (Google DNS)', () => {
      expect(isIpApproved('8.8.8.8')).toBe(false);
    });

    it('rejects 192.168.1.99 (rogue internal)', () => {
      expect(isIpApproved('192.168.1.99')).toBe(false);
    });

    it('rejects hex representation of rogue IP', () => {
      expect(isIpApproved('0xC0A80163')).toBe(false); // 192.168.1.99
    });

    it('rejects malformed input', () => {
      expect(isIpApproved('')).toBe(false);
      expect(isIpApproved('localhost')).toBe(false);
    });
  });
});

// ============================================================================
// CFGPolicyEngine — class-based engine
// ============================================================================

describe('CFGPolicyEngine', () => {
  let engine: CFGPolicyEngine;

  beforeEach(() => {
    engine = new CFGPolicyEngine();
  });

  describe('validateIP()', () => {
    it('returns valid=true for whitelisted IP', () => {
      const result = engine.validateIP('10.0.0.5');
      expect(result.valid).toBe(true);
      expect(result.violation).toBeUndefined();
    });

    it('returns valid=false with UNAUTHORIZED_IP violation for rogue IP', () => {
      const result = engine.validateIP('8.8.8.8');
      expect(result.valid).toBe(false);
      expect(result.violation).toBeDefined();
      expect(result.violation!.type).toBe(ViolationType.UNAUTHORIZED_IP);
      expect(result.violation!.severity).toBe('CRITICAL');
      expect(result.violation!.canRecover).toBe(false);
    });

    it('normalizes obfuscated IP before checking', () => {
      // decimal for 10.0.0.5 should be approved
      const result = engine.validateIP('167772165');
      expect(result.valid).toBe(true);
    });
  });

  describe('validateEncryption()', () => {
    it('returns valid=true when ML-KEM-768 encryption present', () => {
      const result = engine.validateEncryption(true, 'ML-KEM-768');
      expect(result.valid).toBe(true);
    });

    it('returns valid=false (CRITICAL) when encryption missing and required', () => {
      const result = engine.validateEncryption(false, undefined);
      expect(result.valid).toBe(false);
      expect(result.violation!.type).toBe(ViolationType.MISSING_ENCRYPTION);
      expect(result.violation!.severity).toBe('CRITICAL');
      expect(result.violation!.canRecover).toBe(true);
    });

    it('returns valid=false (WARNING) when non-quantum-safe algorithm is used', () => {
      const result = engine.validateEncryption(true, 'RSA-2048');
      expect(result.valid).toBe(false);
      expect(result.violation!.type).toBe(ViolationType.MISSING_ENCRYPTION);
      expect(result.violation!.severity).toBe('WARNING');
    });

    it('accepts ML-KEM-1024 as a valid quantum-safe algorithm', () => {
      const result = engine.validateEncryption(true, 'ML-KEM-1024');
      expect(result.valid).toBe(true);
    });
  });

  describe('validateComplexity()', () => {
    it('returns valid=true when complexity is within limit', () => {
      const result = engine.validateComplexity(5);
      expect(result.valid).toBe(true);
    });

    it('returns valid=true at the exact limit', () => {
      const result = engine.validateComplexity(10);
      expect(result.valid).toBe(true);
    });

    it('returns valid=false (WARNING) when complexity exceeds limit', () => {
      const result = engine.validateComplexity(11);
      expect(result.valid).toBe(false);
      expect(result.violation!.type).toBe(ViolationType.HIGH_COMPLEXITY);
      expect(result.violation!.severity).toBe('WARNING');
      expect(result.violation!.canRecover).toBe(true);
    });
  });

  describe('violation tracking', () => {
    it('accumulates violations across multiple validations', () => {
      engine.validateIP('bad.ip');
      engine.validateEncryption(false);
      engine.validateComplexity(99);
      expect(engine.getViolations()).toHaveLength(3);
    });

    it('clears violations and iteration count on clearViolations()', () => {
      engine.validateIP('bad.ip');
      engine.clearViolations();
      expect(engine.getViolations()).toHaveLength(0);
      expect(engine.getIterationCount()).toBe(0);
    });
  });

  describe('reflexion loop', () => {
    it('triggers reflexion when policy is TRIGGER_REFLEXION_LOOP and violations exist', () => {
      const customEngine = new CFGPolicyEngine({
        ...DEFAULT_POLICY,
        onViolation: 'TRIGGER_REFLEXION_LOOP',
      });
      customEngine.validateIP('bad.ip');
      expect(customEngine.shouldTriggerReflexion()).toBe(true);
    });

    it('does NOT trigger reflexion with REJECT policy', () => {
      const rejectEngine = new CFGPolicyEngine({
        ...DEFAULT_POLICY,
        onViolation: 'REJECT',
      });
      rejectEngine.validateIP('bad.ip');
      expect(rejectEngine.shouldTriggerReflexion()).toBe(false);
    });

    it('does NOT trigger reflexion when maxIterations is reached', () => {
      const limitedEngine = new CFGPolicyEngine({
        ...DEFAULT_POLICY,
        maxIterations: 1,
      });
      limitedEngine.validateIP('bad.ip');
      limitedEngine.incrementIteration();
      expect(limitedEngine.shouldTriggerReflexion()).toBe(false);
    });
  });

  describe('updatePolicy()', () => {
    it('updates partial policy fields without losing others', () => {
      engine.updatePolicy({ maxComplexity: 3 });
      const policy = engine.getPolicy();
      expect(policy.maxComplexity).toBe(3);
      expect(policy.requireMLKEM).toBe(true); // unchanged
    });
  });
});
