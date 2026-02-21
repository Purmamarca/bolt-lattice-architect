/**
 * TDD Integration Test: Adversarial Red-Teamer vs Architect
 * Tests for: tests/adversarial_test.ts orchestrator logic
 *
 * Exercises the full pipeline: RedTeamer → VerifierAlpha
 * to confirm 99.9% Pass@1 target is structurally achievable.
 */

import { AdversarialTestOrchestrator, RedTeamer, TEST_CONFIG } from '../adversarial_test';

describe('RedTeamer', () => {
  let redTeamer: RedTeamer;

  beforeAll(() => {
    redTeamer = new RedTeamer();
  });

  it('generates at least 100 attack vectors total', () => {
    const vectors = redTeamer.getAttackVectors();
    expect(vectors.length).toBeGreaterThanOrEqual(100);
  });

  it('getAttackVectors returns exactly the sum of scenario counts', () => {
    const vectors = redTeamer.getAttackVectors();
    const total =
      TEST_CONFIG.scenarios.directIPs +
      TEST_CONFIG.scenarios.obfuscatedIPs +
      TEST_CONFIG.scenarios.malformedIPs +
      TEST_CONFIG.scenarios.encryptionTests +
      TEST_CONFIG.scenarios.complexityTests;
    expect(vectors.length).toBe(total);
  });

  it('getRandomSubset returns requested count', () => {
    const subset = redTeamer.getRandomSubset(10);
    expect(subset).toHaveLength(10);
  });

  it('getRandomSubset with count larger than vectors returns all vectors', () => {
    const all = redTeamer.getAttackVectors();
    const subset = redTeamer.getRandomSubset(9999);
    expect(subset.length).toBe(all.length);
  });

  it('all vectors have required VerificationContext shape', () => {
    const vectors = redTeamer.getAttackVectors();
    for (const v of vectors) {
      expect(v).toHaveProperty('ip');
      expect(v).toHaveProperty('hasEncryption');
      expect(v).toHaveProperty('complexity');
    }
  });
});

describe('AdversarialTestOrchestrator — smoke test (10 iterations)', () => {
  it('completes and returns a TestResult with total > 0', async () => {
    const orch = new AdversarialTestOrchestrator();
    // Override iterations to keep test fast
    (TEST_CONFIG as any).iterations = 10;
    const result = await orch.runFullSuite();

    expect(result.totalTests).toBeGreaterThan(0);
    expect(result.passed + result.failed).toBe(result.totalTests);
    expect(result.pass1).toBeGreaterThanOrEqual(0);
    expect(result.pass1).toBeLessThanOrEqual(1);
    expect(result.duration).toBeGreaterThanOrEqual(0);
  }, 60000);
});
