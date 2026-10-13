#!/bin/bash
set -eo pipefail
python3 /setup_config.py

# Find the GitHub URL and optional -d (debug) flag in arguments
GITHUB_URL=""
DEBUG_MODE=false
for arg in "$@"; do
  if [[ "$arg" == https://github.com/* ]]; then
    GITHUB_URL="$arg"
  elif [[ "$arg" == "-d" ]]; then
    DEBUG_MODE=true
  fi
done

if [[ -n "$GITHUB_URL" ]]; then
  REPO_PATH=$(echo "$GITHUB_URL" | sed 's|https://github.com/||' | sed 's|/$||')
  FILES=$(curl -s "https://api.github.com/repos/${REPO_PATH}/contents/" \
          | jq -r '.[].name' 2>/dev/null || true)

  if echo "$FILES" | grep -qiE '\.nf$|^nextflow\.config$|^\.nf-core\.yml$'; then
    INST="/root/.config/opencode/instructions_nextflow.md"
    echo "This is a nextflow pipeline"
  elif echo "$FILES" | grep -qE '^DESCRIPTION$'; then
    INST="/root/.config/opencode/instructions_r.md"
    echo "This is a R application"
  elif echo "$FILES" | grep -qiE '\.ipynb$'; then
    INST="/root/.config/opencode/instructions_jupyter.md"
    echo "This is a Jupyter notebook"
  else
    INST="/root/.config/opencode/instructions.md"
    echo "This is a generic application"
  fi

  # Update opencode.json to load the correct instructions file plus the form-filling step
  python3 -c "
import json
cfg = json.load(open('/root/.config/opencode/opencode.json'))
cfg['instructions'] = ['${INST}', '/root/.config/opencode/instructions_form.md']
json.dump(cfg, open('/root/.config/opencode/opencode.json', 'w'), indent=2)
"

  PROMPT="Execute the instructions in ${INST}. The GitHub link is ${GITHUB_URL}"

  if [[ "$DEBUG_MODE" == "true" ]]; then
    # Debug mode: show full OpenCode output including tool calls and bash output
    exec opencode run "$PROMPT"
  else
    # Default mode: filter to show only LLM text narration (suppress bash echoes and output)
    opencode run --format json "$PROMPT" | python3 -u -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        event = json.loads(line)
        if event.get('type') == 'text':
            text = event.get('part', {}).get('text', '')
            if text:
                if not text.endswith('\n'):
                    text += '\n'
                sys.stdout.write(text)
                sys.stdout.flush()
    except json.JSONDecodeError:
        pass
"
  fi
else
  exec opencode "$@"
fi
