/**
 * Adversarial Testing Framework
 * Red-Teamer vs Architect Simulation
 * Target: 99.9% Pass@1 Reliability
 * Version: 2026.Q1
 */

import { VerifierAlpha, VerificationContext } from '../src/lib/verifier-alpha';
import { CFGPolicyEngine, DEFAULT_POLICY } from '../src/lib/security-policy';

// ============================================================================
// TEST CONFIGURATION
// ============================================================================

const TEST_CONFIG = {
  iterations: 100,  // Reduced from 1000 for faster testing
  concurrency: 10,
  targetPass1: 0.999,
  scenarios: {
    directIPs: 10,
    obfuscatedIPs: 30,
    malformedIPs: 20,
    encryptionTests: 20,
    complexityTests: 20
  }
};

// ============================================================================
// RED-TEAMER AGENT (Adversarial)
// ============================================================================

class RedTeamer {
  private attackVectors: VerificationContext[] = [];

  constructor() {
    this.generateAttackVectors();
  }

  /**
   * Generate comprehensive attack vectors
   */
  private generateAttackVectors(): void {
    // Direct IP attacks
    this.attackVectors.push(
      ...this.generateDirectIPAttacks(TEST_CONFIG.scenarios.directIPs)
    );

    // Obfuscation attacks
    this.attackVectors.push(
      ...this.generateObfuscationAttacks(TEST_CONFIG.scenarios.obfuscatedIPs)
    );

    // Malformed attacks
    this.attackVectors.push(
      ...this.generateMalformedAttacks(TEST_CONFIG.scenarios.malformedIPs)
    );

    // Encryption bypass attacks
    this.attackVectors.push(
      ...this.generateEncryptionAttacks(TEST_CONFIG.scenarios.encryptionTests)
    );

    // Complexity attacks
    this.attackVectors.push(
      ...this.generateComplexityAttacks(TEST_CONFIG.scenarios.complexityTests)
    );
  }

  /**
   * Direct IP attacks (approved and unapproved)
   */
  private generateDirectIPAttacks(count: number): VerificationContext[] {
    const approvedIPs = ['10.0.0.5', '192.168.1.50'];
    const unapprovedIPs = [
      '10.0.0.6',
      '192.168.1.99',
      '8.8.8.8',
      '1.1.1.1',
      '172.16.0.1'
    ];

    const attacks: VerificationContext[] = [];

    for (let i = 0; i < count; i++) {
      const isApproved = Math.random() < 0.5;
      const ip = isApproved
        ? approvedIPs[Math.floor(Math.random() * approvedIPs.length)]
        : unapprovedIPs[Math.floor(Math.random() * unapprovedIPs.length)];

      attacks.push({
        ip,
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity: 5
      });
    }

    return attacks;
  }

  /**
   * IP obfuscation attacks (decimal, hex, octal, mixed)
   */
  private generateObfuscationAttacks(count: number): VerificationContext[] {
    const attacks: VerificationContext[] = [];

    // 10.0.0.5 obfuscations
    const ip1Obfuscations = [
      '167772165',           // Decimal
      '0x0a000005',          // Hex
      '012.0.0.05',          // Octal
      '10.0.0x0.5',          // Mixed
      '0x0a.0.0.05',         // Mixed hex/octal
      '167772165',           // Full decimal
    ];

    // 192.168.1.50 obfuscations
    const ip2Obfuscations = [
      '3232235826',          // Decimal
      '0xc0a80132',          // Hex
      '0300.0250.01.062',    // Octal
      '192.168.0x1.50',      // Mixed
      '0xc0.0xa8.01.0x32',   // All hex
    ];

    const allObfuscations = [...ip1Obfuscations, ...ip2Obfuscations];

    for (let i = 0; i < count; i++) {
      const ip = allObfuscations[i % allObfuscations.length];
      
      attacks.push({
        ip,
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity: 5
      });
    }

    return attacks;
  }

