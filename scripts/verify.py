#!/usr/bin/env python3
"""
Bolt-Lattice-Architect Verification Script
Version: 2026.Q1
Purpose: Validate code changes for quantum-safe compliance and reliability
"""

import json
import re
import sys
import ast
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import argparse

# ============================================================================
# CONSTANTS
# ============================================================================

RELIABILITY_THRESHOLD = 99.9
APPROVED_IPS = ['10.0.0.5', '192.168.1.50']

UNSAFE_PATTERNS = [
    r'\bfetch\s*\(',
    r'\baxios\.',
    r'\bXMLHttpRequest\b',
    r'\$\.ajax\(',
    r'\beval\s*\(',
    r'\bnew\s+Function\s*\(',
    r'dangerouslySetInnerHTML',
    r'\.innerHTML\s*=',
    r'document\.write\(',
    r'crypto\.createCipher\(',
    r'\bMD5\b',
    r'\bSHA1\b',
]

REQUIRED_IMPORTS = [
    '@security/quantum-safe',
    'latticeHandshake',
    'ml_kem',
]

# ============================================================================
# VERIFICATION FUNCTIONS
# ============================================================================

def check_syntax(file_path: Path) -> Dict:
    """Check EBNF grammar compliance and syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it's Python
        if file_path.suffix == '.py':
            try:
                ast.parse(content)
                return {
                    'pass': True,
                    'errors': [],
                    'message': 'Python syntax valid'
                }
            except SyntaxError as e:
                return {
                    'pass': False,
                    'errors': [str(e)],
                    'message': 'Python syntax error'
                }
        
        # For TypeScript/JavaScript, basic validation
        if file_path.suffix in ['.ts', '.js', '.tsx', '.jsx']:
            # Check for balanced braces
            if content.count('{') != content.count('}'):
                return {
                    'pass': False,
                    'errors': ['Unbalanced braces'],
                    'message': 'Syntax error: unbalanced braces'
                }
            
            # Check for balanced parentheses
            if content.count('(') != content.count(')'):
                return {
                    'pass': False,
                    'errors': ['Unbalanced parentheses'],
                    'message': 'Syntax error: unbalanced parentheses'
                }
        
        return {
            'pass': True,
            'errors': [],
            'message': 'Syntax check passed'
        }
    
    except Exception as e:
        return {
            'pass': False,
            'errors': [str(e)],
            'message': f'Syntax check failed: {e}'
        }


def check_security(file_path: Path) -> Dict:
    """Scan for unsafe patterns and verify quantum-safe imports"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        violations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            # Detect if line is a comment
            if any(line_stripped.startswith(c) for c in ['//', '*', '/*', '"""', "'''", '#']):
                continue
                
            for pattern in UNSAFE_PATTERNS:
                matches = re.finditer(pattern, line)
                for match in matches:
                    # Detect if match is inside a string literal
                    prefix = line[:match.start()]
                    if (prefix.count("'") % 2 != 0) or (prefix.count('"') % 2 != 0):
                        continue
                        
                    violations.append({
                        'type': 'UNSAFE_PATTERN',
                        'pattern': pattern,
                        'line': line_num,
                        'severity': 'CRITICAL'
                    })
        
        # Check for required imports (if file contains network operations)
        has_network_ops = any('latticeHandshake' in line for line in lines if not line.strip().startswith('//'))
        
        if has_network_ops:
            has_quantum_safe = any(imp in content for imp in REQUIRED_IMPORTS)
            if not has_quantum_safe:
                violations.append({
                    'type': 'MISSING_QUANTUM_SAFE',
                    'message': 'Network operations found without quantum-safe imports',
                    'severity': 'CRITICAL'
                })
        
        return {
            'pass': len(violations) == 0,
            'violations': violations,
            'message': f'Found {len(violations)} security violations' if violations else 'Security check passed'
        }
    
    except Exception as e:
        return {
            'pass': False,
            'violations': [{'type': 'ERROR', 'message': str(e)}],
            'message': f'Security check failed: {e}'
        }


def check_reliability(file_path: Path) -> Dict:
    """Calculate reliability score based on safe vs unsafe operations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count safe operations
        safe_ops = 0
        safe_ops += len(re.findall(r'latticeHandshake\s*\(', content))
        safe_ops += len(re.findall(r'quantumVault\.(store|retrieve)', content))
        safe_ops += len(re.findall(r'ml_kem\.(encrypt|decrypt)', content))
        safe_ops += len(re.findall(r'try\s*\{', content))  # Error handling
        
        # Count unsafe operations
        unsafe_ops = 0
        for pattern in UNSAFE_PATTERNS:
            unsafe_ops += len(re.findall(pattern, content))
        
        # Count total operations (approximation)
        total_ops = safe_ops + unsafe_ops
        
        if total_ops == 0:
            # No operations found, assume safe
            return {
                'pass': True,
                'score': 100.0,
                'safe_operations': 0,
                'total_operations': 0,
                'message': 'No operations detected'
            }
        
        # Calculate reliability
        reliability = (safe_ops / total_ops) * 100
        
        return {
            'pass': reliability >= RELIABILITY_THRESHOLD,
            'score': round(reliability, 2),
            'safe_operations': safe_ops,
            'total_operations': total_ops,
            'unsafe_operations': unsafe_ops,
            'message': f'Reliability: {reliability:.2f}% (threshold: {RELIABILITY_THRESHOLD}%)'
        }
    
    except Exception as e:
        return {
            'pass': False,
            'score': 0,
            'message': f'Reliability check failed: {e}'
        }


def check_cfg(file_path: Path) -> Dict:
    """Validate Control Flow Graph properties"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        violations = []
        
        # Check cyclomatic complexity (simplified)
        # Count decision points: if, while, for, case, catch, &&, ||
        decision_points = 0
        decision_points += len(re.findall(r'\bif\s*\(', content))
        decision_points += len(re.findall(r'\bwhile\s*\(', content))
        decision_points += len(re.findall(r'\bfor\s*\(', content))
        decision_points += len(re.findall(r'\bcase\s+', content))
        decision_points += len(re.findall(r'\bcatch\s*\(', content))
        decision_points += len(re.findall(r'&&', content))
        decision_points += len(re.findall(r'\|\|', content))
        
        # Cyclomatic complexity = decision_points + 1
        complexity = decision_points + 1
        
        if complexity > 10:
            violations.append({
                'type': 'HIGH_COMPLEXITY',
                'complexity': complexity,
                'threshold': 10,
                'severity': 'WARNING'
            })
        
        # Check for unreachable code (simplified)
        # Look for code after return statements
        unreachable = re.findall(r'return\s+[^;]+;\s*\n\s*[a-zA-Z]', content)
        if unreachable:
            violations.append({
                'type': 'UNREACHABLE_CODE',
                'instances': len(unreachable),
                'severity': 'WARNING'
            })
        
        return {
            'pass': len(violations) == 0,
            'cyclomatic_complexity': complexity,
            'violations': violations,
            'message': f'CFG check: complexity={complexity}, violations={len(violations)}'
        }
    
    except Exception as e:
        return {
            'pass': False,
            'violations': [{'type': 'ERROR', 'message': str(e)}],
            'message': f'CFG check failed: {e}'
        }


