# Changelog

All notable changes to the BAML plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-21

### Added
- Production release for Agentic Insights Claude Code Plugin Marketplace
- 3 production-ready skills:
  - `baml-codegen`: MCP-powered code generation (3800 token budget)
  - `baml-implementation`: Implementation patterns and best practices
  - `baml-philosophy`: Design principles and architectural guidance
- 3 specialized agents:
  - `baml-architect`: Schema design and architecture planning
  - `baml-debugger`: Debugging BAML validation errors
  - `baml-tester`: Test generation and validation
- 4 utility commands:
  - `baml-init`: Initialize new BAML projects
  - `baml-schema`: Schema design assistance
  - `baml-test`: Run and validate tests
  - `baml-diagnose`: Troubleshoot common issues
- Core pattern matching (extraction, classification, RAG, agents)
- MCP integration with baml_Docs server
- Multi-tier caching system (4 tiers)
- Multimodal support (image, audio, vision models)
- Test generation (pytest, Jest, RSpec)
- Framework integration (6 languages, 10+ frameworks)
- 5-layer validation pipeline
- Token optimization (50-70% reduction)
- Real-time repository monitoring
- Fallback patterns for offline operation
- LangGraph integration patterns
- Comprehensive documentation and troubleshooting guides

### Changed
- Migrated from standalone repository to marketplace plugin structure
- Updated license to Apache-2.0
- Updated copyright to Agentic Insights
- Aligned version numbers across all configuration files

### Documentation
- Added comprehensive README with quick start guide
- Added TROUBLESHOOTING.md for common issues
- Added metadata.yaml for plugin configuration
- Included extensive reference documentation
- Added pattern library and examples

### Credits
- Original implementation by [Fry](https://github.com/FryrAI)
- Adapted for Agentic Insights marketplace by Agentic Insights team

## [1.0.0] - 2025-01-25

### Added
- Initial MVP release in standalone repository
- Basic pattern matching capabilities
- MCP integration foundation
- Core code generation functionality
