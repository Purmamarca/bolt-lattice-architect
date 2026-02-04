#!/usr/bin/env python3
"""
Lattice Audit Trace Generator
Generates comprehensive audit traces for all operations
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# ============================================================================
# TRACE GENERATOR CLASS
# ============================================================================

class LatticeTraceGenerator:
    def __init__(self, output_file: str = 'lattice_audit.trace'):
        self.output_file = output_file
        self.traces: List[Dict] = []
        self.session_id = self.generate_session_id()
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]
    
    def add_trace(
        self,
        agent: str,
        action: str,
        details: Dict[str, Any],
        status: str = 'SUCCESS'
    ):
        """Add a trace entry"""
        trace = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'agent': agent,
            'action': action,
            'status': status,
            'details': details,
            'version': '2026.Q1',
            'framework': 'Formal-LLM/CFG',
            'security_shield': 'ML-KEM/Lattice'
        }
        
        self.traces.append(trace)
    
    def add_network_scan(self, scan_results: Dict):
        """Add network scan trace"""
        self.add_trace(
            agent='Builder',
            action='SCAN_NETWORK',
            details={
                'scanned_directory': scan_results.get('scanned_directory'),
                'total_findings': scan_results.get('total_findings'),
                'summary': scan_results.get('summary'),
                'findings': scan_results.get('findings', [])[:5]  # First 5 findings
            },
            status='COMPLETED'
        )
    
    def add_refactor(self, file_path: str, changes: List[Dict]):
        """Add refactoring trace"""
        self.add_trace(
            agent='Builder',
            action='REFACTOR',
            details={
                'file': file_path,
                'changes': changes,
                'quantum_safe': True
            },
            status='COMPLETED'
        )
    
    def add_validation(self, validation_results: Dict):
        """Add validation trace"""
        overall_pass = all(
            result.get('pass', False) 
            for result in validation_results.values()
        )
        
        self.add_trace(
            agent='Architect',
            action='VALIDATE_CHANGE',
            details={
                'checks': validation_results,
                'reliability_score': validation_results.get('reliability', {}).get('score'),
                'security_violations': validation_results.get('security', {}).get('violations', []),
                'cfg_complexity': validation_results.get('cfg', {}).get('cyclomatic_complexity')
            },
            status='APPROVED' if overall_pass else 'REJECTED'
        )
    
    def add_security_check(self, file_path: str, security_results: Dict):
        """Add security check trace"""
        self.add_trace(
            agent='Architect',
            action='SECURITY_CHECK',
            details={
                'file': file_path,
                'violations': security_results.get('violations', []),
                'quantum_safe_imports': security_results.get('quantum_safe_imports', False),
                'ml_kem_768': security_results.get('ml_kem_768', False)
            },
            status='PASS' if security_results.get('pass', False) else 'FAIL'
        )
    
    def add_reliability_check(self, file_path: str, reliability_results: Dict):
        """Add reliability check trace"""
        self.add_trace(
            agent='Architect',
            action='RELIABILITY_CHECK',
            details={
                'file': file_path,
                'score': reliability_results.get('score'),
                'threshold': 99.9,
                'safe_operations': reliability_results.get('safe_operations'),
                'total_operations': reliability_results.get('total_operations'),
                'unsafe_operations': reliability_results.get('unsafe_operations')
            },
            status='PASS' if reliability_results.get('pass', False) else 'FAIL'
        )
    
    def add_handshake(self, url: str, method: str, encryption: str):
        """Add lattice handshake trace"""
        self.add_trace(
            agent='LatticeShield',
            action='HANDSHAKE',
            details={
                'url': url,
                'method': method,
                'encryption': encryption,
                'quantum_safe': True
            },
            status='SUCCESS'
        )
    
    def add_encryption(self, operation: str, algorithm: str, data_size: int):
        """Add encryption operation trace"""
        self.add_trace(
            agent='ML-KEM',
            action=operation,
            details={
                'algorithm': algorithm,
                'data_size_bytes': data_size,
                'lattice_level': 5
            },
            status='SUCCESS'
        )
    
    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        total_traces = len(self.traces)
        
        # Count by agent
        agents = {}
        for trace in self.traces:
            agent = trace['agent']
            agents[agent] = agents.get(agent, 0) + 1
        
        # Count by action
        actions = {}
        for trace in self.traces:
            action = trace['action']
            actions[action] = actions.get(action, 0) + 1
        
        # Count by status
        statuses = {}
        for trace in self.traces:
            status = trace['status']
            statuses[status] = statuses.get(status, 0) + 1
        
        return {
            'session_id': self.session_id,
            'total_traces': total_traces,
            'agents': agents,
            'actions': actions,
            'statuses': statuses,
            'start_time': self.traces[0]['timestamp'] if self.traces else None,
            'end_time': self.traces[-1]['timestamp'] if self.traces else None
        }
    
    def save(self):
        """Save traces to file"""
        output = {
            'metadata': {
                'version': '2026.Q1',
                'framework': 'Formal-LLM/CFG',
                'security_shield': 'ML-KEM/Lattice',
                'generated_at': datetime.now().isoformat()
            },
            'summary': self.generate_summary(),
            'traces': self.traces
        }
        
        with open(self.output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Audit trace saved to: {self.output_file}")
        print(f"   Total traces: {len(self.traces)}")
        print(f"   Session ID: {self.session_id}")
    
    def print_summary(self):
        """Print summary to console"""
        summary = self.generate_summary()
        
        print("\n" + "="*80)
        print("📊 LATTICE AUDIT TRACE SUMMARY")
        print("="*80 + "\n")
        
        print(f"Session ID: {summary['session_id']}")
        print(f"Total Traces: {summary['total_traces']}")
        print(f"Start Time: {summary['start_time']}")
        print(f"End Time: {summary['end_time']}")
        
        print("\n📌 Agents:")
        for agent, count in summary['agents'].items():
            print(f"  {agent}: {count}")
        
        print("\n📌 Actions:")
        for action, count in summary['actions'].items():
            print(f"  {action}: {count}")
        
        print("\n📌 Statuses:")
        for status, count in summary['statuses'].items():
            print(f"  {status}: {count}")
        
        print("\n" + "="*80 + "\n")

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_workflow():
    """Example workflow demonstrating trace generation"""
    tracer = LatticeTraceGenerator()
    
    # Step 1: Network scan
    tracer.add_network_scan({
        'scanned_directory': './src',
        'total_findings': 5,
        'summary': {'critical': 0, 'high': 5},
        'findings': [
            {'file': 'src/api/users.ts', 'pattern': 'fetch', 'line': 42}
        ]
    })
    
    # Step 2: Refactor
    tracer.add_refactor(
        'src/api/users.ts',
        [
            {
                'line': 42,
                'before': 'fetch(url)',
                'after': 'latticeHandshake({ url, method: "GET", encryption: "ML-KEM-768" })'
            }
        ]
    )
    
    # Step 3: Validation
    tracer.add_validation({
        'syntax': {'pass': True},
        'security': {'pass': True, 'violations': []},
        'reliability': {'pass': True, 'score': 99.95},
        'cfg': {'pass': True, 'cyclomatic_complexity': 5}
    })
    
    # Step 4: Security check
    tracer.add_security_check('src/api/users.ts', {
        'pass': True,
        'violations': [],
        'quantum_safe_imports': True,
        'ml_kem_768': True
    })
    
    # Step 5: Reliability check
    tracer.add_reliability_check('src/api/users.ts', {
        'pass': True,
        'score': 99.95,
        'safe_operations': 10,
        'total_operations': 10,
        'unsafe_operations': 0
    })
    
    # Step 6: Handshake
    tracer.add_handshake('/api/users', 'GET', 'ML-KEM-768')
    
    # Step 7: Encryption
    tracer.add_encryption('ENCRYPT', 'ML-KEM-768', 1024)
    
    # Save and print
    tracer.print_summary()
    tracer.save()

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate lattice audit trace'
    )
    parser.add_argument(
        '--example',
        action='store_true',
        help='Run example workflow'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='lattice_audit.trace',
        help='Output trace file'
    )
    
    args = parser.parse_args()
    
    if args.example:
        example_workflow()
    else:
        print("Use --example to run example workflow")
        print("Or import LatticeTraceGenerator in your code")

if __name__ == '__main__':
    main()
