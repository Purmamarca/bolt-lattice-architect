import { useSecureGateway } from '../src/security/useSecureGateway';
import { globalPolicy } from '../src/lib/security-policy';

/**
 * Advanced Stress Test with Concurrency
 * Target: 100 iterations, 10 concurrent requests
 * Metrics: Pass@1, Lattice Integrity, CFG Compliance
 */

interface StressTestConfig {
  iterations: number;
  concurrency: number;
  target: string;
}

interface TestScenario {
  name: string;
  ip: string;
  isAuthorized: boolean;
  category: 'direct' | 'obfuscated' | 'malformed';
}

interface TestResult {
  scenario: string;
  ip: string;
  expected: 'PASS' | 'BLOCK';
  actual: 'PASS' | 'BLOCK' | 'ERROR';
  latency: number;
  iteration: number;
  timestamp: number;
}

interface StressTestReport {
  config: StressTestConfig;
  totalTests: number;
  passed: number;
  failed: number;
  bypasses: number;
  falsePositives: number;
  reliability: number;
  avgLatency: number;
  maxLatency: number;
  minLatency: number;
  leakageBytes: number;
  results: TestResult[];
  metrics: {
    passAt1: number;
    latticeIntegrity: number;
    cfgCompliance: number;
  };
}

// ============================================================================
// TEST SCENARIOS
// ============================================================================

const TEST_SCENARIOS: TestScenario[] = [
  // Direct whitelisted IPs
  { name: 'Direct_Whitelist_Primary', ip: '10.0.0.5', isAuthorized: true, category: 'direct' },
  { name: 'Direct_Whitelist_Secondary', ip: '192.168.1.50', isAuthorized: true, category: 'direct' },
  
  // Direct rogue IPs
  { name: 'Direct_Rogue_1', ip: '192.168.1.99', isAuthorized: false, category: 'direct' },
  { name: 'Direct_Rogue_2', ip: '8.8.8.8', isAuthorized: false, category: 'direct' },
  
  // Decimal obfuscation (authorized)
  { name: 'Decimal_Auth_Primary', ip: '167772165', isAuthorized: true, category: 'obfuscated' }, // 10.0.0.5
  { name: 'Decimal_Auth_Secondary', ip: '3232235826', isAuthorized: true, category: 'obfuscated' }, // 192.168.1.50
  
  // Decimal obfuscation (rogue)
  { name: 'Decimal_Rogue_1', ip: '3232235875', isAuthorized: false, category: 'obfuscated' }, // 192.168.1.99
  { name: 'Decimal_Rogue_2', ip: '134744072', isAuthorized: false, category: 'obfuscated' }, // 8.8.8.8
  
  // Hex obfuscation (authorized)
  { name: 'Hex_Auth_Primary', ip: '0xA000005', isAuthorized: true, category: 'obfuscated' }, // 10.0.0.5
  { name: 'Hex_Auth_Secondary', ip: '0xC0A80132', isAuthorized: true, category: 'obfuscated' }, // 192.168.1.50
  
  // Hex obfuscation (rogue)
  { name: 'Hex_Rogue_1', ip: '0xC0A80163', isAuthorized: false, category: 'obfuscated' }, // 192.168.1.99
  { name: 'Hex_Rogue_2', ip: '0x08080808', isAuthorized: false, category: 'obfuscated' }, // 8.8.8.8
  
  // Octal/dotted mix (authorized)
  { name: 'Octal_Auth_Primary', ip: '012.0.0.05', isAuthorized: true, category: 'obfuscated' }, // 10.0.0.5
  { name: 'Octal_Auth_Secondary', ip: '0300.0250.01.062', isAuthorized: true, category: 'obfuscated' }, // 192.168.1.50
  
  // Octal/dotted mix (rogue)
  { name: 'Octal_Rogue_1', ip: '0300.0250.01.0143', isAuthorized: false, category: 'obfuscated' }, // 192.168.1.99
  
  // Malformed/overflow
  { name: 'Malformed_Overflow', ip: '999.999.999.999', isAuthorized: false, category: 'malformed' },
  { name: 'Malformed_Negative', ip: '-1.-1.-1.-1', isAuthorized: false, category: 'malformed' },
  { name: 'Malformed_Letters', ip: 'abc.def.ghi.jkl', isAuthorized: false, category: 'malformed' },
  
  // Whitespace attacks
  { name: 'Whitespace_Leading', ip: '  10.0.0.5', isAuthorized: true, category: 'obfuscated' },
  { name: 'Whitespace_Trailing', ip: '192.168.1.50  ', isAuthorized: true, category: 'obfuscated' },
];

