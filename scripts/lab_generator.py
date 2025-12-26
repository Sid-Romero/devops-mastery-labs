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


def scrape_topics(scraper: DevOpsScraper, skip: bool = False):
    """Scrape DevOps topics from the web or return fallback"""
    from web_scraper import DevOpsTopic

    if skip:
        print("[INFO] Skipping web scrape, using fallback topic")
        return get_fallback_topics()

    print("[INFO] Scraping DevOps content from multiple sources...")
    topics = scraper.scrape_all()

    if not topics:
        print("[WARN] No topics found, using fallback")
        return get_fallback_topics()

    print(f"[INFO] Found {len(topics)} topics")
    return topics


def get_fallback_topics():
    """Return fallback topics when scraping fails"""
    from web_scraper import DevOpsTopic
    import random

    fallbacks = [
        DevOpsTopic(
            title="Container image optimization and multi-stage builds",
            summary="Learn techniques to reduce Docker image size and improve build performance.",
            source="fallback",
            url="",
            tags=["docker", "optimization"],
            technology="docker"
        ),
        DevOpsTopic(
            title="Kubernetes deployment strategies and rollbacks",
            summary="Implement rolling updates, blue-green and canary deployments in Kubernetes.",
            source="fallback",
            url="",
            tags=["kubernetes", "deployment"],
            technology="kubernetes"
        ),
        DevOpsTopic(
            title="Helm chart templating and dependencies",
            summary="Create reusable Helm charts with advanced templating features.",
            source="fallback",
            url="",
            tags=["helm", "charts"],
            technology="helm"
        ),
        DevOpsTopic(
            title="GitOps workflow with ArgoCD",
            summary="Set up continuous delivery using ArgoCD and GitOps principles.",
            source="fallback",
            url="",
            tags=["argocd", "gitops"],
            technology="argocd"
        ),
        DevOpsTopic(
            title="Ansible playbooks for server configuration",
            summary="Automate server setup and configuration management with Ansible.",
            source="fallback",
            url="",
            tags=["ansible", "automation"],
            technology="ansible"
        ),
    ]
    return fallbacks


def select_topic_and_technology(topics, force_technology=None):
    """Select a topic and technology for lab generation"""
    import random

    # Determine technology
    if force_technology:
        technology = force_technology
    else:
        # 70% chance to pick from topic's detected technology
        tech_topics = [t for t in topics if t.technology]
        if tech_topics and random.random() < 0.7:
            selected = random.choice(tech_topics)
            technology = selected.technology
        else:
            technology = random.choice(TECHNOLOGIES)

    # Select topic (prefer matching technology)
    matching = [t for t in topics if t.technology == technology]
    if matching:
        topic = random.choice(matching)
    else:
        topic = random.choice(topics)

    return topic, technology


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

    # Initialize components
    scraper, generator, creator, existing_labs = init_components(config['api_key'])

    # Step 1: Scrape topics or use fallback
    print("\n" + "-" * 60)
    print("Step 1: Fetching DevOps content")
    print("-" * 60)

    topics = scrape_topics(scraper, skip=args.skip_scrape)

    # Step 2: Select topic and technology
    print("\n" + "-" * 60)
    print("Step 2: Selecting topic and technology")
    print("-" * 60)

    topic, technology = select_topic_and_technology(
        topics=topics,
        force_technology=config['force_technology']
    )

    print(f"[INFO] Selected technology: {technology}")
    print(f"[INFO] Selected topic: {topic.title[:60]}...")
    print(f"[INFO] Source: {topic.source}")

    # TODO: Complete in next commit
    # - Step 3: Generate lab with AI
    # - Step 4: Create files

    if args.dry_run:
        print("\n[DRY-RUN] Would generate lab here. Exiting.")
        return 0

    print("\n[INFO] Topic selection complete")
    print("[TODO] Lab generation in next commit")

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

    # Test 4: Fallback topics
    print("\n[TEST] Fallback topics...")
    try:
        fallbacks = get_fallback_topics()
        if len(fallbacks) == 5:
            print(f"       PASSED ({len(fallbacks)} fallback topics)")
            passed += 1
        else:
            print(f"       FAILED: Expected 5 fallbacks, got {len(fallbacks)}")
            failed += 1
    except Exception as e:
        print(f"       FAILED: {e}")
        failed += 1

    # Test 5: Topic selection
    print("\n[TEST] Topic and technology selection...")
    try:
        fallbacks = get_fallback_topics()
        topic, tech = select_topic_and_technology(fallbacks, force_technology='docker')
        if tech == 'docker' and topic is not None:
            print(f"       PASSED (tech={tech}, topic={topic.title[:30]}...)")
            passed += 1
        else:
            print(f"       FAILED: Unexpected result")
            failed += 1
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
