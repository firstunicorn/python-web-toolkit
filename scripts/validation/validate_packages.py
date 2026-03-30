"""
Validate package name/path consistency across the monorepo.

This script checks:
1. Package names in root pyproject.toml match actual package names
2. No orphaned references in poetry.lock
3. All referenced paths exist
"""

import os
import re
import sys
from pathlib import Path

try:
    import tomli
except ImportError:
    print("ERROR: tomli library not found. Install with: pip install tomli")
    sys.exit(1)


def main():
    """Run all validation checks."""
    root_dir = Path(__file__).parent.parent.parent
    os.chdir(root_dir)
    
    errors = []
    
    print("=" * 70)
    print("VALIDATING PACKAGE CONSISTENCY")
    print("=" * 70)
    
    # Check 1: Name/path consistency
    errors.extend(check_name_path_consistency())
    
    # Check 2: Orphaned references
    errors.extend(check_orphaned_references())
    
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)
    
    if errors:
        print(f"\n[FAILED] Found {len(errors)} error(s):\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print("\nPlease fix these issues before committing.")
        sys.exit(1)
    else:
        print("\n[PASSED] All package references are valid\n")
        sys.exit(0)


def check_name_path_consistency():
    """Check that package names match their directory structure."""
    errors = []
    
    print("\n[1/2] Checking name/path consistency...")
    
    root_config = tomli.load(open('pyproject.toml', 'rb'))
    dependencies = root_config.get('tool', {}).get('poetry', {}).get('dependencies', {})
    
    for pkg_name, config in dependencies.items():
        if not isinstance(config, dict) or 'path' not in config:
            continue
        
        path = config['path']
        print(f"  Checking: {pkg_name} -> {path}")
        
        # Check if path exists
        if not os.path.exists(path):
            errors.append(f"Package '{pkg_name}' references non-existent path: {path}")
            continue
        
        # Check if package pyproject.toml exists
        pkg_toml_path = os.path.join(path, 'pyproject.toml')
        if not os.path.exists(pkg_toml_path):
            errors.append(f"Missing pyproject.toml in {path}")
            continue
        
        # Verify package name matches
        pkg_config = tomli.load(open(pkg_toml_path, 'rb'))
        
        # Try PEP 621 format first ([project] section)
        actual_name = pkg_config.get('project', {}).get('name')
        
        # Fall back to Poetry format ([tool.poetry] section)
        if not actual_name:
            actual_name = pkg_config.get('tool', {}).get('poetry', {}).get('name')
        
        if not actual_name:
            errors.append(f"Package at {path} has no name defined in pyproject.toml")
            continue
        
        if actual_name != pkg_name:
            errors.append(
                f"Name mismatch: root dependency key is '{pkg_name}' but "
                f"package defines name as '{actual_name}' at {path}"
            )
        else:
            print(f"    [OK] Name matches")
    
    if not errors:
        print("  [OK] All package names match their paths")
    
    return errors


def check_orphaned_references():
    """Check for orphaned package references in poetry.lock."""
    errors = []
    
    print("\n[2/2] Checking for orphaned references in poetry.lock...")
    
    # Get actual packages
    packages_dir = Path('packages')
    if not packages_dir.exists():
        errors.append("packages/ directory not found")
        return errors
    
    actual_packages = {p.name for p in packages_dir.iterdir() if p.is_dir()}
    print(f"  Actual packages: {sorted(actual_packages)}")
    
    # Find references in lock file
    lock_file = Path('poetry.lock')
    if not lock_file.exists():
        errors.append("poetry.lock not found")
        return errors
    
    lock_content = lock_file.read_text(encoding='utf-8')
    referenced_packages = set(re.findall(r'packages/([^/\s"]+)', lock_content))
    
    if referenced_packages:
        print(f"  Lock file references: {sorted(referenced_packages)}")
    
    # Find orphaned references
    orphaned = referenced_packages - actual_packages
    
    if orphaned:
        errors.append(
            f"Lock file references non-existent packages: {', '.join(sorted(orphaned))}"
        )
        print(f"    [ERROR] Found orphaned references: {orphaned}")
    else:
        print("  [OK] No orphaned references found")
    
    return errors


if __name__ == '__main__':
    main()
