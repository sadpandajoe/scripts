#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import click


def is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def validate_git_ref(ref: str) -> bool:
    """Validate if a git reference exists."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_changed_files(
    base_ref: str, head_ref: str, file_pattern: Optional[str] = None
) -> List[str]:
    """Get list of changed files between two Git refs.

    Args:
        base_ref: Base Git reference (tag/branch/commit)
        head_ref: Head Git reference (tag/branch/commit)
        file_pattern: Optional file pattern to filter results (e.g. "*.py")

    Returns:
        List of changed file paths
    """
    cmd = ["git", "diff", "--name-only", base_ref, head_ref]
    if file_pattern:
        cmd.append("--")
        cmd.append(file_pattern)

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


@click.command()
@click.argument("base_ref")
@click.argument("head_ref")
@click.option("--pattern", "-p", help='File pattern to filter results (e.g. "*.py")')  # noqa: E501
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path for the list of changes",  # noqa: E501
)
def main(base_ref: str, head_ref: str, pattern: Optional[str], output: Optional[str]):  # noqa: E501
    """Compare files changed between two Git references (tags/branches/commits).

    BASE_REF: Starting reference (tag/branch/commit)
    HEAD_REF: Ending reference (tag/branch/commit)
    """  # noqa: E501
    if not is_git_repo():
        click.echo("Error: Not a git repository", err=True)
        sys.exit(1)

    # Validate references
    if not validate_git_ref(base_ref):
        click.echo(f"Error: Invalid git reference '{base_ref}'", err=True)
        click.echo(
            "Note: Make sure you're in the correct repository and the reference exists"  # noqa: E501
        )
        sys.exit(1)

    if not validate_git_ref(head_ref):
        click.echo(f"Error: Invalid git reference '{head_ref}'", err=True)
        click.echo(
            "Note: Make sure you're in the correct repository and the reference exists"  # noqa: E501
        )
        sys.exit(1)

    try:
        changed_files = get_changed_files(base_ref, head_ref, pattern)

        if not changed_files:
            click.echo("No changes found between the specified references.")
            return

        click.echo(f"Found {len(changed_files)} changed files:")
        for file in changed_files:
            click.echo(f"  - {file}")

        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text("\n".join(changed_files) + "\n")
            click.echo(f"\nWritten output to: {output_path}")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error: Git command failed: {e.stderr}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
