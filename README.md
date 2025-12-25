# Agentic Insights Plugin Marketplace

**Claude Code plugins for AI engineering.**

Plugins for building and deploying AI agents, drawn from consulting engagements and research projects.

![Plugin Installation Demo](./recordings/plugin-installation.gif)

## Claude Code Installation

```bash
/plugin marketplace add Agentic-Insights/claude-plugins-marketplace
```

## Available Plugins

### [aws-agentcore-langgraph](./plugins/aws-agentcore-langgraph/)

Deploy LangGraph 1.0 agents on AWS Bedrock AgentCore.

**Skill Installation (Claude Code):**
```bash
/plugin install aws-agentcore-langgraph@agentic-insights
```

<details>
<summary><strong>Includes</strong></summary>

**🔌 Skill:**
- `aws-agentcore-langgraph` - Deploy LangGraph agents with AgentCore runtime, memory, and Gateway

**⚡ CLI:**
- `agentcore configure` - Configure deployment
- `agentcore launch` - Deploy to AWS
- `agentcore invoke` - Test invocation
- `agentcore destroy` - Clean up

</details>

[Documentation →](./plugins/aws-agentcore-langgraph/)

---

### [build-agent-skills](./plugins/build-agent-skills/) 🆕

Build portable skills with the **[Agent Skills](https://agentskills.io)** open standard. Works with Claude Code, Cursor, and GitHub Copilot.

**Skill Installation (Claude Code):**
```bash
/plugin install build-agent-skills@agentic-insights
```

<details>
<summary><strong>Includes</strong></summary>

**🔌 Skill:**
- `working-with-agent-skills` - Create, validate, and publish Agent Skills

**⚡ CLI:**
- `skills-ref validate` - Validate structure and metadata
- `skills-ref inspect` - Inspect skill details

</details>

[Documentation →](./plugins/build-agent-skills/)

---

### [baml](./plugins/baml/) 🆕

Type-safe LLM extraction with BAML. Generate code from requirements, design schemas, run tests, debug issues. Includes LangGraph integration and MCP-powered codegen.

**Skill Installation (Claude Code):**
```bash
/plugin install baml@agentic-insights
```

<details>
<summary><strong>Includes</strong></summary>

**🔌 Skills:**
- `baml-codegen` - Generate code from natural language via MCP
- `baml-implementation` - Core patterns and best practices
- `baml-philosophy` - Design principles and architecture

**🤖 Agents:**
- `baml-architect` - Schema design
- `baml-debugger` - Debug validation errors
- `baml-tester` - Test generation

**⚡ Commands:**
- `/baml-init` - Initialize projects
- `/baml-schema` - Design schemas
- `/baml-test` - Run tests
- `/baml-diagnose` - Troubleshoot issues

**📋 Requires:**
- MCP server: `baml_Docs`
- MCP server: `baml_Examples` (optional)

</details>

[Documentation →](./plugins/baml/)

**Credits:** Original implementation by [Fry](https://github.com/FryrAI)

---

### [vhs-recorder](./plugins/vhs-recorder/) 🆕

Record terminal sessions with Charm's VHS. Create CLI demos, tutorials, and documentation videos.

**Skill Installation (Claude Code):**
```bash
/plugin install vhs-recorder@agentic-insights
```

<details>
<summary><strong>Includes</strong></summary>

**🔌 Skill:**
- `vhs-recorder` - Create VHS tape files with proper structure and timing

**📚 Examples:**
- `basic-demo.tape` - VHS introduction
- `cli-tool-demo.tape` - CLI demo with hidden setup/cleanup
- `git-workflow.tape` - Multi-stage git workflow
- `tutorial-with-errors.tape` - Tutorial with corrections

</details>

[Documentation →](./plugins/vhs-recorder/)

---

### [adversarial-coach](./plugins/adversarial-coach/) 🆕

Adversarial code review subagent based on Block's [g3 dialectical autocoding research](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf). Validates implementations against requirements with fresh context objectivity.

**Skill Installation (Claude Code):**
```bash
/plugin install adversarial-coach@agentic-insights
```

<details>
<summary><strong>Includes</strong></summary>

**⚡ Command:**
- `/coach [requirements-file]` - Adversarial implementation review

**🤖 Agent:**
- `coach` - Independent code reviewer with fresh context

**🎯 Key Features:**
- Reviews from fresh context (no implementation bias)
- Validates against stated requirements
- Returns `IMPLEMENTATION_APPROVED` or specific actionable fixes
- Catches missing auth, incomplete error handling, skipped requirements

</details>

[Documentation →](./plugins/adversarial-coach/)

## Categories

- **Agent Development** - Agent Skills standard, skill creation, validation
- **Infrastructure** - AWS Bedrock, cloud, DevOps
- **AI Engineering** - LangGraph, RAG, agentic workflows
- **Developer Tools** - Terminal recording, CLI demos, documentation
- **Code Quality** - Adversarial review, validation, testing
- **Consulting** - Fractional CTO tools (coming soon)

## About Agentic Insights

AI engineering consulting for startups and scale-ups:

- **Fractional CTO** - Technical leadership and architecture
- **AI Applications** - LLMs, RAG, agentic workflows
- **Production Engineering** - Reliable systems with non-deterministic AI
- **MLOps** - Kubernetes-native AI deployments

These plugins encode patterns from consulting engagements.

[agenticinsights.com](https://agenticinsights.com)

## Contributing

Contributions welcome:
- New plugins
- Plugin improvements
- Documentation and examples
- Bug reports via [GitHub Issues](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues)

## License

Plugins have individual licenses. See each directory for details.

| Plugin | License |
|--------|---------|
| Marketplace | MIT |
| aws-agentcore-langgraph | Apache-2.0 |
| build-agent-skills | Apache-2.0 |
| baml | Apache-2.0 |
| para-pkm | MIT |
| vhs-recorder | MIT |
| adversarial-coach | Apache-2.0 |

## Support

- [GitHub Issues](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues)
- [Book a consultation](https://calendar.app.google/mR44LvVuK46PT5nK9)
