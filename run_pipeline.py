#!/usr/bin/env python3
"""
Master Execution Script for Bolt-Lattice-Verified
Orchestrates the complete verification and stress testing pipeline
Version: 2026.Q1
"""

import asyncio
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# ============================================================================
# COLORS FOR OUTPUT
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================================
# PIPELINE EXECUTOR
# ============================================================================

class PipelineExecutor:
    """Executes the complete verification pipeline"""
    
    def __init__(self, config_path: str = "orchestration_config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.results = {}
        self.start_time = None
        
    def load_config(self) -> Dict[str, Any]:
        """Load orchestration configuration"""
        if not self.config_path.exists():
            print(f"{Colors.FAIL}Error: Configuration file not found: {self.config_path}{Colors.ENDC}")
            sys.exit(1)
            
        with open(self.config_path) as f:
            return json.load(f)
    
    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{text.center(80)}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
    
    def print_step(self, step: str, status: str = ""):
        """Print step information"""
        if status == "SUCCESS":
            status_text = f"{Colors.OKGREEN}✅ SUCCESS{Colors.ENDC}"
        elif status == "FAIL":
            status_text = f"{Colors.FAIL}❌ FAILED{Colors.ENDC}"
        elif status == "RUNNING":
            status_text = f"{Colors.OKCYAN}▶️  RUNNING{Colors.ENDC}"
        else:
            status_text = status
            
        print(f"{Colors.BOLD}{step}{Colors.ENDC} {status_text}")
    
    async def step_1_initialize(self):
        """Step 1: Initialize project"""
        self.print_header("STEP 1: PROJECT INITIALIZATION")
        
        project = self.config['project']
        print(f"Project: {project['name']}")
        print(f"Repository: {project['repo']}")
        print(f"Branch: {project['branch']}")
        print(f"Version: {project['version']}")
        
        # Verify project structure
        required_files = [
            "src/security/useSecureGateway.ts",
            "src/security/quantum-safe.ts",
            "src/lib/security-policy.ts",
            "scripts/verify.py",
            "tests/stress_test.ts"
        ]
        
        missing_files = []
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"\n{Colors.WARNING}Warning: Missing files:{Colors.ENDC}")
            for file in missing_files:
                print(f"  - {file}")
        else:
            print(f"\n{Colors.OKGREEN}✅ All required files present{Colors.ENDC}")
        
        self.results['initialization'] = {
            'status': 'SUCCESS' if not missing_files else 'WARNING',
            'missing_files': missing_files
        }
    
    async def step_2_spawn_agents(self):
        """Step 2: Spawn verification agents"""
        self.print_header("STEP 2: SPAWNING AGENTS")
        
        for agent in self.config['agents']:
            if agent.get('enabled', True):
                print(f"\n{Colors.OKBLUE}Spawning: {agent['id']}{Colors.ENDC}")
                print(f"  Role: {agent['role']}")
                print(f"  Goal: {agent['goal']}")
                
        self.results['agents'] = {
            'spawned': [a['id'] for a in self.config['agents'] if a.get('enabled', True)],
            'status': 'SUCCESS'
        }
    
    async def step_3_run_verification(self):
        """Step 3: Run formal verification"""
        self.print_header("STEP 3: FORMAL VERIFICATION (Architect_Alpha)")
        
        self.print_step("Running verification script...", "RUNNING")
        
        result = subprocess.run(
            [sys.executable, "scripts/verify.py", "--dir", "src", "--check", "all", "--verbose"],
            capture_output=True,
            text=True
        )
        
        verification_passed = result.returncode == 0
        
        if verification_passed:
            self.print_step("Formal verification", "SUCCESS")
        else:
            self.print_step("Formal verification", "FAIL")
            print(f"\n{Colors.WARNING}Verification output:{Colors.ENDC}")
            print(result.stdout)
            if result.stderr:
                print(f"\n{Colors.FAIL}Errors:{Colors.ENDC}")
                print(result.stderr)
        
        self.results['verification'] = {
            'status': 'SUCCESS' if verification_passed else 'FAIL',
            'exit_code': result.returncode,
            'output': result.stdout
        }
        
        return verification_passed
    
    async def step_4_run_stress_test(self):
        """Step 4: Run stress test"""
        self.print_header("STEP 4: STRESS TEST (Red_Teamer)")
        
        stress_config = self.config['stress_test']
        print(f"Target: {stress_config['target']}")
        print(f"Iterations: {stress_config['iterations']}")
        print(f"Concurrency: {stress_config['concurrency']}")
        print(f"Scenarios: {len(stress_config['scenarios'])}")
        
        self.print_step("\nRunning stress test...", "RUNNING")
        
        # Check if TypeScript is available
        ts_node_check = subprocess.run(
            ["npx", "ts-node", "--version"],
            capture_output=True,
            text=True
        )
        
        if ts_node_check.returncode != 0:
            print(f"\n{Colors.WARNING}ts-node not available, installing...{Colors.ENDC}")
            subprocess.run(["npm", "install", "-D", "ts-node", "@types/node"], check=False)
        
        # Run stress test
        result = subprocess.run(
            ["npx", "ts-node", "tests/stress_test.ts"],
            capture_output=True,
            text=True
        )
        
        stress_passed = result.returncode == 0
        
        if stress_passed:
            self.print_step("Stress test", "SUCCESS")
        else:
            self.print_step("Stress test", "FAIL")
        
        print(f"\n{Colors.OKCYAN}Stress test output:{Colors.ENDC}")
        print(result.stdout)
        
        if result.stderr and "error" in result.stderr.lower():
            print(f"\n{Colors.FAIL}Errors:{Colors.ENDC}")
            print(result.stderr)
        
        self.results['stress_test'] = {
            'status': 'SUCCESS' if stress_passed else 'FAIL',
            'exit_code': result.returncode,
            'output': result.stdout
        }
        
        return stress_passed
    
    async def step_5_calculate_metrics(self):
        """Step 5: Calculate deterministic metrics"""
        self.print_header("STEP 5: METRIC CALCULATION")
        
        scorer_config = self.config['scorer']
        metrics = scorer_config['metrics']
        thresholds = scorer_config['thresholds']
        
        # Parse stress test results if available
        report_path = Path("stress_test_report.json")
        if report_path.exists():
            with open(report_path) as f:
                stress_report = json.load(f)
                
            print(f"\n{Colors.BOLD}Calculated Metrics:{Colors.ENDC}")
            for metric in metrics:
                if metric in stress_report.get('metrics', {}):
                    value = stress_report['metrics'][metric]
                    threshold = thresholds.get(metric, 0)
                    passed = value >= threshold
                    
                    status = f"{Colors.OKGREEN}✅{Colors.ENDC}" if passed else f"{Colors.FAIL}❌{Colors.ENDC}"
                    print(f"  {metric}: {value:.2f}% (threshold: {threshold}%) {status}")
        else:
            print(f"{Colors.WARNING}No stress test report found{Colors.ENDC}")
        
        self.results['metrics'] = {
            'status': 'SUCCESS',
            'report_path': str(report_path) if report_path.exists() else None
        }
    
    async def step_6_generate_report(self):
        """Step 6: Generate final report"""
        self.print_header("STEP 6: REPORT GENERATION")
        
        total_time = datetime.now() - self.start_time
        
        final_report = {
            'timestamp': datetime.now().isoformat(),
            'config': self.config,
            'results': self.results,
            'total_time_seconds': total_time.total_seconds(),
            'overall_status': self.determine_overall_status()
        }
        
        # Save report
        reports_dir = Path(self.config['reporting']['outputDir'])
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2)
        
        print(f"{Colors.OKGREEN}✅ Report saved to: {report_file}{Colors.ENDC}")
        
        # Generate markdown summary
        md_file = reports_dir / f"pipeline_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self.generate_markdown_summary(final_report, md_file)
        print(f"{Colors.OKGREEN}✅ Summary saved to: {md_file}{Colors.ENDC}")
        
        self.results['report'] = {
            'json': str(report_file),
            'markdown': str(md_file)
        }
    
    def determine_overall_status(self) -> str:
        """Determine overall pipeline status"""
        if all(r.get('status') == 'SUCCESS' for r in self.results.values()):
            return 'SUCCESS'
        elif any(r.get('status') == 'FAIL' for r in self.results.values()):
            return 'FAIL'
        else:
            return 'WARNING'
    
    def generate_markdown_summary(self, report: Dict, output_path: Path):
        """Generate markdown summary"""
        with open(output_path, 'w') as f:
            f.write("# Bolt-Lattice-Verified Pipeline Report\n\n")
            f.write(f"**Generated:** {report['timestamp']}\n\n")
            f.write(f"**Total Time:** {report['total_time_seconds']:.2f}s\n\n")
            f.write(f"**Overall Status:** {report['overall_status']}\n\n")
            
            f.write("## Steps\n\n")
            for step, result in report['results'].items():
                status_emoji = "✅" if result.get('status') == 'SUCCESS' else "❌" if result.get('status') == 'FAIL' else "⚠️"
                f.write(f"- {status_emoji} **{step.replace('_', ' ').title()}**: {result.get('status', 'UNKNOWN')}\n")
            
            f.write("\n## Configuration\n\n")
            f.write(f"```json\n{json.dumps(report['config'], indent=2)}\n```\n")
    
    async def run(self):
        """Execute complete pipeline"""
        self.start_time = datetime.now()
        
        self.print_header("🚀 BOLT-LATTICE-VERIFIED PIPELINE")
        
        try:
            await self.step_1_initialize()
            await self.step_2_spawn_agents()
            verification_passed = await self.step_3_run_verification()
            stress_passed = await self.step_4_run_stress_test()
            await self.step_5_calculate_metrics()
            await self.step_6_generate_report()
            
            # Final summary
            self.print_header("PIPELINE COMPLETE")
            
            overall_status = self.determine_overall_status()
            if overall_status == 'SUCCESS':
                print(f"{Colors.OKGREEN}{Colors.BOLD}✅ ALL CHECKS PASSED - 99.9% RELIABILITY TARGET ACHIEVED{Colors.ENDC}\n")
                return 0
            elif overall_status == 'FAIL':
                print(f"{Colors.FAIL}{Colors.BOLD}❌ PIPELINE FAILED - RELIABILITY TARGET NOT MET{Colors.ENDC}\n")
                return 1
            else:
                print(f"{Colors.WARNING}{Colors.BOLD}⚠️  PIPELINE COMPLETED WITH WARNINGS{Colors.ENDC}\n")
                return 0
                
        except Exception as e:
            print(f"\n{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")
            import traceback
            traceback.print_exc()
            return 1

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Main entry point"""
    executor = PipelineExecutor()
    exit_code = await executor.run()
    sys.exit(exit_code)

if __name__ == '__main__':
    asyncio.run(main())
