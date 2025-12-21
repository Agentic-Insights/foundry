# VHS Recorder Plugin

Professional terminal recording guidance for Claude Code using [Charm's VHS](https://github.com/charmbracelet/vhs).

## Overview

The VHS Recorder plugin provides comprehensive guidance for creating polished terminal recordings using VHS tape files. Whether you're documenting CLI tools, creating tutorials, or building animated README examples, this plugin ensures professional, well-timed recordings that tell a clear story.

## What is VHS?

VHS is a tool for generating terminal GIFs, MP4s, and WebM videos from declarative tape files. Instead of recording your terminal in real-time, you write a script that describes what should happen, giving you perfect control over timing, appearance, and content.

## Use Cases

- **Documentation**: Create step-by-step visual guides for CLI tools
- **README Heroes**: Build engaging animated examples for project READMEs
- **Tutorials**: Record multi-step command sequences with perfect timing
- **Release Announcements**: Showcase new features with professional demos
- **Bug Reports**: Demonstrate issues with reproducible recordings

## Installation

### Install the Plugin

```bash
# Install from marketplace
claude-code plugin install agentic-insights/vhs-recorder

# Or install from local path
claude-code plugin install /path/to/claude-plugins-marketplace/plugins/vhs-recorder
```

### Install VHS and Dependencies

VHS requires `ttyd` and `ffmpeg`:

```bash
# macOS
brew install vhs

# Linux
go install github.com/charmbracelet/vhs@latest

# Verify installation
vhs --version
```

## Skills

### `vhs-recorder`

Comprehensive workflow for creating VHS recordings:

- **Structure**: Output declaration → Settings → Requirements → Content
- **Timing**: Guidance on `Sleep` vs `Wait` strategies
- **Visibility**: Using `Hide`/`Show` for clean recordings
- **Best Practices**: Typography, dimensions, and pacing recommendations
- **Patterns**: Common recording scenarios and solutions

Invoke with:
```bash
# In Claude Code conversation
"Create a terminal recording showing how to install and run my CLI tool"
```

## Quick Start

1. **Create a tape file** (`demo.tape`):

```tape
Output demo.gif

Set Width 1200
Set Height 600
Set FontSize 32

Type "echo 'Hello from VHS!'"
Enter
Sleep 2s
```

2. **Generate the recording**:

```bash
vhs demo.tape
```

3. **View the output**: `demo.gif` is created in the current directory

## Key Features

### Complete Tape File Structure

The skill guides you through all sections of a professional tape file:

```
┌─────────────────────────────┐
│ 1. Output Declaration       │  Where to save recordings
│ 2. Settings/Configuration   │  Terminal appearance & behavior
│ 3. Requirements (optional)  │  Dependency checks
│ 4. Setup (hidden)           │  Environment preparation
│ 5. Recording Commands       │  The demonstration
│ 6. Cleanup (hidden)         │  Teardown operations
└─────────────────────────────┘
```

### Timing Strategies

Learn when to use:
- **`Wait`**: Wait for shell prompt or specific output patterns
- **`Sleep`**: Fixed delays for known durations
- **`Wait /pattern/`**: Wait for specific text to appear
- **Per-command timing**: Override global `TypingSpeed` for emphasis

### Appearance Presets

Recommendations for different use cases:

| Use Case | Dimensions | Font | Purpose |
|----------|-----------|------|---------|
| README Hero | 1200×600 | 32-46px | Eye-catching intro |
| Tutorial | 1400×800 | 24-28px | Detailed walkthrough |
| Social Media | 1920×1080 | 46-52px | Shareable demos |
| Compact | 800×500 | 20-24px | Quick examples |

### Hidden Setup/Cleanup

Master the `Hide`/`Show` pattern for clean recordings:

```tape
Hide
Type "npm install --silent"
Enter
Sleep 5s
Type "clear"
Enter
Show

# Now record the actual demo
Type "npm run demo"
Enter
```

## Examples

### Basic Command Demonstration

```tape
Output demo.gif
Set Width 1200
Set Height 600

Type "ls -la"
Enter
Wait
Sleep 2s
```

### Multi-Stage Tutorial

```tape
Output tutorial.gif
Set FontSize 28

# Stage 1: Show problem
Type "git status"
Enter
Wait
Sleep 2s

# Stage 2: Fix
Type "git add ."
Enter
Type "git commit -m 'fix: resolve conflict'"
Enter
Wait
Sleep 1s

# Stage 3: Verify
Type "git status"
Enter
Wait
Sleep 3s
```

See the `examples/` directory for complete tape file examples.

## Configuration

The plugin provides guidance on all VHS settings:

### Terminal Appearance
- `Width`, `Height` - Terminal dimensions
- `FontSize`, `FontFamily` - Typography
- `Theme` - Color scheme (built-in or custom JSON)
- `Padding`, `BorderRadius` - Visual polish
- `WindowBar` - macOS-style title bar options

### Timing & Behavior
- `TypingSpeed` - Global or per-command typing delay
- `Framerate` - Frame capture rate
- `PlaybackSpeed` - Speed up or slow down final output
- `LoopOffset` - Trim loop point for GIFs

### Output Options
- `.gif` - Animated GIF for web
- `.mp4` - Video for social media
- `.webm` - Modern web video format
- `directory/` - PNG sequence for post-processing
- `.ascii` - Text output for CI testing

## Best Practices

### The 3-2-1 Timing Rule
- **3 seconds** after command completion
- **2 seconds** between actions
- **1 second** for quick pauses

### Quality Checklist
- [ ] Output formats declared first
- [ ] Settings configured before commands
- [ ] Setup/cleanup hidden with `Hide`/`Show`
- [ ] Terminal cleared before main content
- [ ] Appropriate `Wait` vs `Sleep` usage
- [ ] Timing allows reading all output
- [ ] No sensitive information exposed
- [ ] Tested successfully with `vhs tape.tape`

### Common Pitfalls

1. **Too Fast**: Commands run before previous output completes
   - **Fix**: Use `Wait` or `Sleep` after commands

2. **Ugly State**: Recording starts with messy terminal
   - **Fix**: Use `Hide` → `clear` → `Show` pattern

3. **Inconsistent Timing**: Hard to follow the flow
   - **Fix**: Apply 3-2-1 timing rule consistently

4. **Exposed Secrets**: API keys or tokens visible
   - **Fix**: Use placeholder values or redacted strings

## Advanced Techniques

### Dynamic Content Waiting

```tape
Type "npm run build"
Enter
Wait /Build succeeded/  # Wait for specific output

Type "npm start"
Enter
Wait /Server listening/
Sleep 1s
```

### Environment Variables

```tape
Env DATABASE_URL "postgresql://localhost/demo"
Env LOG_LEVEL "debug"
```

### Screenshot Capture

```tape
Type "curl https://api.example.com"
Enter
Wait /200 OK/
Screenshot screenshots/success.png
Sleep 1s
```

### Multi-Output Strategy

```tape
Output demo.gif        # For README
Output demo.mp4        # For social media
Output demo.webm       # For modern browsers
Output frames/         # For post-processing
```

## Resources

- [VHS GitHub Repository](https://github.com/charmbracelet/vhs)
- [VHS Documentation](https://github.com/charmbracelet/vhs/blob/main/README.md)
- [Charm.sh Community](https://charm.sh)
- Run `vhs manual` for complete command reference

## Validation

The plugin guides you through testing and validation:

1. **Quick Preview**: Use `.ascii` output for instant feedback
2. **Dependency Check**: Verify `vhs`, `ttyd`, `ffmpeg` are installed
3. **Dry Run**: Test timing and flow before final render
4. **Quality Review**: Follow the complete checklist

## Contributing

Found a useful VHS pattern or improvement? Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Add examples or improve documentation
4. Submit a pull request

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/Agentic-Insights/claude-plugins-marketplace/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Agentic-Insights/claude-plugins-marketplace/discussions)
- **VHS Issues**: [VHS GitHub Issues](https://github.com/charmbracelet/vhs/issues)

---

**Related Plugins**
- [`build-agent-skills`](../build-agent-skills/) - Create custom Claude Code skills
- [`superpowers`](https://github.com/superpowers-marketplace/superpowers) - Advanced development workflows

**Powered by [Agentic Insights](https://agenticinsights.com)** - AI Engineering Consulting