// ============================================================================
// STRESS TEST RUNNER
// ============================================================================

class StressTestRunner {
  private config: StressTestConfig;
  private results: TestResult[] = [];
  private leakageBytes: number = 0;

  constructor(config: StressTestConfig) {
    this.config = config;
  }

  /**
   * Run a single test scenario
   */
  private async runTest(
    scenario: TestScenario,
    iteration: number
  ): Promise<TestResult> {
    const startTime = performance.now();
    
    try {
      const result = await useSecureGateway(scenario.ip, { 
        cmd: 'stress_test',
        iteration 
      });
      
      const latency = performance.now() - startTime;
      
      if (scenario.isAuthorized) {
        // Should pass
        return {
          scenario: scenario.name,
          ip: scenario.ip,
          expected: 'PASS',
          actual: 'PASS',
          latency,
          iteration,
          timestamp: Date.now()
        };
      } else {
        // Should have been blocked but wasn't - SECURITY BYPASS!
        this.leakageBytes += JSON.stringify(result.payload).length;
        return {
          scenario: scenario.name,
          ip: scenario.ip,
          expected: 'BLOCK',
          actual: 'PASS',
          latency,
          iteration,
          timestamp: Date.now()
        };
      }
    } catch (error: any) {
      const latency = performance.now() - startTime;
      
      if (!scenario.isAuthorized) {
        // Correctly blocked
        return {
          scenario: scenario.name,
          ip: scenario.ip,
          expected: 'BLOCK',
          actual: 'BLOCK',
          latency,
          iteration,
          timestamp: Date.now()
        };
      } else {
        // False positive - authorized IP blocked
        return {
          scenario: scenario.name,
          ip: scenario.ip,
          expected: 'PASS',
          actual: 'BLOCK',
          latency,
          iteration,
          timestamp: Date.now()
        };
      }
    }
  }

  /**
   * Run tests with concurrency control
   */
  private async runBatch(scenarios: TestScenario[], iteration: number): Promise<void> {
    const batchSize = this.config.concurrency;
    
    for (let i = 0; i < scenarios.length; i += batchSize) {
      const batch = scenarios.slice(i, i + batchSize);
      const promises = batch.map(scenario => this.runTest(scenario, iteration));
      const batchResults = await Promise.all(promises);
      this.results.push(...batchResults);
    }
  }

  /**
   * Run complete stress test
   */
  async run(): Promise<StressTestReport> {
    console.log('='.repeat(80));
    console.log('🔥 ADVANCED STRESS TEST - BOLT-LATTICE-ARCHITECT');
    console.log('='.repeat(80));
    console.log(`Target: ${this.config.target}`);
    console.log(`Iterations: ${this.config.iterations}`);
    console.log(`Concurrency: ${this.config.concurrency}`);
    console.log(`Total Tests: ${this.config.iterations * TEST_SCENARIOS.length}`);
    console.log('='.repeat(80) + '\n');

    const startTime = Date.now();

    // Run iterations
    for (let i = 1; i <= this.config.iterations; i++) {
      process.stdout.write(`\rIteration ${i}/${this.config.iterations}...`);
      await this.runBatch(TEST_SCENARIOS, i);
    }
    
    console.log('\n\n' + '='.repeat(80));
    console.log('📊 ANALYZING RESULTS...');
    console.log('='.repeat(80) + '\n');

    const totalTime = Date.now() - startTime;
    return this.generateReport(totalTime);
  }

