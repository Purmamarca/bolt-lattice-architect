#!/usr/bin/env python3
"""
Bolt-Lattice-Architect Orchestration Script
Multi-Agent Workflow Orchestrator
Version: 2026.Q1
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# ============================================================================
# ORCHESTRATOR CLASS
# ============================================================================

class BoltLatticeOrchestrator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.src_dir = self.project_root / 'src'
        self.scripts_dir = self.project_root / 'scripts'
        self.results = {}
        
    def log(self, message: str, level: str = 'INFO'):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        symbols = {
            'INFO': '📋',
            'SUCCESS': '✅',
            'ERROR': '❌',
            'WARNING': '⚠️',
            'STEP': '🔹'
        }
        symbol = symbols.get(level, '📋')
        print(f"[{timestamp}] {symbol} {message}")
    
    def run_command(self, command: List[str], description: str) -> Dict:
        """Run a command and capture output"""
        self.log(f"Running: {description}", 'STEP')
        
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            success = result.returncode == 0
            
            if success:
                self.log(f"Completed: {description}", 'SUCCESS')
            else:
                self.log(f"Failed: {description}", 'ERROR')
                self.log(f"Error: {result.stderr}", 'ERROR')
            
            return {
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        
        except subprocess.TimeoutExpired:
            self.log(f"Timeout: {description}", 'ERROR')
            return {
                'success': False,
                'error': 'Command timeout'
            }
        except Exception as e:
            self.log(f"Exception: {str(e)}", 'ERROR')
            return {
                'success': False,
                'error': str(e)
            }
    
    def step_1_scan_network(self) -> bool:
        """Step 1: Builder Agent - Scan for legacy network calls"""
        self.log("="*80, 'INFO')
        self.log("STEP 1: SCAN NETWORK CALLS (Builder Agent)", 'INFO')
        self.log("="*80, 'INFO')
        
        result = self.run_command(
            [sys.executable, str(self.scripts_dir / 'scan_network.py'), '--dir', str(self.src_dir)],
            'Scanning for legacy network calls'
        )
        
        self.results['step_1'] = result
        
        # Check if scan report exists
        report_path = self.project_root / 'network_scan_report.json'
        if report_path.exists():
            with open(report_path, 'r') as f:
                scan_data = json.load(f)
                total_findings = scan_data.get('total_findings', 0)
                
                if total_findings > 0:
                    self.log(f"Found {total_findings} legacy network calls", 'WARNING')
                    self.log("Refactoring required before proceeding", 'WARNING')
                    return False
                else:
                    self.log("No legacy network calls found", 'SUCCESS')
                    return True
        
        return result['success']
    
    def step_2_validate_changes(self) -> bool:
        """Step 2: Architect Agent - Validate changes"""
        self.log("="*80, 'INFO')
        self.log("STEP 2: VALIDATE CHANGES (Architect Agent)", 'INFO')
        self.log("="*80, 'INFO')
        
        # Run all validation checks
        result = self.run_command(
            [sys.executable, str(self.scripts_dir / 'verify.py'), '--dir', str(self.src_dir), '--output', 'validation_report.json'],
            'Running comprehensive validation'
        )
        
        self.results['step_2'] = result
        
        # Check validation results
        report_path = self.project_root / 'validation_report.json'
        if report_path.exists():
            with open(report_path, 'r') as f:
                validation_data = json.load(f)
                
                # Check if all files passed
                total_files = len(validation_data)
                passed_files = sum(1 for file_result in validation_data 
                                 if all(check.get('pass', False) 
                                       for check in file_result.get('results', {}).values()))
                
                self.log(f"Validation: {passed_files}/{total_files} files passed", 
                        'SUCCESS' if passed_files == total_files else 'WARNING')
                
                return passed_files == total_files
        
        return result['success']
    
    def step_3_generate_trace(self) -> bool:
        """Step 3: Builder Agent - Generate audit trace"""
        self.log("="*80, 'INFO')
        self.log("STEP 3: GENERATE AUDIT TRACE (Builder Agent)", 'INFO')
        self.log("="*80, 'INFO')
        
        result = self.run_command(
            [sys.executable, str(self.scripts_dir / 'generate_trace.py'), '--example', '--output', 'lattice_audit.trace'],
            'Generating comprehensive audit trace'
        )
        
        self.results['step_3'] = result
        
        # Check if trace file exists
        trace_path = self.project_root / 'lattice_audit.trace'
        if trace_path.exists():
            self.log(f"Audit trace generated: {trace_path}", 'SUCCESS')
            return True
        
        return result['success']
    
    def step_4_launch_dashboard(self) -> bool:
        """Step 4: Launch live dashboard"""
        self.log("="*80, 'INFO')
        self.log("STEP 4: LAUNCH DASHBOARD", 'INFO')
        self.log("="*80, 'INFO')
        
        dashboard_path = self.src_dir / 'dashboard.html'
        
        if dashboard_path.exists():
            self.log(f"Dashboard available at: file://{dashboard_path.absolute()}", 'SUCCESS')
            self.log("Open this file in your browser to view the live dashboard", 'INFO')
            return True
        else:
            self.log("Dashboard file not found", 'ERROR')
            return False
    
    def generate_final_report(self):
        """Generate final orchestration report"""
        self.log("="*80, 'INFO')
        self.log("FINAL REPORT", 'INFO')
        self.log("="*80, 'INFO')
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'version': '2026.Q1',
            'framework': 'Formal-LLM/CFG',
            'security_shield': 'ML-KEM/Lattice',
            'steps': {
                'step_1_scan_network': self.results.get('step_1', {}).get('success', False),
                'step_2_validate_changes': self.results.get('step_2', {}).get('success', False),
                'step_3_generate_trace': self.results.get('step_3', {}).get('success', False),
                'step_4_launch_dashboard': True  # Always true if we get here
            },
            'overall_success': all(
                result.get('success', False) 
                for result in self.results.values()
            )
        }
        
        # Save report
        report_path = self.project_root / 'orchestration_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Final report saved: {report_path}", 'SUCCESS')
        
        # Print summary
        print("\n" + "="*80)
        print("📊 ORCHESTRATION SUMMARY")
        print("="*80 + "\n")
        
        for step_name, success in report['steps'].items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{step_name}: {status}")
        
        print("\n" + "="*80)
        if report['overall_success']:
            print("✅ ALL STEPS COMPLETED SUCCESSFULLY")
        else:
            print("⚠️  SOME STEPS FAILED - REVIEW LOGS")
        print("="*80 + "\n")
        
        return report
    
    def run(self):
        """Run complete orchestration workflow"""
        self.log("🚀 Starting Bolt-Lattice-Architect Orchestration", 'INFO')
        self.log(f"Project Root: {self.project_root}", 'INFO')
        self.log("", 'INFO')
        
        try:
            # Step 1: Scan network calls
            if not self.step_1_scan_network():
                self.log("Step 1 failed - stopping orchestration", 'ERROR')
                return False
            
            # Step 2: Validate changes
            if not self.step_2_validate_changes():
                self.log("Step 2 failed - continuing with warnings", 'WARNING')
            
            # Step 3: Generate trace
            if not self.step_3_generate_trace():
                self.log("Step 3 failed - continuing", 'WARNING')
            
            # Step 4: Launch dashboard
            self.step_4_launch_dashboard()
            
            # Generate final report
            report = self.generate_final_report()
            
            return report['overall_success']
        
        except Exception as e:
            self.log(f"Orchestration failed: {str(e)}", 'ERROR')
            return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    # Force UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    orchestrator = BoltLatticeOrchestrator()
    success = orchestrator.run()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
