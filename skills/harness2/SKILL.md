---
name: harness2
description: Recursive agent harness optimizer based on Google Research Harness2 (arXiv:2610.14224). Optimizes frozen-model agent scaffolding (prompts, guardrails, skills, tool guidance, scripts, subagents, and memory) via the Propose-Probe-Compose loop and persistent experience library.
license: Apache-2.0
metadata:
  version: v1
  publisher: user
---

# Google Harness2 Optimizer

This skill implements the recursive harness optimization framework from Google Research Harness2 (*arXiv:2610.14224*, Google Cloud AI Research & Northwestern University).

In modern agent architectures, the underlying foundation language model remains completely frozen. Performance, reliability, and precision depend on the surrounding **agent harness**:
1. **System Prompts**: Core agent behavior and persona boundaries.
2. **Guardrails**: Invariants, safety constraints, and platform profiles.
3. **Memory**: Scratchpad files, conversation transcripts, and state records.
4. **Skills**: Modular procedural runbooks.
5. **Tool Guidance**: MCP instructions, tool schemas, and parameter guidance.
6. **Scripts**: Deterministic validation scripts and runtime helpers.
7. **Subagents**: Worker topologies and specialist agents.
8. **Plugins / Middleware**: Bundled extensions, lifecycle hooks, and external integrations.

---

## The Dual-Recursion Architecture

```
+-------------------------------------------------------------+
|                 Level 1: Task-Level Recursion               |
|                                                             |
|   [Task Failure / Friction]                                 |
|              |                                              |
|              v                                              |
|       +--------------+                                      |
|       |   PROPOSE    | --> Formulate contrastive edits      |
|       +--------------+     (Invariant vs Domain)            |
|              |                                              |
|              v                                              |
|       +--------------+                                      |
|       |    PROBE     | --> Test candidate against           |
|       +--------------+     invariants & sandbox             |
|              |                                              |
|              v                                              |
|       +--------------+                                      |
|       |   COMPOSE    | --> Merge passing edits into         |
|       +--------------+     harness components               |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|            Level 2: Harnessing-Level Recursion              |
|                                                             |
|   +-----------------------------------------------------+   |
|   |         PERSISTENT EXPERIENCE LIBRARY               |   |
|   |  - cue: contextual trigger condition                |   |
|   |  - lesson: exact actionable rule or code pattern    |   |
|   |  - evidence: empirical baseline vs probe contrast   |   |
|   |  - confidence: high | medium | provisional          |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
```

---

## Operating Procedures

### 1. When to Trigger This Skill
- After resolving a complex multi-turn debugging session with non-obvious fixes.
- When an agent encounters repeated tool execution errors or format drift.
- When auditing the agent skill, rule, or tool guidance library for redundancies or conflicting instructions.
- When requested directly by the user or through slash commands (`/goal`, `/plan`, `/learn`).

### 2. Step-by-Step Optimization Workflow

#### Step 1: Audit Recent Traces
Run the Harness2 core auditor to scan recent conversation transcripts for tool errors and execution friction:

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" audit --transcript "path\to\transcript.jsonl"
```

#### Step 2: Propose Contrastive Modifications
Identify whether the failure stems from an invariant issue (applies universally) or a domain issue (specific tool or task):
- Draft the minimal required change to the target harness component.
- Delegate to the `harness-proposer` subagent if running within a multi-agent workflow.

#### Step 3: Probe Candidate Modifications
Before committing any changes to the active harness, probe the candidate file for compliance:

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" probe --file "path\to\candidate_file.md"
```

The probe verifies:
1. Anti-AI tone compliance (strictly NO em dashes, no corporate buzzwords).
2. Platform compatibility (Windows 11 POSIX emulation, `.as_posix()` path normalization, safe file locking).
3. Structural formatting and syntax validity.

#### Step 4: Compose and Record Experience
Once validated:
1. Merge the candidate modification into the destination harness file (skill, rule, or script).
2. Record the 4-part lesson in the persistent Experience Library:

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" experience add `
  --title "Descriptor" `
  --cue "When running tool X under condition Y" `
  --lesson "Use parameter Z instead of W" `
  --evidence "Baseline produced exit code 1; probe completed with code 0" `
  --confidence high
```

---

## Querying Persistent Experience

To review existing verified lessons stored across agent conversations:

```powershell
python "C:\Users\danny\.gemini\config\plugins\harness2\scripts\harness2_core.py" experience list
```
