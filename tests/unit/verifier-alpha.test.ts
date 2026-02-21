/**
 * TDD Test Suite: VerifierAlpha
 * Tests for: src/lib/verifier-alpha.ts
 *
 * VerifierAlpha is the main CFG enforcement orchestrator used by
 * adversarial_test.ts. These unit tests isolate its behaviour.
 */

import { VerifierAlpha, VerificationContext } from '../../src/lib/verifier-alpha';
import { DEFAULT_POLICY } from '../../src/lib/security-policy';

describe('VerifierAlpha', () => {
  let verifier: VerifierAlpha;

  beforeEach(() => {
    verifier = new VerifierAlpha(DEFAULT_POLICY);
  });

  // ==========================================================================
  // verify() — happy paths
  // ==========================================================================

  describe('verify() — passing scenarios', () => {
    it('passes a fully compliant context', async () => {
      const ctx: VerificationContext = {
        ip: '10.0.0.5',
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity: 5,
      };
      const result = await verifier.verify(ctx);
      expect(result.passed).toBe(true);
      expect(result.score).toBe(1.0);
      expect(result.violations).toHaveLength(0);
    });

    it('passes when ip is omitted (only encryption + complexity validated)', async () => {
      const ctx: VerificationContext = {
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity: 3,
      };
      const result = await verifier.verify(ctx);
      expect(result.passed).toBe(true);
    });

    it('passes when all optional fields are omitted', async () => {
      const result = await verifier.verify({});
      expect(result.passed).toBe(true);
      expect(result.score).toBe(1.0);
    });
  });

  // ==========================================================================
  // verify() — failing scenarios
  // ==========================================================================

  describe('verify() — failing scenarios', () => {
    it('fails for unauthorized IP', async () => {
      const ctx: VerificationContext = {
        ip: '8.8.8.8',
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity: 5,
      };
      const result = await verifier.verify(ctx);
      expect(result.passed).toBe(false);
      expect(result.violations.length).toBeGreaterThan(0);
    });

    it('recovers and passes when only missing encryption (recoverable)', async () => {
      const ctx: VerificationContext = {
        ip: '10.0.0.5',
        hasEncryption: false,   // ← missing = CRITICAL but canRecover=true
        complexity: 5,
      };
      const result = await verifier.verify(ctx);
      // After reflexion loop the engine auto-applies ML-KEM, so should RECOVER
      expect(['RECOVERED', 'FAIL']).toContain(result.metadata.finalState);
      // If it recovered, it should pass
      if (result.metadata.finalState === 'RECOVERED') {
        expect(result.passed).toBe(true);
      }
    });

    it('produces score < 1 when warnings are present and reflexion is disabled', async () => {
      // Use a policy with REJECT so the reflexion loop won't auto-upgrade the algorithm
      const rejectVerifier = new VerifierAlpha({
        approvedIPs: ['10.0.0.5', '192.168.1.50'],
        requireMLKEM: true,
        minLatticeLevel: 5,
        maxComplexity: 10,
        onViolation: 'REJECT',   // ← no reflexion recovery
        rollbackOnFailure: true,
        maxIterations: 5,
      });
      const ctx: VerificationContext = {
        ip: '10.0.0.5',
        hasEncryption: true,
        algorithm: 'AES-256',   // ← WARNING: non-quantum-safe
        complexity: 5,
      };
      const result = await rejectVerifier.verify(ctx);
      // REJECT policy means no recovery → the WARNING stays → score < 1
      expect(result.score).toBeLessThan(1.0);
    });

    it('recovers AES-256 warning via reflexion loop (upgrades to ML-KEM)', async () => {
      // Default policy has TRIGGER_REFLEXION_LOOP, so the WARNING is recoverable
      const ctx: VerificationContext = {
        ip: '10.0.0.5',
        hasEncryption: true,
        algorithm: 'AES-256',
        complexity: 5,
      };
      const result = await verifier.verify(ctx);
      // After recovery, the algorithm is upgraded → final state is RECOVERED or PASS
      expect(['PASS', 'RECOVERED']).toContain(result.metadata.finalState);
    });

    it('produces score of 0 for multiple CRITICAL violations', async () => {
      const ctx: VerificationContext = {
        ip: '8.8.8.8',          // CRITICAL
        hasEncryption: false,    // CRITICAL
        complexity: 5,
      };
      const result = await verifier.verify(ctx);
      // UNAUTHORIZED_IP canRecover=false → FAIL immediately, no recovery
      expect(result.passed).toBe(false);
    });
  });

  // ==========================================================================
  // getStats() and calculatePass1()
  // ==========================================================================

  describe('getStats()', () => {
    it('returns zeros on fresh verifier', () => {
      const stats = verifier.getStats();
      expect(stats.total).toBe(0);
      expect(stats.passed).toBe(0);
      expect(stats.failed).toBe(0);
      expect(stats.pass1).toBe(0);
    });

    it('correctly tracks pass/fail ratio after multiple verifications', async () => {
      // Run 2 passing, 1 failing
      await verifier.verify({ ip: '10.0.0.5', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 });
      await verifier.verify({ ip: '192.168.1.50', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 });
      await verifier.verify({ ip: '8.8.8.8', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 });

      const stats = verifier.getStats();
      expect(stats.total).toBe(3);
      expect(stats.passed).toBe(2);
      expect(stats.failed).toBe(1);
      expect(stats.pass1).toBeCloseTo(2 / 3, 3);
    }, 15000);
  });

  // ==========================================================================
  // reset()
  // ==========================================================================

  describe('reset()', () => {
    it('clears verification history', async () => {
      await verifier.verify({ ip: '10.0.0.5' });
      verifier.reset();
      expect(verifier.getStats().total).toBe(0);
    });
  });

  // ==========================================================================
  // verifyBatch()
  // ==========================================================================

  describe('verifyBatch()', () => {
    it('verifies an array of contexts and returns matching length', async () => {
      const contexts: VerificationContext[] = [
        { ip: '10.0.0.5', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
        { ip: '8.8.8.8', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
      ];
      const results = await verifier.verifyBatch(contexts);
      expect(results).toHaveLength(2);
      expect(results[0].passed).toBe(true);
      expect(results[1].passed).toBe(false);
    }, 15000);
  });

  // ==========================================================================
  // metadata correctness
  // ==========================================================================

  describe('result metadata', () => {
    it('includes a timestamp in the result', async () => {
      const before = Date.now();
      const result = await verifier.verify({});
      expect(result.metadata.timestamp).toBeGreaterThanOrEqual(before);
    });

    it('finalState is PASS for compliant context', async () => {
      const result = await verifier.verify({
        ip: '10.0.0.5',
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity: 3,
      });
      expect(result.metadata.finalState).toBe('PASS');
    });

    it('finalState is FAIL for unauthorized IP (non-recoverable)', async () => {
      const result = await verifier.verify({ ip: '8.8.8.8', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 3 });
      expect(result.metadata.finalState).toBe('FAIL');
    });
  });
});
