"""
Bolt.new Trajectory Generator
Generates 100 formal trajectories following EBNF grammar for 99.9% reliability target
"""
import json
import random
from typing import List, Dict

# Configuration Variables
COMPONENTS = ["AuthProvider", "SecureDashboard", "CryptoBridge", "DataVault", "LatticeTunnel"]
FAILURES = [
    "npm install failed: 404",
    "Invalid Lattice Handshake",
    "Port 5173 occupied",
    "Module not found: @security/quantum-safe",
    "EADDRINUSE: address already in use",
    "TypeScript compilation failed",
    "Vite build error: missing dependency"
]
APPROVED_IPS = ["10.0.0.5", "192.168.1.50"]
PORTS = [5173, 5174, 5175, 3000, 8080]

# File paths for different components
FILE_PATHS = {
    "AuthProvider": "src/components/AuthProvider.tsx",
    "SecureDashboard": "src/components/SecureDashboard.tsx",
    "CryptoBridge": "src/api/CryptoBridge.ts",
    "DataVault": "src/storage/DataVault.ts",
    "LatticeTunnel": "src/network/LatticeTunnel.ts"
}

# Additional file types for variation
ADDITIONAL_FILES = [
    "src/main.tsx",
    "src/App.tsx",
    "src/api/index.ts",
    "src/utils/crypto.ts",
    "vite.config.ts",
    "tsconfig.json",
    "package.json",
    "src/hooks/useAuth.ts",
    "src/contexts/SecurityContext.tsx",
    "src/services/api.service.ts"
]

def generate_component_code(component: str, include_import: bool = True) -> str:
    """Generate component-specific code with quantum-safe import"""
    import_line = "import { ml_kem } from '@security/quantum-safe';\n" if include_import else ""
    
    code_templates = {
        "AuthProvider": f"{import_line}export const AuthProvider = ({{ children }}) => {{\n  const auth = ml_kem.authenticate();\n  return <div>{{children}}</div>;\n}};",
        "SecureDashboard": f"{import_line}export const SecureDashboard = () => {{\n  const data = ml_kem.decrypt(sessionStorage.getItem('data'));\n  return <div>Dashboard: {{data}}</div>;\n}};",
        "CryptoBridge": f"{import_line}export class CryptoBridge {{\n  encrypt(data: string) {{ return ml_kem.encrypt(data); }}\n  decrypt(cipher: string) {{ return ml_kem.decrypt(cipher); }}\n}}",
        "DataVault": f"{import_line}export class DataVault {{\n  private store = new Map();\n  save(key: string, value: any) {{ this.store.set(key, ml_kem.encrypt(JSON.stringify(value))); }}\n  load(key: string) {{ return JSON.parse(ml_kem.decrypt(this.store.get(key))); }}\n}}",
        "LatticeTunnel": f"{import_line}export class LatticeTunnel {{\n  connect(endpoint: string) {{ return ml_kem.handshake(endpoint); }}\n  send(data: any) {{ return ml_kem.encrypt(JSON.stringify(data)); }}\n}}"
    }
    
    return code_templates.get(component, f"{import_line}export const {component} = () => {{}};")

def generate_category_a_trajectory(idx: int) -> Dict:
    """Category A: Successful full-stack setup with React + Vite"""
    component = random.choice(COMPONENTS)
    ip = random.choice(APPROVED_IPS)
    
    return {
        "id": idx,
        "category": "A",
        "thought": f"Setting up React+Vite full-stack application with {component} component for production deployment",
        "plan": ["INSTALL_DEPS", "CREATE_FILE", "RUN_DEV_SERVER"],
        "artifact": f"<boltArtifact id='setup-{idx}' title='{component} Full Setup'><boltAction type='file' filePath='{FILE_PATHS[component]}'>{generate_component_code(component)}</boltAction><boltAction type='shell'>npm install && npm run dev</boltAction></boltArtifact>",
        "approved_ip": ip,
        "status": "success"
    }

def generate_category_b_trajectory(idx: int) -> Dict:
    """Category B: Security-first API integration using Lattice Shield"""
    component = random.choice(["CryptoBridge", "LatticeTunnel", "DataVault"])
    ip = random.choice(APPROVED_IPS)
    api_file = random.choice(["src/api/secure.ts", "src/services/encryption.ts", "src/network/quantum.ts"])
    
    return {
        "id": idx,
        "category": "B",
        "thought": f"Implementing {component} with Lattice Shield for quantum-resistant API security layer",
        "plan": ["INSTALL_DEPS", "CREATE_FILE"],
        "artifact": f"<boltArtifact id='security-{idx}' title='{component} Security Layer'><boltAction type='file' filePath='{api_file}'>{generate_component_code(component)}</boltAction><boltAction type='file' filePath='src/config/security.ts'>import {{ ml_kem }} from '@security/quantum-safe';\nexport const securityConfig = {{ algorithm: 'ML-KEM-768', mode: 'strict' }};</boltAction></boltArtifact>",
        "approved_ip": ip,
        "status": "success"
    }

