# Repository Inventory

All 19 repositories cloned successfully on 2026-10-13 with `git clone --depth 1` (shallow, to save ~10 GB; full history not needed). No clone failures, no moved repos, no forks substituted. `git status --short` was empty (0 changes) for all at clone time. Local root: `repos/`. Metadata: `logs/repo-meta.tsv`.

| ID | Name | GitHub URL | Clone | Local path | Branch | Commit SHA | License | Latest release | Last commit | ★ | Maintenance observations |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H01 | visa-vulnerability-agentic-harness | https://github.com/visa/visa-vulnerability-agentic-harness | OK | `repos/visa-vulnerability-agentic-harness` | main | `4128e870377850db16cb082115105cc8ee6f1a72` | NOASSERTION | v1.5.0 (2026-10-09) | 2026-10-09 | 2928 | Apache-2.0 per LICENSE text (GitHub API says NOASSERTION; file reviewed manually). Very active; v1.5.0 released 2026-10-09. |
| H02 | vulnhuntr | https://github.com/protectai/vulnhuntr | OK | `repos/vulnhuntr` | main | `ead88c5adba4279dae5c56d65124c530a9a1c5ae` | AGPL-3.0 | none | 2025-02-06 | 2801 | AGPL-3.0. **Stale**: last commit 2025-02-06, no GitHub releases. Python-only analysis. |
| H03 | strix | https://github.com/usestrix/strix | OK | `repos/strix` | main | `956a26715b02ec2d60c6a6ffcf9c6146633a4318` | Apache-2.0 | v1.7.0 (2026-10-05) | 2026-10-14 | 68421 | Apache-2.0. Very active (commits today). Also offers hosted app.strix.ai, but local OSS mode used. |
| H04 | pentagi | https://github.com/vxcontrol/pentagi | OK | `repos/pentagi` | main | `843dfeb4bfc809c09d1bc5022e567c602d8fc9dd` | MIT | v2.2.0 (2026-10-05) | 2026-10-10 | 28309 | MIT for code + separate EULA.md present; review before commercial use. Active. |
| H05 | shannon | https://github.com/KeygraphHQ/shannon | OK | `repos/shannon` | main | `2468b67d9e40d70d0b189462c5041c24e1dc886c` | AGPL-3.0 | v3.4.0 (2026-10-06) | 2026-10-07 | 48858 | AGPL-3.0, so network-service use triggers copyleft. Active; LICENSES/ dir has third-party notices. |
| H06 | PentestGPT | https://github.com/GreyDGL/PentestGPT | OK | `repos/PentestGPT` | main | `e8b1bb77d1ac00329675cec3b060aba971ec1ac8` | MIT | v1.0.0 (2025-12-24) | 2026-07-14 | 15933 | MIT. Moderately active (last commit 2026-07-14). Pulls git dep from separate org PentestGPT-Project. |
| H07 | SWE-agent | https://github.com/SWE-agent/SWE-agent | OK | `repos/SWE-agent` | main | `3ea751c087f32b16e039a2233dd6eefecef325d5` | MIT | v1.1.0 (2025-05-22) | 2026-07-16 | 20545 | MIT. Last commit 2026-07-16; last release v1.1.0 2025-05; upstream now points to mini-swe-agent. |
| H08 | inspect_ai | https://github.com/UKGovernmentBEIS/inspect_ai | OK | `repos/inspect_ai` | main | `dfcb169e1cb170a8fbe2c37a0e3befc45c2c2b85 (tag 0.3.280; cloned main d5862e0)` | MIT | 0.3.280 (2026-10-14) | 2026-10-14 | 2997 | MIT. Very active (release 0.3.280 published today). Checked out tag 0.3.280 (see SHA). |
| H09 | promptfoo | https://github.com/promptfoo/promptfoo | OK | `repos/promptfoo` | main | `a32c0882440adfc70aaca2c16280247261c4c03c` | MIT | code-scan-action-0.2.2 (2026-10-08) | 2026-10-13 | 25982 | MIT. Very active. |
| H10 | garak | https://github.com/NVIDIA/garak | OK | `repos/garak` | main | `cd87893be81bed4ced9afd86b88577289f4644bf` | Apache-2.0 | v0.17.0 (2026-09-09) | 2026-10-10 | 9562 | Apache-2.0. Active; v0.17.0 2026-09-09. |
| H11 | PyRIT | https://github.com/microsoft/PyRIT | OK | `repos/PyRIT` | main | `78bc1cb63695f6240751d0326a2ae0bad7cea50a` | MIT | v1.1.0 (2026-09-04) | 2026-10-14 | 4619 | MIT. Very active; v1.1.0 2026-09-04 (source is 1.2.0.dev0). |
| H12 | OpenHands | https://github.com/OpenHands/OpenHands | OK | `repos/OpenHands` | main | `0e9ce191390f535347ff17055038c45eeef3fedf` | MIT | v1.27.1 (2026-10-12) | 2026-10-13 | 90839 | MIT. Very active. Repo is now the Agent Canvas frontend/CLI. |
| H13 | aider | https://github.com/Aider-AI/aider | OK | `repos/aider` | main | `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` | Apache-2.0 | v0.86.0 (2025-08-09) | 2026-05-22 | 49531 | Apache-2.0. **Slowing**: last commit 2026-05-22, last release v0.86 (2025-08). |
| H14 | semgrep | https://github.com/semgrep/semgrep | OK | `repos/semgrep` | develop | `38a67a7eaf724fc266bf96e5705742bff8589775` | LGPL-2.1 | v1.180.0 (2026-10-07) | 2026-10-07 | 17039 | LGPL-2.1 engine; Semgrep Registry rules & Pro engine have separate terms. Default branch is `develop`. |
| H15 | opengrep | https://github.com/opengrep/opengrep | OK | `repos/opengrep` | main | `ffe40a1fa2f282e0a20d65c4dde8702bc45dad0c` | LGPL-2.1 | v1.30.2 (2026-10-07) | 2026-10-10 | 3180 | LGPL-2.1 (Semgrep fork). Active; v1.30.2 2026-10-07. |
| H16 | zaproxy | https://github.com/zaproxy/zaproxy | OK | `repos/zaproxy` | main | `38ffe34a1b03fd3241e0bb233c2a083df875ee33` | Apache-2.0 | v2.17.0 (2025-12-15) | 2026-10-08 | 15931 | Apache-2.0. Active; v2.17.0 2025-12-15. |
| H17 | langgraph | https://github.com/langchain-ai/langgraph | OK | `repos/langgraph` | main | `a6731f436700c7d46a9224ccd3a0e0ce3a5bfdb5` | MIT | cli==0.4.34 (2026-10-13) | 2026-10-13 | 43225 | MIT. Very active. |
| H18 | autogen | https://github.com/microsoft/autogen | OK | `repos/autogen` | main | `027ecf0a379bcc1d09956d46d12d44a3ad9cee14` | CC-BY-4.0 | python-v0.7.5 (2025-09-30) | 2026-04-06 | 61393 | Code: MIT (`LICENSE-CODE`); docs: CC-BY-4.0 (`LICENSE`, which is what GitHub detects). **Maintenance mode**: README points to Microsoft Agent Framework. |
| H19 | crewAI | https://github.com/crewAIInc/crewAI | OK | `repos/crewAI` | main | `75808b0eca0ca17ef0cd578130d7055cd4c13f12` | MIT | 1.15.27 (2026-10-09) | 2026-10-14 | 59666 | MIT. Very active. |

## Reference-only projects (per §17, not cloned)

- **Anthropic Project Glasswing**: initiative, not a cloneable harness. No repo invented.
- **Google Project Zero**: research team, not a single tool.
- **CAI** (aliasrobotics/cai): archived. Reference only unless you explicitly request installation.
