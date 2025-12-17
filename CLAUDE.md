# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Structure

```
aws-skills-cc/
├── .claude-plugin/          # Plugin manifests for Claude Code
├── skills/                  # Skills distributed via plugin
│   └── aws-agentcore-langgraph/
│       ├── SKILL.md
│       ├── reference/       # AgentCore and LangGraph docs
│       └── scripts/         # Utility scripts
├── examples/                # Working examples (for developers who clone)
│   └── langgraph-web-search/
└── README.md
```

## Plugin Development

This repo is a Claude Code plugin marketplace. The skill at `skills/aws-agentcore-langgraph/` documents AWS Bedrock AgentCore + LangGraph integration patterns.

## Working with Examples

```bash
cd examples/langgraph-web-search
cp .env.example .env
uv sync
uv run python agent.py
```

## Key Files

- `.claude-plugin/plugin.json` - Plugin manifest
- `.claude-plugin/marketplace.json` - Marketplace definition
- `skills/aws-agentcore-langgraph/SKILL.md` - Main skill entry point
