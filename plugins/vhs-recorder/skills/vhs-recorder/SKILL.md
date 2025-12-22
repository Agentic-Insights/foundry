---
name: vhs-recorder
description: Create professional terminal recordings with VHS tape files - guides through syntax, timing, settings, and best practices
---

<EXTREMELY-IMPORTANT>
This skill guides you through creating high-quality terminal recordings using Charm's VHS tool. VHS uses a declarative tape file format to script terminal interactions and produce GIF/MP4/WebM outputs.

VHS recordings are commonly used for:
- CLI tool demonstrations
- Tutorial videos
- Documentation examples
- Software release announcements
- README hero animations
</EXTREMELY-IMPORTANT>

# VHS Recorder Skill Overview

## When to Use This Skill

Use this skill when you need to:
- Create terminal recordings for documentation
- Demonstrate CLI tool usage
- Build animated examples for READMEs
- Record step-by-step command sequences
- Produce professional software demo videos

## Prerequisites

Before starting, verify VHS and its dependencies are installed:

```bash
# Check VHS installation
which vhs

# Check required dependencies
which ttyd
which ffmpeg

# Install if missing (macOS)
brew install vhs

# Install if missing (Linux)
go install github.com/charmbracelet/vhs@latest
```

**CRITICAL**: VHS requires both `ttyd` and `ffmpeg` on your `$PATH`. If either is missing, the recording will fail.

## Quick Start

### Basic Recording Structure

Every VHS tape file follows this pattern:

```tape
# 1. Declare outputs
Output demo.gif
Output demo.mp4

# 2. Configure settings
Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Catppuccin Mocha"
Set Padding 40
Set TypingSpeed 50ms

# 3. Optional requirements
Require git
Require node

# 4. Hidden setup (if needed)
Hide
Type "cd /tmp/demo"
Enter
Sleep 500ms
Type "clear"
Enter
Show

# 5. Main recording
Type "echo 'Hello, World!'"
Enter
Wait
Sleep 2s

# 6. Hidden cleanup (if needed)
Hide
Type "cd /tmp && rm -rf demo"
Enter
Show
```

### Run the Recording

```bash
vhs demo.tape
```

This generates `demo.gif` and `demo.mp4` in the current directory.

## Step-by-Step Workflow

### Step 1: Define Outputs

```tape
Output demo.gif          # For web/README
Output demo.mp4          # For social media
Output demo.webm         # For modern browsers
Output frames/           # PNG sequence for post-processing
```

### Step 2: Configure Settings

**Essential settings** (set these first):

```tape
Set Width 1200           # Terminal width
Set Height 600           # Terminal height
Set FontSize 32          # Text size
Set Theme "Catppuccin Mocha"  # Color scheme
Set Padding 40           # Space around terminal
Set TypingSpeed 50ms     # How fast to type
```

See [settings.md](./references/settings.md) for complete configuration options.

### Step 3: Add Requirements (Optional)

```tape
Require git
Require node
Require docker
```

### Step 4: Hidden Setup

Use `Hide`/`Show` to prepare without recording:

```tape
Hide
Type "npm install --silent"
Enter
Sleep 5s
Type "clear"
Enter
Show
```

### Step 5: Record Main Content

**Basic commands**:

```tape
Type "command here"      # Type text
Enter                    # Press Enter
Wait                     # Wait for prompt
Sleep 2s                 # Fixed pause
```

**Key patterns**:

```tape
# Standard command with pause
Type "ls -la"
Enter
Wait                     # Wait for command to finish
Sleep 2s                 # Give viewer time to read

# Wait for specific output
Type "npm install"
Enter
Wait /added/            # Wait for this text to appear

# Override typing speed
Type@500ms "slow typing for emphasis"
Type@10ms "fast typing for boilerplate"
```

See [vhs-syntax.md](./references/vhs-syntax.md) for all commands.

### Step 6: Control Timing

