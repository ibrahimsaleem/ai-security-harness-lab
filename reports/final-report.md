# Final Report: AI Security Harness Lab

Lab: `~/Developer/ai-security-harness-lab` · Date: 2026-10-13 · Spec: `AGENTS.md` (plaintext of the provided `Agent.md` RTF)

## 1. Executive summary
- **19/19 repositories cloned**, commit SHAs and licenses recorded (`repository-inventory.md`).
- **16 tools installed** in isolated, lab-local environments and **passed safe smoke tests** (38 sandboxed test runs, 0 network, 0 paid tokens).
- **2 blocked:** Shannon (its only documented entry is `npx …@latest`, which needs approval) and OWASP ZAP (no Java, Docker daemon off).
- **PentAGI:** compose config validates. Deliberately not deployed, because the default config mounts the Docker socket as root.
- **No AI-powered or active security test was run.** Level 3/4 await your approval (§14 below).
- Only verified security findings: Semgrep and Opengrep each found **12/12** seeded issues in the synthetic fixture, identically.

## 2. System compatibility
Apple M5 Pro (arm64), 24 GB RAM, 732 GB free, macOS 27. Compatible with every tool on paper. Real constraints: the **Docker daemon isn't running**, **Java is missing**, there is **no CUDA**, and 24 GB RAM limits local LLMs and concurrent Docker stacks. Details: `system-inventory.md`.

## 3. Successfully installed (PASS)
VVAH 1.5.0 · VulnHuntr 0.1.0 · Strix 1.7.0 · PentestGPT 1.0.0 · SWE-agent 1.1.0 · Inspect AI 0.3.280 · Promptfoo 0.124.1 · Garak 0.17.1.pre1 · PyRIT 1.2.0.dev0 · OpenHands agent-canvas 1.27.1 (CLI only) · Aider 0.86.2 · Semgrep 1.180.0 · Opengrep 1.30.2 · LangGraph 1.2.15 · AutoGen 0.7.5 · CrewAI 1.15.27

## 4. Failed or blocked installs

| Tool | Status | Why | Unblock |
|---|---|---|---|
| Shannon | BLOCKED | `npx @keygraph/shannon@latest` downloads and executes code; needs approval. Also needs Docker + LLM creds | Approve a pinned version (e.g. `@3.4.0`) |
| OWASP ZAP | BLOCKED | No Java 17+; Docker daemon off | Approve Temurin JDK install **or** start Docker and use `zaproxy/zap-stable` |
| PentAGI | Config-only | Docker daemon off; root + host docker.sock by default | Approve Docker start + a socket-proxy or rootless design |

Issues found and fixed during install (none were real tool breakage):
1. Inspect `[dev]` failed to resolve because the shallow clone had no tags. Fixed by checking out release tag 0.3.280.
2. VulnHuntr crashed on missing `requests` (undeclared dependency). Fixed by using its pinned `requirements.txt`.
3. Aider crashed on Python 3.13 (`audioop`). Fixed by reinstalling on 3.12.
4. Inspect eval **silently failed** (exit 0, status `error`) while fetching a tiktoken file. Fixed by pre-seeding the cache. Lesson: check tool-native status, not just exit codes.

## 5. Verified functional tests (Level 2, offline)
- Semgrep and Opengrep: 9 local rules, 12 findings each, JSON + SARIF output, zero diffs between engines.
- Inspect AI: mock-LLM eval, status success, accuracy 1.0.
- Garak: `test.Test` probe vs `test.Blank`, PASS 40/40, JSONL + HTML report.
- Promptfoo: echo-provider eval, 1/1 assertions, 0 tokens.
- PentestGPT: 133 + 115 unit tests passed (live, docker and localhost-attack tests excluded).
- PyRIT: Base64 converter round-trip.
- LangGraph: checkpoint plus human-approval `interrupt()` and resume.
- AutoGen: agent run on the replay client.
- CrewAI: crew construction only.
- VVAH: `setup` readiness check (correctly reports no API key) and `estimate` on the fixture (no model calls).

## 6. Top 10 recommended projects (for this lab's goals)
1. **Semgrep**: verified, deterministic, SARIF, free baseline.
2. **VVAH**: most complete LLM code-vuln pipeline with built-in stop points and SARIF. Very active.
3. **Inspect AI**: best reproducible scoring and eval layer. Verified offline.
4. **Promptfoo**: LLM app regression and red-team. Verified offline.
5. **Garak**: broad LLM probe library. Verified offline.
6. **LangGraph**: orchestration with a verified human-approval gate.
7. **PyRIT**: multi-turn AI red-team library.
8. **Opengrep**: open fork with Semgrep rule compatibility (verified identical results). Use it if you want to avoid Semgrep licensing terms.
9. **Strix**: most active agentic AppSec tester. Level 4 only.
10. **Aider**: lightweight patch generator for the approved-fix step.

