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

# VHS Recorder Skill Workflow

## When to Use This Skill

Use this skill when you need to:
- Create terminal recordings for documentation
- Demonstrate CLI tool usage
- Build animated examples for READMEs
- Record step-by-step command sequences
- Produce professional software demo videos

## Prerequisites Check

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

## VHS Tape File Structure

Every VHS tape file follows this structure:

```
┌─────────────────────────────┐
│ 1. Output Declaration       │  Where to save the recording
│ 2. Settings/Configuration   │  Terminal appearance & behavior
│ 3. Requirements (optional)  │  Fail-fast dependency checks
│ 4. Setup (often hidden)     │  Prepare environment
│ 5. Recording Commands       │  The actual demonstration
│ 6. Cleanup (often hidden)   │  Teardown operations
└─────────────────────────────┘
```

## Step-by-Step Workflow

### Step 1: Define Output Formats

Start every tape file by declaring where to save outputs:

```tape
Output demo.gif
Output demo.mp4
Output demo.webm
```

**Multi-output strategy**:
- GIF for web (README, docs)
- MP4 for social media
- WebM for modern browsers
- PNG sequence for post-processing: `Output frames/`

### Step 2: Configure Terminal Settings

Set all configuration BEFORE any interactive commands:

```tape
# Terminal Dimensions
Set Width 1200
Set Height 600

# Typography
Set FontSize 32
Set FontFamily "JetBrains Mono"
Set LetterSpacing 1
Set LineHeight 1.4

# Appearance
Set Theme "Catppuccin Mocha"
Set Padding 40
Set BorderRadius 8
Set WindowBar Colorful

# Timing
Set TypingSpeed 50ms
Set Framerate 60
Set PlaybackSpeed 1.0
```

**Common presets**:

| Use Case | Width | Height | FontSize | Padding |
|----------|-------|--------|----------|---------|
| README hero | 1200 | 600 | 32-46 | 40 |
| Tutorial detail | 1400 | 800 | 24-28 | 30 |
| Social media | 1920 | 1080 | 46-52 | 60 |
| Compact demo | 800 | 500 | 20-24 | 20 |

### Step 3: Declare Requirements (Optional)

Fail early if dependencies are missing:

```tape
Require git
Require node
Require npm
```

Place `Require` commands at the top of the file, immediately after settings.

### Step 4: Hidden Setup

Use `Hide`/`Show` to prepare the environment without recording:

```tape
Hide

# Setup that shouldn't appear in the recording
Type "cd /tmp/demo"
Enter
Sleep 500ms

Type "npm install --silent"
Enter
Sleep 5s

Type "clear"
Enter

Show
```

**When to use hidden setup**:
- Installing dependencies
- Cloning repositories
- Building projects
- Creating test files
- Clearing the terminal before recording starts

### Step 5: Record the Demonstration

Now record the actual content using these command patterns:

#### Typing Commands

```tape
# Standard typing (uses global TypingSpeed)
Type "echo 'Hello, World!'"
Enter

# Override typing speed for emphasis
Type@500ms "This types slowly for dramatic effect"
Enter

# Fast typing for boilerplate
Type@10ms "npm run build && npm test"
Enter
```

#### Waiting Strategies

```tape
# Wait for shell prompt (default behavior)
Wait

# Wait for specific text to appear
Wait /Done in/

# Wait for text anywhere on screen
Wait+Screen /SUCCESS/

# Custom timeout (default is 15s)
Wait@5s /Loading complete/

# Fixed sleep for known durations
Sleep 2s
```

**Choose the right waiting strategy**:
- `Wait` (no args) → Shell prompt returns
- `Wait /pattern/` → Specific output appears
- `Sleep <duration>` → Known fixed delays

#### Navigation & Editing

```tape
# Arrow keys
Up 2
Down 1
Left 5
Right 3

# Editing
Backspace 10
Tab 2
Space 3

# Page navigation
PageUp
PageDown

# Modifier keys
Ctrl+C
Ctrl+D
Ctrl+L
```

#### Clipboard Operations

```tape
# Copy text to clipboard
Copy "docker-compose up -d"

# Paste from clipboard
Paste
Enter
```

### Step 6: Control Recording Flow

#### Pausing for Effect

```tape
Type "rm -rf production-database"
Sleep 2s          # Let the danger sink in
Backspace 100     # Phew, that was close!

Type "rm -rf test-database"
Enter
```

#### Hiding Cleanup

```tape
Hide

# Teardown commands
Type "docker-compose down"
Enter
Sleep 2s

Type "rm -rf demo-project"
Enter

Show
```

## Timing Best Practices

### The 3-2-1 Timing Rule

| Situation | Recommended Timing |
|-----------|-------------------|
| After commands | `Sleep 3s` or `Wait` |
| Between actions | `Sleep 2s` |
| Quick pause | `Sleep 1s` |
| Dramatic pause | `Sleep 5s` |

### TypingSpeed Guidelines

```tape
Set TypingSpeed 50ms   # Natural, readable (default)
Set TypingSpeed 100ms  # Slow, tutorial style
Set TypingSpeed 25ms   # Fast, experienced user
Set TypingSpeed 10ms   # Instant (setup/cleanup)
```

