# System Inventory

Collected 2026-10-13 (local) by Phase 1 discovery. Raw commands: `uname`, `sw_vers`, `sysctl`, `df`, `system_profiler`, `<tool> --version`.

| Item | Value |
|---|---|
| OS | macOS 27.0.1 (build 26A434), Darwin 27.0.0 |
| Architecture | arm64 (Apple Silicon) |
| CPU | Apple M5 Pro, 15 cores |
| RAM | 24 GB unified (low free pages at discovery time; other apps running) |
| GPU | Apple M5 Pro integrated, 16 GPU cores, Metal 4. No NVIDIA/CUDA. VRAM is shared with system RAM |
| Disk | 926 GiB volume, 732 GiB free at start (lab now uses ~19 GB) |
| Git | 2.55.0 |
| Python | 3.12.14 (pyenv, global). **Added lab-local only** via uv: 3.10.21, 3.11.16, 3.13.15 in `environments/python` |
| uv | 0.12.19 (Homebrew) |
| pipx | **missing**, so `uv tool` (lab-scoped `UV_TOOL_DIR`) used instead |
| Poetry | **missing**, so VulnHuntr installed from its hash-pinned `requirements.txt` (exported from poetry.lock) |
| Node.js / npm | v24.21.0 / 11.19.0 |
| Docker CLI / Compose | 29.8.0 / v5.5.1. **Daemon not running** (Docker Desktop not started) |
| Java | **missing**, which blocks OWASP ZAP (needs Java 17+) |
| Go | missing (only needed to build PentAGI from source; not required for its Docker deployment) |
| GNU Make | 3.81 |
| Local LLM servers | Ollama installed, **not running**, no models listed. vLLM not present |
| Network | GitHub and PyPI reachable (HTTP 200). No proxy detected |
| AI CLIs present | `claude` (Claude Code) on PATH. Note VVAH and PentestGPT can drive it as a backend; it was hidden from tests via fake `$HOME` |

## Missing dependencies

| Missing | Impact | Fix (needs your approval) |
|---|---|---|
| Docker daemon | Can't run Strix sandbox, PentAGI, Shannon, OpenHands sandbox, SWE-agent, or ZAP container | Start Docker Desktop (no sudo) |
| Java 17+ | ZAP desktop/daemon can't run | `brew install --cask temurin` (system-wide) **or** use ZAP Docker image `zaproxy/zap-stable` |
| Poetry, pipx | None. Worked around with uv | Optional |
| Ollama running + model | No local-LLM testing yet | `ollama serve` + `ollama pull <model>` (~5–20 GB per model) |
| cosign | Opengrep signature not cryptographically verified (SHA-256 digest matched GitHub's asset digest) | `brew install cosign` |

## Compatibility concerns

- **No CUDA.** Local models run via Ollama/MLX on Metal only. 24 GB unified RAM practically caps comfortable local models at roughly 14B–32B quantized, which is weak for agentic security work compared with frontier models.
- **Docker-on-Mac is a VM.** Pentest stacks (PentAGI, Shannon, Strix) will run under Docker Desktop's Linux VM. PentAGI's default compose mounts the Docker socket **as root**, which is prohibited without explicit approval.
- **Memory pressure.** Don't run PentAGI (multi-container: Postgres/pgvector, etc.) alongside OpenHands or a local LLM on 24 GB.
- **Python versions matter.** Aider breaks on 3.13 (`pydub` needs removed `audioop`) and was reinstalled on 3.12. VulnHuntr requires 3.10.