Not in the top 10: VulnHuntr (stale since 2025-02, Python-only), AutoGen (maintenance mode), Shannon and PentAGI (AGPL/EULA and heavy, active-exploit risk), SWE-agent (effort moved to mini-swe-agent), CrewAI (redundant with LangGraph), OpenHands (heavy, broad filesystem access).

## 7–10. Best by category
- **Source-code scanning:** Semgrep/Opengrep (static baseline) + VVAH (LLM, `--stop-after s9`). VulnHuntr only for Python and only as a second opinion.
- **AI red teaming:** Promptfoo (app-level, CI) + Garak (model-level probe sweep), scored and compared in Inspect AI. PyRIT for scripted multi-turn attacks.
- **Software remediation:** Aider (smallest blast radius, patch output). SWE-agent once Docker is on. VVAH S10 only on copies.
- **Orchestration framework:** LangGraph, adopted after a plain Python controller (see `integration-recommendations.md`).

## 11. Suggested architecture
See `integration-recommendations.md`: SARIF-centric controller → human gate → patch-only fix agents. AI-eval track runs separately. Pentest tools stay outside the pipeline behind a Level-4 boundary.

## 12. Estimated operational costs
- **Infrastructure:** $0 extra. Runs on this Mac; ~19 GB disk used now. Docker stacks (PentAGI etc.) add roughly 10–20 GB of images.
- **Static tools:** $0.
- **VVAH:** its own estimate for the 507-token fixture is a **252k–1M input-token budget for S1–S9** (fixed agent overhead dominates). Multiply by your chosen model's current per-token price. Real repos cost more; exploit verification and S10/S11 cost extra. Prompt caching lowers it.
- **Promptfoo/Garak/PyRIT:** roughly (number of probes or tests) × (prompt + response tokens). A full Garak sweep is thousands of prompts. Use a local Ollama model first for $0 API cost.
- **Local models:** $0 API, but 24 GB RAM limits you to small and medium quantized models. Expect noticeably weaker agentic results.

## 13. Security and privacy risks
- **Code disclosure:** VVAH, VulnHuntr, Aider and SWE-agent send source to the model provider. Use the fixture or approved repos only.
- **Active exploitation:** Shannon, PentAGI, Strix and PentestGPT run real attacks. Use isolated targets only, never the host or public IPs.
- **Docker socket:** PentAGI default = root + host docker.sock, which is effectively root on the Docker VM. Use a socket proxy or a separate VM.
- **Ambient credentials:** VVAH and PentestGPT auto-detect the `claude` / Codex CLI logins on this machine. Real runs outside the fake `$HOME` could spend your subscription or API quota without an explicit key. Keep running them under a lab `$HOME`.
- **Supply chain:** PentestGPT pulls a git dependency from a second org. Opengrep's signature wasn't verified (no cosign). `npx …@latest` patterns should be pinned.
- **Licensing:** Shannon and VulnHuntr are AGPL-3.0. PentAGI has an EULA. Semgrep and Opengrep are LGPL-2.1, and Semgrep registry rules have their own terms. AutoGen code is MIT and its docs are CC-BY-4.0.
- **Telemetry:** disabled via env for Semgrep, Promptfoo and CrewAI in lab configs. Re-check whenever new tools are added.

## 14. Exact next steps (each needs your approval)
1. **Level 3, cheapest first:** start `ollama serve`, pull one model, then run Garak + Promptfoo against it ($0 API).
2. **Level 3, VVAH:** choose a model/provider and a spend cap, then `vvaharness scan --repo fixtures/sample-vulnerable-app --stop-after s9`.
3. **Unblock Docker:** start Docker Desktop, then Strix `--help`-level checks, SWE-agent, and the ZAP container.
4. **Shannon:** approve `npx @keygraph/shannon@3.4.0 --help` (pinned).
5. **ZAP:** approve the JDK (brew cask) **or** the Docker image route.
6. **Level 4 (separate approval):** build an isolated vulnerable target container (e.g. OWASP Juice Shop on an internal Docker network) before any pentest tool runs.
7. Housekeeping: `uv cache prune` for the uv caches, and delete `environments/.npm-cache` if disk matters.

## Completion checklist (§16)
- [x] 19/19 clones attempted and succeeded, SHAs recorded
- [x] Every license reviewed (2 corrected manually: VVAH, AutoGen)
- [x] Every compatible tool had an isolated install attempt
- [x] Every installed tool has a smoke-test result
- [x] Blocked tools documented (Shannon, ZAP, PentAGI runtime)
- [x] No unauthorized security tests (localhost-attack tests explicitly excluded)
- [x] No existing user projects modified
- [x] No API charges (network blocked during all tests)
- [x] All 7 reports generated
