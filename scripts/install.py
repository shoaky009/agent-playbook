#!/usr/bin/env python3
"""Install shared instructions for Codex, pi, and omp, plus personal skills."""

import argparse
import filecmp
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone


def same_content(source, destination):
    if destination.is_symlink():
        return False
    if source.is_file() and destination.is_file():
        return filecmp.cmp(source, destination, shallow=False)
    if source.is_dir() and destination.is_dir():
        children = {child.name for child in source.iterdir()}
        if children != {child.name for child in destination.iterdir()}:
            return False
        return all(same_content(source / name, destination / name) for name in children)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    parser.add_argument(
        "--agent", choices=("codex", "pi", "omp", "all"), default="all",
        help="Agent receiving AGENTS.md (default: all); shared skills are installed once",
    )
    parser.add_argument(
        "--codex-home", type=Path,
        default=Path(os.environ.get("CODEX_HOME") or "~/.codex"),
        help="Codex home directory (default: CODEX_HOME or ~/.codex)",
    )
    parser.add_argument(
        "--pi-agent-dir", type=Path, default=Path("~/.pi/agent"),
        help="Pi agent directory (default: ~/.pi/agent)",
    )
    parser.add_argument(
        "--omp-agent-dir", type=Path, default=Path("~/.omp/agent"),
        help="Oh My Pi agent directory (default: ~/.omp/agent)",
    )
    parser.add_argument(
        "--skills-dir", type=Path, default=Path("~/.agents/skills"),
        help="Personal skills directory (default: ~/.agents/skills)",
    )
    args = parser.parse_args()
    repository = Path(__file__).resolve().parent.parent
    skills_dir = args.skills_dir.expanduser().resolve()
    agent_dirs = {
        "codex": args.codex_home,
        "pi": args.pi_agent_dir,
        "omp": args.omp_agent_dir,
    }
    selected = agent_dirs if args.agent == "all" else {args.agent: agent_dirs[args.agent]}
    destinations = [directory.expanduser().resolve() for directory in selected.values()]

    for directory in (*destinations, skills_dir):
        if directory == repository or repository in directory.parents:
            parser.error("Installation directories must be outside this repository")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_relative = Path("backups") / "agent-playbook" / timestamp
    entries = [
        (repository / "AGENTS.md", directory / "AGENTS.md", directory / backup_relative / "AGENTS.md")
        for directory in destinations
    ]
    for source in sorted((repository / "skills").iterdir()):
        if source.is_dir() and (source / "SKILL.md").is_file():
            entries.append((
                source,
                skills_dir / source.name,
                skills_dir.parent / backup_relative / "skills" / source.name,
            ))

    for source, destination, backup in entries:
        if same_content(source, destination):
            print(f"Unchanged: {destination}")
            continue

        if destination.exists() or destination.is_symlink():
            print(f"Backup: {destination} -> {backup}")
            if not args.dry_run:
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(backup))

        print(f"Install: {source} -> {destination}")
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, shutil.Error) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        sys.exit(1)
