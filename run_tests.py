#!/usr/bin/env python3
"""
Test runner for Jira Spec Sheet Sync
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Run tests for Jira Spec Sheet Sync")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--pattern", "-k", help="Run tests matching pattern")
    parser.add_argument("--file", "-f", help="Run specific test file")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies first")
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Install dependencies if requested
    if args.install_deps:
        print("📦 Installing test dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return 1
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.coverage:
        cmd.extend(["--cov=utils", "--cov=spec-sheet", "--cov-report=html", "--cov-report=term"])
    
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    
    if args.pattern:
        cmd.extend(["-k", args.pattern])
    
    if args.file:
        cmd.append(f"tests/{args.file}")
    else:
        cmd.append("tests/")
    
    print(f"🧪 Running tests: {' '.join(cmd[2:])}")
    print("=" * 60)
    
    try:
        # Run tests
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("🎉 All tests passed!")
            
            if args.coverage:
                print("📊 Coverage report generated in htmlcov/index.html")
        else:
            print("\n" + "=" * 60)
            print("❌ Some tests failed!")
            
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Install it with: pip install pytest")
        print("   Or run with --install-deps to install automatically")
        return 1
    except KeyboardInterrupt:
        print("\n⏹️  Tests cancelled by user")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 