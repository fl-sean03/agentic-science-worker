#!/usr/bin/env python3
"""
Validate skill files follow Claude Code best practices.

Checks:
- Valid YAML frontmatter
- Required fields (name, description)
- Name follows conventions (lowercase, hyphens, max 64 chars)
- Description is meaningful (max 1024 chars)
- SKILL.md body is under 500 lines
- No XML tags in content
"""

import re
import sys
from pathlib import Path


def parse_frontmatter(content: str) -> tuple:
    """Extract YAML frontmatter and body from markdown."""
    if not content.startswith('---'):
        return None, content

    # Find the closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return None, content

    end_pos = end_match.end() + 3
    frontmatter_text = content[3:end_pos - 4]
    body = content[end_pos:]

    # Simple YAML parsing
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, body


def validate_skill(skill_path: Path) -> list:
    """Validate a single skill file."""
    errors = []
    warnings = []

    content = skill_path.read_text()
    frontmatter, body = parse_frontmatter(content)

    # Check frontmatter exists
    if frontmatter is None:
        errors.append("Missing YAML frontmatter (---)")
        return errors

    # Check required fields
    if 'name' not in frontmatter:
        errors.append("Missing required field: name")
    else:
        name = frontmatter['name']
        # Validate name format
        if len(name) > 64:
            errors.append(f"Name too long: {len(name)} chars (max 64)")
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"Invalid name format: must be lowercase letters, numbers, hyphens only")
        if name != skill_path.parent.name:
            warnings.append(f"Name '{name}' doesn't match directory '{skill_path.parent.name}'")

    if 'description' not in frontmatter:
        errors.append("Missing required field: description")
    else:
        desc = frontmatter['description']
        if len(desc) > 1024:
            errors.append(f"Description too long: {len(desc)} chars (max 1024)")
        if len(desc) < 20:
            warnings.append("Description very short - consider adding more detail")

    # Check body length
    body_lines = len(body.strip().split('\n'))
    if body_lines > 500:
        errors.append(f"SKILL.md body too long: {body_lines} lines (max 500)")
    elif body_lines > 400:
        warnings.append(f"SKILL.md body is {body_lines} lines - approaching 500 line limit")

    # Check for XML tags (forbidden)
    if re.search(r'<[a-zA-Z][^>]*>', content):
        errors.append("Contains XML-like tags (forbidden in skills)")

    # Check for common issues
    if 'allowed-tools' in frontmatter and not frontmatter['allowed-tools']:
        warnings.append("allowed-tools is empty - consider removing or specifying tools")

    return errors, warnings


def main():
    skills_dir = Path("/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/.claude/skills")

    if not skills_dir.exists():
        print("ERROR: Skills directory not found")
        sys.exit(1)

    all_valid = True
    total_skills = 0
    total_errors = 0
    total_warnings = 0

    print("Validating skills...")
    print("-" * 50)

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            print(f"WARN: {skill_dir.name}/ missing SKILL.md")
            continue

        total_skills += 1
        errors, warnings = validate_skill(skill_file)

        if errors:
            all_valid = False
            total_errors += len(errors)
            print(f"FAIL: {skill_dir.name}")
            for error in errors:
                print(f"  ERROR: {error}")
        else:
            print(f"PASS: {skill_dir.name}")

        for warning in warnings:
            total_warnings += 1
            print(f"  WARN: {warning}")

    print("-" * 50)
    print(f"Skills validated: {total_skills}")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")

    if all_valid:
        print("\nAll skills validated successfully!")
        sys.exit(0)
    else:
        print(f"\nValidation failed with {total_errors} errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
