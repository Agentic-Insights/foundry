# VHS Demo Recordings

Terminal recordings for AgentCore demos using [VHS](https://github.com/charmbracelet/vhs).

## Prerequisites

```bash
# macOS
brew install vhs ffmpeg

# Linux (via Homebrew)
brew install vhs ffmpeg

# Or via Go
go install github.com/charmbracelet/vhs@latest
```

## Quick Start

```bash
# Render all demos
./tapes/render.sh

# Render specific demo
./tapes/render.sh hero      # Hero/overview demo
./tapes/render.sh 01        # Memory demo
./tapes/render.sh deep      # Deep research agent

# Clean and re-render
./tapes/render.sh --clean
./tapes/render.sh
```

## Tape Files

| File | Description | Duration |
|------|-------------|----------|
| `00-overview.tape` | Project structure tour | ~15s |
| `01-memory.tape` | Memory persistence demo | ~20s |
| `02-gateway.tape` | MCP gateway integration | ~20s |
| `03-browser.tape` | Cloud browser automation | ~20s |
| `04-code-interpreter.tape` | Sandboxed code execution | ~20s |
| `05-guardrails.tape` | Safety controls demo | ~20s |
| `06-policy.tape` | Cedar authorization | ~20s |
| `07-runtime.tape` | Serverless deployment | ~20s |
| `08-deep-research.tape` | Complete showcase | ~25s |
| `09-hero.tape` | Marketing hero demo | ~15s |

## Output

Recordings are saved to `recordings/` (gitignored):
- `*.gif` - For README embeds, social media
- `*.mp4` - For higher quality playback

## Customization

### Shared Settings

Edit `_settings.tape` to change:
- Theme (see `vhs themes` for options)
- Font size and family
- Window dimensions
- Typing speed

### Adding New Demos

1. Create `NN-name.tape`
2. Source settings: `Source tapes/_settings.tape`
3. Set output: `Output recordings/NN-name.gif`
4. Add commands

## Best Practices

- **Pacing**: Use `Sleep` for readability (~500ms between sections)
- **Hide setup**: Wrap prep commands in `Hide`/`Show`
- **Wait for output**: Use `Sleep` after commands that produce output
- **Keep it short**: 15-30 seconds per demo is ideal

## Publishing

VHS can publish GIFs to their CDN:

```bash
vhs publish recordings/09-hero.gif
# Returns a shareable URL
```

## References

- [VHS Documentation](https://github.com/charmbracelet/vhs)
- [Tape File Reference](https://github.com/charmbracelet/vhs#tape-syntax)
- [Available Themes](https://github.com/charmbracelet/vhs#themes)
