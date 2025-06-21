#!/usr/bin/env python3
"""
Test runner for Team Bonding Event Planner
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed with exit code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def check_prerequisites():
    """Check if required services are running."""
    print("🔍 Checking prerequisites...")

    # Check if we're in the right directory
    if not os.path.exists("tests"):
        print("❌ Please run this script from the project root directory")
        return False

    # Check if backend directory exists
    if not os.path.exists("backend"):
        print("❌ Backend directory not found")
        return False

    print("✅ Prerequisites check passed")
    return True


def run_backend_tests():
    """Run backend unit tests."""
    return run_command(
        [sys.executable, "-m", "pytest", "tests/backend/", "-v"],
        "Running Backend Unit Tests",
    )


def run_integration_tests():
    """Run integration tests."""
    return run_command(
        [sys.executable, "-m", "pytest", "tests/integration/", "-v"],
        "Running Integration Tests",
    )


def run_frontend_tests():
    """Run frontend tests."""
    return run_command(
        [sys.executable, "-m", "pytest", "tests/frontend/", "-v"],
        "Running Frontend Tests",
    )


def run_all_tests():
    """Run all tests."""
    return run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v"], "Running All Tests"
    )


def run_with_coverage():
    """Run tests with coverage report."""
    print("\n" + "=" * 60)
    print("📊 Running Tests with Coverage")
    print("=" * 60)

    # Install coverage if not available
    try:
        import coverage
    except ImportError:
        print("📦 Installing coverage...")
        subprocess.run([sys.executable, "-m", "pip", "install", "coverage"], check=True)

    # Run tests with coverage
    cmd = [sys.executable, "-m", "coverage", "run", "-m", "pytest", "tests/", "-v"]

    if run_command(cmd, "Running Tests with Coverage"):
        # Generate coverage report
        print("\n📈 Generating Coverage Report...")
        subprocess.run([sys.executable, "-m", "coverage", "report"])

        # Generate HTML report
        print("\n🌐 Generating HTML Coverage Report...")
        subprocess.run([sys.executable, "-m", "coverage", "html"])
        print("📁 HTML report generated in htmlcov/")
        return True

    return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Test runner for Team Bonding Event Planner"
    )
    parser.add_argument(
        "--type",
        choices=["backend", "integration", "frontend", "all", "coverage"],
        default="all",
        help="Type of tests to run",
    )
    parser.add_argument("--file", help="Run specific test file")

    args = parser.parse_args()

    print("🧪 Team Bonding Event Planner - Test Runner")
    print("=" * 60)

    if not check_prerequisites():
        sys.exit(1)

    success = True

    if args.file:
        # Run specific test file
        test_file = Path(args.file)
        if test_file.exists():
            success = run_command(
                [sys.executable, "-m", "pytest", str(test_file), "-v"],
                f"Running Test File: {test_file}",
            )
        else:
            print(f"❌ Test file not found: {test_file}")
            success = False
    else:
        # Run tests by type
        if args.type == "backend":
            success = run_backend_tests()
        elif args.type == "integration":
            success = run_integration_tests()
        elif args.type == "frontend":
            success = run_frontend_tests()
        elif args.type == "coverage":
            success = run_with_coverage()
        else:  # all
            success = run_all_tests()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
