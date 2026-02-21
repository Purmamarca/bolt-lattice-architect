/**
 * src/security/useSecureGateway.ts
 *
 * Standalone (non-React) secure gateway module.
 * Used directly by Node.js tests (stress_test, quick_test, adversarial_test).
 *
 * The React hook equivalent lives in src/hooks/useSecureGateway.ts
 */

import { ml_kem } from './quantum-safe';
import { normalizeIp, isIpApproved } from '../lib/security-policy';

export { normalizeIp, isIpApproved };

export interface GatewayResult {
  success: boolean;
  destination: string;
  payload: any;
  verified: boolean;
}

/**
 * Standalone gateway function for server-side / test use.
 * Mirrors the React hook's secureRequest method.
 */
export async function useSecureGateway(
  targetIp: string,
  data: any
): Promise<GatewayResult> {
  const normalizedIp = normalizeIp(targetIp);

  // 1. IP Validation (Against normalized IP)
  if (!isIpApproved(normalizedIp)) {
    throw new Error(
      `CFG Policy Violation: IP ${targetIp} (normalized: ${normalizedIp}) is not in the approved whitelist.`
    );
  }

  // 2. Quantum-Safe Signing (ML-KEM-768)
  const keyPair = await ml_kem.generateKeyPair('ML-KEM-768');
  const encryptedPayload = await ml_kem.encryptData(
    data,
    keyPair.publicKey,
    'ML-KEM-768'
  );

  // 3. Simulated Interception Signing
  console.log(`[GATEWAY] Intercepted request to ${targetIp} (as ${normalizedIp})`);
  console.log(`[GATEWAY] Signature: ${encryptedPayload.signature}`);

  return {
    success: true,
    destination: normalizedIp,
    payload: encryptedPayload,
    verified: true,
  };
}
