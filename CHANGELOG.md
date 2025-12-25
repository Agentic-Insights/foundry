# Changelog

## [3.0.0](https://github.com/Agentic-Insights/claude-plugins-marketplace/compare/v2.4.0...v3.0.0) (2025-12-25)


### ⚠ BREAKING CHANGES

* Repository restructured as multi-plugin marketplace

### Features

* add Agent Skills benchmark framework ([0402d59](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/0402d59cb4a0aebde25207ad14ebc23d1bdff307))
* add AgentCore Memory demo example ([24e589b](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/24e589b0a956db90bb2cf7de3e22f0a463b6da66)), closes [#8](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues/8)
* add AgentCore primitive demos for Gateway, Browser, Code Interpreter, and Guardrails ([9bb866c](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/9bb866cd56e0213fccc3e5e5fa7ef95361156e0f))
* add BAML extraction example for type-safe LLM parsing ([6945f9b](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/6945f9bb9f2037caa5293678e6b437ffa08b3163))
* add baml plugin, marketplace browser, and restructure skills ([dd20bcb](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/dd20bcbb8e265f51255d070ff9d5b9558bb32720))
* add build-agent-skills to marketplace and streamline plugin listings ([495bdaa](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/495bdaac0fa3e5765b68f394a7315d449926284e))
* add justfile for plugin version management ([a7ef0d3](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/a7ef0d329648e90c78fc9a142912ceeb4c30e029))
* add plugin validation script and CI/CD workflow ([af4cf80](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/af4cf80cdeb01699575ca9657f7732ec2abf5d83))
* add Policy, Runtime demos and Deep Research Agent ([98a468e](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/98a468e80b8b1b9ea9ac6a11c115762e9ede6d24))
* add VHS terminal recording infrastructure ([7ebf073](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/7ebf0732dab8670337332b5e53bd0e3344388e7d))
* **adversarial-coach:** add coach-player adversarial review plugin ([b4a39c4](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/b4a39c483613495bfe7cfb60b6ddea741e74244e))
* **aws-agentcore-langgraph:** add multi-agent orchestration patterns and reference architecture ([0c05bce](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/0c05bce4af806f29de8261ca7fd2ef29a2de35b3))
* **build-agent-skills:** add Agent Skills open standard plugin ([39b481c](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/39b481cf6292c474eb04268fd89ca5ea93fabe67))
* **plugins:** add para-pkm plugin for PARA knowledge management ([b5bce00](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/b5bce004f2c0b17819579b0e98f7e97fe6688138))
* restructure plugins to Agent Skills spec, update BAML from BoundaryML gist ([8d44523](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/8d44523393752c909e09bfa5aa8c8b4f5fdcfbbe))
* transform aws-skills-cc into claude-plugins-marketplace ([3b17f2f](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/3b17f2f2e3683a51f4cbc28691625a83cc908408))
* update VHS tapes for clean, live recordings ([ba6df75](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/ba6df75f1635cfd46fa808d8736069ffc6649582))
* **vhs-recorder:** add terminal recording plugin and update .gitignore ([8ccf885](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/8ccf88530e1f9d9ac7da0a4c51654b85178d5f8f))


### Bug Fixes

* add ./ prefix to plugin source paths in marketplace.json ([2855e32](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/2855e3294de3b3bb8af22646f00985d45924ae74))
* add missing para-pkm and vhs-recorder plugins to marketplace ([36e3a30](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/36e3a30f74b23e3f628891eb1695488ac7c84bf2))
* add plugin auto-update support documentation ([f0137c2](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/f0137c2a27975afacd464251c1d87c156694d797))
* add skills-ref validation to justfile, fix SKILL.md frontmatter ([ea244c1](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/ea244c1cf9f63df077d36800cc63e032e4e28680))
* configure release-please workflow permissions ([fb15268](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/fb15268c8ba46807f4dc1a742a3eef3e32136e0e))
* convert author field from string to object in plugin manifests ([aa6da34](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/aa6da34237352de8a3a00ef1d9cf2868a3db98bf))
* marketplace source path must start with ./ ([65813a5](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/65813a5d8ff21de53ab9582c2cd906a2efe4d94e))
* marketplace source path must start with ./ ([fda533d](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/fda533d70741102125f97fdbc53074050a45f1b0))
* update marketplace versions and remove invalid references ([c6a5fa8](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/c6a5fa82ed2abe6d7442e78dd372a3017bc8efc8))
* use ddgs package for DuckDuckGo search ([95e784d](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/95e784dac2e28b83162f610a1c75243d6f6ed2fd))

## [2.3.0](https://github.com/Agentic-Insights/claude-plugins-marketplace/compare/v2.2.0...v2.3.0) (2025-12-21)


### Features

* **plugins:** add para-pkm plugin for PARA knowledge management ([b5bce00](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/b5bce004f2c0b17819579b0e98f7e97fe6688138))

## [2.2.0](https://github.com/Agentic-Insights/claude-plugins-marketplace/compare/v2.1.0...v2.2.0) (2025-12-21)


### Features

* add build-agent-skills to marketplace and streamline plugin listings ([495bdaa](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/495bdaac0fa3e5765b68f394a7315d449926284e))

## [2.1.0](https://github.com/Agentic-Insights/claude-plugins-marketplace/compare/v2.0.0...v2.1.0) (2025-12-21)


### Features

* **build-agent-skills:** add Agent Skills open standard plugin ([39b481c](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/39b481cf6292c474eb04268fd89ca5ea93fabe67))

## [2.0.0](https://github.com/Agentic-Insights/claude-plugins-marketplace/compare/v1.0.2...v2.0.0) (2025-12-21)


### ⚠ BREAKING CHANGES

* Repository restructured as multi-plugin marketplace

### Features

* add AgentCore Memory demo example ([24e589b](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/24e589b0a956db90bb2cf7de3e22f0a463b6da66)), closes [#8](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues/8)
* add AgentCore primitive demos for Gateway, Browser, Code Interpreter, and Guardrails ([9bb866c](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/9bb866cd56e0213fccc3e5e5fa7ef95361156e0f))
* add BAML extraction example for type-safe LLM parsing ([6945f9b](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/6945f9bb9f2037caa5293678e6b437ffa08b3163))
* add Policy, Runtime demos and Deep Research Agent ([98a468e](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/98a468e80b8b1b9ea9ac6a11c115762e9ede6d24))
* add VHS terminal recording infrastructure ([7ebf073](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/7ebf0732dab8670337332b5e53bd0e3344388e7d))
* transform aws-skills-cc into claude-plugins-marketplace ([3b17f2f](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/3b17f2f2e3683a51f4cbc28691625a83cc908408))
* update VHS tapes for clean, live recordings ([ba6df75](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/ba6df75f1635cfd46fa808d8736069ffc6649582))


### Bug Fixes

* use ddgs package for DuckDuckGo search ([95e784d](https://github.com/Agentic-Insights/claude-plugins-marketplace/commit/95e784dac2e28b83162f610a1c75243d6f6ed2fd))

## [1.0.2](https://github.com/Agentic-Insights/aws-skills-cc/compare/v1.0.1...v1.0.2) (2025-12-17)


### Bug Fixes

* marketplace source path must start with ./ ([65813a5](https://github.com/Agentic-Insights/aws-skills-cc/commit/65813a5d8ff21de53ab9582c2cd906a2efe4d94e))
* marketplace source path must start with ./ ([fda533d](https://github.com/Agentic-Insights/aws-skills-cc/commit/fda533d70741102125f97fdbc53074050a45f1b0))

## [1.0.1](https://github.com/Agentic-Insights/aws-skills-cc/compare/v1.0.0...v1.0.1) (2025-12-17)


### Bug Fixes

* add plugin auto-update support documentation ([f0137c2](https://github.com/Agentic-Insights/aws-skills-cc/commit/f0137c2a27975afacd464251c1d87c156694d797))
* configure release-please workflow permissions ([fb15268](https://github.com/Agentic-Insights/aws-skills-cc/commit/fb15268c8ba46807f4dc1a742a3eef3e32136e0e))
