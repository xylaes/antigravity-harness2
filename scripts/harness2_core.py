#!/usr/bin/env python3
"""Google Harness2 Core Engine for Antigravity.

Implements the Dual-Recursion Cycle:
1. Task-Level Recursion: Propose - Probe - Compose loop
2. Harnessing-Level Recursion: Persistent Experience Library

Based on Google Research Harness2 (arXiv:2610.14224).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_LIBRARY_DIR = Path(os.environ.get("AGY_HARNESS_LIBRARY", r"C:\Users\danny\.gemini\antigravity\scratch\harness_library"))
DEFAULT_LIBRARY_FILE = DEFAULT_LIBRARY_DIR / "EXPERIENCE.md"
BANNED_WORDS = {"leverage", "delighted", "testament", "spearhead", "esteemed"}


def ensure_library_file() -> Path:
    DEFAULT_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    if not DEFAULT_LIBRARY_FILE.is_file():
        DEFAULT_LIBRARY_FILE.write_text(
            "# Harness2 Persistent Experience Library\n\n"
            "This library retains transferable lessons, empirical contrasts, and verified\n"
            "fixes across agent conversations. Every entry records the exact cue, lesson,\n"
            "empirical evidence, and confidence rating.\n\n"
            "---\n\n",
            encoding="utf-8",
        )
    return DEFAULT_LIBRARY_FILE


def check_anti_ai_rules(text: str) -> list[str]:
    """Check text for em dashes and corporate buzzwords."""
    violations = []
    # Check for em dash (U+2014)
    if "\u2014" in text:
        violations.append("Violation: Em dash ('\u2014') detected. Use standard hyphens, commas, or colons instead.")

    # Check for banned corporate buzzwords
    for word in BANNED_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
            violations.append(f"Violation: Banned corporate buzzword '{word}' detected.")

    return violations


def check_platform_invariants(file_path: Path) -> list[str]:
    """Check for platform compatibility on Windows 11."""
    warnings = []
    text = file_path.read_text(encoding="utf-8", errors="replace")

    if file_path.suffix == ".py":
        if re.search(r"^\s*import fcntl", text, re.MULTILINE):
            warnings.append("Platform Warning: Direct 'import fcntl' found without Windows fallback.")
        if re.search(r"^\s*import (?:termios|pty)", text, re.MULTILINE):
            warnings.append("Platform Warning: POSIX-only module imported without Windows guard.")
        if "\\" in text and "Path" in text and ".as_posix()" not in text:
            # Informational check
            pass

    return warnings


def audit_transcript(transcript_path: Path) -> dict:
    """Analyze a transcript JSONL file for errors, friction, and tool execution failures."""
    if not transcript_path.is_file():
        return {"error": f"File not found: {transcript_path}"}

    total_steps = 0
    failures = []

    with transcript_path.open("r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            total_steps += 1
            status = data.get("status", "")
            content = str(data.get("content", ""))

            if status == "ERROR" or "Command exited with code" in content:
                m = re.search(r"Command exited with code ([1-9]\d*)", content)
                exit_code = m.group(1) if m else "ERROR"
                failures.append({
                    "step_index": data.get("step_index", idx),
                    "exit_code": exit_code,
                    "preview": content[:240].replace("\n", " "),
                })

    return {
        "transcript_path": str(transcript_path),
        "total_steps": total_steps,
        "failure_count": len(failures),
        "failures": failures,
    }


def probe_file(file_path: Path) -> bool:
    """Probe a candidate harness file for validity, platform compatibility, and guardrails."""
    if not file_path.is_file():
        print(f"[FAIL] Target file does not exist: {file_path}")
        return False

    content = file_path.read_text(encoding="utf-8", errors="replace")
    violations = check_anti_ai_rules(content)
    warnings = check_platform_invariants(file_path)

    print(f"--- Probing Candidate: {file_path.name} ---")
    passed = True

    if violations:
        passed = False
        print("  [FAIL] Rule violations:")
        for v in violations:
            print(f"    * {v}")
    else:
        print("  [PASS] Anti-AI tone checks passed (no em dashes, no buzzwords).")

    if warnings:
        print("  [WARN] Platform warnings:")
        for w in warnings:
            print(f"    * {w}")
    else:
        print("  [PASS] Platform invariants satisfied.")

    # Syntax check for Python
    if file_path.suffix == ".py":
        try:
            compile(content, str(file_path), "exec")
            print("  [PASS] Python syntax validation passed.")
        except SyntaxError as e:
            passed = False
            print(f"  [FAIL] Python syntax error: {e}")

    # Syntax check for JSON
    elif file_path.suffix == ".json":
        try:
            json.loads(content)
            print("  [PASS] JSON syntax validation passed.")
        except json.JSONDecodeError as e:
            passed = False
            print(f"  [FAIL] JSON parse error: {e}")

    print(f"--- Probe Result: {'PASSED' if passed else 'FAILED'} ---")
    return passed


def add_experience(title: str, cue: str, lesson: str, evidence: str, confidence: str = "high") -> bool:
    """Add a validated Harness2 experience entry to the library."""
    lib_file = ensure_library_file()

    entry = (
        f"## {title}\n"
        f"- **Recorded**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- **cue**: {cue}\n"
        f"- **lesson**: {lesson}\n"
        f"- **evidence**: {evidence}\n"
        f"- **confidence**: {confidence}\n\n"
        "---\n\n"
    )

    violations = check_anti_ai_rules(entry)
    if violations:
        print("[FAIL] Cannot add entry due to rule violations:")
        for v in violations:
            print(f"  * {v}")
        return False

    with lib_file.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(f"[SUCCESS] Recorded experience '{title}' in {lib_file}")
    return True


def list_experience() -> None:
    lib_file = ensure_library_file()
    print(lib_file.read_text(encoding="utf-8", errors="replace"))


def search_experience(keyword: str) -> None:
    lib_file = ensure_library_file()
    content = lib_file.read_text(encoding="utf-8", errors="replace")
    entries = content.split("\n---\n")
    matches = [e.strip() for e in entries if keyword.lower() in e.lower() and e.strip()]

    print(f"Found {len(matches)} matching entries for query '{keyword}':\n")
    for idx, match in enumerate(matches, 1):
        print(f"[{idx}]\n{match}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Harness2 Core Engine for Antigravity")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # audit subcommand
    audit_parser = subparsers.add_parser("audit", help="Audit transcript logs for tool errors and friction")
    audit_parser.add_argument("--transcript", type=Path, required=True, help="Path to transcript.jsonl file")

    # probe subcommand
    probe_parser = subparsers.add_parser("probe", help="Probe candidate harness file against invariants")
    probe_parser.add_argument("--file", type=Path, required=True, help="Path to file to probe")

    # experience subcommand
    exp_parser = subparsers.add_parser("experience", help="Manage persistent Experience Library")
    exp_sub = exp_parser.add_subparsers(dest="exp_command", required=True)

    exp_sub.add_parser("list", help="List all recorded experience entries")

    search_p = exp_sub.add_parser("search", help="Search experience entries by keyword")
    search_p.add_argument("query", type=str, help="Search query")

    add_p = exp_sub.add_parser("add", help="Add a new verified 4-part experience entry")
    add_p.add_argument("--title", required=True, help="Descriptor / Task Slug")
    add_p.add_argument("--cue", required=True, help="Trigger condition / context")
    add_p.add_argument("--lesson", required=True, help="Exact actionable rule or code pattern")
    add_p.add_argument("--evidence", required=True, help="Empirical baseline vs probe contrast")
    add_p.add_argument("--confidence", default="high", choices=["high", "medium", "provisional"], help="Confidence level")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        res = audit_transcript(args.transcript)
        print(json.dumps(res, indent=2))
        return 0

    if args.command == "probe":
        ok = probe_file(args.file)
        return 0 if ok else 1

    if args.command == "experience":
        if args.exp_command == "list":
            list_experience()
            return 0
        if args.exp_command == "search":
            search_experience(args.query)
            return 0
        if args.exp_command == "add":
            ok = add_experience(
                title=args.title,
                cue=args.cue,
                lesson=args.lesson,
                evidence=args.evidence,
                confidence=args.confidence,
            )
            return 0 if ok else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
