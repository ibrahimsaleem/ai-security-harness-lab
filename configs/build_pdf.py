"""Build reports/AI-Security-Harness-Lab-Report.pdf from lab data. Run with environments/pdftools/bin/python."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

LAB = Path(__file__).resolve().parent.parent
OUT = LAB / "reports" / "AI-Security-Harness-Lab-Report.pdf"

INK, MUTED, ACCENT, RULE, BAND = (colors.HexColor(c) for c in ("#1b1f24", "#5b6470", "#1f5f8b", "#d0d7de", "#eef3f7"))
STATUS_COLOR = {"PASS": "#1a7f37", "BLOCKED": "#bf3989", "CONFIG ONLY": "#9a6700"}

ss = getSampleStyleSheet()
S = {
    "title": ParagraphStyle("t", parent=ss["Title"], fontSize=26, leading=32, textColor=INK, alignment=TA_CENTER),
    "sub": ParagraphStyle("s", parent=ss["Normal"], fontSize=12, leading=16, textColor=MUTED, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=17, leading=21, textColor=ACCENT, spaceBefore=6, spaceAfter=8),
    "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=13, leading=16, textColor=INK, spaceBefore=8, spaceAfter=4),
    "body": ParagraphStyle("b", parent=ss["Normal"], fontSize=9.5, leading=13, textColor=INK, spaceAfter=4),
    "cell": ParagraphStyle("c", parent=ss["Normal"], fontSize=8, leading=10, textColor=INK),
    "cellb": ParagraphStyle("cb", parent=ss["Normal"], fontSize=8, leading=10, textColor=INK, fontName="Helvetica-Bold"),
    "small": ParagraphStyle("sm", parent=ss["Normal"], fontSize=8, leading=10, textColor=MUTED),
    "bullet": ParagraphStyle("bl", parent=ss["Normal"], fontSize=9.5, leading=13, textColor=INK, leftIndent=12, bulletIndent=2),
}
P = lambda t, s="body": Paragraph(t, S[s])


def table(rows, widths, header=True, zebra=True):
    data = [[P(c, "cellb" if header and i == 0 else "cell") if isinstance(c, str) else c for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), BAND))
    if zebra:
        st += [("BACKGROUND", (0, i), (-1, i), colors.HexColor("#fafbfc")) for i in range(2, len(rows), 2)]
    t.setStyle(TableStyle(st))
    return t


def status(s):
    key = next((k for k in STATUS_COLOR if s.startswith(k)), None)
    return f'<font color="{STATUS_COLOR[key]}"><b>{s}</b></font>' if key else f"<b>{s}</b>"


# ---- repo metadata from clone step -------------------------------------------------
META = {}
for line in (LAB / "logs/repo-meta.tsv").read_text().splitlines():
    f = line.split("\t")
    rel = f[12] if not f[12].startswith("{") else "none"
    META[f[0]] = dict(url=f[1].removesuffix(".git"), branch=f[2], sha=f[3], date=f[4], spdx=f[7], stars=f[10], release=rel)
META["inspect_ai"]["sha"] = "dfcb169e1cb170a8fbe2c37a0e3befc45c2c2b85 (release tag 0.3.280)"

# ---- per-harness details (verified in the lab; D = documented only, T = tested here) ------
R = [
 dict(id="H01", name="Visa Vulnerability Agentic Harness (VVAH)", dir="visa-vulnerability-agentic-harness", group="Primary AI security harness",
      purpose="Agentic source-code security analysis: attack-surface/threat modelling, vulnerability discovery, adversarial finding verification, structured reports and SARIF. Optional remediation (S10), remediation validation (S11) and exploit verification, all off by default.",
      license="Apache-2.0 (LICENSE text reviewed by hand; GitHub API reports NOASSERTION).",
      maint="Very active. v1.5.0 released 2026-10-09.",
      install="Python 3.11 venv <font face='Courier'>environments/vvah</font>; <font face='Courier'>pip install .</font> from source.",
      version="1.5.0", status="PASS",
      tests=["L1 <font face='Courier'>vvaharness --version</font> / <font face='Courier'>--help</font>: pass.",
             "L2 <font face='Courier'>vvaharness setup</font>: readiness check works. Exit 1 = 'Not ready: 3 blocking', all of which are missing API keys (expected).",
             "L2 <font face='Courier'>vvaharness estimate</font> on synthetic fixture: 7 files, ~507 source tokens, S1-S9 budget 252k-1M input tokens. No model calls."],
      models="Anthropic; any OpenAI-compatible endpoint (incl. open-weight models); can drive Claude Code / Codex / Gemini CLIs. No native Ollama provider.",
      caps="Vulnerability discovery, LLM + tree-sitter static analysis, per-role multi-agent pipeline, SARIF/JSON/MD output, optional exploit verification.",
      risks="Sends source code to the model provider. Auto-detects a logged-in claude CLI. Remediation edits source, so use on copies only.",
      next="Choose a model and spend cap, then <font face='Courier'>vvaharness scan --repo fixtures/sample-vulnerable-app --stop-after s9</font>."),
 dict(id="H02", name="VulnHuntr", dir="vulnhuntr", group="Primary AI security harness",
      purpose="LLM-assisted discovery of remotely exploitable vulnerabilities in Python code by tracing call chains from user input to sinks.",
      license="AGPL-3.0 (strong copyleft).", maint="Stale: last commit 2025-02-06, no GitHub releases.",
      install="Python 3.10 venv <font face='Courier'>environments/vulnhuntr</font>; hash-pinned <font face='Courier'>requirements.txt</font> + <font face='Courier'>--no-deps</font> source install (Poetry absent).",
      version="0.1.0", status="PASS",
      tests=["L1 <font face='Courier'>vulnhuntr --help</font>: pass after fix. A plain <font face='Courier'>pip install .</font> crashes because <font face='Courier'>requests</font> is not declared as a dependency (upstream packaging gap)."],
      models="Claude, GPT, Ollama (<font face='Courier'>-l {claude,gpt,ollama}</font>), optional custom endpoint.",
      caps="Python only. Classes: LFI, arbitrary file overwrite, RCE, XSS, SQLi, SSRF, IDOR. Text/log output (no SARIF).",
      risks="Sends source to model provider. AGPL licensing.",
      next="Optional second opinion for Python repos only; low priority because upstream is stale."),
 dict(id="H03", name="Strix", dir="strix", group="Primary AI security harness",
      purpose="Agentic application security testing: AI agents run real tools inside a Docker sandbox against a target app.",
      license="Apache-2.0.", maint="Very active (commits on clone day). v1.7.0 2026-10-05. Also offers a hosted service (not used).",
      install="<font face='Courier'>uv tool install strix-agent</font> (lab-scoped tool dir). Remote shell installer not used.",
      version="1.7.0", status="PASS (L1)",
      tests=["L1 <font face='Courier'>strix --help</font> and <font face='Courier'>--version</font>: pass."],
      models="Many providers via LiteLLM, incl. Ollama.",
      caps="Dynamic testing, multi-agent, run reports; MCP and SARIF references in source; CI mode documented.",
      risks="Active testing tool. Needs Docker and pulls a sandbox image on first run. Only against isolated, authorised targets.",
      next="Start Docker Desktop; Level-4 approval with an isolated target before any <font face='Courier'>--target</font> run."),
 dict(id="H04", name="PentAGI", dir="pentagi", group="Primary AI security harness",
      purpose="Multi-agent autonomous penetration-testing platform with web UI, running tools in containers.",
      license="MIT for code, plus a separate EULA.md (review before commercial use).", maint="Active. v2.2.0 2026-10-05.",
      install="Docker Compose only; not deployed.", version="v2.2.0 (repo)", status="CONFIG ONLY",
      tests=["L2 <font face='Courier'>docker compose --env-file .env.example config --quiet</font>: validates.",
             "Runtime NOT TESTED: Docker daemon off and deployment requires approval."],
      models="Many providers; Ollama heavily referenced in source.",
      caps="Autonomous pentest, multi-agent, GraphQL/REST API, Langfuse/observability stacks.",
      risks="Default compose mounts <font face='Courier'>/var/run/docker.sock</font> into a container running as root (effectively root on the Docker VM). Requires >= 20 GB disk, heavy RAM.",
      next="Approve Docker start and a socket-proxy / separate-VM design before deployment."),
 dict(id="H05", name="Shannon", dir="shannon", group="Primary AI security harness",
      purpose="Autonomous white-box application penetration testing that actively executes exploits.",
      license="AGPL-3.0.", maint="Active. v3.4.0 2026-10-06.",
      install="Not installed: documented entry point <font face='Courier'>npx @keygraph/shannon@latest</font> downloads and executes code.",
      version="v3.4.0 (repo)", status="BLOCKED",
      tests=["L2 <font face='Courier'>docker compose config --quiet</font>: validates (Temporal service, named volume only, no socket mount)."],
      models="Anthropic primarily; a few Ollama / LiteLLM references.",
      caps="Dynamic exploitation, source-aware testing, Temporal workflows, Markdown reports; SARIF references in source.",
      risks="Executes real exploits. Never point at production, public targets or the host. AGPL.",
      next="Approve a pinned run, e.g. <font face='Courier'>npx @keygraph/shannon@3.4.0 --help</font>; needs Docker + LLM credentials."),
 dict(id="H06", name="PentestGPT", dir="PentestGPT", group="Primary AI security harness",
      purpose="AI-assisted penetration-testing and CTF workflows. Agent mode drives Claude Code or Codex CLIs; legacy interactive mode supports many LLMs.",
      license="MIT.", maint="Moderately active: last commit 2026-07-14, v1.0.0 2025-12-24.",
      install="<font face='Courier'>make install</font> (reviewed: runs <font face='Courier'>uv sync</font>) creating <font face='Courier'>repos/PentestGPT/.venv</font> and <font face='Courier'>pentestgpt_agent/.venv</font>, Python 3.12.",
      version="1.0.0", status="PASS",
      tests=["L1 <font face='Courier'>pentestgpt-legacy --help</font>: pass.",
             "L2 root unit tests: 133 passed. L2 agent unit tests: 115 passed.",
             "Excluded: <font face='Courier'>live</font> marker (spends tokens), <font face='Courier'>docker</font> marker, and tests that start a vulnerable SSTI server on localhost and attack it."],
      models="Claude Code / Codex CLI backends; legacy: OpenAI, Gemini, DeepSeek, xAI, Qwen, Moonshot, local Ollama.",
      caps="Dynamic pentest/CTF, supervisor/executor loop, MCP tool server (unit-tested).",
      risks="Uses ambient Claude/Codex logins. Git dependency pulled from a second org (PentestGPT-Project/UnifedAgentWrapper, pinned by SHA).",
      next="Level-4 only, against an isolated CTF-style target."),
 dict(id="H07", name="SWE-agent", dir="SWE-agent", group="Primary AI security harness",
      purpose="Software-engineering agent for issue resolution; useful for reviewing vulnerability reports and drafting candidate fixes.",
      license="MIT.", maint="Last commit 2026-07-16; last release v1.1.0 (2025-05). README says most effort moved to mini-swe-agent.",
      install="Python 3.11 venv <font face='Courier'>environments/swe-agent</font>; <font face='Courier'>pip install -e .</font>",
      version="1.1.0", status="PASS (L1)",
      tests=["L1 <font face='Courier'>sweagent --help</font>: pass."],
      models="Any provider via LiteLLM, incl. local.",
      caps="Patch generation, trajectories, batch mode.", risks="Edits code. Runs need Docker (SWE-ReX sandbox).",
      next="With Docker on, patch-only runs on a copy of the fixture."),
 dict(id="H08", name="Inspect AI (UK AISI)", dir="inspect_ai", group="Primary AI security harness",
      purpose="Framework for evaluating models and agents: datasets, solvers, scorers, sandboxed tools, approval policies, log viewer.",
      license="MIT.", maint="Very active (release 0.3.280 on clone day).",
      install="Python 3.12 venv <font face='Courier'>environments/inspect_ai</font>; <font face='Courier'>pip install -e .[dev]</font> at tag 0.3.280.",
      version="0.3.280", status="PASS",
      tests=["Install fix: shallow clone had no tags, so setuptools-scm reported 0.1.dev1 and the [dev] resolve failed. Fixed by checking out the release tag.",
             "L1 <font face='Courier'>inspect --version</font> / <font face='Courier'>--help</font>: pass.",
             "L2 mock-LLM eval: first runs exited 0 but log status was <b>error</b> (tiktoken download blocked). After pre-seeding the cache: status success, accuracy 1.0."],
      models="Nearly all providers, incl. Ollama and vLLM.",
      caps="LLM/agent evaluation, agent solvers, MCP support, .eval logs; ideal scoring layer.", risks="Paid evals cost tokens; keep to local models unless approved.",
      next="Use as the common scorer to compare tools across runs."),
 dict(id="H09", name="Promptfoo", dir="promptfoo", group="Primary AI security harness",
      purpose="LLM application evaluation and red-team testing (prompt injection, jailbreaks, PII leakage, etc.).",
      license="MIT.", maint="Very active.",
      install="npm <font face='Courier'>--prefix environments/promptfoo</font>, pinned 0.124.1; telemetry and update checks disabled.",
      version="0.124.1", status="PASS",
      tests=["L1 <font face='Courier'>--version</font> / <font face='Courier'>--help</font>: pass.",
             "L2 echo-provider eval: 1/1 assertions, 0 tokens.",
             "L3 local llama3.1:8b: 5/5 secret-leak tests passed (no leak), 351 local tokens."],
      models="Nearly all providers, incl. Ollama.",
      caps="Red-team plugins, regression tests, JSON/HTML/CSV output, CI/GitHub Action.",
      risks="Model-graded asserts default to a cloud grader model; use deterministic asserts or a local grader.",
      next="Point at an LLM application you own; add red-team plugin suite with a local grader."),
 dict(id="H10", name="NVIDIA Garak", dir="garak", group="Primary AI security harness",
      purpose="LLM vulnerability scanner: probes (injection, jailbreak, encoding, leakage, toxicity...) plus detectors.",
      license="Apache-2.0.", maint="Active. v0.17.0 2026-09-09.",
      install="Python 3.12 venv <font face='Courier'>environments/garak</font>; <font face='Courier'>pip install -e .</font>",
      version="0.17.1.pre1", status="PASS",
      tests=["L1 <font face='Courier'>--version</font> / <font face='Courier'>--help</font>: pass.",
             "L2 <font face='Courier'>test.Test</font> probe vs <font face='Courier'>test.Blank</font>: PASS 40/40.",
             "L3 local llama3.1:8b (<=20 prompts/probe): promptinject attack success 55%; encoding DecodeMatch 0%, DecodeApprox 10%."],
      models="Many generators incl. Ollama and local Hugging Face.",
      caps="LLM red teaming; JSONL + HTML reports.", risks="Some detectors download extra models; full sweeps are thousands of prompts.",
      next="Larger sweep against the local model (no API cost)."),
 dict(id="H11", name="Microsoft PyRIT", dir="PyRIT", group="Additional security / coding tool",
      purpose="Python Risk Identification Tool: AI red-team orchestration with targets, converters, scorers and multi-turn attacks.",
      license="MIT.", maint="Very active. v1.1.0 2026-09-04 (source is 1.2.0.dev0).",
      install="Python 3.12 venv <font face='Courier'>environments/pyrit</font>; <font face='Courier'>pip install -e .</font>",
      version="1.2.0.dev0", status="PASS",
      tests=["L1 import + <font face='Courier'>pyrit_scan --help</font>: pass.",
             "L2 Base64Converter round-trip: pass (module is <font face='Courier'>pyrit.converter</font> in 1.x)."],
      models="Azure/OpenAI and others; Ollama and LiteLLM references.",
      caps="Multi-turn attack orchestration, converters, scorers, memory DB.", risks="Do not attack AI systems you don't own.",
      next="Pin <font face='Courier'>pyrit==1.1.0</font> for stability; scripted attacks vs local model."),
 dict(id="H12", name="OpenHands", dir="OpenHands", group="Additional security / coding tool",
      purpose="General software-engineering agent platform; repo is now the Agent Canvas frontend/CLI and agent-server launcher.",
      license="MIT.", maint="Very active. v1.27.1 2026-10-12.",
      install="npm <font face='Courier'>--prefix environments/openhands</font> <font face='Courier'>@openhands/agent-canvas</font> (CLI only; never started).",
      version="agent-canvas 1.27.1", status="PASS (L1)",
      tests=["L1 <font face='Courier'>agent-canvas --help</font>: pass (help path reviewed; does not start services)."],
      models="Any via LiteLLM; ACP agents (Claude Code, Codex, Gemini...).",
      caps="Coding agent, multiple sandboxes, automations, agent server API.",
      risks="Option 1 (no sandbox) gives the agent full filesystem access. Option 2 mounts a projects dir into Docker.",
      next="Only with approval: Docker sandbox and a dedicated empty projects directory."),
 dict(id="H13", name="Aider", dir="aider", group="Additional security / coding tool",
      purpose="AI pair-programming / code-editing CLI that commits changes to git.",
      license="Apache-2.0.", maint="Slowing: last commit 2026-05-22, last release v0.86 (2025-08).",
      install="<font face='Courier'>uv tool install --python 3.12 aider-chat</font> (lab-scoped).",
      version="0.86.2", status="PASS",
      tests=["First install on Python 3.13 failed at runtime (pydub needs removed <font face='Courier'>audioop</font>); reinstalled on 3.12.",
             "L1 <font face='Courier'>aider --version</font> / <font face='Courier'>--help</font>: pass."],
      models="Any via LiteLLM, incl. Ollama.", caps="Patch generation with git integration; scripting mode.",
      risks="Edits and commits code. Use only in throwaway copies.", next="Patch-only step in the approved-fix workflow."),
 dict(id="H14", name="Semgrep", dir="semgrep", group="Additional security / coding tool",
      purpose="Rule-based static application security testing (SAST).",
      license="LGPL-2.1 engine; registry rules and Pro engine have separate terms.", maint="Very active. v1.180.0 2026-10-07. Default branch <font face='Courier'>develop</font>.",
      install="<font face='Courier'>uv tool install semgrep</font>; metrics off, version check off, no cloud login.",
      version="1.180.0", status="PASS",
      tests=["L1 <font face='Courier'>--version</font>: pass.",
             "L2 9 local rules on synthetic fixture: 12 findings, 0 errors, all 9 seeded categories hit; JSON + SARIF written."],
      models="None (deterministic).", caps="SAST, JSON/SARIF, CI.", risks="Cloud features must stay disabled.",
      next="Grow the local rule pack; use as the deterministic baseline."),
 dict(id="H15", name="Opengrep", dir="opengrep", group="Additional security / coding tool",
      purpose="Open-source fork of Semgrep's engine; Semgrep rule compatible.",
      license="LGPL-2.1.", maint="Active. v1.30.2 2026-10-07.",
      install="Official release binary <font face='Courier'>opengrep_osx_arm64</font> into <font face='Courier'>environments/opengrep</font>. install.sh reviewed but not used (writes to ~/.opengrep and ~/.local/bin). SHA-256 matched GitHub asset digest; cosign signature not verified.",
      version="1.30.2", status="PASS",
      tests=["L1 <font face='Courier'>--version</font>: pass.",
             "L2 same rules on fixture: 12 findings, identical to Semgrep."],
      models="None (deterministic).", caps="SAST, JSON/SARIF, drop-in Semgrep rules (verified).",
      risks="Install cosign to verify signatures.", next="Run alongside Semgrep for cross-checking."),
 dict(id="H16", name="OWASP ZAP", dir="zaproxy", group="Additional security / coding tool",
      purpose="Dynamic application security testing (spider, passive and active scanning, automation framework).",
      license="Apache-2.0.", maint="Active. v2.17.0 2025-12-15.",
      install="Not installed: Java 17+ missing and Docker daemon off.", version="v2.17.0 (repo)", status="BLOCKED",
      tests=["None possible without Java or Docker."],
      models="None.", caps="DAST, REST API, HTML/XML/JSON reports (SARIF only via a separate add-on, not verified).",
      risks="Active scanning only with approval against owned targets.",
      next="Approve Temurin JDK (Homebrew cask) or Docker image <font face='Courier'>zaproxy/zap-stable</font>."),
 dict(id="H17", name="LangGraph", dir="langgraph", group="Agent orchestration framework",
      purpose="Stateful graph-based agent orchestration with checkpointing and human-in-the-loop interrupts.",
      license="MIT.", maint="Very active.",
      install="Python 3.12 venv <font face='Courier'>environments/langgraph</font>; PyPI stable.", version="1.2.15", status="PASS",
      tests=["L2 offline graph: scan -> human gate (<font face='Courier'>interrupt()</font>) -> report, with InMemorySaver checkpoint; resumed via <font face='Courier'>Command(resume=True)</font>; output asserted."],
      models="Any via LangChain integrations.", caps="Checkpointing, approval gates, tool invocation, multi-agent.",
      risks="Do not give agents arbitrary shell tools.", next="Recommended orchestrator once the plain controller needs approvals."),
 dict(id="H18", name="Microsoft AutoGen", dir="autogen", group="Agent orchestration framework",
      purpose="Multi-agent application framework (agentchat, core, ext).",
      license="Code MIT (LICENSE-CODE); docs CC-BY-4.0 (what GitHub detects).", maint="Maintenance mode; README points to Microsoft Agent Framework.",
      install="Python 3.12 venv <font face='Courier'>environments/autogen</font>; autogen-agentchat + autogen-ext[openai] 0.7.5.",
      version="0.7.5", status="PASS",
      tests=["L2 AssistantAgent with ReplayChatCompletionClient (no API): reply asserted."],
      models="Many, incl. Ollama extension.", caps="Multi-agent teams, messaging, tools.",
      risks="Maintenance mode: avoid for new builds.", next="Not recommended as the orchestration layer."),
 dict(id="H19", name="CrewAI", dir="crewAI", group="Agent orchestration framework",
      purpose="Role-based multi-agent crews and flows.",
      license="MIT.", maint="Very active. 1.15.27 2026-10-09.",
      install="Python 3.12 venv <font face='Courier'>environments/crewai</font>; PyPI; telemetry disabled.", version="1.15.27", status="PASS",
      tests=["L1 <font face='Courier'>crewai version</font>: pass.",
             "L2 Agent/Task/Crew construction with fake key; <font face='Courier'>kickoff()</font> not called (would call an LLM)."],
      models="Many via LiteLLM, incl. Ollama.", caps="Role-based agents, delegation, sequential/hierarchical processes.",
      risks="Telemetry on by default; keep disabled.", next="Alternative to LangGraph; not needed for this pipeline."),
]


def header_footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawString(0.75 * inch, 0.5 * inch, "AI Security Harness Lab - Installation & Testing Report")
    c.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
    c.setStrokeColor(RULE)
    c.line(0.75 * inch, 0.65 * inch, letter[0] - 0.75 * inch, 0.65 * inch)
    c.restoreState()


def build():
    W = letter[0] - 1.5 * inch
    st = []
    # Cover
    st += [Spacer(1, 1.6 * inch), P("AI Security Harness Lab", "title"), Spacer(1, 6),
           P("Installation, smoke-testing and capability review of 19 open-source AI security repositories", "sub"),
           Spacer(1, 0.35 * inch), P("Mohammad Ibrahim Saleem &nbsp;|&nbsp; 2026-10-14", "sub"), Spacer(1, 0.6 * inch)]
    st.append(table([["Metric", "Result"],
                     ["Repositories cloned", "19 / 19 (SHA, license, release recorded)"],
                     ["Installed in isolated environments", "16"],
                     ["Passed safe smoke tests", "16 (38 sandboxed L1/L2 runs + 2 local-model L3 runs)"],
                     ["Blocked", "Shannon (needs approval to run npx), OWASP ZAP (no Java, Docker off)"],
                     ["Config-validated only", "PentAGI (root + host docker.sock by default)"],
                     ["Network during L1/L2 tests", "None (sandbox-exec denied all IP traffic)"],
                     ["Paid AI tokens consumed", "0"]], [2.4 * inch, W - 2.4 * inch]))
    st.append(PageBreak())

    # Summary + system
    st.append(P("1. Executive summary", "h1"))
    for b in ["All 19 repositories were cloned; every license was reviewed (VVAH and AutoGen corrected by hand).",
              "16 tools installed into separate, lab-local environments. Nothing system-wide, no sudo, no remote install scripts.",
              "Every test ran under macOS sandbox-exec with network and socket binding denied and a fake $HOME, so real credentials and CLI logins were unreachable.",
              "Semgrep and Opengrep each found 12/12 seeded issues in a synthetic fixture, identically. These are the only verified security findings.",
              "A local llama3.1:8b model resisted 5/5 Promptfoo secret-leak attempts but was hijacked by 55% of Garak prompt-injection probes (20-prompt sample).",
              "No active penetration tests, exploit verification or cloud-model calls were run."]:
        st.append(Paragraph(b, S["bullet"], bulletText="-"))
    st.append(P("2. System", "h1"))
    st.append(table([["Item", "Value"],
                     ["OS / arch", "macOS 27.0.1, arm64"], ["CPU / GPU", "Apple M5 Pro, 15 CPU cores, 16 GPU cores (Metal 4, no CUDA)"],
                     ["RAM / disk", "24 GB unified / 732 GB free at start; lab uses ~24 GB incl. model"],
                     ["Python", "3.12 (pyenv) + lab-local 3.10, 3.11, 3.13 via uv"], ["Node / npm", "24.21.0 / 11.19.0"],
                     ["Docker", "CLI 29.8.0, Compose v5.5.1; daemon not running"], ["Missing", "Java 17+, Poetry, pipx, Go, cosign"],
                     ["Local LLM", "Ollama 0.34.4 on 127.0.0.1:11434 with llama3.1:8b"]], [1.6 * inch, W - 1.6 * inch]))
    st.append(P("3. Isolation and safety controls", "h1"))
    for b in ["Interpreters, venvs, uv tools, npm packages and caches all under <font face='Courier'>environments/</font> (<font face='Courier'>configs/lab.env</font>).",
              "Test runner <font face='Courier'>configs/smoke.sh</font>: sandbox-exec profile denies outbound IP, bind and inbound; Level 3 profile allows only localhost:11434.",
              "Tests requiring localhost services, Docker, or live model backends were excluded until approved.",
              "Only touch outside the lab: three uv Python symlinks briefly created in ~/.local/bin and removed immediately; ~/.cache/uv gained cache entries."]:
        st.append(Paragraph(b, S["bullet"], bulletText="-"))
    st.append(PageBreak())

    # Overview table
    st.append(P("4. All repositories at a glance", "h1"))
    rows = [["ID", "Project", "License", "Version", "Status", "Last commit"]]
    for r in R:
        m = META[r["dir"]]
        rows.append([r["id"], r["name"], m["spdx"] if m["spdx"] != "NOASSERTION" else "Apache-2.0*", r["version"], status(r["status"]), m["date"]])
    st.append(table(rows, [0.45 * inch, 2.4 * inch, 0.95 * inch, 1.2 * inch, 1.05 * inch, W - 6.05 * inch]))
    st.append(Spacer(1, 4))
    st.append(P("* GitHub reports NOASSERTION; LICENSE file is Apache-2.0. AutoGen code is MIT (docs CC-BY-4.0).", "small"))
    st.append(PageBreak())

    # Per-repo details
    st.append(P("5. Repository and harness details", "h1"))
    for i, r in enumerate(R):
        m = META[r["dir"]]
        block = [P(f'{r["id"]} - {r["name"]}', "h2"), P(f'<i>{r["group"]}</i> &nbsp; Status: {status(r["status"])}', "small"), Spacer(1, 3)]
        lab = lambda k: P(f"<b>{k}</b>", "cell")
        block.append(table([
            [lab("Purpose"), P(r["purpose"], "cell")],
            [lab("Repository"), P(f'{m["url"]}<br/>branch <font face="Courier">{m["branch"]}</font> &nbsp; commit <font face="Courier">{m["sha"]}</font>', "cell")],
            [lab("License"), P(r["license"], "cell")],
            [lab("Release / activity"), P(f'Latest release: {m["release"]}. Last commit {m["date"]}. Stars: {m["stars"]}. {r["maint"]}', "cell")],
            [lab("Installation"), P(r["install"], "cell")],
            [lab("Installed version"), P(r["version"], "cell")],
            [lab("Tests run"), P("<br/>".join("- " + t for t in r["tests"]), "cell")],
            [lab("AI models"), P(r["models"], "cell")],
            [lab("Capabilities"), P(r["caps"], "cell")],
            [lab("Risks"), P(r["risks"], "cell")],
            [lab("Next step"), P(r["next"], "cell")],
        ], [1.25 * inch, W - 1.25 * inch], header=False, zebra=False))
        st.append(KeepTogether(block))
        st.append(Spacer(1, 10))
    st.append(PageBreak())

    # Capability matrix (condensed)
    st.append(P("6. Capability matrix", "h1"))
    st.append(P("T = verified by a test in this lab; D = documented and present in source, not tested here; - = not a feature.", "small"))
    st.append(Spacer(1, 6))
    Y = lambda s: s
    cm = [["Tool", "Vuln discovery", "Static", "Dynamic", "LLM red team", "Local models", "Multi-agent", "Outputs"],
          ["VVAH", "D", "D", "partial D", "-", "via OpenAI-compat", "D", "SARIF, JSON, MD"],
          ["VulnHuntr", "D (Python)", "D", "-", "-", "D (Ollama)", "-", "text"],
          ["Strix", "D", "partial", "D", "-", "D", "D", "reports"],
          ["PentAGI", "D", "-", "D", "-", "D", "D", "web UI"],
          ["Shannon", "D", "partial", "D (exploits)", "-", "partial", "D", "MD"],
          ["PentestGPT", "D", "-", "D", "-", "D (legacy)", "partial", "logs"],
          ["SWE-agent", "partial", "-", "-", "-", "D", "-", "trajectories"],
          ["Inspect AI", "-", "-", "-", "D (scoring T)", "D", "D", ".eval T"],
          ["Promptfoo", "-", "partial", "partial", "D + L3 T", "T (Ollama)", "-", "JSON T, HTML"],
          ["Garak", "-", "-", "-", "D + L3 T", "T (Ollama)", "-", "JSONL T, HTML T"],
          ["PyRIT", "-", "-", "-", "D (converter T)", "D", "D", "DB"],
          ["OpenHands", "partial", "-", "-", "-", "D", "partial", "conversations"],
          ["Aider", "-", "-", "-", "-", "D", "-", "git commits"],
          ["Semgrep", "T", "T", "-", "-", "n/a", "-", "JSON T, SARIF T"],
          ["Opengrep", "T", "T", "-", "-", "n/a", "-", "JSON T, SARIF T"],
          ["ZAP", "D", "-", "D", "-", "n/a", "-", "HTML/XML/JSON"],
          ["LangGraph", "-", "-", "-", "-", "D", "D (gate T)", "-"],
          ["AutoGen", "-", "-", "-", "-", "D", "D (T replay)", "-"],
          ["CrewAI", "-", "-", "-", "-", "D", "D", "-"]]
    st.append(table(cm, [0.95 * inch, 0.85 * inch, 0.6 * inch, 0.8 * inch, 0.95 * inch, 1.0 * inch, 0.8 * inch, W - 5.95 * inch]))
    st.append(PageBreak())

    # Results + recommendations
    st.append(P("7. Verified test results", "h1"))
    st.append(table([["Test", "Result"],
                     ["Semgrep vs Opengrep on synthetic fixture (9 rules)", "12 findings each, identical; SQLi x2, hardcoded secrets x3, pickle, unsafe YAML, mktemp, shell=True, eval, path traversal, admin route without auth"],
                     ["Inspect AI mock-LLM eval", "status success, accuracy 1.0 (after tiktoken cache fix)"],
                     ["Garak test.Test vs test.Blank", "PASS 40/40"],
                     ["Promptfoo echo provider", "1/1 assertions, 0 tokens"],
                     ["PentestGPT unit tests", "133 + 115 passed"],
                     ["LangGraph approval gate / AutoGen replay / PyRIT converter", "all passed"],
                     ["Promptfoo vs llama3.1:8b (L3, local)", "5/5 secret-leak attempts resisted"],
                     ["Garak vs llama3.1:8b (L3, local, 20 prompts/probe)", "promptinject 55% attack success; encoding 0% (exact) / 10% (approx)"]],
                    [2.6 * inch, W - 2.6 * inch]))
    st.append(P("8. Top recommendations", "h1"))
    st.append(table([["Use case", "Recommended"],
                     ["Source-code scanning", "Semgrep / Opengrep baseline + VVAH (--stop-after s9)"],
                     ["AI red teaming", "Promptfoo (app level) + Garak (model level), scored in Inspect AI; PyRIT for multi-turn"],
                     ["Remediation", "Aider in patch-only mode on copies; SWE-agent once Docker is on"],
                     ["Orchestration", "Plain Python controller with SARIF merge, then LangGraph for human approval gates"],
                     ["Level-4 only (isolated targets)", "Strix, PentAGI, Shannon, PentestGPT, ZAP"],
                     ["Avoid for new work", "AutoGen (maintenance mode), VulnHuntr (stale)"]], [1.9 * inch, W - 1.9 * inch]))
    st.append(P("Suggested pipeline", "h2"))
    st.append(P("Semgrep + Opengrep + VVAH -> merged SARIF -> triage -> human review gate (LangGraph interrupt) -> patch proposal (Aider / SWE-agent on a copy) -> regression tests -> report. "
                "AI-evaluation track runs separately: Promptfoo + Garak + PyRIT scored in Inspect AI. Pentest tools stay outside the pipeline behind a Level-4 authorisation boundary."))
    st.append(P("9. Costs and risks", "h1"))
    for b in ["Static tools and local models: $0 API cost. VVAH estimated 252k-1M input tokens for S1-S9 on a 507-token fixture; multiply by the chosen model's price.",
              "Code-scanning agents send source code to the model provider; use the synthetic fixture or explicitly approved repos only.",
              "Shannon, PentAGI, Strix and PentestGPT execute real attacks; PentAGI's default config grants root Docker socket access.",
              "VVAH and PentestGPT auto-detect logged-in Claude/Codex CLIs, so they could spend quota without an explicit key. Keep a lab $HOME.",
              "Licensing: Shannon and VulnHuntr AGPL-3.0; PentAGI EULA; Semgrep/Opengrep LGPL-2.1."]:
        st.append(Paragraph(b, S["bullet"], bulletText="-"))
    st.append(P("10. Next steps (approval required)", "h1"))
    for i, b in enumerate(["Larger Garak/Promptfoo sweep against the local model ($0).",
                           "VVAH scan of the fixture with a chosen model and spend cap.",
                           "Start Docker Desktop to unblock Strix, SWE-agent, ZAP and PentAGI.",
                           "Pinned Shannon run (npx @keygraph/shannon@3.4.0 --help).",
                           "Java or ZAP Docker image for OWASP ZAP.",
                           "Build an isolated vulnerable target container before any Level-4 pentest."], 1):
        st.append(Paragraph(b, S["bullet"], bulletText=f"{i}."))

    doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.85 * inch,
                            title="AI Security Harness Lab Report", author="Mohammad Ibrahim Saleem")
    doc.build(st, onFirstPage=header_footer, onLaterPages=header_footer)


if __name__ == "__main__":
    assert len(R) == 19 and all(r["dir"] in META for r in R), "every harness needs clone metadata"
    build()
    print(OUT)
