#!/usr/bin/env python3
"""
Network Call Scanner - Builder Agent
Scans source code for legacy network calls and suggests quantum-safe refactoring
"""

import re
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# ============================================================================
# LEGACY PATTERNS TO DETECT
# ============================================================================

LEGACY_PATTERNS = {
    'fetch': {
        'pattern': r'\bfetch\s*\(',
        'description': 'Legacy fetch() call',
        'replacement': 'latticeHandshake()',
        'severity': 'HIGH'
    },
    'axios': {
        'pattern': r'\baxios\.(get|post|put|delete|patch)',
        'description': 'Axios HTTP call',
        'replacement': 'latticeHandshake()',
        'severity': 'HIGH'
    },
    'XMLHttpRequest': {
        'pattern': r'\bnew\s+XMLHttpRequest\s*\(',
        'description': 'XMLHttpRequest usage',
        'replacement': 'latticeHandshake()',
        'severity': 'CRITICAL'
    },
    'jquery_ajax': {
        'pattern': r'\$\.ajax\s*\(',
        'description': 'jQuery AJAX call',
        'replacement': 'latticeHandshake()',
        'severity': 'HIGH'
    },
    'http_module': {
        'pattern': r'(http|https)\.request\s*\(',
        'description': 'Node.js HTTP module',
        'replacement': 'latticeHandshake()',
        'severity': 'HIGH'
    }
}

# ============================================================================
# SCANNER CLASS
# ============================================================================

class NetworkScanner:
    def __init__(self, root_dir: str = './src'):
        self.root_dir = Path(root_dir)
        self.findings: List[Dict] = []
    
    def scan(self) -> List[Dict]:
        """Scan all source files for legacy network calls"""
        print(f"🔍 Scanning directory: {self.root_dir}")
        
        # Find all source files
        patterns = ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx']
        files = []
        for pattern in patterns:
            files.extend(self.root_dir.glob(pattern))
        
        print(f"Found {len(files)} source files\n")
        
        for file_path in files:
            # Skip node_modules, .git, etc.
            if any(part.startswith('.') or part == 'node_modules' for part in file_path.parts):
                continue
            
            self.scan_file(file_path)
        
        return self.findings
    
    def scan_file(self, file_path: Path):
        """Scan a single file for legacy patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern_name, pattern_info in LEGACY_PATTERNS.items():
                matches = re.finditer(pattern_info['pattern'], content, re.MULTILINE)
                
                for match in matches:
                    # Find line number
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line_end = content.find('\n', match.start())
                    if line_end == -1: line_end = len(content)
                    line_content = content[line_start:line_end].strip()
                    
                    # Skip if the match is in a comment or string
                    line_prefix = content[line_start:match.start()]
                    is_comment = any(comment_char in line_prefix for comment_char in ['//', '*', '/*'])
                    
                    # Simple quote check: count quotes on the same line
                    # Note: This is an approximation
                    is_string = (line_prefix.count("'") % 2 != 0) or (line_prefix.count('"') % 2 != 0)
                    
                    if is_comment or is_string:
                        continue
                    
                    line_num = content[:match.start()].count('\n') + 1
                    
                    finding = {
                        'file': str(file_path.relative_to(self.root_dir.parent)),
                        'line': line_num,
                        'pattern': pattern_name,
                        'description': pattern_info['description'],
                        'severity': pattern_info['severity'],
                        'code': line_content,
                        'replacement': pattern_info['replacement'],
                        'suggestion': self.generate_suggestion(line_content, pattern_name)
                    }
                    
                    self.findings.append(finding)
        
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
    
    def generate_suggestion(self, code: str, pattern_name: str) -> str:
        """Generate refactoring suggestion"""
        if 'fetch' in pattern_name:
            return self.suggest_fetch_refactor(code)
        elif 'axios' in pattern_name:
            return self.suggest_axios_refactor(code)
        else:
            return "Replace with latticeHandshake() from '@security/quantum-safe'"
    
    def suggest_fetch_refactor(self, code: str) -> str:
        """Suggest fetch() refactoring"""
        # Extract URL if possible
        url_match = re.search(r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]', code)
        url = url_match.group(1) if url_match else 'YOUR_URL'
        
        return f"""
// Before:
{code}

// After:
import {{ latticeHandshake }} from '@security/quantum-safe';

const response = await latticeHandshake({{
  url: '{url}',
  method: 'GET',
  encryption: 'ML-KEM-768'
}});
"""
    
    def suggest_axios_refactor(self, code: str) -> str:
        """Suggest axios refactoring"""
        # Extract method
        method_match = re.search(r'axios\.(get|post|put|delete|patch)', code)
        method = method_match.group(1).upper() if method_match else 'GET'
        
        return f"""
// Before:
{code}

// After:
import {{ latticeHandshake }} from '@security/quantum-safe';

const response = await latticeHandshake({{
  url: YOUR_URL,
  method: '{method}',
  encryption: 'ML-KEM-768'
}});
"""
    
    def print_report(self):
        """Print formatted report"""
        if not self.findings:
            print("✅ No legacy network calls found!")
            return
        
        print("\n" + "="*80)
        print("🚨 LEGACY NETWORK CALLS DETECTED")
        print("="*80 + "\n")
        
        # Group by severity
        critical = [f for f in self.findings if f['severity'] == 'CRITICAL']
        high = [f for f in self.findings if f['severity'] == 'HIGH']
        
        if critical:
            print(f"🔴 CRITICAL: {len(critical)} findings")
            for finding in critical:
                self.print_finding(finding)
        
        if high:
            print(f"🟡 HIGH: {len(high)} findings")
            for finding in high:
                self.print_finding(finding)
        
        print("\n" + "="*80)
        print(f"TOTAL: {len(self.findings)} legacy network calls found")
        print("="*80 + "\n")
        
        print("📋 RECOMMENDED ACTION:")
        print("  1. Review each finding")
        print("  2. Replace with latticeHandshake() from '@security/quantum-safe'")
        print("  3. Run verification: python3 ./scripts/verify.py")
        print()
    
    def print_finding(self, finding: Dict):
        """Print a single finding"""
        print(f"\n  File: {finding['file']}:{finding['line']}")
        print(f"  Pattern: {finding['description']}")
        print(f"  Code: {finding['code']}")
        print(f"  Suggestion: {finding['suggestion']}")
    
    def save_report(self, output_path: str = 'network_scan_report.json'):
        """Save report to JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'scanned_directory': str(self.root_dir),
            'total_findings': len(self.findings),
            'findings': self.findings,
            'summary': {
                'critical': len([f for f in self.findings if f['severity'] == 'CRITICAL']),
                'high': len([f for f in self.findings if f['severity'] == 'HIGH'])
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {output_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    import sys
    
    # Force UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(
        description='Scan for legacy network calls and suggest quantum-safe refactoring'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='./src',
        help='Directory to scan (default: ./src)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='network_scan_report.json',
        help='Output JSON report path'
    )
    
    args = parser.parse_args()
    
    scanner = NetworkScanner(args.dir)
    scanner.scan()
    scanner.print_report()
    scanner.save_report(args.output)

if __name__ == '__main__':
    main()
