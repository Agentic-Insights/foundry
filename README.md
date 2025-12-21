# Agentic Insights Plugin Marketplace

**Professional Claude Code plugins for AI engineering excellence.**

A curated collection of production-ready plugins for building and deploying AI systems, developed through real-world consulting engagements.

## Available Plugins

### [build-agent-skills](./plugins/build-agent-skills/) 🆕

Build skills with the **[Agent Skills](https://agentskills.io)** open standard - create, validate, and publish portable skills for AI agents across Claude Code, Cursor, GitHub Copilot, and more.

**Key Features:**
- Complete Agent Skills specification guide
- Validation workflow with `skills-ref` tool
- Cross-platform compatibility guidance
- Real-world examples and templates
- Best practices for skill development

**Use Cases:**
- Creating new skills following the open standard
- Validating skills for compliance
- Converting documentation into portable skills
- Publishing skills to marketplaces
- Ensuring cross-platform compatibility

[View Documentation →](./plugins/build-agent-skills/)

---

### [aws-agentcore-langgraph](./plugins/aws-agentcore-langgraph/)

Deploy LangGraph 1.0 agents on AWS Bedrock AgentCore with production-ready infrastructure.

**Key Features:**
- Runtime wrapping for StateGraph deployment
- Persistent memory integration (STM/LTM)
- Gateway MCP tool connections
- Streamlined CLI deployment workflow

**Use Cases:**
- Deploying stateful LangGraph agents to AWS
- Adding persistent memory to conversational agents
- Connecting agents to external tools and APIs
- Managing production agent infrastructure

[View Documentation →](./plugins/aws-agentcore-langgraph/)

## Installation

### Add the Marketplace

```bash
/plugin marketplace add Agentic-Insights/claude-plugins-marketplace
```

### Install a Plugin

```bash
/plugin install aws-agentcore-langgraph@agentic-insights
```

## Plugin Categories

- **Agent Development** - Agent Skills standard, skill creation and validation
- **Infrastructure & Deployment** - AWS Bedrock, cloud infrastructure, DevOps patterns
- **AI Engineering** - LangGraph, RAG, agentic workflows
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

## Support

- **Issues**: [GitHub Issues](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues)
- **Consulting**: [Book a consultation](https://calendar.app.google/mR44LvVuK46PT5nK9) or visit [agenticinsights.com](https://agenticinsights.com)
