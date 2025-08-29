#!/usr/bin/env python3
"""
Test runner script for Playwright automation framework.

This script provides an easy way to run tests with common configurations.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🚀 {description}")
    print(f"Command: {' '.join(command)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, check=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def install_dependencies() -> bool:
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Install Python packages
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      "Installing Python packages"):
        return False
    
    # Install Playwright browsers
    if not run_command([sys.executable, "-m", "playwright", "install"], 
                      "Installing Playwright browsers"):
        return False
    
    return True


def setup_environment():
    """Set up environment files."""
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            import shutil
            shutil.copy("env.example", ".env")
            print("✅ Created .env file from env.example")
        else:
            print("⚠️  No env.example file found")


def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Playwright Test Runner")
    
    # Test selection
    parser.add_argument("--ui", action="store_true", help="Run UI tests only")
    parser.add_argument("--api", action="store_true", help="Run API tests only") 
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--regression", action="store_true", help="Run regression tests")
    
    # Browser options
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                       default="chromium", help="Browser to use")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    
    # Execution options
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--install", action="store_true", help="Install dependencies before running")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML report")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")
    
    # Advanced options
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--video", action="store_true", help="Record videos")
    parser.add_argument("--test-file", help="Run specific test file")
    parser.add_argument("--test-pattern", "-k", help="Run tests matching pattern")
    
    args = parser.parse_args()
    
    # Create reports directory
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    
    # Install dependencies if requested
    if args.install:
        if not install_dependencies():
            sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Test selection
    if args.ui:
        cmd.extend(["-m", "ui"])
    elif args.api:
        cmd.extend(["-m", "api"])
    elif args.smoke:
        cmd.extend(["-m", "smoke"])
    elif args.regression:
        cmd.extend(["-m", "regression"])
    
    # Specific test file
    if args.test_file:
        cmd.append(args.test_file)
    
    # Test pattern
    if args.test_pattern:
        cmd.extend(["-k", args.test_pattern])
    
    # Browser options
    cmd.extend(["--browser", args.browser])
    if args.headed:
        cmd.append("--headed")
    
    # Parallel execution
    if args.parallel:
        cmd.extend(["-n", "auto"])
    
    # Debug mode
    if args.debug:
        cmd.extend(["-s", "-v", "--tb=short"])
        
    # Video recording
    if args.video:
        os.environ["RECORD_VIDEOS"] = "true"
    
    # Reports
    if args.html_report:
        cmd.extend(["--html=reports/html_report.html", "--self-contained-html"])
    
    if args.allure:
        cmd.extend(["--alluredir=reports/allure-results"])
    
    # Default options
    cmd.extend(["--verbose", "--tb=short"])
    
    # Run the tests
    print(f"\n🎭 Running Playwright Tests")
    print(f"Browser: {args.browser}")
    print(f"Mode: {'Headed' if args.headed else 'Headless'}")
    
    success = run_command(cmd, "Running tests")
    
    # Generate Allure report if requested
    if args.allure and success:
        try:
            print("\n📊 Generating Allure report...")
            subprocess.run(["allure", "serve", "reports/allure-results"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Allure not installed or failed to generate report")
            print("Install with: pip install allure-pytest")
    
    # Print results summary
    if success:
        print("\n🎉 Tests completed successfully!")
        if args.html_report:
            print("📊 HTML report: reports/html_report.html")
        if os.path.exists("reports/screenshots") and os.listdir("reports/screenshots"):
            print("📸 Screenshots: reports/screenshots/")
        if args.video and os.path.exists("reports/videos") and os.listdir("reports/videos"):
            print("🎬 Videos: reports/videos/")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 