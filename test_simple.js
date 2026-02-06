/**
 * Simple Test - Debug Version
 */

const { VerifierAlpha } = require('./dist/src/lib/verifier-alpha');
const { DEFAULT_POLICY } = require('./dist/src/lib/security-policy');

async function simpleTest() {
  console.log('🔍 Running Simple Test...\n');
  
  const verifier = new VerifierAlpha(DEFAULT_POLICY);
  
  // Test 1: Valid request
  console.log('Test 1: Valid IP + Encryption');
  const result1 = await verifier.verify({
    ip: '10.0.0.5',
    hasEncryption: true,
    algorithm: 'ML-KEM-768',
    complexity: 5
  });
  console.log(`  Result: ${result1.passed ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`  Score: ${(result1.score * 100).toFixed(2)}%\n`);
  
  // Test 2: Invalid IP
  console.log('Test 2: Invalid IP');
  const result2 = await verifier.verify({
    ip: '8.8.8.8',
    hasEncryption: true,
    algorithm: 'ML-KEM-768',
    complexity: 5
  });
  console.log(`  Result: ${result2.passed ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`  Score: ${(result2.score * 100).toFixed(2)}%\n`);
  
  // Test 3: Missing encryption (should auto-recover)
  console.log('Test 3: Missing Encryption (Auto-Recovery)');
  const result3 = await verifier.verify({
    ip: '10.0.0.5',
    hasEncryption: false,
    complexity: 5
  });
  console.log(`  Result: ${result3.passed ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`  Score: ${(result3.score * 100).toFixed(2)}%`);
  console.log(`  Recovery Attempts: ${result3.metadata.recoveryAttempts}\n`);
  
  // Stats
  const stats = verifier.getStats();
  console.log('📊 Overall Stats:');
  console.log(`  Total: ${stats.total}`);
  console.log(`  Passed: ${stats.passed}`);
  console.log(`  Failed: ${stats.failed}`);
  console.log(`  Pass@1: ${(stats.pass1 * 100).toFixed(2)}%`);
}

simpleTest().catch(err => {
  console.error('❌ Test failed:', err);
  console.error(err.stack);
  process.exit(1);
});