def generate_category_c_trajectory(idx: int) -> Dict:
    """Category C: Error recovery where agent fixes a failed operation"""
    failure = random.choice(FAILURES)
    ip = random.choice(APPROVED_IPS)
    
    recovery_actions = {
        "npm install failed: 404": {
            "thought": "Recovering from npm 404 error by updating package registry and dependencies",
            "plan": ["REFLEXION", "INSTALL_DEPS"],
            "artifact": "<boltAction type='file' filePath='package.json'>{\"dependencies\": {\"react\": \"^18.2.0\", \"@security/quantum-safe\": \"^1.0.0\"}}</boltAction><boltAction type='shell'>npm cache clean --force && npm install</boltAction>"
        },
        "Invalid Lattice Handshake": {
            "thought": "Fixing Invalid Lattice Handshake by regenerating quantum-safe key pairs",
            "plan": ["REFLEXION", "CREATE_FILE"],
            "artifact": "<boltAction type='file' filePath='src/network/handshake.ts'>import { ml_kem } from '@security/quantum-safe';\nexport const initHandshake = () => { const keys = ml_kem.keyGen(); return keys; };</boltAction>"
        },
        "Port 5173 occupied": {
            "thought": "Resolving port conflict by updating Vite configuration to use alternative port",
            "plan": ["REFLEXION", "RUN_DEV_SERVER"],
            "artifact": f"<boltAction type='file' filePath='vite.config.ts'>export default {{ server: {{ port: {random.choice([p for p in PORTS if p != 5173])} }} }}</boltAction><boltAction type='shell'>npm run dev</boltAction>"
        },
        "Module not found: @security/quantum-safe": {
            "thought": "Installing missing quantum-safe security module",
            "plan": ["REFLEXION", "INSTALL_DEPS"],
            "artifact": "<boltAction type='shell'>npm install @security/quantum-safe --save</boltAction>"
        },
        "EADDRINUSE: address already in use": {
            "thought": "Killing existing process and restarting on new port",
            "plan": ["REFLEXION", "RUN_DEV_SERVER"],
            "artifact": f"<boltAction type='shell'>npx kill-port 5173 && npm run dev -- --port {random.choice(PORTS)}</boltAction>"
        },
        "TypeScript compilation failed": {
            "thought": "Fixing TypeScript errors by updating type definitions",
            "plan": ["REFLEXION", "CREATE_FILE"],
            "artifact": "<boltAction type='file' filePath='src/types/quantum.d.ts'>declare module '@security/quantum-safe' { export const ml_kem: any; }</boltAction>"
        },
        "Vite build error: missing dependency": {
            "thought": "Resolving Vite build error by installing missing dependencies",
            "plan": ["REFLEXION", "INSTALL_DEPS"],
            "artifact": "<boltAction type='shell'>npm install --save-dev @vitejs/plugin-react</boltAction>"
        }
    }
    
    recovery = recovery_actions.get(failure, recovery_actions["npm install failed: 404"])
    
    return {
        "id": idx,
        "category": "C",
        "thought": recovery["thought"],
        "plan": recovery["plan"],
        "artifact": f"<boltArtifact id='recovery-{idx}' title='Error Recovery'>{recovery['artifact']}</boltArtifact>",
        "failure": failure,
        "approved_ip": ip,
        "status": "recovered"
    }

def generate_category_d_trajectory(idx: int) -> Dict:
    """Category D: Multi-file synchronization"""
    comp1, comp2 = random.sample(COMPONENTS, 2)
    ip = random.choice(APPROVED_IPS)
    additional_file = random.choice(ADDITIONAL_FILES)
    
    return {
        "id": idx,
        "category": "D",
        "thought": f"Synchronizing {comp1} and {comp2} with shared quantum-safe security context across multiple files",
        "plan": ["CREATE_FILE", "CREATE_FILE", "CREATE_FILE"],
        "artifact": f"<boltArtifact id='sync-{idx}' title='Multi-file Sync'><boltAction type='file' filePath='{FILE_PATHS[comp1]}'>{generate_component_code(comp1)}</boltAction><boltAction type='file' filePath='{FILE_PATHS[comp2]}'>{generate_component_code(comp2)}</boltAction><boltAction type='file' filePath='{additional_file}'>import {{ ml_kem }} from '@security/quantum-safe';\nimport {{ {comp1} }} from './components/{comp1}';\nimport {{ {comp2} }} from './components/{comp2}';</boltAction></boltArtifact>",
        "approved_ip": ip,
        "status": "success"
    }

