# Agentic Insights Plugin Marketplace

**Professional Claude Code plugins for AI engineering excellence.**

A curated collection of production-ready plugins for building and deploying AI systems, developed through real-world consulting engagements.

## Claude Code Installation

```bash
/plugin marketplace add Agentic-Insights/claude-plugins-marketplace
```

## Available Plugins

### [aws-agentcore-langgraph](./plugins/aws-agentcore-langgraph/)

Deploy LangGraph 1.0 agents on AWS Bedrock AgentCore with production-ready infrastructure.

**Skill Installation (Claude Code):**
```bash
/plugin install aws-agentcore-langgraph@agentic-insights
```

<details>
<summary><strong>What's included</strong></summary>

**🔌 Skill:**
- `aws-agentcore-langgraph` - Deploy LangGraph agents with AgentCore runtime, memory, and Gateway integration

**⚡ CLI Commands:**
- `agentcore configure` - Configure agent deployment
- `agentcore launch` - Deploy agent to AWS
- `agentcore invoke` - Test agent invocation
- `agentcore destroy` - Clean up resources

</details>

[View Documentation →](./plugins/aws-agentcore-langgraph/)

---

### [build-agent-skills](./plugins/build-agent-skills/) 🆕

Build skills with the **[Agent Skills](https://agentskills.io)** open standard - create, validate, and publish portable skills for AI agents across Claude Code, Cursor, GitHub Copilot, and more.

**Skill Installation (Claude Code):**
```bash
/plugin install build-agent-skills@agentic-insights
```

<details>
<summary><strong>What's included</strong></summary>

**🔌 Skill:**
- `working-with-agent-skills` - Create, validate, and publish Agent Skills following the official open standard

**⚡ CLI Commands:**
- `skills-ref validate` - Validate skill structure and metadata
- `skills-ref inspect` - Inspect skill details

</details>

[View Documentation →](./plugins/build-agent-skills/)

---

### [vhs-recorder](./plugins/vhs-recorder/) 🆕

Professional terminal recording with Charm's VHS - comprehensive guidance for creating polished CLI demonstrations, tutorials, and documentation videos.

**Skill Installation (Claude Code):**
```bash
/plugin install vhs-recorder@agentic-insights
```

<details>
<summary><strong>What's included</strong></summary>

**🔌 Skill:**
- `vhs-recorder` - Complete workflow for creating VHS tape files with proper structure, timing, and best practices

**📚 Examples:**
- `basic-demo.tape` - Simple introduction to VHS
- `cli-tool-demo.tape` - CLI tool demonstration with hidden setup/cleanup
- `git-workflow.tape` - Multi-stage git workflow recording
- `tutorial-with-errors.tape` - Realistic tutorial with corrections

</details>

[View Documentation →](./plugins/vhs-recorder/)

## Plugin Categories

- **Agent Development** - Agent Skills standard, skill creation and validation
- **Infrastructure & Deployment** - AWS Bedrock, cloud infrastructure, DevOps patterns
- **AI Engineering** - LangGraph, RAG, agentic workflows
- **Developer Tools** - Terminal recording, CLI demonstrations, documentation
- **Consulting Workflows** - Fractional CTO tools and patterns (coming soon)

## About Agentic Insights

Professional AI engineering consulting for startups and scale-ups. We specialize in:

- **Fractional CTO Services** - Strategic technical leadership and architecture
- **AI Application Development** - LLMs, RAG systems, agentic workflows
- **Production Engineering** - Building reliable systems with non-deterministic AI
- **MLOps & Infrastructure** - Kubernetes-native AI deployments

These plugins encode repeatable patterns and solutions from real consulting engagements.

**Learn more:** [agenticinsights.com](https://agenticinsights.com)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:
- Creating new plugins
- Improving existing plugins
- Documentation and examples
- Bug reports and feature requests

## License

Individual plugins may have different licenses. See each plugin's directory for details.

- Marketplace infrastructure: MIT
- build-agent-skills: Apache-2.0
- aws-agentcore-langgraph: Apache-2.0
- vhs-recorder: MIT

## Support

- **Issues**: [GitHub Issues](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues)
- **Consulting**: [Book a consultation](https://calendar.app.google/mR44LvVuK46PT5nK9) or visit [agenticinsights.com](https://agenticinsights.com)
