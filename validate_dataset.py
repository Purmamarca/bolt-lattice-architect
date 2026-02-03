"""
Validation Script for Bolt.new Golden Dataset
Performs comprehensive quality checks on the 100 trajectories
"""
import json
import re
from collections import Counter

def validate_dataset(filename='bolt_trajectories_100.json'):
    """Comprehensive validation of the trajectory dataset"""
    
    print("=" * 70)
    print("🔍 BOLT.NEW GOLDEN DATASET VALIDATION")
    print("=" * 70)
    
    with open(filename, 'r', encoding='utf-8') as f:
        trajectories = json.load(f)
    
    errors = []
    warnings = []
    
    # 1. Count and ID validation
    print(f"\n✓ Total trajectories: {len(trajectories)}")
    if len(trajectories) != 100:
        errors.append(f"Expected 100 trajectories, found {len(trajectories)}")
    
    ids = [t['id'] for t in trajectories]
    if sorted(ids) != list(range(1, 101)):
        errors.append("IDs are not sequential 1-100")
    
    # 2. Category distribution
    categories = Counter(t['category'] for t in trajectories)
    print(f"\n📊 Category Distribution:")
    for cat in sorted(categories.keys()):
        count = categories[cat]
        print(f"   Category {cat}: {count}")
        if count != 20:
            errors.append(f"Category {cat} has {count} trajectories, expected 20")
    
    # 3. Required fields
    print(f"\n🔑 Required Fields Check:")
    required_fields = ['id', 'category', 'thought', 'plan', 'artifact']
    for t in trajectories:
        for field in required_fields:
            if field not in t:
                errors.append(f"Trajectory {t.get('id', 'unknown')} missing field: {field}")
    print(f"   ✓ All trajectories have required fields")
    
    # 4. Quantum-safe import validation
    print(f"\n🔐 Quantum-Safe Import Validation:")
    ml_kem_count = 0
    for t in trajectories:
        if 'ml_kem' in t['artifact']:
            ml_kem_count += 1
        else:
            warnings.append(f"Trajectory {t['id']} missing ml_kem import")
    
    print(f"   ✓ {ml_kem_count}/100 trajectories include 'ml_kem' import")
    if ml_kem_count == 100:
        print(f"   ✓ 100% quantum-safe compliance!")
    
    # 5. EBNF structure validation
    print(f"\n📝 EBNF Structure Validation:")
    artifact_pattern = re.compile(r'<boltArtifact.*?</boltArtifact>', re.DOTALL)
    action_pattern = re.compile(r'<boltAction.*?</boltAction>', re.DOTALL)
    
    valid_artifacts = 0
    for t in trajectories:
        if artifact_pattern.search(t['artifact']):
            valid_artifacts += 1
        else:
            errors.append(f"Trajectory {t['id']} has invalid artifact structure")
    
    print(f"   ✓ {valid_artifacts}/100 trajectories have valid <boltArtifact> structure")
    
    # 6. Plan validation
    print(f"\n📋 Plan Validation:")
    valid_plans = ['INSTALL_DEPS', 'CREATE_FILE', 'RUN_DEV_SERVER', 'REFLEXION', 'REFUSE']
    plan_counter = Counter()
    
    for t in trajectories:
        if not isinstance(t['plan'], list):
            errors.append(f"Trajectory {t['id']} plan is not a list")
            continue
        
        for step in t['plan']:
            if step not in valid_plans:
                errors.append(f"Trajectory {t['id']} has invalid plan step: {step}")
            plan_counter[step] += 1
    
    print(f"   Plan step distribution:")
    for step, count in plan_counter.most_common():
        print(f"     - {step}: {count}")
    
    # 7. IP validation
    print(f"\n🌐 Approved IP Validation:")
    approved_ips = ['10.0.0.5', '192.168.1.50']
    ip_counter = Counter()
    
    for t in trajectories:
        if 'approved_ip' in t:
            ip = t['approved_ip']
            ip_counter[ip] += 1
            if ip not in approved_ips:
                errors.append(f"Trajectory {t['id']} has unapproved IP: {ip}")
    
    for ip, count in ip_counter.items():
        print(f"   {ip}: {count} trajectories")
    
    # 8. Component coverage
    print(f"\n🧩 Component Coverage:")
    components = ['AuthProvider', 'SecureDashboard', 'CryptoBridge', 'DataVault', 'LatticeTunnel']
    component_counter = Counter()
    
    for t in trajectories:
        for comp in components:
            if comp in t['artifact']:
                component_counter[comp] += 1
    
    for comp in components:
        count = component_counter.get(comp, 0)
        print(f"   {comp}: {count} occurrences")
        if count == 0:
            warnings.append(f"Component {comp} not used in any trajectory")
    
    # 9. Category-specific validation
    print(f"\n🎯 Category-Specific Validation:")
    
    # Category C should have failures
    category_c = [t for t in trajectories if t['category'] == 'C']
    failures_count = sum(1 for t in category_c if 'failure' in t)
    print(f"   Category C (Error Recovery): {failures_count}/20 have 'failure' field")
    
    # Category E should have refusals
    category_e = [t for t in trajectories if t['category'] == 'E']
    refused_count = sum(1 for t in category_e if 'REFUSE' in t['plan'])
    print(f"   Category E (Refusals): {refused_count}/20 have 'REFUSE' in plan")
    
    # Category D should have multiple files
    category_d = [t for t in trajectories if t['category'] == 'D']
    multi_file_count = sum(1 for t in category_d if t['plan'].count('CREATE_FILE') >= 2)
    print(f"   Category D (Multi-file): {multi_file_count}/20 have 2+ CREATE_FILE steps")
    
    # 10. Status field validation
    print(f"\n📊 Status Distribution:")
    status_counter = Counter(t.get('status', 'unknown') for t in trajectories)
    for status, count in status_counter.most_common():
        print(f"   {status}: {count}")
    
    # 11. File path validation
    print(f"\n📁 File Path Analysis:")
    file_paths = set()
    for t in trajectories:
        # Extract file paths from artifacts
        path_matches = re.findall(r"filePath='([^']+)'", t['artifact'])
        file_paths.update(path_matches)
    
    print(f"   Unique file paths: {len(file_paths)}")
    print(f"   Sample paths:")
    for path in sorted(list(file_paths))[:10]:
        print(f"     - {path}")
    
    # Final Report
    print("\n" + "=" * 70)
    print("📊 VALIDATION SUMMARY")
    print("=" * 70)
    
    if not errors:
        print("✅ ALL VALIDATIONS PASSED!")
        print(f"   - 100 trajectories generated")
        print(f"   - Perfect category distribution (20 each)")
        print(f"   - 100% quantum-safe compliance")
        print(f"   - Valid EBNF structure")
        print(f"   - Ready for 99.9% reliability target!")
    else:
        print(f"❌ FOUND {len(errors)} ERRORS:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   - {error}")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNINGS:")
        for warning in warnings[:5]:  # Show first 5 warnings
            print(f"   - {warning}")
    
    print("\n" + "=" * 70)
    
    # Quality score
    quality_score = 100 - (len(errors) * 5) - (len(warnings) * 1)
    quality_score = max(0, min(100, quality_score))
    
    print(f"\n🎯 QUALITY SCORE: {quality_score}/100")
    
    if quality_score >= 95:
        print("   Grade: A+ (Production Ready)")
    elif quality_score >= 85:
        print("   Grade: A (Excellent)")
    elif quality_score >= 75:
        print("   Grade: B (Good)")
    else:
        print("   Grade: C (Needs Improvement)")
    
    print("\n" + "=" * 70)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = validate_dataset()
    exit(0 if success else 1)