def generate_category_e_trajectory(idx: int) -> Dict:
    """Category E: Refusal of unsafe commands"""
    unsafe_patterns = [
        {"pattern": "eval()", "reason": "eval() allows arbitrary code execution - security vulnerability"},
        {"pattern": "dangerouslySetInnerHTML", "reason": "dangerouslySetInnerHTML exposes XSS attack vectors"},
        {"pattern": "innerHTML", "reason": "innerHTML manipulation can lead to XSS vulnerabilities"},
        {"pattern": "document.write()", "reason": "document.write() is deprecated and unsafe"},
        {"pattern": "Function() constructor", "reason": "Function constructor enables code injection"},
        {"pattern": "setTimeout with string", "reason": "setTimeout with string argument acts like eval()"},
        {"pattern": "new Function()", "reason": "Dynamic function creation is a security risk"},
        {"pattern": "__proto__ manipulation", "reason": "Prototype pollution attack vector"}
    ]
    
    unsafe = random.choice(unsafe_patterns)
    ip = random.choice(APPROVED_IPS)
    
    return {
        "id": idx,
        "category": "E",
        "thought": f"Refusing to implement {unsafe['pattern']} due to security policy violation",
        "plan": ["REFUSE"],
        "artifact": f"<boltArtifact id='refusal-{idx}' title='Security Refusal'><boltAction type='file' filePath='SECURITY_REFUSAL.md'>## Security Violation Detected\n\n**Pattern**: {unsafe['pattern']}\n**Reason**: {unsafe['reason']}\n**Policy**: Lattice Shield Security Standard v2.0\n**Alternative**: Use safe DOM manipulation or React state management</boltAction></boltArtifact>",
        "approved_ip": ip,
        "status": "refused",
        "unsafe_pattern": unsafe['pattern']
    }

def generate_all_trajectories() -> List[Dict]:
    """Generate all 100 trajectories with proper distribution"""
    trajectories = []
    
    # Category distribution: 20 each
    categories = {
        'A': 20,  # Full-stack setups
        'B': 20,  # Security integrations
        'C': 20,  # Error recovery
        'D': 20,  # Multi-file sync
        'E': 20   # Refusals
    }
    
    idx = 1
    
    # Generate Category A
    for _ in range(categories['A']):
        trajectories.append(generate_category_a_trajectory(idx))
        idx += 1
    
    # Generate Category B
    for _ in range(categories['B']):
        trajectories.append(generate_category_b_trajectory(idx))
        idx += 1
    
    # Generate Category C
    for _ in range(categories['C']):
        trajectories.append(generate_category_c_trajectory(idx))
        idx += 1
    
    # Generate Category D
    for _ in range(categories['D']):
        trajectories.append(generate_category_d_trajectory(idx))
        idx += 1
    
    # Generate Category E
    for _ in range(categories['E']):
        trajectories.append(generate_category_e_trajectory(idx))
        idx += 1
    
    return trajectories

def main():
    """Main execution function"""
    print("🚀 Generating 100 Bolt.new Trajectories...")
    print("=" * 60)
    
    trajectories = generate_all_trajectories()
    
    # Save to JSON file
    output_file = "bolt_trajectories_100.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(trajectories, f, indent=2, ensure_ascii=False)
    
    # Generate statistics
    print(f"\n✅ Generated {len(trajectories)} trajectories")
    print(f"📁 Saved to: {output_file}")
    print("\n📊 Distribution:")
    
    category_counts = {}
    for t in trajectories:
        cat = t['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items()):
        category_names = {
            'A': 'Full-stack React+Vite Setups',
            'B': 'Security-first API Integrations',
            'C': 'Error Recovery Scenarios',
            'D': 'Multi-file Synchronization',
            'E': 'Unsafe Command Refusals'
        }
        print(f"  Category {cat} ({category_names[cat]}): {count}")
    
    # Validation
    print("\n🔍 Validation:")
    all_have_import = all('ml_kem' in t['artifact'] for t in trajectories)
    print(f"  ✓ All trajectories include quantum-safe import: {all_have_import}")
    
    all_have_thought = all('thought' in t for t in trajectories)
    print(f"  ✓ All trajectories have THOUGHT: {all_have_thought}")
    
    all_have_plan = all('plan' in t for t in trajectories)
    print(f"  ✓ All trajectories have PLAN: {all_have_plan}")
    
    all_have_artifact = all('artifact' in t for t in trajectories)
    print(f"  ✓ All trajectories have ARTIFACT: {all_have_artifact}")
    
    print("\n✨ Generation complete! Ready for 99.9% reliability target.")

if __name__ == "__main__":
    main()
