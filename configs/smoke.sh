#!/bin/zsh
# Safe smoke tests. Every command runs under sandbox-exec with all IP traffic and socket binding denied,
# a lab-local fake $HOME (no real credentials reachable), stdin closed, and a timeout.
source ${0:A:h}/lab.env
E=$LAB/environments R=$LAB/repos F=$LAB/fixtures/sample-vulnerable-app A=$LAB/artifacts
export HOME=$A/home XDG_CONFIG_HOME=$A/home/.config XDG_DATA_HOME=$A/home/.local/share XDG_CACHE_HOME=$A/home/.cache
export TIKTOKEN_CACHE_DIR=$LAB/environments/.tiktoken-cache
export DOCKER_CONFIG=/Users/ibrahim/.docker  # read-only: locate compose plugin
export SEMGREP_ENABLE_VERSION_CHECK=0 AIDER_CHECK_UPDATE=false ANONYMIZED_TELEMETRY=false CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true
mkdir -p $HOME $LAB/logs/smoke $A/out
SB=${SB:-'(version 1)(allow default)(deny network-outbound (remote ip "*:*"))(deny network-bind)(deny network-inbound)'}
OUT=$LAB/logs/smoke-results.tsv
[[ -f $OUT ]] || print -r -- $'project\tlevel\tcommand\tstart_utc\tsecs\texit\tlog' > $OUT

t() { # t <project> <level> <command...>
  local p=$1 l=$2 cmd=$3 n=$(( $(print -l $LAB/logs/smoke/$1-*.log(N) | grep -c .) + 1 ))
  local log=$LAB/logs/smoke/$p-$n.log start=$(date -u +%FT%TZ) s=$SECONDS
  print -r -- "\$ $cmd" > $log
  (cd $LAB && perl -e 'alarm shift; exec @ARGV' ${TIMEOUT:-300} sandbox-exec -p "$SB" /bin/zsh -c "$cmd" >> $log 2>&1 </dev/null)
  local ec=$?
  print -r -- "$p	$l	$cmd	$start	$((SECONDS-s))	$ec	logs/smoke/${log:t}" >> $OUT
  printf '%-12s L%s exit=%-3s %s\n' $p $l $ec "$cmd"
}

[[ -n $1 ]] && { eval "$@"; exit; }  # allow ad-hoc: smoke.sh t proj 1 'cmd'

# --- H01 VVAH
t vvah 1 "$E/vvah/bin/vvaharness --version"
t vvah 1 "$E/vvah/bin/vvaharness --help"
t vvah 2 "$E/vvah/bin/vvaharness setup"
t vvah 2 "$E/vvah/bin/vvaharness estimate --repo $F"
# --- H02 VulnHuntr
t vulnhuntr 1 "$E/vulnhuntr/bin/vulnhuntr --help"
# --- H03 Strix
t strix 1 "strix --help"
t strix 1 "strix --version"
# --- H06 PentestGPT (live/docker markers and localhost-target tests excluded)
t pentestgpt 1 "$R/PentestGPT/.venv/bin/pentestgpt-legacy --help"
t pentestgpt 2 "cd $R/PentestGPT && .venv/bin/python -m pytest tests -q -p no:cacheprovider -m 'not live and not docker' --ignore=tests/docker"
t pentestgpt 2 "cd $R/PentestGPT/pentestgpt_agent && .venv/bin/python -m pytest -q -p no:cacheprovider -m 'not live' --ignore=tests/live --ignore=tests/test_local_target.py --ignore=tests/test_local_benchmark.py"
# --- H07 SWE-agent
t swe-agent 1 "$E/swe-agent/bin/sweagent --help"
# --- H08 Inspect AI (mockllm = built-in offline model)
t inspect_ai 1 "$E/inspect_ai/bin/inspect --version"
t inspect_ai 1 "$E/inspect_ai/bin/inspect --help"
t inspect_ai 2 "$E/inspect_ai/bin/inspect eval configs/inspect_mock_task.py --model mockllm/model --log-dir $A/out/inspect --no-ansi"
# --- H09 Promptfoo (echo provider = no model calls)
t promptfoo 1 "promptfoo --version"
t promptfoo 1 "promptfoo --help"
t promptfoo 2 "promptfoo eval -c configs/promptfoo-echo.yaml --no-cache --no-progress-bar -o $A/out/promptfoo-echo.json"
# --- H10 Garak (test.Blank generator = offline dummy target)
t garak 1 "$E/garak/bin/garak --version"
t garak 1 "$E/garak/bin/garak --help"
t garak 2 "$E/garak/bin/garak --target_type test.Blank --probes test.Test --report_prefix lab-smoke"
# --- H11 PyRIT
t pyrit 1 "$E/pyrit/bin/python -c 'import pyrit; print(pyrit.__version__)'"
t pyrit 1 "$E/pyrit/bin/pyrit_scan --help"
t pyrit 2 "$E/pyrit/bin/python -c 'import asyncio; from pyrit.converter import Base64Converter as B; r=asyncio.run(B().convert_async(prompt=\"lab\")); assert r.output_text==\"bGFi\", r; print(\"converter OK\", r.output_text)'"
# --- H12 OpenHands (help only; never started)
t openhands 1 "$E/openhands/node_modules/.bin/agent-canvas --help"
# --- H13 Aider
t aider 1 "aider --version"
t aider 1 "aider --help"
# --- H14/H15 Semgrep, Opengrep (local rules on synthetic fixture)
t semgrep 1 "semgrep --version"
t semgrep 2 "semgrep scan --metrics off --disable-version-check --config configs/lab-rules.yml --json -o $A/out/semgrep.json --sarif-output=$A/out/semgrep.sarif $F"
t opengrep 1 "opengrep --version"
t opengrep 2 "opengrep scan --config configs/lab-rules.yml --json -o $A/out/opengrep.json --sarif-output=$A/out/opengrep.sarif $F"
# --- H17-H19 frameworks (offline examples)
t langgraph 2 "$E/langgraph/bin/python configs/langgraph_offline.py"
t autogen 2 "$E/autogen/bin/python configs/autogen_offline.py"
t crewai 1 "$E/crewai/bin/crewai version"
t crewai 2 "$E/crewai/bin/python configs/crewai_offline.py"
# --- Docker-heavy: config validation only (daemon not required, nothing started)
t pentagi 2 "cd $R/pentagi && docker compose --env-file .env.example -f docker-compose.yml config --quiet"
t shannon 2 "cd $R/shannon && docker compose -f docker-compose.yml config --quiet"
