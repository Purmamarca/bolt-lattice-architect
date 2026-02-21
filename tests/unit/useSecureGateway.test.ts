/**
 * TDD Test Suite: useSecureGateway (standalone)
 * Tests for: src/security/useSecureGateway.ts
 *
 * Previously this module existed only as a compiled .js file.
 * These tests drove the creation of the .ts source (TDD Red phase).
 */

import { useSecureGateway, normalizeIp, isIpApproved } from '../../src/security/useSecureGateway';

// ============================================================================
// normalizeIp (re-export verification)
// ============================================================================

describe('normalizeIp (re-exported from useSecureGateway)', () => {
  it('normalizes whitespace-padded IP', () => {
    expect(normalizeIp('  10.0.0.5')).toBe('10.0.0.5');
  });

  it('normalizes decimal IP representation', () => {
    expect(normalizeIp('167772165')).toBe('10.0.0.5');
  });

  it('normalizes hex IP representation', () => {
    expect(normalizeIp('0xA000005')).toBe('10.0.0.5');
  });
});

// ============================================================================
// useSecureGateway() — standalone async function
// ============================================================================

describe('useSecureGateway()', () => {
  describe('authorized IPs — should succeed', () => {
    it('resolves for directly whitelisted IP 10.0.0.5', async () => {
      const result = await useSecureGateway('10.0.0.5', { test: true });
      expect(result.success).toBe(true);
      expect(result.verified).toBe(true);
      expect(result.destination).toBe('10.0.0.5');
    }, 10000);

    it('resolves for directly whitelisted IP 192.168.1.50', async () => {
      const result = await useSecureGateway('192.168.1.50', { test: true });
      expect(result.success).toBe(true);
      expect(result.destination).toBe('192.168.1.50');
    }, 10000);

    it('resolves for decimal representation of approved IP', async () => {
      // 167772165 == 10.0.0.5
      const result = await useSecureGateway('167772165', { test: true });
      expect(result.success).toBe(true);
      expect(result.destination).toBe('10.0.0.5');
    }, 10000);

    it('resolves for hex representation of approved IP', async () => {
      // 0xA000005 == 10.0.0.5
      const result = await useSecureGateway('0xA000005', { test: true });
      expect(result.success).toBe(true);
      expect(result.destination).toBe('10.0.0.5');
    }, 10000);

    it('resolves for whitespace-padded approved IP', async () => {
      const result = await useSecureGateway('  10.0.0.5', { data: 'padded' });
      expect(result.success).toBe(true);
      expect(result.destination).toBe('10.0.0.5');
    }, 10000);

    it('returns an encrypted payload object', async () => {
      const result = await useSecureGateway('10.0.0.5', { cmd: 'ping' });
      expect(result.payload).toBeDefined();
      expect(result.payload.ciphertext).toBeDefined();
      expect(result.payload.signature).toBeDefined();
    }, 10000);
  });

  describe('unauthorized IPs — must throw', () => {
    it('throws for unauthorized IP 192.168.1.99', async () => {
      await expect(useSecureGateway('192.168.1.99', {}))
        .rejects
        .toThrow('CFG Policy Violation');
    });

    it('throws for public IP 8.8.8.8', async () => {
      await expect(useSecureGateway('8.8.8.8', {}))
        .rejects
        .toThrow('CFG Policy Violation');
    });

    it('throws for hex representation of rogue IP 0xC0A80163 (192.168.1.99)', async () => {
      await expect(useSecureGateway('0xC0A80163', {}))
        .rejects
        .toThrow('CFG Policy Violation');
    });

    it('throws for malformed IP', async () => {
      await expect(useSecureGateway('not-an-ip', {}))
        .rejects
        .toThrow('CFG Policy Violation');
    });
  });

  describe('error message quality', () => {
    it('error message includes the original IP', async () => {
      try {
        await useSecureGateway('8.8.8.8', {});
        fail('Expected to throw');
      } catch (e: any) {
        expect(e.message).toContain('8.8.8.8');
      }
    });

    it('error message includes the normalized IP', async () => {
      try {
        // decimal of 192.168.1.99 = 3232235875
        await useSecureGateway('3232235875', {});
        fail('Expected to throw');
      } catch (e: any) {
        expect(e.message).toContain('192.168.1.99');
      }
    });
  });
});
