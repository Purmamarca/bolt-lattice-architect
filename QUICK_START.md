# 🚀 Quick Start Guide - Bolt-Lattice-Architect Orchestration

## Prerequisites

```bash
npm install
```

## Run Adversarial Tests (1,000 iterations)

```bash
npm run test:adversarial
```

Expected output:

```
🚀 Starting Adversarial Testing Framework
📊 Configuration: 1000 iterations
🎯 Target: 99.9% Pass@1

✓ Completed 100/1000 tests
✓ Completed 200/1000 tests
...
✓ Completed 1000/1000 tests

======================================================================
📈 ADVERSARIAL TEST RESULTS
======================================================================
Total Tests:      1000
Passed:           995 (99.50%)
Failed:           5 (0.50%)
Pass@1:           99.500%
Average Score:    98.75%
Duration:         12.34s

🎯 Target Pass@1:  99.9%
Status:           ✅ PASSED or ❌ FAILED

📊 Violation Breakdown:
  UNAUTHORIZED_IP: 3
  HIGH_COMPLEXITY: 2
======================================================================
```

## Run Full Orchestration

```bash
npm run orchestrate
```

This will:

1. Initialize Verifier Alpha
2. Setup threat intelligence
3. Configure webhooks
4. Execute orchestration sequence
5. Sync threat feeds
6. Run adversarial tests
7. Generate final report

## Start Continuous Threat Sync

```bash
npm run orchestrate:continuous
```

Runs continuous threat intelligence sync every 5 minutes.
Press Ctrl+C to stop.

## Simulate External Integration

```bash
npm run orchestrate:webhook
```

Simulates incoming webhooks from external AI systems (like "Jules").

## Programmatic Usage

### Basic Verification

```typescript
import { VerifierAlpha } from "./src/lib/verifier-alpha";

const verifier = new VerifierAlpha();

const result = await verifier.verify({
  ip: "10.0.0.5",
  hasEncryption: true,
  algorithm: "ML-KEM-768",
  complexity: 5,
});

console.log(result.passed); // true/false
console.log(result.score); // 0.0 to 1.0
```

### Batch Testing

```typescript
const contexts = [
  { ip: "10.0.0.5", hasEncryption: true, algorithm: "ML-KEM-768" },
  { ip: "192.168.1.50", hasEncryption: true, algorithm: "ML-KEM-768" },
  { ip: "8.8.8.8", hasEncryption: false }, // Should fail
];

const results = await verifier.verifyBatch(contexts);
const pass1 = verifier.calculatePass1();

console.log(`Pass@1: ${pass1 * 100}%`);
```

### Dynamic Policy Updates

```typescript
import { OrchestrationCoordinator } from "./src/lib/threat-intelligence";

const orchestrator = new OrchestrationCoordinator(verifier);
const policyManager = orchestrator.getPolicyManager();

// Enable auto-apply for critical threats
policyManager.setAutoApply(true);

// Manual sync
await policyManager.syncThreatIntelligence();

// Get pending updates
const pending = policyManager.getPendingUpdates();
console.log(`Pending updates: ${pending.length}`);
```

### Orchestration Sequence

```typescript
await orchestrator.executeSequence([
  "JULES_SCAN_THREAT_FEED",
  "JULES_REFACTOR_CFG",
  "ANTIGRAVITY_SUSPEND_TEST",
  "ANTIGRAVITY_RELOAD_POLICY",
  "ANTIGRAVITY_RESUME_STRESS_TEST",
]);

const eventLog = orchestrator.getEventLog();
console.log(`Executed ${eventLog.length} steps`);
```

## File Structure

```
bolt-lattice-architect/
├── src/
│   ├── lib/
│   │   ├── security-policy.ts        # CFG policy engine
│   │   ├── verifier-alpha.ts         # Verification agent
│   │   └── threat-intelligence.ts    # Threat intel framework
│   └── security/
│       └── quantum-safe.ts           # ML-KEM-768 implementation
├── tests/
│   └── adversarial_test.ts          # 1,000-iteration test suite
├── examples/
│   └── full_orchestration.ts        # Integration example
└── reports/                          # Generated test reports
```

## Key Metrics

| Metric            | Target  | How to Check                |
| ----------------- | ------- | --------------------------- |
| Pass@1            | ≥ 99.9% | `verifier.calculatePass1()` |
| Lattice Integrity | 100%    | All requests use ML-KEM-768 |
| CFG Compliance    | ≥ 99.9% | Policy violations < 0.1%    |

## Troubleshooting

### Tests failing?

- Check IP whitelist in `src/lib/security-policy.ts`
- Verify ML-KEM-768 is enabled
- Review violation logs

### Need to adjust targets?

```typescript
// In tests/adversarial_test.ts
const TEST_CONFIG = {
  iterations: 1000, // Adjust test count
  targetPass1: 0.999, // Adjust target (0.999 = 99.9%)
  concurrency: 10, // Parallel requests
};
```

### Want to add custom threat feeds?

```typescript
const aggregator = new ThreatIntelligenceAggregator();

aggregator.addFeed({
  id: "custom-feed",
  name: "My Custom Feed",
  url: "https://api.example.com/threats",
  apiKey: "your-api-key",
  updateInterval: 1800000, // 30 minutes
  priority: 7,
  enabled: true,
});
```

## Reports

After running tests, check the `reports/` directory for:

- `adversarial_test_<timestamp>.json` - Detailed test results
- `orchestration_report_<timestamp>.json` - Full orchestration logs

## Next Steps

1. **Validate 99.9% Target**: Run `npm run test:adversarial`
2. **Configure Real Feeds**: Add API keys for threat intelligence
3. **Deploy Webhooks**: Set up production HTTP server
4. **Monitor Continuously**: Use `npm run orchestrate:continuous`

---

**Need Help?** Check `ORCHESTRATION_SUMMARY.md` for detailed documentation.
