"""
AI Lab Generator Module (Google Gemini)
=======================================
Uses Google Gemini API to generate DevOps lab content
based on scraped topics and technology focus.
(Only free  one actually right now)
(will add LLms later eventually)
"""

import os
import json
import random
from typing import Optional, Dict, Any
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential

from google import genai
from google.genai import types


@dataclass
class GeneratedLab:
    """Represents a generated lab structure"""
    title: str
    slug: str
    technology: str
    difficulty: str  # easy, medium, hard
    description: str
    objectives: list[str]
    prerequisites: list[str]
    steps: list[Dict[str, str]]
    files: Dict[str, str]  # filename -> content
    hints: list[str]
    solution_notes: str


# Available technologies for random selection
TECHNOLOGIES = ['docker', 'kubernetes', 'helm', 'argocd', 'ansible', 'aws', 'terraform']

# Difficulty levels
DIFFICULTIES = ['easy', 'medium', 'hard']


class GeminiLabGenerator:
    """Generates DevOps labs using Google Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Gemini API key"""
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        self.client = genai.Client(api_key=self.api_key)
        # Use gemini-2.0-flash (current model, free tier)
        self.model_name = 'gemini-2.0-flash'

    def _build_prompt(self, topic_title: str, topic_summary: str,
                      technology: str, existing_labs: list[str]) -> str:
        """Build the prompt for lab generation"""

        # List existing labs to avoid duplicates
        existing_labs_str = "\n".join(f"- {lab}" for lab in existing_labs[-20:])

        prompt = f"""You are an expert DevOps engineer and technical educator.
Generate a hands-on lab exercise for learning {technology.upper()}.

## Context
The lab should be inspired by this trending topic:
**Title:** {topic_title}
**Summary:** {topic_summary}

## Requirements
1. Create a PRACTICAL, HANDS-ON lab (not just reading/theory)
2. The lab should take 30-90 minutes to complete
3. Include real commands, real files, real configurations
4. Progressive difficulty with clear steps
5. Must be completable on a local machine (Docker Desktop, minikube, etc.).
6. Avoid emojis, slang, or informal language
7. The goal is to document a complete lab that can be directly used. But you shall not give the direct solutions, only hints and solution notes.
## Existing Labs (avoid duplicates)
{existing_labs_str}

## Technology Focus: {technology.upper()}
Generate a lab specifically for {technology}. Examples:
- docker: Dockerfile optimization, multi-stage builds, compose, networking
- kubernetes: deployments, services, configmaps, secrets, ingress
- helm: chart creation, values, dependencies, hooks
- argocd: GitOps setup, app-of-apps, sync policies, rollbacks
- ansible: playbooks, roles, inventories, vault, dynamic inventory
- aws: S3, EC2, IAM, VPC, Lambda
- terraform: infrastructure as code, modules, state management, providers

## Output Format (JSON)
Return a valid JSON object with this exact structure:
```json
{{
  "title": "Short descriptive title (max 60 chars)",
  "slug": "lowercase-hyphenated-slug",
  "technology": "{technology}",
  "difficulty": "easy|medium|hard",
  "description": "2-3 sentence description of what the lab teaches",
  "objectives": [
    "Learning objective 1",
    "Learning objective 2",
    "Learning objective 3"
  ],
  "prerequisites": [
    "Prerequisite 1 (e.g., Docker installed)",
    "Prerequisite 2"
  ],
  "steps": [
    {{
      "title": "Step 1 title",
      "content": "Detailed instructions with commands in markdown code blocks"
    }},
    {{
      "title": "Step 2 title",
      "content": "More instructions..."
    }}
  ],
  "files": {{
    "Dockerfile": "# Dockerfile content here...",
    "docker-compose.yml": "version: '3.8'\\nservices:...",
    "README.md": "# Lab Title\\n\\n## Description\\n..."
  }},
  "hints": [
    "Hint if stuck on step 1",
    "Hint for common mistakes"
  ],
  "solution_notes": "Brief explanation of the complete solution"
}}
```

## Important Rules
1. The "files" object MUST include a complete README.md
2. Include ALL necessary files (Dockerfile, configs, scripts, etc.)
3. Use realistic, production-like examples
4. Difficulty assessment should be honest based on:
   - easy: Basic concepts, simple commands, < 45 min
   - medium: Multiple components, debugging needed, 45-75 min
   - hard: Complex architecture, troubleshooting, > 75 min
5. Return ONLY the JSON object, no markdown wrapper, no extra text

Generate the lab now:"""

        return prompt

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=4, max=30), reraise=True)
    def _call_gemini(self, prompt: str, temperature: float = 0.7, max_tokens: int = 8192) -> str:
        """Call Gemini API with retry logic"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text
        except Exception as e:
            print(f"Gemini API error: {type(e).__name__}: {e}")
            raise

    def generate_lab(self, topic_title: str, topic_summary: str,
                     technology: Optional[str] = None,
                     existing_labs: Optional[list[str]] = None) -> GeneratedLab:
        """Generate a lab using Gemini API"""

        # Random technology if not specified
        if not technology:
            technology = random.choice(TECHNOLOGIES)

        existing_labs = existing_labs or []

        print(f"Generating {technology.upper()} lab with Gemini...")
        print(f"   Topic: {topic_title[:50]}...")

        prompt = self._build_prompt(topic_title, topic_summary, technology, existing_labs)

        # Generate with Gemini (new SDK) - uses retry wrapper
        response_text = self._call_gemini(prompt, temperature=0.7, max_tokens=8192)
        response_text = response_text.strip()

        # DEBUG: Save raw response for troubleshooting
        debug_mode = os.environ.get('DEBUG_GEMINI', 'false').lower() == 'true'
        if debug_mode:
            debug_file = f"/tmp/gemini_response_{technology}.json"
            with open(debug_file, 'w') as f: #debugging purpose and close the file right after
                f.write(response_text) # gemini raw response
            print(f"   DEBUG: Raw response saved to {debug_file}")
        # need to enable corresponding env var in github actions for that later

        # Remove markdown code block if present
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            # Remove first line (```json) and last line (```)
            response_text = '\n'.join(lines[1:-1])

        # Fix invalid escape sequences in JSON (which is common with regex patterns)
        # the goal is to replace invalid \X escapes with \\X (except valid ones that are: \n \r \t \b \f \" \\ \/) ->  JSON can parse it correctly
        def fix_escapes(text):
            # Find all backslash sequences and fix invalid ones
            valid_escapes = {'n', 'r', 't', 'b', 'f', '"', '\\', '/', 'u'}
            result = []  # we built the fixed string here char by char
            i = 0  # current index of the message
            while i < len(text):
                if text[i] == '\\' and i + 1 < len(text):  # if we find a backslash
                    next_char = text[i + 1]  # look at the next char

                    if next_char not in valid_escapes:
                        # Invalid escape - double the backslash
                        result.append('\\\\')
                        i += 1  # skip the next char as we already processed it
                    else:
                        result.append(text[i])
                        i += 1
                else:
                    result.append(text[i])
                    i += 1
            return ''.join(result)

        response_text = fix_escapes(response_text)

        try:
            lab_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"   Response preview: {response_text[:500]}...")
            raise ValueError(f"Failed to parse Gemini response as JSON: {e}")

        # Validate required fields
        required_fields = ['title', 'slug', 'technology', 'difficulty',
                          'description', 'objectives', 'steps', 'files']
        for field in required_fields:
            if field not in lab_data:
                raise ValueError(f"Missing required field: {field}")

        # Create GeneratedLab object
        lab = GeneratedLab(
            title=lab_data['title'],
            slug=lab_data['slug'],
            technology=lab_data['technology'],
            difficulty=lab_data['difficulty'],
            description=lab_data['description'],
            objectives=lab_data.get('objectives', []),
            prerequisites=lab_data.get('prerequisites', []),
            steps=lab_data.get('steps', []),
            files=lab_data.get('files', {}),
            hints=lab_data.get('hints', []),
            solution_notes=lab_data.get('solution_notes', '')
        )

        print(f"✅ Generated: {lab.title}")
        print(f"   Difficulty: {lab.difficulty}")
        print(f"   Files: {list(lab.files.keys())}")

        return lab

    def assess_difficulty(self, lab: GeneratedLab) -> str:
        """Re-assess difficulty using AI (double-check)"""

        prompt = f"""Assess the difficulty of this DevOps lab:

