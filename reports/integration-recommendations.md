# Integration Recommendations

## Recommendation: start with a plain Python controller and SARIF as the common format; add LangGraph when you need approvals

The simplest thing that meets the requirements:

```text
fixture / approved repo
   │
   ├─► Semgrep + Opengrep (local rules, offline)  ──► SARIF   ✅ tested
   ├─► VVAH scan --stop-after s9 (LLM)            ──► SARIF   (needs approval: model, spend cap)
   └─► VulnHuntr (Python repos only, LLM)          ──► text → normalise
                     │
                     ▼
         merge + dedupe SARIF (rule/file/line)  ──► triage queue
                     │
           HUMAN REVIEW  (LangGraph interrupt() gate: tested offline)
                     │ approved findings only
                     ▼
         fix proposal: Aider / SWE-agent in a throwaway git worktree of a COPY
                     │
         regression tests ──► report (MD + SARIF)

AI-app track (separate):  Promptfoo (regression + red-team plugins) · Garak (probe sweep) · PyRIT (multi-turn attacks)
                          ──► Inspect AI as the scoring / reproducibility layer
```

### Why this shape
- **SARIF is already shared.** Semgrep, Opengrep and VVAH emit it (Semgrep/Opengrep verified here), so merging is a ~30-line script and needs no framework.
- **Static first, LLM second.** Free deterministic scanners give a baseline; VVAH and VulnHuntr add LLM-suggested findings, labelled as such (§13 classes kept separate in the triage record).
- **LangGraph for the gate.** The offline test proved checkpointing plus `interrupt()`/`Command(resume=…)`, which is exactly the "human approves before fix" step. Adopt it once the plain script needs durable state across reviews. Until then, a CLI prompt is enough.
- **AutoGen:** don't build on it. It's in maintenance mode.
- **CrewAI:** fine, but adds role/backstory abstraction this pipeline doesn't need.

### Hard boundaries in the design
1. Pentest tools (Shannon, PentAGI, Strix, PentestGPT agent) are **not wired into the pipeline**. They run only as separate, manually started Level-4 jobs against an isolated, user-owned target in Docker, with no host Docker socket.
2. Fix agents never touch the original repo: they work on a copy, output a patch, and a human applies it.
3. Any stage that sends code to a cloud model is opt-in per run, with a token or spend cap (VVAH `estimate` first).
4. All tool runs reuse `configs/smoke.sh`-style isolation (fake `$HOME`, network allowed only to the chosen model endpoint).

## Integration readiness per tool

| Tool | Ready to integrate? | Interface | Next step |
|---|---|---|---|
| Semgrep / Opengrep | **Yes** | CLI → SARIF/JSON | Write fuller rule pack or vendor registry rules offline |
| VVAH | After L3 approval | CLI → SARIF | `estimate`, then `scan --stop-after s9` on fixture |
| VulnHuntr | After L3 approval | CLI → text | Python-only; stale upstream, so low priority |
| Promptfoo | **Yes (offline)** | CLI/Node → JSON | Point at an LLM app you own |
| Garak | **Yes (offline)** | CLI → JSONL | Point at a local Ollama model first (no cost) |
| Inspect AI | **Yes (offline)** | Python → `.eval` | Use as the scorer for comparing tools |
| PyRIT | Library ready | Python | Multi-turn attack scenarios vs local model |
| LangGraph | **Yes** | Python | Wrap the controller once approvals are needed |
| Aider / SWE-agent | After L3 approval | CLI | Patch-only mode on a copy |
| Strix / PentAGI / Shannon / ZAP | Level 4 only | Docker | Needs Docker daemon + target approval |
