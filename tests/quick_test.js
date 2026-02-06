"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const useSecureGateway_1 = require("../src/security/useSecureGateway");
/**
 * Quick Verification Test
 * Tests a few scenarios to verify the system works
 */
async function quickTest() {
    console.log('🧪 Quick Verification Test\n');
    console.log('='.repeat(60));
    const tests = [
        { name: 'Direct Whitelist', ip: '10.0.0.5', shouldPass: true },
        { name: 'Direct Rogue', ip: '192.168.1.99', shouldPass: false },
        { name: 'Decimal Auth', ip: '167772165', shouldPass: true },
        { name: 'Hex Rogue', ip: '0xC0A80163', shouldPass: false },
    ];
    let passed = 0;
    let failed = 0;
    for (const test of tests) {
        process.stdout.write(`${test.name} [${test.ip}]... `);
        try {
            const result = await (0, useSecureGateway_1.useSecureGateway)(test.ip, { test: true });
            if (test.shouldPass) {
                console.log('✅ PASS (Authorized)');
                passed++;
            }
            else {
                console.log('❌ FAIL (Security bypass!)');
                failed++;
            }
        }
        catch (error) {
            if (!test.shouldPass) {
                console.log('✅ PASS (Blocked)');
                passed++;
            }
            else {
                console.log('❌ FAIL (False positive)');
                failed++;
            }
        }
    }
    console.log('='.repeat(60));
    console.log(`\nResults: ${passed}/${tests.length} passed`);
    if (passed === tests.length) {
        console.log('✅ All tests passed!\n');
        process.exit(0);
    }
    else {
        console.log('❌ Some tests failed\n');
        process.exit(1);
    }
}
quickTest().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
