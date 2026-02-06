/**
 * Mini Adversarial Test - 10 iterations
 */

const { VerifierAlpha } = require('./dist/src/lib/verifier-alpha');
const { DEFAULT_POLICY } = require('./dist/src/lib/security-policy');

async function miniTest() {
  console.log('🚀 Mini Adversarial Test (10 iterations)\n');
  
  const verifier = new VerifierAlpha(DEFAULT_POLICY);
  
  const testCases = [
    { name: 'Valid IP + Encryption', ip: '10.0.0.5', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
    { name: 'Valid IP + Encryption', ip: '192.168.1.50', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
    { name: 'Invalid IP', ip: '8.8.8.8', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
    { name: 'Obfuscated IP (decimal)', ip: '167772165', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
    { name: 'Obfuscated IP (hex)', ip: '0x0a000005', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
    { name: 'Missing Encryption', ip: '10.0.0.5', hasEncryption: false, complexity: 5 },
    { name: 'High Complexity', ip: '10.0.0.5', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 15 },
    { name: 'Malformed IP', ip: '999.999.999.999', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
    { name: 'Non-quantum algorithm', ip: '10.0.0.5', hasEncryption: true, algorithm: 'AES-256', complexity: 5 },
    { name: 'Empty IP', ip: '', hasEncryption: true, algorithm: 'ML-KEM-768', complexity: 5 },
  ];
  
  for (let i = 0; i < testCases.length; i++) {
    const testCase = testCases[i];
    try {
      const result = await verifier.verify(testCase);
      console.log(`${i + 1}. ${testCase.name}: ${result.passed ? '✅' : '❌'} (score: ${(result.score * 100).toFixed(0)}%)`);
    } catch (error) {
      console.error(`${i + 1}. ${testCase.name}: ❌ ERROR - ${error.message}`);
    }
  }
  
  const stats = verifier.getStats();
  console.log('\n📊 Results:');
  console.log(`  Total: ${stats.total}`);
  console.log(`  Passed: ${stats.passed}`);
  console.log(`  Failed: ${stats.failed}`);
  console.log(`  Pass@1: ${(stats.pass1 * 100).toFixed(2)}%`);
  console.log(`  Target: 99.9%`);
  console.log(`  Status: ${stats.pass1 >= 0.999 ? '✅ PASSED' : stats.pass1 >= 0.5 ? '⚠️  ACCEPTABLE' : '❌ FAILED'}`);
}

miniTest().catch(err => {
  console.error('❌ Test failed:', err);
  console.error(err.stack);
  process.exit(1);
});
