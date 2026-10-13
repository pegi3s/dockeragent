#!/usr/bin/env python3
"""
Fills in /root/.config/opencode/opencode.json at container start from:
  - /data/config.json  : provider and model settings
  - /opt/.apikey       : API key (single line, no trailing whitespace)

Expected /data/config.json structure:
{
  "provider_id":   "deepseek",
  "provider_name": "DeepSeek",
  "npm":           "@ai-sdk/openai-compatible",
  "base_url":      "https://api.deepseek.com/v1",
  "model_id":      "deepseek-chat",
  "model_name":    "DeepSeek Chat"
}

Example for other providers:
  OpenAI:     base_url = "https://api.openai.com/v1",  npm = "@ai-sdk/openai"
  Anthropic:  base_url = "https://api.anthropic.com",  npm = "@ai-sdk/anthropic"
  Gemini:     base_url = "https://generativelanguage.googleapis.com/v1beta", npm = "@ai-sdk/google"
"""

import json
import os
import sys

CONFIG_FILE = "/data/config.json"
API_KEY_FILE = "/opt/.apikey"
TEMPLATE = "/root/.config/opencode/opencode.json"

REQUIRED_KEYS = ["provider_id", "provider_name", "npm", "base_url", "model_id", "model_name"]


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


if not os.path.exists(CONFIG_FILE):
    die(f"Config file not found: {CONFIG_FILE}\n"
        "Create it with keys: " + ", ".join(REQUIRED_KEYS))

if not os.path.exists(API_KEY_FILE):
    die(f"API key file not found: {API_KEY_FILE}\n"
        "Create it containing only your API key, then mount the parent directory with -v /opt:/opt")

with open(CONFIG_FILE) as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError as e:
        die(f"Invalid JSON in {CONFIG_FILE}: {e}")

with open(API_KEY_FILE) as f:
    api_key = f.read().strip()

for key in REQUIRED_KEYS:
    if key not in config:
        die(f"Missing key '{key}' in {CONFIG_FILE}")

if not api_key:
    die(f"API key file is empty: {API_KEY_FILE}")

with open(TEMPLATE) as f:
    template = f.read()

substitutions = {
    "__PROVIDER_ID__":   config["provider_id"],
    "__PROVIDER_NAME__": config["provider_name"],
    "__NPM__":           config["npm"],
    "__BASE_URL__":      config["base_url"],
    "__MODEL_ID__":      config["model_id"],
    "__MODEL_NAME__":    config["model_name"],
    "__API_KEY__":       api_key,
}

for placeholder, value in substitutions.items():
    template = template.replace(placeholder, value)

try:
    json.loads(template)
except json.JSONDecodeError as e:
    die(f"Generated opencode.json is not valid JSON: {e}")

with open(TEMPLATE, "w") as f:
    f.write(template)

print(f"OpenCode configured: {config['provider_id']}/{config['model_id']}")
