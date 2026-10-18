# Capability Matrix

**Evidence key:** ✅T = verified by a test in this lab · ✅D = documented in README/docs and present in source (grep evidence, `logs/` + repo) but **not tested here** · ◐ = partial / via adapter · — = not a feature.
No AI-powered capability has been tested yet (Level 3 not approved), so every LLM-driven row is ✅D at most.

Local-model evidence comes from source grep (files mentioning `ollama` / `litellm` / OpenAI-compatible base URL), not marketing.

| | Vuln discovery | Static code analysis | Dynamic testing | LLM red teaming | AI models | Local models | Multi-agent | Reporting formats | API | Integration options |
|---|---|---|---|---|---|---|---|---|---|---|
| **H01 VVAH** | ✅D (S1–S9 pipeline: threat model, discovery, adversarial verify) | ✅D (LLM + tree-sitter code graph) | ◐D (optional exploit verification, off by default) | — | Anthropic, any OpenAI-compatible endpoint, or Claude Code/Codex/Gemini CLIs | ◐D (open-weight via OpenAI-compatible endpoint; no native Ollama) | ✅D (per-role agents) | SARIF, structured JSON/MD | CLI; MCP refs in source | SARIF → CI/code scanning |
| **H02 VulnHuntr** | ✅D (Python-only remote-exploitable: LFI, RCE, SSRF, XSS, SQLi, AFO, IDOR) | ✅D (LLM call-chain tracing) | — | — | Claude, GPT | ✅D (`-l ollama`) | — | Console/log text | CLI | Wrap CLI output |
| **H03 Strix** | ✅D | ◐D | ✅D (agents run tools in Docker sandbox against a target) | — | Via LiteLLM (many providers) | ✅D (LiteLLM/Ollama) | ✅D | Run reports; SARIF refs in source | CLI, MCP | CI mode documented |
| **H04 PentAGI** | ✅D | — | ✅D (autonomous pentest; tools in containers) | — | Many providers | ✅D (Ollama heavily referenced) | ✅D | Web UI reports | GraphQL/REST | Langfuse/observability stacks |
| **H05 Shannon** | ✅D | ◐D (white-box source-aware) | ✅D (**executes real exploits**) | — | Anthropic primarily | ◐D (few refs) | ✅D (Temporal workflows) | MD reports; SARIF in source | CLI | Temporal |
| **H06 PentestGPT** | ✅D (CTF/pentest) | — | ✅D | — | Claude Code / Codex CLI backends; legacy: OpenAI, Gemini, DeepSeek, Qwen… | ✅D (legacy mode: Ollama) | ◐D (supervisor/executor loop) | Logs/episodes | CLI, MCP tool server ✅T (unit tests) | MCP |
| **H07 SWE-agent** | ◐ (can triage issues) | — | — | — | Via LiteLLM | ✅D | — | Trajectories | CLI, Python | Batch mode, SWE-bench |
| **H08 Inspect AI** | — | — | — | ✅D (evals, agent benchmarks, sandboxed tools) | Nearly all providers | ✅D (Ollama, vLLM, etc.) | ✅D (agent solvers) | `.eval` logs ✅T, viewer | Python API ✅T | Eval sets; strong for scoring other tools |
| **H09 Promptfoo** | — | ◐D (code-scan action) | ◐ (HTTP target testing) | ✅D (red-team plugins: injection, jailbreak, PII…). Harness mechanics ✅T (echo) | Nearly all providers | ✅D (Ollama) | — | JSON ✅T, HTML, CSV, SARIF refs | CLI, Node API | CI/GitHub Action |
| **H10 Garak** | — | — | — | ✅D (probes: injection, jailbreak, leakage, toxicity…). Probe/detector loop ✅T (test.Blank) | Many generators | ✅D (Ollama, HF local) | — | JSONL ✅T + HTML ✅T | CLI, Python | Report JSONL ingest |
| **H11 PyRIT** | — | — | — | ✅D (attack orchestration, converters, scorers). Converter ✅T | Azure/OpenAI + others | ✅D (Ollama, LiteLLM refs) | ✅D (multi-turn attacks) | DB memory, outputs | Python API ✅T, `pyrit_scan` | Python library |
| **H12 OpenHands** | ◐ | — | — | — | Any (LiteLLM) | ✅D | ◐D (multiple sandboxes) | Conversations | Agent server API | ACP agents (Claude Code, Codex…) |
| **H13 Aider** | — | — | — | — | Any (LiteLLM) | ✅D (Ollama) | — | Git commits | CLI, scripting | Patch generation |
| **H14 Semgrep** | ✅T (rule-based) | ✅T (12/12 seeded hits) | — | — | — (Pro/Assistant AI is cloud, not used) | n/a | — | JSON ✅T, SARIF ✅T | CLI | CI, SARIF |
| **H15 Opengrep** | ✅T | ✅T (identical 12 hits) | — | — | — | n/a | — | JSON ✅T, SARIF ✅T | CLI | Drop-in Semgrep rule compat ✅T |
| **H16 ZAP** | ✅D (DAST) | — | ✅D (spider, passive/active scan) | — | — | n/a | — | HTML/XML/JSON (SARIF only via separate add-on, not verified) | REST API, Automation Framework | CI, Docker |
| **H17 LangGraph** | — | — | — | — | Any (via LangChain) | ✅D | ✅D | — | Python ✅T | **Checkpoint + `interrupt()` approval gate ✅T** |
| **H18 AutoGen** | — | — | — | — | Many | ✅D (Ollama ext) | ✅D (teams) | — | Python ✅T (replay client) | Maintenance mode |
| **H19 CrewAI** | — | — | — | — | Many (LiteLLM) | ✅D | ✅D (role-based crews) | — | Python (construction ✅T only) | Flows |

## Finding-confidence classes (§13)
Only one class exists in the lab so far: **static-analysis-supported findings** (Semgrep/Opengrep on the synthetic fixture, 12 each, matching the seeded vulnerabilities). There are no LLM-suggested, test-confirmed, or human-validated findings yet.

## Safety-relevant capability notes
- **Active exploitation by design:** Shannon, PentAGI, Strix, PentestGPT. Keep these behind a separate authorization boundary (Level 4 only).
- **Edits source code:** VVAH `--remediate`/S10, SWE-agent, Aider, OpenHands. Never point them at real projects without review.
- **Built-in human gates:** VVAH (`--stop-after`, S10/S11 off by default), LangGraph `interrupt()` (tested), Inspect `approval` policies (documented).