  /**
   * Malformed IP attacks
   */
  private generateMalformedAttacks(count: number): VerificationContext[] {
    const attacks: VerificationContext[] = [];

    const malformedIPs = [
      '999.999.999.999',     // Overflow
      '-1.-1.-1.-1',         // Negative
      'abc.def.ghi.jkl',     // Letters
      '192.168.1',           // Incomplete
      '192.168.1.1.1',       // Too many octets
      '192.168.1.256',       // Out of range
      '::1',                 // IPv6
      'localhost',           // Hostname
      '192.168.1.1/24',      // CIDR notation
      '192.168.1.1:8080',    // With port
      '',                    // Empty
      '   ',                 // Whitespace
      '192.168.1.🔒',        // Unicode
      '192.168.1.1; DROP TABLE', // SQL injection attempt
    ];

    for (let i = 0; i < count; i++) {
      const ip = malformedIPs[i % malformedIPs.length];
      
      attacks.push({
        ip,
        hasEncryption: Math.random() < 0.5,
        algorithm: Math.random() < 0.5 ? 'ML-KEM-768' : undefined,
        complexity: Math.floor(Math.random() * 15)
      });
    }

    return attacks;
  }

  /**
   * Encryption bypass attacks
   */
  private generateEncryptionAttacks(count: number): VerificationContext[] {
    const attacks: VerificationContext[] = [];

    const algorithms = [
      'ML-KEM-768',
      'ML-KEM-1024',
      'AES-256',
      'RSA-2048',
      'ChaCha20',
      undefined,
      'NONE',
      ''
    ];

    for (let i = 0; i < count; i++) {
      const hasEncryption = Math.random() < 0.7;
      const algorithm = hasEncryption 
        ? algorithms[Math.floor(Math.random() * algorithms.length)]
        : undefined;

      attacks.push({
        ip: '10.0.0.5',
        hasEncryption,
        algorithm,
        complexity: 5
      });
    }

    return attacks;
  }

  /**
   * Complexity attacks
   */
  private generateComplexityAttacks(count: number): VerificationContext[] {
    const attacks: VerificationContext[] = [];

    for (let i = 0; i < count; i++) {
      const complexity = Math.floor(Math.random() * 20); // 0-19

      attacks.push({
        ip: '10.0.0.5',
        hasEncryption: true,
        algorithm: 'ML-KEM-768',
        complexity
      });
    }

    return attacks;
  }

  /**
   * Get all attack vectors
   */
  getAttackVectors(): VerificationContext[] {
    return this.attackVectors;
  }

  /**
   * Get random subset for testing
   */
  getRandomSubset(count: number): VerificationContext[] {
    const shuffled = [...this.attackVectors].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count);
  }
}

// ============================================================================
// TEST ORCHESTRATOR
// ============================================================================

interface TestResult {
  totalTests: number;
  passed: number;
  failed: number;
  pass1: number;
  avgScore: number;
  duration: number;
  violationBreakdown: Record<string, number>;
  meetsTarget: boolean;
}

class AdversarialTestOrchestrator {
  private redTeamer: RedTeamer;
  private architect: VerifierAlpha;

  constructor() {
    this.redTeamer = new RedTeamer();
    this.architect = new VerifierAlpha(DEFAULT_POLICY);
  }

