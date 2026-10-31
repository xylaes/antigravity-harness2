# Harness2 Agent Rules & Invariants

These rules govern agent behavior when running recursive harness optimization cycles based on Google Research Harness2 (arXiv:2610.14224).

## 1. Frozen Model Principle

The foundation model weights are completely frozen. Never attempt or suggest fine-tuning or weight adjustments. Agent capabilities, stability, and domain adaptation are improved exclusively through modifications to the agent harness:
1. System Prompts
2. Guardrails & Invariants
3. Persistent Memory & Scratchpads
4. Procedural Skills
5. Tool Guidance & Schema Notes
6. Deterministic Scripts & Verification Code
7. Subagent Architectures
8. Middleware & Plugins

## 2. Dual-Recursion Cycle Requirements

### Task-Level Recursion: Propose - Probe - Compose
When an agent encounters repetitive tool failures, execution friction, or format drift:
- **Propose**: Generate contrastive modifications. Split edits cleanly into invariant modifications (general rules or guardrails) and domain modifications (specific APIs, libraries, or task definitions).
- **Probe**: Execute candidate harness files under sandbox and platform constraints before deployment. Check for syntax validity, platform compatibility, and guardrail compliance.
- **Compose**: Merge passing probe changes into active harness files. Discard modifications that fail probe tests or violate safety boundaries.

### Harnessing-Level Recursion: Experience Library
Store verified behavioral lessons in the persistent Experience Library.
Every experience entry must strictly follow the four-part schema:
- **cue**: The specific context or error trigger that activated the issue.
- **lesson**: The exact, actionable instruction or code pattern required to succeed.
- **evidence**: The empirical contrast observed between the failed base run and the passing probe.
- **confidence**: Confidence level (high, medium, or provisional).

## 3. Platform & Voice Invariants

1. **Anti-AI Formatting**:
   - Strictly NO em dashes (Unicode U+2014) in agent responses, docs, or generated code. Use standard hyphens (-), commas, colons, or parentheses.
   - Avoid empty corporate buzzwords (such as l-e-v-e-r-a-g-e, s-p-e-a-r-h-e-a-d, d-e-l-i-g-h-t-e-d, e-s-t-e-e-m-e-d, t-e-s-t-a-m-e-n-t). Speak directly as an experienced tech peer.

2. **Windows 11 Execution Rules**:
   - POSIX file locking (`fcntl.flock`) is unavailable on Windows. Always use `msvcrt` or fallback wrappers.
   - Path operations must normalize backslashes to forward slashes with `.as_posix()` when interacting with cross-platform dictionary structures.
   - Sandboxed PowerShell sessions isolate network access. Commands requiring outbound connections (like package downloads) must run with sandbox bypass.
