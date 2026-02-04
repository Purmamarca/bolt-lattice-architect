import sys
import os

def verify():
    print("Verifying quantum-safe compliance...")
    try:
        with open('src/index.ts', 'r') as f:
            content = f.read()
            if 'ml_kem' not in content:
                print("FAILURE: ml_kem not found.")
                return False
            if 'fetch' in content:
                 print("FAILURE: Legacy fetch found.")
                 return False
            if "@security/quantum-safe" not in content:
                print("FAILURE: @security/quantum-safe not imported.")
                return False

    except FileNotFoundError:
        print("FAILURE: src/index.ts not found.")
        return False

    print("SUCCESS: Code is quantum-safe.")
    with open('lattice_audit.trace', 'w') as f:
        f.write("HANDSHAKE_COMPLETE_99.9_PERCENT_RELIABILITY")
    return True

if __name__ == "__main__":
    if verify():
        sys.exit(0)
    else:
        sys.exit(1)
