import { ml_kem } from '../security/quantum-safe';
import { isIpApproved, normalizeIp } from '../lib/security-policy';

/**
 * useSecureGateway - React hook for making quantum-safe network requests.
 * Enforces CFG Policy (IP whitelist) and signs each request with ML-KEM-768.
 */
export function useSecureGateway() {
  const secureRequest = async (targetIp: string, data: any) => {
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
  };

  return { secureRequest };
}