  /**
   * Generate comprehensive report
   */
  private generateReport(totalTime: number): StressTestReport {
    const totalTests = this.results.length;
    const passed = this.results.filter(r => r.expected === r.actual).length;
    const failed = totalTests - passed;
    
    // Count bypasses (expected BLOCK but got PASS)
    const bypasses = this.results.filter(
      r => r.expected === 'BLOCK' && r.actual === 'PASS'
    ).length;
    
    // Count false positives (expected PASS but got BLOCK)
    const falsePositives = this.results.filter(
      r => r.expected === 'PASS' && r.actual === 'BLOCK'
    ).length;
    
    const reliability = (passed / totalTests) * 100;
    
    const latencies = this.results.map(r => r.latency);
    const avgLatency = latencies.reduce((a, b) => a + b, 0) / latencies.length;
    const maxLatency = Math.max(...latencies);
    const minLatency = Math.min(...latencies);
    
    // Calculate metrics
    const passAt1 = (this.results.filter(r => 
      r.iteration === 1 && r.expected === r.actual
    ).length / TEST_SCENARIOS.length) * 100;
    
    const latticeIntegrity = bypasses === 0 ? 100 : 0;
    const cfgCompliance = reliability;
    
    const report: StressTestReport = {
      config: this.config,
      totalTests,
      passed,
      failed,
      bypasses,
      falsePositives,
      reliability,
      avgLatency,
      maxLatency,
      minLatency,
      leakageBytes: this.leakageBytes,
      results: this.results,
      metrics: {
        passAt1,
        latticeIntegrity,
        cfgCompliance
      }
    };
    
    this.printReport(report, totalTime);
    return report;
  }

  /**
   * Print formatted report
   */
  private printReport(report: StressTestReport, totalTime: number): void {
    console.log('📈 FINAL REPORT');
    console.log('='.repeat(80));
    console.log(`Total Tests:        ${report.totalTests}`);
    console.log(`Passed:             ${report.passed} (${((report.passed/report.totalTests)*100).toFixed(2)}%)`);
    console.log(`Failed:             ${report.failed} (${((report.failed/report.totalTests)*100).toFixed(2)}%)`);
    console.log(`Security Bypasses:  ${report.bypasses} ⚠️`);
    console.log(`False Positives:    ${report.falsePositives}`);
    console.log(`Data Leakage:       ${report.leakageBytes} bytes`);
    console.log('');
    console.log(`Reliability:        ${report.reliability.toFixed(2)}% ${report.reliability >= 99.9 ? '✅' : '❌'}`);
    console.log(`Avg Latency:        ${report.avgLatency.toFixed(2)}ms`);
    console.log(`Max Latency:        ${report.maxLatency.toFixed(2)}ms`);
    console.log(`Min Latency:        ${report.minLatency.toFixed(2)}ms`);
    console.log(`Total Time:         ${(totalTime/1000).toFixed(2)}s`);
    console.log('');
    console.log('📊 METRICS');
    console.log('='.repeat(80));
    console.log(`Pass@1:             ${report.metrics.passAt1.toFixed(2)}%`);
    console.log(`Lattice Integrity:  ${report.metrics.latticeIntegrity.toFixed(2)}%`);
    console.log(`CFG Compliance:     ${report.metrics.cfgCompliance.toFixed(2)}%`);
    console.log('='.repeat(80));
    
    // Success criteria
    const success = report.reliability >= 99.9 && report.leakageBytes === 0;
    console.log('');
    if (success) {
      console.log('✅ MISSION SUCCESS - 99.9% RELIABILITY TARGET ACHIEVED');
    } else {
      console.log('❌ MISSION FAILED - RELIABILITY TARGET NOT MET');
      if (report.reliability < 99.9) {
        console.log(`   - Reliability: ${report.reliability.toFixed(2)}% (target: 99.9%)`);
      }
      if (report.leakageBytes > 0) {
        console.log(`   - Data leakage: ${report.leakageBytes} bytes (target: 0)`);
      }
    }
    console.log('='.repeat(80) + '\n');
  }
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  // Check for environment variable override for final certification
  const iterations = process.env.STRESS_ITERATIONS ? parseInt(process.env.STRESS_ITERATIONS) : 100;
  const concurrency = process.env.STRESS_CONCURRENCY ? parseInt(process.env.STRESS_CONCURRENCY) : 10;
  
  const config: StressTestConfig = {
    iterations,
    concurrency,
    target: 'src/security/useSecureGateway.ts'
  };

  const runner = new StressTestRunner(config);
  const report = await runner.run();

  // Save report to file
  const fs = require('fs');
  fs.writeFileSync(
    'stress_test_report.json',
    JSON.stringify(report, null, 2)
  );
  console.log('📄 Full report saved to: stress_test_report.json\n');

  // Exit with appropriate code
  process.exit(report.reliability >= 99.9 && report.leakageBytes === 0 ? 0 : 1);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
