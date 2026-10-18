# AI Security Harness Lab

A reproducible local lab for installing, smoke-testing and comparing 19 open-source AI security harnesses, LLM red-team tools, static scanners and agent orchestration frameworks.

**Start here:** [`reports/AI-Security-Harness-Lab-Report.pdf`](reports/AI-Security-Harness-Lab-Report.pdf) (full per-repo details) or [`reports/final-report.md`](reports/final-report.md).

## Results at a glance

| | |
|---|---|
| Repositories cloned | 19 / 19 (commit SHA + license recorded) |
| Installed in isolated envs | 16 |
| Passed safe smoke tests | 16 |
| Blocked | Shannon (pending approval to run `npx`), OWASP ZAP (no Java / Docker off) |
| Config-validated only | PentAGI |
| Paid API tokens used | 0 |

Highlights: Semgrep and Opengrep each found 12/12 seeded issues in the synthetic fixture with identical results. A local `llama3.1:8b` resisted 5/5 Promptfoo secret-leak tests but was hijacked by 55% of Garak prompt-injection probes (20-prompt sample).

## Layout

| Path | Contents |
|---|---|
| `AGENTS.md` / `Agent.md` | Lab specification (plaintext / original RTF) |
| `reports/` | System inventory, repository inventory, installation results, smoke tests, capability matrix, integration recommendations, final report, PDF |
| `configs/lab.env` | Keeps every interpreter, tool and cache inside the lab |
| `configs/smoke.sh` | Sandboxed smoke-test runner (macOS `sandbox-exec`, network denied, fake `$HOME`) |
| `configs/*.yaml`, `configs/*_offline.py` | Local Semgrep/Opengrep rules, Promptfoo/Garak/Inspect configs, offline framework checks |
| `configs/build_pdf.py` | Regenerates the PDF report |
| `fixtures/sample-vulnerable-app/` | Synthetic insecure code for static analysis only (fake credentials; never run it) |
| `logs/` | Install logs, per-test logs, `smoke-results.tsv`, repo metadata |
| `artifacts/out/` | Scanner and eval outputs (SARIF/JSON/.eval) |

Not committed (recreated by setup): `repos/` (the 19 clones), `environments/` (venvs, tools, caches).

## Reproduce (macOS, Apple Silicon)

Requires `git`, `uv`, Node.js >= 22, and optionally Docker and Ollama.

```bash
source configs/lab.env
uv python install 3.10 3.11 3.13
mkdir -p repos && cd repos
# clone the 19 repositories listed in AGENTS.md section 6 (shallow clones are fine)
cd ..
# install each tool into its own environment as described in reports/installation-results.md
./configs/smoke.sh            # runs every safe smoke test, results in logs/smoke-results.tsv
```

`fixtures/sample-vulnerable-app` is committed as plain files. Run `git init` inside it if a harness requires a git repository.

## Safety

No active penetration tests, exploit verification or scans of real targets were run. Level 3/4 testing (cloud models, Docker-based pentest tools) requires explicit approval. See `AGENTS.md` section 2.

## Author

Mohammad Ibrahim Saleem ([@ibrahimsaleem](https://github.com/ibrahimsaleem))
