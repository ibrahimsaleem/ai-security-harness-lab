# Smoke-Test Results

All commands ran under `sandbox-exec` with **all IP traffic, socket bind and inbound denied**, a lab-local fake `$HOME` (`artifacts/home`, so no real credentials or CLI logins were reachable), stdin closed and a 300 s timeout. Runner: `configs/smoke.sh`. Raw table: `logs/smoke-results.tsv`.

**Network access during tests: none (enforced).** **AI tokens consumed: 0 paid** (Inspect mockllm counted 35 local mock tokens; Promptfoo echo provider 0).

| # | Project | Lvl | Command | Start (UTC) | s | Exit | Result | Relevant output | Log |
|---|---|---|---|---|---|---|---|---|---|
| 1 | vvah | 1 | `environments/vvah/bin/vvaharness --version` | 2026-10-14T03:20:24Z | 0 | 0 | PASS | Visa Vulnerability Agentic Harness 1.5.0 | `logs/smoke/vvah-1.log` |
| 2 | vvah | 1 | `environments/vvah/bin/vvaharness --help` | 2026-10-14T03:20:24Z | 0 | 0 | PASS | Run `vvaharness <command> --help` for a command's own options. | `logs/smoke/vvah-2.log` |
| 3 | vvah | 2 | `environments/vvah/bin/vvaharness setup` | 2026-10-14T03:20:24Z | 1 | 1 | PASS (diagnostic works; exit 1 = "Not ready: 3 blocking" — all are missing API keys) | Not ready: fix the 3 blocking item(s) above, then `vvaharness scan`. | `logs/smoke/vvah-3.log` |
| 4 | vvah | 2 | `environments/vvah/bin/vvaharness estimate --repo fixtures/sample-vulnerable-app` | 2026-10-14T03:20:25Z | 1 | 0 | PASS | --stop-after s3 for the final inventory. Cost depends on model pricing. | `logs/smoke/vvah-4.log` |
| 5 | vulnhuntr | 1 | `environments/vulnhuntr/bin/vulnhuntr --help` | 2026-10-14T03:20:26Z | 1 | 0 | PASS | -v, --verbosity       Increase output verbosity (-v for INFO, -vv for DEBUG) | `logs/smoke/vulnhuntr-1.log` |
| 6 | strix | 1 | `strix --help` | 2026-10-14T03:20:28Z | 0 | 0 | PASS | strix completions SHELL  Generate zsh, bash, or fish tab completion | `logs/smoke/strix-1.log` |
| 7 | strix | 1 | `strix --version` | 2026-10-14T03:20:28Z | 0 | 0 | PASS | strix 1.7.0 | `logs/smoke/strix-2.log` |
| 8 | pentestgpt | 1 | `repos/PentestGPT/.venv/bin/pentestgpt-legacy --help` | 2026-10-14T03:20:28Z | 1 | 0 | PASS | --version             show program's version number and exit | `logs/smoke/pentestgpt-1.log` |
| 9 | pentestgpt | 2 | `cd repos/PentestGPT && .venv/bin/python -m pytest tests -q -p no:cacheprovider -m 'not liv…` | 2026-10-14T03:20:28Z | 1 | 0 | PASS | 133 passed in 0.83s | `logs/smoke/pentestgpt-2.log` |
| 10 | pentestgpt | 2 | `cd repos/PentestGPT/pentestgpt_agent && .venv/bin/python -m pytest -q -p no:cacheprovider …` | 2026-10-14T03:20:30Z | 1 | 0 | PASS | 115 passed in 0.31s | `logs/smoke/pentestgpt-3.log` |
| 11 | swe-agent | 1 | `environments/swe-agent/bin/sweagent --help` | 2026-10-14T03:20:30Z | 0 | 0 | PASS | quick-stats or qs: Calculate quick stats from a directory of trajectories | `logs/smoke/swe-agent-1.log` |
| 12 | inspect_ai | 1 | `environments/inspect_ai/bin/inspect --version` | 2026-10-14T03:20:30Z | 1 | 0 | PASS | 0.3.280 | `logs/smoke/inspect_ai-1.log` |
| 13 | inspect_ai | 1 | `environments/inspect_ai/bin/inspect --help` | 2026-10-14T03:20:31Z | 0 | 0 | PASS | view        Inspect log viewer. | `logs/smoke/inspect_ai-2.log` |
| 14 | inspect_ai | 2 | `environments/inspect_ai/bin/inspect eval configs/inspect_mock_task.py --model mockllm/mode…` | 2026-10-14T03:20:32Z | 2 | 0 | FAIL (exit 0 but eval status=error: tiktoken download blocked by sandbox) | .eval | `logs/smoke/inspect_ai-3.log` |
| 15 | promptfoo | 1 | `promptfoo --version` | 2026-10-14T03:20:34Z | 1 | 0 | PASS | 0.124.1 | `logs/smoke/promptfoo-1.log` |
| 16 | promptfoo | 1 | `promptfoo --help` | 2026-10-14T03:20:35Z | 1 | 0 | PASS | help [command]                   display help for command | `logs/smoke/promptfoo-2.log` |
| 17 | promptfoo | 2 | `promptfoo eval -c configs/promptfoo-echo.yaml --no-cache --no-progress-bar -o artifacts/ou…` | 2026-10-14T03:20:35Z | 0 | 0 | PASS | Writing output to /Users/ibrahim/Developer/ai-security-harness-lab/artifacts/out/promptfoo-echo.json | `logs/smoke/promptfoo-3.log` |
| 18 | garak | 1 | `environments/garak/bin/garak --version` | 2026-10-14T03:20:36Z | 1 | 0 | PASS | garak LLM vulnerability scanner v0.17.1.pre1 ( https://github.com/NVIDIA/garak ) at 2026-10-13T22:20:36.269170 | `logs/smoke/garak-1.log` |
| 19 | garak | 1 | `environments/garak/bin/garak --help` | 2026-10-14T03:20:36Z | 0 | 0 | PASS | See https://github.com/NVIDIA/garak | `logs/smoke/garak-2.log` |
| 20 | garak | 2 | `environments/garak/bin/garak --target_type test.Blank --probes test.Test --report_prefix l…` | 2026-10-14T03:20:36Z | 0 | 0 | PASS | ✔️  garak run complete in 0.29s | `logs/smoke/garak-3.log` |
| 21 | pyrit | 1 | `environments/pyrit/bin/python -c 'import pyrit; print(pyrit.__version__)'` | 2026-10-14T03:20:36Z | 0 | 0 | PASS | 1.2.0.dev0 | `logs/smoke/pyrit-1.log` |
| 22 | pyrit | 1 | `environments/pyrit/bin/pyrit_scan --help` | 2026-10-14T03:20:36Z | 0 | 0 | PASS | stop-server         Stop the backend server | `logs/smoke/pyrit-2.log` |
| 23 | pyrit | 2 | `environments/pyrit/bin/python -c 'import asyncio; from pyrit.prompt_converter import Base6…` | 2026-10-14T03:20:37Z | 0 | 1 | TEST-AUTHOR ERROR (module renamed to pyrit.converter in 1.x); superseded by next row | ModuleNotFoundError: No module named 'pyrit.prompt_converter' | `logs/smoke/pyrit-3.log` |
| 24 | openhands | 1 | `environments/openhands/node_modules/.bin/agent-canvas --help` | 2026-10-14T03:20:37Z | 0 | 0 | PASS | OH_AGENT_SERVER_LOCAL_PATH=/path/to/sdk npx @openhands/agent-canvas | `logs/smoke/openhands-1.log` |
| 25 | aider | 1 | `aider --version` | 2026-10-14T03:20:37Z | 2 | 0 | PASS | aider 0.86.2 | `logs/smoke/aider-1.log` |
| 26 | aider | 1 | `aider --help` | 2026-10-14T03:20:39Z | 1 | 0 | PASS | override defaults. | `logs/smoke/aider-2.log` |
| 27 | semgrep | 1 | `semgrep --version` | 2026-10-14T03:20:39Z | 0 | 0 | PASS | 1.180.0 | `logs/smoke/semgrep-1.log` |
| 28 | semgrep | 2 | `semgrep scan --metrics off --disable-version-check --config configs/lab-rules.yml --json -…` | 2026-10-14T03:20:40Z | 1 | 0 | PASS | Ran 9 rules on 6 files: 12 findings. | `logs/smoke/semgrep-2.log` |
| 29 | opengrep | 1 | `opengrep --version` | 2026-10-14T03:20:41Z | 1 | 0 | PASS | 1.30.2 | `logs/smoke/opengrep-1.log` |
| 30 | opengrep | 2 | `opengrep scan --config configs/lab-rules.yml --json -o artifacts/out/opengrep.json --sarif…` | 2026-10-14T03:20:42Z | 1 | 0 | PASS | Ran 9 rules on 6 files: 12 findings. | `logs/smoke/opengrep-2.log` |
| 31 | langgraph | 2 | `environments/langgraph/bin/python configs/langgraph_offline.py` | 2026-10-14T03:20:43Z | 1 | 0 | PASS | langgraph offline OK: {'findings': ['lab-sqli-string-format', 'APPROVED'], 'approved': True} | `logs/smoke/langgraph-1.log` |
| 32 | autogen | 2 | `environments/autogen/bin/python configs/autogen_offline.py` | 2026-10-14T03:20:43Z | 0 | 0 | PASS | autogen offline OK: Finding confirmed: SQLi in db.py | `logs/smoke/autogen-1.log` |
| 33 | crewai | 1 | `environments/crewai/bin/crewai version` | 2026-10-14T03:20:44Z | 0 | 0 | PASS | crewai version: 1.15.27 | `logs/smoke/crewai-1.log` |
| 34 | crewai | 2 | `environments/crewai/bin/python configs/crewai_offline.py` | 2026-10-14T03:20:44Z | 2 | 0 | PASS | crewai offline OK: crew constructed, process = Process.sequential | `logs/smoke/crewai-2.log` |
| 35 | pentagi | 2 | `cd repos/pentagi && docker compose --env-file .env.example -f docker-compose.yml config --…` | 2026-10-14T03:20:45Z | 0 | 0 | PASS |  | `logs/smoke/pentagi-1.log` |
| 36 | shannon | 2 | `cd repos/shannon && docker compose -f docker-compose.yml config --quiet` | 2026-10-14T03:20:45Z | 0 | 0 | PASS |  | `logs/smoke/shannon-1.log` |
| 37 | pyrit | 2 | `environments/pyrit/bin/python -c 'import asyncio; from pyrit.converter import Base64Conver…` | 2026-10-14T03:21:02Z | 0 | 0 | PASS | converter OK bGFi | `logs/smoke/pyrit-4.log` |
| 38 | inspect_ai | 2 | `environments/inspect_ai/bin/inspect eval configs/inspect_mock_task.py --model mockllm/mode…` | 2026-10-14T03:21:45Z | 1 | 0 | PASS (eval status=success, accuracy 1.0) | .eval | `logs/smoke/inspect_ai-4.log` |

## Verification beyond exit codes

- **Inspect AI**: first two runs exited 0 but the eval log status was `error` (tiktoken tried to download `o200k_base` → blocked by sandbox). Fixed by pre-seeding `environments/.tiktoken-cache`; final run: status `success`, accuracy 1.0. *Exit code alone was misleading — eval log status was checked directly.*
- **Semgrep / Opengrep**: 12 findings each, 0 errors, identical rule/file hits covering all 9 seeded categories (see `artifacts/out/*.json|sarif`).
- **Promptfoo**: 1/1 assertions passed with `echo` provider; tokenUsage total 0.
- **Garak**: `test.Test` probe vs `test.Blank` generator → `always.Pass: PASS ok on 40/40`; report in `artifacts/home/.local/share/garak/garak_runs/`.
- **PentestGPT**: root suite 133 passed; `pentestgpt_agent` suite 115 passed. Excluded: `live` marker (spends tokens), `docker` marker, and `test_local_target.py` / `test_local_benchmark.py` (start a vulnerable SSTI server on localhost and attack it — needs approval per §2).
- **LangGraph**: StateGraph + InMemorySaver checkpoint + `interrupt()` human-approval gate resumed with `Command(resume=True)` → asserted output.
- **AutoGen**: AssistantAgent with `ReplayChatCompletionClient` (no API) → asserted reply.
- **CrewAI**: Agent/Task/Crew constructed with fake key; `kickoff()` deliberately not called (it would call an LLM). Construction-only test.
- **PentAGI / Shannon**: `docker compose config --quiet` validates (daemon not running; nothing pulled or started).

## Level 3: local model (approved 2026-10-14)
Target: `llama3.1:8b` via Ollama 0.34.4 on 127.0.0.1:11434 (model ID 46e0c10c039e). Sandbox allowed **only** `localhost:11434`; all other network blocked. **Paid tokens: 0** (local inference only).

| Tool | Config | Result | Log / artifact |
|---|---|---|---|
| Promptfoo | `configs/promptfoo-ollama.yaml`, 5 secret-leak tests, deterministic asserts, temp 0 | 5/5 PASS (no secret leaked); 351 local tokens | `artifacts/out/promptfoo-ollama.json` |
| Garak | `promptinject.HijackHateHumans` + `encoding.InjectBase64`, ≤20 prompts each, 1 generation | **promptinject: 55% attack success (9/20 resisted)**; encoding DecodeMatch 0% (20/20), DecodeApprox 10% (18/20) | `artifacts/home/.local/share/garak/garak_runs/lab-ollama.report.{jsonl,html}` |

Notes: the first attempt at each failed due to a quoting bug in my command (unexpanded `$A`/`$E`), not a tool fault. These are small samples (20 prompts), so use them as smoke-level signal, not a benchmark.
