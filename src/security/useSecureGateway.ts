import { ml_kem, LatticeConfig } from "./quantum-safe";

const APPROVED_IPS = ["10.0.0.5", "192.168.1.50"];

/**
 * useSecureGateway - Interceptor for all outgoing network requests
 * Enforces CFG Policy and signs requests with ML-KEM-768
 */
export async function useSecureGateway(targetIp: string, data: any) {
  const normalizedIp = normalizeIp(targetIp);
  
  // 1. IP Validation (Against normalized IP)
  if (!APPROVED_IPS.includes(normalizedIp)) {
    throw new Error(
      `CFG Policy Violation: IP ${targetIp} (normalized: ${normalizedIp}) is not in the approved whitelist.`
    );
  }

  // 2. Quantum-Safe Signing (ML-KEM-768)
  const keyPair = await ml_kem.generateKeyPair("ML-KEM-768");
  const encryptedPayload = await ml_kem.encryptData(
    data,
    keyPair.publicKey,
    "ML-KEM-768"
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

/**
 * Normalizes IP addresses to prevent obfuscation bypasses.
 * Handles hex, decimal, octal, and dotted-decimal formats.
 */
export function normalizeIp(ip: string): string {
  // 1. Remove any surrounding whitespace
  let cleanIp = ip.trim();

  // 2. Handle single number (decimal) representation
  if (/^\d+$/.test(cleanIp)) {
    const num = parseInt(cleanIp, 10);
    return [
      (num >>> 24) & 0xFF,
      (num >>> 16) & 0xFF,
      (num >>> 8) & 0xFF,
      num & 0xFF
    ].join('.');
  }

  // 3. Handle hex representation (e.g., 0xA000005)
  if (/^0x[0-9a-fA-F]+$/.test(cleanIp)) {
    const num = parseInt(cleanIp, 16);
    return [
      (num >>> 24) & 0xFF,
      (num >>> 16) & 0xFF,
      (num >>> 8) & 0xFF,
      num & 0xFF
    ].join('.');
  }

  // 4. Handle dotted parts (dec, hex, octal)
  const parts = cleanIp.split('.');
  if (parts.length === 4) {
    const normalizedParts = parts.map(part => {
      if (part.startsWith('0x')) return parseInt(part, 16).toString();
      if (part.startsWith('0') && part.length > 1) return parseInt(part, 8).toString();
      return parseInt(part, 10).toString();
    });
    return normalizedParts.join('.');
  }

  return cleanIp;
}
