#!/usr/bin/env python3
"""
Lab Generator - Main Orchestrator
==================================
Entry point called by GitHub Actions.
Orchestrates the lab generation process:
1. Scrape DevOps content from the web
2. Select a random topic and technology
3. Generate a lab using Gemini AI
4. Create the lab files in the repository

Usage:
    python lab_generator.py              # Normal run
    python lab_generator.py --dry-run    # Test without creating files
    python lab_generator.py --test       # Run local tests
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from web_scraper import DevOpsScraper
from ai_generator import GeminiLabGenerator, TECHNOLOGIES
from file_creator import LabFileCreator


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='DevOps Lab Generator')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without creating files (test mode)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run local tests'
    )
    parser.add_argument(
        '--technology',
        type=str,
        choices=TECHNOLOGIES,
        help='Force a specific technology'
    )
    parser.add_argument(
        '--skip-scrape',
        action='store_true',
        help='Skip web scraping (use fallback topic)'
    )
    return parser.parse_args()


def load_config():
    """Load configuration from environment variables"""
    load_dotenv()

    config = {
        'api_key': os.environ.get('GEMINI_API_KEY'),
        'force_technology': os.environ.get('FORCE_TECHNOLOGY', '').strip().lower(),
    }

    # Validate force_technology
    if config['force_technology'] and config['force_technology'] not in TECHNOLOGIES:
        print(f"[WARN] Invalid FORCE_TECHNOLOGY: {config['force_technology']}")
        print(f"       Valid options: {TECHNOLOGIES}")
        config['force_technology'] = None

    return config


def init_components(api_key: str):
    """Initialize all components"""
    print("[INFO] Initializing components...")

    scraper = DevOpsScraper()
    generator = GeminiLabGenerator(api_key)
    creator = LabFileCreator()

    existing_labs = creator.get_existing_labs()
    print(f"[INFO] Found {len(existing_labs)} existing labs")

    return scraper, generator, creator, existing_labs


def validate_environment():
    """Validate that the environment is properly configured"""
    errors = []

    # Check for API key
    if not os.environ.get('GEMINI_API_KEY'):
        errors.append("GEMINI_API_KEY environment variable not set")

    # Check that we can import all modules
    try:
        from web_scraper import DevOpsScraper
        from ai_generator import GeminiLabGenerator
        from file_creator import LabFileCreator
    except ImportError as e:
        errors.append(f"Failed to import module: {e}")

    return errors


# Entry point - to be completed in next commits
def main():
    """Main entry point"""
    args = parse_args()

    # Run tests if requested
    if args.test:
        return run_tests()

    print("=" * 60)
    print("DevOps Lab Generator")
    print("=" * 60)

    # Validate environment
    errors = validate_environment()
    if errors:
        for err in errors:
            print(f"[ERROR] {err}")
        print("\nSetup instructions:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your GEMINI_API_KEY to .env")
        return 1

    # Load config
    config = load_config()

    # Override technology from CLI if provided
    if args.technology:
        config['force_technology'] = args.technology

    print(f"[INFO] Dry run: {args.dry_run}")
    print(f"[INFO] Skip scrape: {args.skip_scrape}")
    print(f"[INFO] Technology: {config['force_technology'] or 'random'}")

    # TODO: Complete in next commits
    # - Step 1: Scrape topics
    # - Step 2: Select topic and technology
    # - Step 3: Generate lab
    # - Step 4: Create files

    print("\n[INFO] Orchestrator structure ready")
    print("[TODO] Complete implementation in next commits")

    return 0


def run_tests():
    """Run local tests"""
    print("=" * 60)
    print("Running Local Tests")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: Environment validation
    print("\n[TEST] Environment validation...")
    errors = validate_environment()
    if not errors:
        print("       PASSED")
        passed += 1
    else:
        print(f"       FAILED: {errors}")
        failed += 1

    # Test 2: Config loading
    print("\n[TEST] Config loading...")
    try:
        config = load_config()
        if config['api_key']:
            print("       PASSED (API key found)")
            passed += 1
        else:
            print("       SKIPPED (no API key)")
    except Exception as e:
        print(f"       FAILED: {e}")
        failed += 1

    # Test 3: Import modules
    print("\n[TEST] Module imports...")
    try:
        from web_scraper import DevOpsScraper, DevOpsTopic
        from ai_generator import GeminiLabGenerator, GeneratedLab
        from file_creator import LabFileCreator
        print("       PASSED")
        passed += 1
    except Exception as e:
        print(f"       FAILED: {e}")
        failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Tests: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
