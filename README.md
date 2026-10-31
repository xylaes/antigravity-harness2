# Google Harness² Plugin for Antigravity

[![Repository](https://img.shields.io/badge/GitHub-google--research%2Fharness2-blue.svg)](https://github.com/google-research/harness2)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Framework](https://img.shields.io/badge/Harness%C2%B2-arXiv%3A2610.14224-orange.svg)](https://arxiv.org/abs/2610.14224)

An Antigravity plugin integrating the **Harness²** framework from Google Research (*Harness²: Recursive Agent Harnessing for an Open World*, arXiv:2610.14224).

Harness² enables autonomous AI agents to dynamically improve their performance, reliability, and precision on unseen, open-world tasks without modifying or fine-tuning underlying foundation model weights. The system optimizes the agent harness through dual-recursion cycles backed by persistent procedural memory.

---

## Architecture Overview

```
+-------------------------------------------------------------------------+
|                               FROZEN LLM                                |
+-------------------------------------------------------------------------+
                                     ^
                                     |
               +-------------------------------------------+
               |             THE AGENT HARNESS             |
               |                                           |
               |  1. System Prompts   5. Tool Guidance     |
               |  2. Guardrails       6. Scripts           |
               |  3. Memory           7. Subagents         |
               |  4. Skills           8. Plugins           |
               +-------------------------------------------+
                                     ^
                                     |
+-------------------------------------------------------------------------+
|                           THE DUAL RECURSION                            |
|                                                                         |
|  [Level 1: Task-Level]                                                  |
|    Failure Trace -> PROPOSE (Contrastive) -> PROBE (Sandboxed)          |
|                  -> COMPOSE (Merged Invariants & Domain Rules)          |
|                                                                         |
|  [Level 2: Harnessing-Level]                                            |
|    Verified Lessons -> EXPERIENCE LIBRARY                               |
|                        (cue, lesson, evidence, confidence)              |
+-------------------------------------------------------------------------+
```

### The 8 Harness Components

In Antigravity, foundation models remain frozen. Agent capabilities are shaped entirely by these 8 modular components:

1. **System Prompts**: Core agent role, system prompt headers, and model persona.
2. **Guardrails**: Global constraints (`RULE[user_global]`), workspace rules, and safety bounds.
3. **Memory**: Scratchpad files (`agent_scratchpad.md`), persistent transcripts, and state records.
4. **Skills**: Modular, step-by-step procedural runbooks (`skills/*/SKILL.md`).
5. **Tool Guidance**: MCP tool descriptions, parameter schemas, and `instructions.md` documents.
6. **Scripts**: Deterministic Python and shell utilities for validation and execution.
7. **Subagents**: Specialized worker agents (`define_subagent`, `invoke_subagent`).
8. **Plugins / Middleware**: Bundled extensions, lifecycle hooks, and external services.

---

## What This Plugin Bundles

* **Skills**:
  * `skills/harness2/SKILL.md`: The primary procedural runbook for running Propose-Probe-Compose optimization cycles, auditing transcripts, and querying the Experience Library.
* **Subagents**:
  * `agents/harness-proposer.md`: Analyzes execution transcripts and proposes contrastive modifications (invariant vs domain).
  * `agents/harness-prober.md`: Evaluates candidate edits in sandboxed conditions, testing platform invariants, syntax, and anti-AI tone rules.
* **Rules**:
  * `rules/AGENTS.md`: Enforces frozen-model constraints, the 4-part experience schema, anti-AI formatting rules, and Windows 11 platform invariants whenever the plugin is active.
* **Core Script**:
  * `scripts/harness2_core.py`: CLI engine providing transcript auditing, candidate file probing, and Experience Library management.
* **Assets**:
  * `assets/logo.svg`: High-contrast vector monogram for UI card presentation.

---

## Quick Start & CLI Usage

### 1. Audit Transcripts for Friction and Tool Errors

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" audit `
  --transcript "path\to\transcript.jsonl"
```

### 2. Probe Candidate Harness Modifications

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" probe `
  --file "path\to\candidate_skill_or_rule.md"
```

### 3. Query the Experience Library

```powershell
# List all entries:
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" experience list

# Search by topic:
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" experience search "locking"
```

### 4. Record a Verified 4-Part Lesson

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" experience add `
  --title "Descriptor Slug" `
  --cue "When invoking tool X under condition Y" `
  --lesson "Use parameter Z instead of W" `
  --evidence "Baseline produced exit code 1; probe completed with code 0" `
  --confidence high
```

---

## Windows 11 Compatibility Invariants

1. **File Locking**:
   POSIX `fcntl.flock` is not available on Windows. Wrap imports in `try/except` and fall back to `msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)`.
2. **Path Normalization**:
   Virtual tree dictionaries and cross-platform key indices require forward slashes. Always use `Path.relative_to(...).as_posix()` rather than raw strings.
3. **Sandbox vs Network Boundaries**:
   Standard PowerShell sandbox blocks outbound socket connections on port 443. Commands that download packages or clone repositories must run with sandbox bypass, while all builds, audits, and tests run inside the sandbox.
