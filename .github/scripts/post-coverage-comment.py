#!/usr/bin/env python3
"""Generate and post a combined coverage comment to a PR."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def parse_lcov(lcov_file: Path) -> dict[str, dict[str, float]]:
    """Parse an LCOV file and return coverage statistics."""
    if not lcov_file.exists():
        return {}

    content = lcov_file.read_text()
    files = {}
    current_file = None
    lines_found = 0
    lines_hit = 0
    funcs_found = 0
    funcs_hit = 0
    branches_found = 0
    branches_hit = 0

    for line in content.strip().split('\n'):
        if line.startswith('SF:'):
            current_file = line[3:]
            lines_found = lines_hit = 0
            funcs_found = funcs_hit = 0
            branches_found = branches_hit = 0
        elif line.startswith('LF:'):
            lines_found = int(line[3:])
        elif line.startswith('LH:'):
            lines_hit = int(line[3:])
        elif line.startswith('FNF:'):
            funcs_found = int(line[4:])
        elif line.startswith('FNH:'):
            funcs_hit = int(line[4:])
        elif line.startswith('BRF:'):
            branches_found = int(line[4:])
        elif line.startswith('BRH:'):
            branches_hit = int(line[4:])
        elif line == 'end_of_record' and current_file:
            files[current_file] = {
                'lines': (lines_hit / lines_found * 100) if lines_found > 0 else 0,
                'funcs': (funcs_hit / funcs_found * 100) if funcs_found > 0 else 0,
                'branches': (branches_hit / branches_found * 100) if branches_found > 0 else 0,
                'lines_hit': lines_hit,
                'lines_found': lines_found,
                'funcs_hit': funcs_hit,
                'funcs_found': funcs_found,
                'branches_hit': branches_hit,
                'branches_found': branches_found,
            }

    return files


def calculate_totals(files: dict[str, dict[str, float]]) -> dict[str, float]:
    """Calculate total coverage from files."""
    total_lines_hit = sum(f['lines_hit'] for f in files.values())
    total_lines_found = sum(f['lines_found'] for f in files.values())
    total_funcs_hit = sum(f['funcs_hit'] for f in files.values())
    total_funcs_found = sum(f['funcs_found'] for f in files.values())
    total_branches_hit = sum(f['branches_hit'] for f in files.values())
    total_branches_found = sum(f['branches_found'] for f in files.values())

    return {
        'lines': (total_lines_hit / total_lines_found * 100) if total_lines_found > 0 else 0,
        'funcs': (total_funcs_hit / total_funcs_found * 100) if total_funcs_found > 0 else 0,
        'branches': (total_branches_hit / total_branches_found * 100) if total_branches_found > 0 else 0,
    }


def format_coverage_comment(backend_files: dict, frontend_files: dict) -> str:
    """Format the coverage comment as markdown."""
    backend_totals = calculate_totals(backend_files)
    frontend_totals = calculate_totals(frontend_files)

    # Combine for overall
    all_files = {**backend_files, **frontend_files}
    overall_totals = calculate_totals(all_files)

    comment = "## Code Coverage Report\n\n"

    # Total section
    comment += "### Total\n\n"
    comment += f"| Lines | Functions | Branches |\n"
    comment += f"|-------|-----------|----------|\n"
    comment += f"| {overall_totals['lines']:.2f}% | {overall_totals['funcs']:.2f}% | {overall_totals['branches']:.2f}% |\n\n"

    # Backend section with file breakdown
    comment += "### Backend\n\n"
    comment += f"**Total:** {backend_totals['lines']:.2f}% lines | {backend_totals['funcs']:.2f}% functions | {backend_totals['branches']:.2f}% branches\n\n"

    if backend_files:
        comment += "| File | Lines | Functions | Branches |\n"
        comment += "|------|-------|-----------|----------|\n"
        for file, stats in sorted(backend_files.items()):
            filename = Path(file).name
            comment += f"| {filename} | {stats['lines']:.2f}% | {stats['funcs']:.2f}% | {stats['branches']:.2f}% |\n"
        comment += "\n"

    # Frontend section with file breakdown
    comment += "### Frontend\n\n"
    comment += f"**Total:** {frontend_totals['lines']:.2f}% lines | {frontend_totals['funcs']:.2f}% functions | {frontend_totals['branches']:.2f}% branches\n\n"

    if frontend_files:
        comment += "| File | Lines | Functions | Branches |\n"
        comment += "|------|-------|-----------|----------|\n"
        for file, stats in sorted(frontend_files.items()):
            filename = Path(file).name
            comment += f"| {filename} | {stats['lines']:.2f}% | {stats['funcs']:.2f}% | {stats['branches']:.2f}% |\n"

    return comment


def post_comment(pr_number: str, comment_body: str, github_token: str) -> None:
    """Post or update a comment on the PR."""
    # Check for existing coverage comment
    result = subprocess.run(
        ['gh', 'api', f'repos/{{owner}}/{{repo}}/issues/{pr_number}/comments'],
        capture_output=True,
        text=True,
        env={**os.environ, 'GH_TOKEN': github_token}
    )

    if result.returncode == 0:
        comments = json.loads(result.stdout)
        coverage_comment = None

        for comment in comments:
            if comment['user']['login'] == 'github-actions[bot]' and '## Code Coverage Report' in comment['body']:
                coverage_comment = comment
                break

        if coverage_comment:
            # Update existing comment
            subprocess.run(
                ['gh', 'api', '-X', 'PATCH', f'repos/{{owner}}/{{repo}}/issues/comments/{coverage_comment["id"]}',
                 '-f', f'body={comment_body}'],
                env={**os.environ, 'GH_TOKEN': github_token},
                check=True
            )
            print(f"Updated existing coverage comment (ID: {coverage_comment['id']})")
        else:
            # Create new comment
            subprocess.run(
                ['gh', 'api', '-X', 'POST', f'repos/{{owner}}/{{repo}}/issues/{pr_number}/comments',
                 '-f', f'body={comment_body}'],
                env={**os.environ, 'GH_TOKEN': github_token},
                check=True
            )
            print("Created new coverage comment")
    else:
        print(f"Error fetching comments: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    backend_lcov = Path('coverage.lcov')
    frontend_lcov = Path('lcov.info')

    backend_files = parse_lcov(backend_lcov)
    frontend_files = parse_lcov(frontend_lcov)

    comment = format_coverage_comment(backend_files, frontend_files)

    pr_number = os.environ.get('PR_NUMBER')
    github_token = os.environ.get('GITHUB_TOKEN')

    if not pr_number or not github_token:
        print("Error: PR_NUMBER and GITHUB_TOKEN environment variables required", file=sys.stderr)
        sys.exit(1)

    post_comment(pr_number, comment, github_token)


if __name__ == '__main__':
    main()