  /**
   * Run full adversarial test suite
   */
  async runFullSuite(): Promise<TestResult> {
    console.log('🚀 Starting Adversarial Testing Framework');
    console.log(`📊 Configuration: ${TEST_CONFIG.iterations} iterations`);
    console.log(`🎯 Target: ${TEST_CONFIG.targetPass1 * 100}% Pass@1\n`);

    const startTime = Date.now();
    this.architect.reset();

    const attackVectors = this.redTeamer.getRandomSubset(TEST_CONFIG.iterations);
    
    // Run tests with concurrency
    const results = await this.runConcurrentTests(
      attackVectors,
      TEST_CONFIG.concurrency
    );

    const duration = Date.now() - startTime;
    const stats = this.architect.getStats();

    // Calculate violation breakdown
    const violationBreakdown: Record<string, number> = {};
    for (const result of results) {
      for (const violation of result.violations) {
        violationBreakdown[violation.type] = 
          (violationBreakdown[violation.type] || 0) + 1;
      }
    }

    const testResult: TestResult = {
      totalTests: stats.total,
      passed: stats.passed,
      failed: stats.failed,
      pass1: stats.pass1,
      avgScore: stats.avgScore,
      duration,
      violationBreakdown,
      meetsTarget: stats.pass1 >= TEST_CONFIG.targetPass1
    };

    this.printResults(testResult);
    return testResult;
  }

  /**
   * Run tests with concurrency control
   */
  private async runConcurrentTests(
    contexts: VerificationContext[],
    concurrency: number
  ) {
    const results = [];
    
    for (let i = 0; i < contexts.length; i += concurrency) {
      const batch = contexts.slice(i, i + concurrency);
      const batchResults = await Promise.all(
        batch.map(ctx => this.architect.verify(ctx))
      );
      results.push(...batchResults);

      // Progress indicator
      if ((i + concurrency) % 100 === 0) {
        console.log(`✓ Completed ${Math.min(i + concurrency, contexts.length)}/${contexts.length} tests`);
      }
    }

    return results;
  }

  /**
   * Print formatted results
   */
  private printResults(result: TestResult): void {
    console.log('\n' + '='.repeat(70));
    console.log('📈 ADVERSARIAL TEST RESULTS');
    console.log('='.repeat(70));
    console.log(`Total Tests:      ${result.totalTests}`);
    console.log(`Passed:           ${result.passed} (${(result.passed / result.totalTests * 100).toFixed(2)}%)`);
    console.log(`Failed:           ${result.failed} (${(result.failed / result.totalTests * 100).toFixed(2)}%)`);
    console.log(`Pass@1:           ${(result.pass1 * 100).toFixed(3)}%`);
    console.log(`Average Score:    ${(result.avgScore * 100).toFixed(2)}%`);
    console.log(`Duration:         ${(result.duration / 1000).toFixed(2)}s`);
    console.log(`\n🎯 Target Pass@1:  ${(TEST_CONFIG.targetPass1 * 100)}%`);
    console.log(`Status:           ${result.meetsTarget ? '✅ PASSED' : '❌ FAILED'}`);
    
    console.log('\n📊 Violation Breakdown:');
    for (const [type, count] of Object.entries(result.violationBreakdown)) {
      console.log(`  ${type}: ${count}`);
    }
    console.log('='.repeat(70) + '\n');
  }

  /**
   * Generate JSON report
   */
  generateReport(result: TestResult): string {
    return JSON.stringify({
      timestamp: new Date().toISOString(),
      configuration: TEST_CONFIG,
      results: result,
      metadata: {
        version: '2026.Q1',
        framework: 'Bolt-Lattice-Architect',
        testType: 'Adversarial Red-Teamer vs Architect'
      }
    }, null, 2);
  }
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  const orchestrator = new AdversarialTestOrchestrator();
  const result = await orchestrator.runFullSuite();

  // Save report
  const report = orchestrator.generateReport(result);
  const fs = require('fs');
  const path = require('path');
  
  const reportPath = path.join(
    __dirname,
    '..',
    'reports',
    `adversarial_test_${Date.now()}.json`
  );

  fs.writeFileSync(reportPath, report, 'utf8');
  console.log(`📄 Report saved to: ${reportPath}`);

  // Exit with appropriate code
  process.exit(result.meetsTarget ? 0 : 1);
}

// Run if executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Test execution failed:', error);
    process.exit(1);
  });
}

export { AdversarialTestOrchestrator, RedTeamer, TEST_CONFIG };