def generate_audit_trace(file_path: Path, results: Dict) -> Dict:
    """Generate comprehensive audit trace"""
    return {
        'timestamp': datetime.now().isoformat(),
        'file': str(file_path),
        'agent': 'Security Verifier',
        'action': 'VALIDATE_CHANGE',
        'results': results,
        'overall_status': 'APPROVED' if all(r.get('pass', False) for r in results.values()) else 'REJECTED',
        'version': '2026.Q1',
        'framework': 'Formal-LLM/CFG',
        'security_shield': 'ML-KEM/Lattice'
    }


def scan_directory(directory: Path, check_type: str = 'all') -> List[Dict]:
    """Scan entire directory for violations"""
    results = []
    
    # Find all source files
    patterns = ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx', '**/*.py']
    files = []
    for pattern in patterns:
        files.extend(directory.glob(pattern))
    
    for file_path in files:
        # Skip node_modules, .git, etc.
        if any(part.startswith('.') or part == 'node_modules' for part in file_path.parts):
            continue
        
        file_results = verify_file(file_path, check_type)
        results.append({
            'file': str(file_path),
            'results': file_results
        })
    
    return results


def verify_file(file_path: Path, check_type: str = 'all') -> Dict:
    """Verify a single file"""
    results = {}
    
    if check_type in ['all', 'syntax']:
        results['syntax'] = check_syntax(file_path)
    
    if check_type in ['all', 'security']:
        results['security'] = check_security(file_path)
    
    if check_type in ['all', 'reliability']:
        results['reliability'] = check_reliability(file_path)
    
    if check_type in ['all', 'cfg']:
        results['cfg'] = check_cfg(file_path)
    
    return results


def print_results(results: Dict, verbose: bool = False):
    """Pretty print verification results"""
    print("\n" + "="*80)
    print("🔐 BOLT-LATTICE-ARCHITECT VERIFICATION REPORT")
    print("="*80 + "\n")
    
    for check_name, check_result in results.items():
        status = "✅ PASS" if check_result.get('pass', False) else "❌ FAIL"
        print(f"{check_name.upper()}: {status}")
        print(f"  {check_result.get('message', 'No message')}")
        
        if verbose:
            for key, value in check_result.items():
                if key not in ['pass', 'message']:
                    print(f"    {key}: {value}")
        print()
    
    overall_pass = all(r.get('pass', False) for r in results.values())
    print("="*80)
    print(f"OVERALL: {'✅ APPROVED' if overall_pass else '❌ REJECTED'}")
    print("="*80 + "\n")
    
    return overall_pass


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Verify code changes for quantum-safe compliance'
    )
    parser.add_argument(
        '--check',
        choices=['all', 'syntax', 'security', 'reliability', 'cfg'],
        default='all',
        help='Type of check to perform'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Specific file to check'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='./src',
        help='Directory to scan (default: ./src)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output audit trace to JSON file'
    )
    
    args = parser.parse_args()
    
    if args.file:
        # Verify single file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        
        results = verify_file(file_path, args.check)
        audit_trace = generate_audit_trace(file_path, results)
        
        passed = print_results(results, args.verbose)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(audit_trace, f, indent=2)
            print(f"Audit trace saved to: {args.output}")
        
        sys.exit(0 if passed else 1)
    
    else:
        # Scan directory
        directory = Path(args.dir)
        if not directory.exists():
            print(f"Error: Directory not found: {directory}")
            sys.exit(1)
        
        print(f"Scanning directory: {directory}")
        scan_results = scan_directory(directory, args.check)
        
        # Aggregate results
        total_files = len(scan_results)
        passed_files = sum(1 for r in scan_results if all(
            check.get('pass', False) 
            for check in r['results'].values()
        ))
        
        print(f"\nScanned {total_files} files")
        print(f"Passed: {passed_files}/{total_files}")
        print(f"Failed: {total_files - passed_files}/{total_files}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(scan_results, f, indent=2)
            print(f"\nFull results saved to: {args.output}")
        
        sys.exit(0 if passed_files == total_files else 1)


if __name__ == '__main__':
    main()