Title: {lab.title}
Technology: {lab.technology}
Description: {lab.description}
Number of steps: {len(lab.steps)}
Files included: {list(lab.files.keys())}

Prerequisites: {lab.prerequisites}

Based on:
- Complexity of concepts
- Time to complete
- Required prior knowledge
- Debugging/troubleshooting needed

Return ONLY one word: easy, medium, or hard"""

        try:
            response_text = self._call_gemini(prompt, temperature=0.1, max_tokens=10)
            difficulty = response_text.strip().lower()
            if difficulty not in DIFFICULTIES:
                difficulty = lab.difficulty  # Keep original if invalid
        except Exception:
            difficulty = lab.difficulty  # Keep original on error

        return difficulty


# Standalone test
if __name__ == "__main__":
    import sys

    # Check for API key
    if not os.environ.get('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY environment variable not set")
        print("   Export it: export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)

    generator = GeminiLabGenerator()

    # Test generation
    lab = generator.generate_lab(
        topic_title="Building efficient Docker images with multi-stage builds",
        topic_summary="Learn how to reduce Docker image size by 80% using multi-stage builds",
        technology="docker",
        existing_labs=["lab-01-multistage-node", "lab-02-python-env-secrets"]
    )

    print("\n Generated Lab Summary:")
    print(f"   Title: {lab.title}")
    print(f"   Slug: {lab.slug}")
    print(f"   Tech: {lab.technology}")
    print(f"   Difficulty: {lab.difficulty}")
    print(f"   Steps: {len(lab.steps)}")
    print(f"   Files: {list(lab.files.keys())}")