**Per-command overrides**:
```tape
Type@500ms "Pay attention to this!"  # Slow emphasis
Type@10ms "boilerplate code here"   # Fast filler
```

## Advanced Patterns

### Environment Configuration

```tape
Env DATABASE_URL "postgresql://localhost/demo"
Env LOG_LEVEL "debug"
```

### Dynamic Content Waiting

```tape
# Wait for build completion
Type "npm run build"
Enter
Wait /Build succeeded/

# Wait for server startup
Type "npm start"
Enter
Wait /Server listening on/
Sleep 1s
```

### Screenshot Capture

```tape
# Capture frame at specific point
Type "curl https://api.example.com/status"
Enter
Wait /200 OK/
Screenshot screenshots/success.png
Sleep 1s
```

### Multi-Stage Demonstrations

```tape
# Stage 1: Show the problem
Type "git status"
Enter
Wait
Sleep 2s

# Stage 2: Apply the fix
Type "git add ."
Enter
Type "git commit -m 'fix: resolve merge conflict'"
Enter
Wait
Sleep 1s

# Stage 3: Verify resolution
Type "git status"
Enter
Wait
Sleep 3s
```

## Common Pitfalls & Solutions

### Problem: Recording Too Fast

```tape
# ❌ Bad: Commands run before output appears
Type "npm install"
Enter
Type "npm start"  # Runs before install finishes!
Enter

# ✅ Good: Wait for completion
Type "npm install"
Enter
Wait /added/      # Wait for install to finish
Sleep 1s
Type "npm start"
Enter
```

### Problem: Ugly Terminal State

```tape
# ❌ Bad: Recording starts with messy terminal
Show
Type "ls"

# ✅ Good: Clean slate
Hide
Type "clear"
Enter
Show
Type "ls"
```

### Problem: Inconsistent Timing

```tape
# ❌ Bad: Hard to follow
Type "command1"
Enter
Type "command2"
Enter

# ✅ Good: Breathing room
Type "command1"
Enter
Wait
Sleep 2s

Type "command2"
Enter
Wait
Sleep 2s
```

### Problem: Sensitive Information

```tape
# ❌ Bad: Exposing secrets
Type "export API_KEY=sk_live_abc123xyz"

# ✅ Good: Use placeholders
Type "export API_KEY=sk_live_xxx_redacted"
```

## Testing & Iteration

### Quick Preview with ASCII Output

```tape
Output demo.ascii
# ... rest of tape file

# View immediately in terminal
cat demo.ascii
```

**Why**: ASCII output is instant (no video encoding). Perfect for iteration.

### Validation Checklist

Before finalizing your recording:

- [ ] All dependencies installed (`vhs`, `ttyd`, `ffmpeg`)
- [ ] Output formats declared at top
- [ ] Settings configured before commands
- [ ] Hidden setup/cleanup for cleanliness
- [ ] Appropriate `Wait` vs `Sleep` usage
- [ ] Timing allows reading output
- [ ] No sensitive information exposed
- [ ] Terminal cleared before main content
- [ ] Tested with `vhs tape.tape`

## Complete Example: CLI Tool Demo

```tape
# demo.tape - Complete example

# Outputs
Output demo.gif
Output demo.mp4

# Configuration
Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Catppuccin Mocha"
Set Padding 40
Set TypingSpeed 50ms

# Dependencies
Require git
Require node

# Hidden Setup
Hide
Type "cd /tmp && rm -rf demo-project"
Enter
Sleep 500ms
Type "git clone https://github.com/example/demo-project"
Enter
Sleep 3s
Type "cd demo-project"
Enter
Type "clear"
Enter
Show

# Main Recording
Type "# Let's explore this project"
Enter
Sleep 1s

Type "ls -la"
Enter
Wait
Sleep 2s

Type "cat package.json"
Enter
Wait
Sleep 3s

Type "# Install dependencies"
Enter
Type "npm install"
Enter
Wait /added/
Sleep 2s

Type "# Run the demo"
Enter
Type "npm run demo"
Enter
Wait /Demo complete/
Sleep 3s

# Hidden Cleanup
Hide
Type "cd /tmp && rm -rf demo-project"
Enter
Show
```

## Execution

Run the tape file:

```bash
vhs demo.tape
```

**Options**:
- `vhs demo.tape` → Generate all declared outputs
- `vhs < demo.tape` → Read from stdin
- `vhs --help` → View all CLI options

## Resources

- [VHS GitHub Repository](https://github.com/charmbracelet/vhs)
- [VHS Manual](https://github.com/charmbracelet/vhs/blob/main/README.md) (or run `vhs manual`)
- [Charm.sh Community](https://charm.sh)

## Quality Checklist

Before considering your VHS recording complete:

1. **Structure**: Output → Settings → Requirements → Content
2. **Timing**: Every command has appropriate `Wait` or `Sleep`
3. **Visibility**: Setup/cleanup hidden with `Hide`/`Show`
4. **Clarity**: Terminal cleared before main content
5. **Pacing**: Viewers can read all output before next action
6. **Testing**: Ran `vhs tape.tape` successfully
7. **Outputs**: All declared formats generated correctly
8. **Privacy**: No sensitive information exposed

---

**Remember**: Great terminal recordings tell a story. Use timing, pauses, and clear structure to guide viewers through your demonstration.
