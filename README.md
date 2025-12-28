# Agentic Insights Foundry

**Where agentic tools are forged.** Claude Code plugins for AI engineering.

![Plugin Installation Demo](./recordings/assets/plugin-installation.gif)

## Philosophy

Context is everything. Before agents can act, they must understand.

This foundry grew from years of work on **context engineering** - the practice of giving AI systems the right information at the right time. It started with [Codebase Context](https://codebasecontext.org) and the `.context.md` specification, which evolved into the [AGENTS.md](https://agents.md/) standard now adopted across the industry. The same principles drive MCP, skills, and every plugin here.

**Our principles:**

- **Context over prompting** - Rich, structured context beats clever prompt tricks
- **Open standards** - Portable formats that work across tools and vendors
- **Consulting-grade** - Production patterns from real client engagements
- **Evidence over claims** - Test it, measure it, prove it works

These plugins encode repeatable solutions from AI engineering consulting. Each represents a pattern that worked in production, extracted and packaged for reuse.

**Full story:** [codebasecontext.org](https://codebasecontext.org)

## Quick Install

```bash
/plugin marketplace add agentic-insights/foundry
```

## Plugins

| Plugin | Description | Install |
|--------|-------------|---------|
| [aws-agentcore-langgraph](./plugins/aws-agentcore-langgraph/) | Deploy LangGraph agents on AWS Bedrock AgentCore | `/plugin install aws-agentcore-langgraph@agentic-insights` |
| [baml](./plugins/baml/) | Type-safe LLM extraction with BAML codegen | `/plugin install baml@agentic-insights` |
| [build-agent-skills](./plugins/build-agent-skills/) | Build skills with Agent Skills open standard | `/plugin install build-agent-skills@agentic-insights` |
| [copywriter](./plugins/copywriter/) | UX/marketing copy + Chain-of-Density summarization | `/plugin install copywriter@agentic-insights` |
| [adversarial-coach](./plugins/adversarial-coach/) | Adversarial code review (Block g3 research) | `/plugin install adversarial-coach@agentic-insights` |
| [vhs-recorder](./plugins/vhs-recorder/) | Record terminal demos with Charm VHS | `/plugin install vhs-recorder@agentic-insights` |
| [para-pkm](./plugins/para-pkm/) | PARA knowledge management system | `/plugin install para-pkm@agentic-insights` |

---

## Plugin Details

<details>
<summary><strong>aws-agentcore-langgraph</strong></summary>

Deploy LangGraph 1.0 agents on AWS Bedrock AgentCore.

- **Skill:** `aws-agentcore-langgraph` - Runtime, memory, and Gateway integration
- **CLI:** `agentcore configure|launch|invoke|destroy`

[Documentation →](./plugins/aws-agentcore-langgraph/)
</details>

<details>
<summary><strong>baml</strong></summary>

Type-safe LLM extraction with BAML. MCP-powered codegen with LangGraph integration.

- **Skill:** `baml-codegen` - Generate code, schemas, tests from requirements
- **Agents:** `baml-architect`, `baml-debugger`, `baml-tester`
- **Commands:** `/baml-init`, `/baml-schema`, `/baml-test`, `/baml-diagnose`
- **Requires:** MCP server `baml_Docs` (optional: `baml_Examples`)

[Documentation →](./plugins/baml/) | Credits: [Fry](https://github.com/FryrAI)
</details>

<details>
<summary><strong>build-agent-skills</strong></summary>

Build portable skills with the [Agent Skills](https://agentskills.io) open standard.

- **Skill:** `working-with-agent-skills` - Create, validate, publish skills
- **CLI:** `skills-ref validate|inspect`

[Documentation →](./plugins/build-agent-skills/)
</details>

<details>
<summary><strong>copywriter</strong></summary>

Expert copywriting for UX, marketing, and product content with Chain-of-Density summarization.

- **Skills:** `copywriter` (UX copy, landing pages, emails), `chain-of-density` (iterative compression)
- **Agent:** `cod-iteration` - Single-iteration density worker

[Documentation →](./plugins/copywriter/) | Credits: [daffy0208/ai-dev-standards](https://github.com/daffy0208/ai-dev-standards)
</details>

<details>
<summary><strong>adversarial-coach</strong></summary>

Adversarial code review based on Block's [g3 dialectical autocoding research](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf).

- **Command:** `/coach [requirements-file]` - Independent implementation review
- **Agent:** `coach` - Fresh context reviewer, catches missing auth/error handling

[Documentation →](./plugins/adversarial-coach/)
</details>

<details>
<summary><strong>vhs-recorder</strong></summary>

Record terminal sessions with Charm's VHS for CLI demos and tutorials.

- **Skill:** `vhs-recorder` - Create VHS tape files with timing control
- **Examples:** `basic-demo.tape`, `cli-tool-demo.tape`, `git-workflow.tape`

[Documentation →](./plugins/vhs-recorder/)
</details>

<details>
<summary><strong>para-pkm</strong></summary>

PARA (Projects, Areas, Resources, Archives) knowledge management system.

- **Skill:** `para-pkm` - Organize knowledge bases with PARA methodology
- **Scripts:** `init_para_kb.py`, `archive_project.py`, `validate_para.py`

[Documentation →](./plugins/para-pkm/)
</details>

---

## License

| Plugin | License |
|--------|---------|
| aws-agentcore-langgraph | Apache-2.0 |
| baml | Apache-2.0 |
| build-agent-skills | Apache-2.0 |
| copywriter | Apache-2.0 |
| adversarial-coach | Apache-2.0 |
| vhs-recorder | Apache-2.0 |
| para-pkm | Apache-2.0 |

## Contributing

[GitHub Issues](https://github.com/agentic-insights/foundry/issues) for bugs and feature requests.