**The 3-2-1 Rule**:
- 3 seconds after important commands
- 2 seconds between actions
- 1 second for quick transitions

See [timing-control.md](./references/timing-control.md) for complete timing strategies.

## Common Patterns

### Clean Start

```tape
Hide
Type "clear"
Enter
Show
```

### Command-Wait-Pause Pattern

```tape
Type "command"
Enter
Wait                     # Wait for completion
Sleep 2s                 # Let viewer read output
```

### Fast Hidden Setup

```tape
Hide
Type@10ms "cd /tmp && mkdir demo && cd demo"
Enter
Sleep 500ms
Show
```

### Dramatic Effect

```tape
Type "rm -rf production/"
Sleep 3s                 # Let danger sink in
Backspace 100            # Phew, that was close!
```

## Reference Documentation

For detailed information, see these reference guides:

| Topic | File | Contents |
|-------|------|----------|
| **VHS Syntax** | [vhs-syntax.md](./references/vhs-syntax.md) | Complete command reference, waiting strategies, navigation keys |
| **Timing Control** | [timing-control.md](./references/timing-control.md) | TypingSpeed, Wait vs Sleep, pacing patterns, timing best practices |
| **Settings** | [settings.md](./references/settings.md) | Terminal appearance, themes, dimensions, typography, configuration presets |
| **Examples** | [examples.md](./references/examples.md) | Real-world tape files: CLI demos, Git workflows, Docker, API testing |

## Quality Checklist

Before finalizing your VHS recording:

- [ ] All dependencies installed (`vhs`, `ttyd`, `ffmpeg`)
- [ ] Output formats declared at top
- [ ] Settings configured before commands
- [ ] Hidden setup/cleanup for cleanliness
- [ ] Appropriate `Wait` vs `Sleep` usage
- [ ] Timing allows reading output (2-3s after important commands)
- [ ] No sensitive information exposed
- [ ] Terminal cleared before main content
- [ ] Tested with `vhs tape.tape`

## Common Issues

### Recording Too Fast

**Problem**: Commands run before previous output appears

```tape
# ❌ Bad
Type "npm install"
Enter
Type "npm start"  # Runs too soon!

# ✅ Good
Type "npm install"
Enter
Wait /added/      # Wait for completion
Sleep 1s
Type "npm start"
```

### Messy Terminal State

**Problem**: Recording shows previous commands/output

```tape
# ✅ Solution: Clear before recording
Hide
Type "clear"
Enter
Show

Type "your command here"
```

### Inconsistent Pacing

**Problem**: Hard to follow

```tape
# ✅ Solution: Consistent timing pattern
Type "command"
Enter
Wait
Sleep 2s          # Always pause after commands
```

## Quick Tips

1. **Test with ASCII**: Use `Output demo.ascii` for instant previews
2. **Use Hide/Show**: Keep setup/cleanup out of recordings
3. **Wait for output**: Use `Wait /pattern/` for dynamic content
4. **Consistent timing**: Follow the 3-2-1 rule
5. **Clear terminal**: Start with clean state
6. **Check dependencies**: Run `Require` checks early
7. **Multi-format**: Generate GIF + MP4 + WebM
8. **Viewer pacing**: 2-3 seconds after important output

## Resources

- [VHS GitHub Repository](https://github.com/charmbracelet/vhs)
- [VHS Manual](https://github.com/charmbracelet/vhs/blob/main/README.md) (or run `vhs manual`)
- [Charm.sh Community](https://charm.sh)
- View all themes: `vhs themes`

## Next Steps

1. Review [examples.md](./references/examples.md) for real-world patterns
2. Consult [settings.md](./references/settings.md) to customize appearance
3. Read [timing-control.md](./references/timing-control.md) for pacing mastery
4. Reference [vhs-syntax.md](./references/vhs-syntax.md) for complete command list

---

**Remember**: Great terminal recordings tell a story. Use timing, pauses, and clear structure to guide viewers through your demonstration.
