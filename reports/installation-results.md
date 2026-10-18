# Installation Results

Every Python tool has its **own** venv or uv-tool env. All interpreters, tools, caches and Node packages live under `environments/`. Nothing was installed system-wide; no `sudo`; no remote install scripts run. Env config: `configs/lab.env`. Install logs: `logs/install-*.log`.

"Installed" means dependencies resolved and the CLI or package loads. Status reflects the smoke tests in `smoke-test-results.md`.

| ID | Harness | Cloned | Installed | Version | Environment | Status | Blocker / notes |
|---|---|---|---|---|---|---|---|
| H01 | VVAH | Yes | Yes | 1.5.0 | `environments/vvah` (py3.11, `pip install .` from source) | PASS | Scans need an API key (Anthropic or OpenAI-compatible) or the logged-in `claude` CLI. `setup` reports exactly that |
| H02 | VulnHuntr | Yes | Yes | 0.1.0 | `environments/vulnhuntr` (py3.10, hash-pinned `requirements.txt` + `--no-deps` source) | PASS | Poetry absent. A plain `pip install .` **misses `requests`** (upstream packaging gap); pinned reqs fix it |
| H03 | Strix | Yes | Yes | 1.7.0 (PyPI `strix-agent`) | `uv tool` (`environments/uv-tools/strix-agent`) | PASS (L1) | Real use needs a running Docker daemon (pulls sandbox image) + LLM key. Remote installer not used |
| H04 | PentAGI | Yes | No (Docker-only) | v2.2.0 (repo) | Docker Compose (not started) | PASS (config validates) / NOT TESTED (runtime) | Docker daemon off. **Default compose mounts `/var/run/docker.sock` as `root`**, prohibited without approval. ≥20 GB disk |
| H05 | Shannon | Yes | No | v3.4.0 (repo) | none | BLOCKED | Documented entry is `npx @keygraph/shannon@latest` (download+execute), which needs your approval. Also needs Docker + LLM creds. Compose file validates |
| H06 | PentestGPT | Yes | Yes | 1.0.0 | `repos/PentestGPT/.venv` + `pentestgpt_agent/.venv` (`make install` → `uv sync`, py3.12) | PASS | Agent mode drives Claude Code / Codex CLIs. Git dependency from `PentestGPT-Project/UnifedAgentWrapper` pinned by SHA |
| H07 | SWE-agent | Yes | Yes | 1.1.0 (source) | `environments/swe-agent` (py3.11, `pip install -e .`) | PASS (L1) | Runs need Docker (SWE-ReX sandbox) + LLM. Upstream says most effort is now on mini-swe-agent |
| H08 | Inspect AI | Yes | Yes | 0.3.280 | `environments/inspect_ai` (py3.12, `-e .[dev]`) | PASS | Shallow clone has no tags, so setuptools-scm gave 0.1.dev1 and the `[dev]` resolve failed. Fixed by checking out tag `0.3.280`. Needs a pre-seeded tiktoken cache for offline runs |
| H09 | Promptfoo | Yes | Yes | 0.124.1 | `environments/promptfoo` (npm `--prefix`, pinned) | PASS | Telemetry and update check disabled via env |
| H10 | Garak | Yes | Yes | 0.17.1.pre1 (source) | `environments/garak` (py3.12, `-e .`) | PASS | `--probes` CLI flag is deprecated since 0.15 (still works) |
| H11 | PyRIT | Yes | Yes | 1.2.0.dev0 (source) | `environments/pyrit` (py3.12, `-e .`) | PASS | Main branch (latest release is v1.1.0). Use `pip install pyrit==1.1.0` for a stable pin |
| H12 | OpenHands | Yes | Yes (CLI only) | agent-canvas 1.27.1 | `environments/openhands` (npm `--prefix`) | PASS (L1) / NOT TESTED (runtime) | Not started. Option 1 gives agent **full filesystem access**; Option 2 needs Docker. Approval required |
| H13 | Aider | Yes | Yes | 0.86.2 | `uv tool` (py3.12) | PASS | First install on py3.13 **failed at runtime** (`pyaudioop` missing). Reinstalled on 3.12 |
| H14 | Semgrep | Yes | Yes | 1.180.0 | `uv tool` | PASS | `--metrics off`, version check disabled. No cloud login |
| H15 | Opengrep | Yes | Yes | 1.30.2 | `environments/opengrep` (official release binary) | PASS | `install.sh` reviewed but **not used** (writes to `~/.opengrep`, `~/.local/bin`). SHA-256 matches GitHub asset digest. No SLSA attestation; cosign absent so `.sig` unverified |
| H16 | OWASP ZAP | Yes | No | v2.17.0 (repo) | none | BLOCKED | Java 17+ missing and Docker daemon off. Both fixes need approval |
| H17 | LangGraph | Yes | Yes | 1.2.15 (PyPI stable) | `environments/langgraph` (py3.12) | PASS | |
| H18 | AutoGen | Yes | Yes | agentchat/ext 0.7.5 (PyPI) | `environments/autogen` (py3.12) | PASS | **Maintenance mode** upstream; successor is Microsoft Agent Framework |
| H19 | CrewAI | Yes | Yes | 1.15.27 (PyPI) | `environments/crewai` (py3.12) | PASS | Telemetry disabled via env (`CREWAI_DISABLE_TELEMETRY`) |

**Totals:** 19/19 cloned · 16 installed · 16 PASS on safe tests · 2 BLOCKED (Shannon, ZAP) · PentAGI config-validated but deliberately not deployed.

## Disk usage
`repos/` 3.9 GB · `environments/` ~15 GB (incl. 4.9 GB uv cache, 1.5 GB npm cache, both safe to delete).

## Things that touched paths outside the lab
- `uv python install` created 3 symlinks in `~/.local/bin` (python3.10/3.11/3.13) before `UV_PYTHON_BIN_DIR` was set. **Removed immediately**; now pinned to `environments/bin`.
- `~/.cache/uv` gained new entries during the session (cache only, not installed packages). Couldn't attribute them with certainty and left them alone. Safe to prune with `uv cache prune`.
- `~/.cache/gh`: `gh api` metadata lookups.
- Docker smoke tests read `~/.docker` (to find the compose plugin). Read-only.
