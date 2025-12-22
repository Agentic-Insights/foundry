# VHS Tape File Syntax Reference

Complete reference for VHS tape file commands and syntax.

## File Structure

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

## Output Commands

Declare where to save recordings:

```tape
Output demo.gif
Output demo.mp4
Output demo.webm
Output frames/       # PNG sequence for post-processing
```

**Multi-output strategy**:
- GIF for web (README, docs)
- MP4 for social media
- WebM for modern browsers
- PNG sequence for post-processing

## Typing Commands

```tape
# Standard typing (uses global TypingSpeed)
Type "echo 'Hello, World!'"

# Override typing speed for emphasis
Type@500ms "This types slowly for dramatic effect"

# Fast typing for boilerplate
Type@10ms "npm run build && npm test"
```

## Navigation & Editing

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
Enter

# Page navigation
PageUp
PageDown

# Modifier keys
Ctrl+C
Ctrl+D
Ctrl+L
```

## Clipboard Operations

```tape
# Copy text to clipboard
Copy "docker-compose up -d"

# Paste from clipboard
Paste
```

## Waiting Strategies

```tape
# Wait for shell prompt (default behavior)
Wait

# Wait for specific text to appear in output
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
- `Wait /pattern/` → Specific output appears in last command
- `Wait+Screen /pattern/` → Text appears anywhere on screen
- `Sleep <duration>` → Known fixed delays

## Visibility Control

```tape
Hide

# Commands here won't appear in the recording
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

## Requirements

Fail early if dependencies are missing:

```tape
Require git
Require node
Require npm
Require docker
```

Place `Require` commands at the top of the file, immediately after settings.

## Environment Variables

```tape
Env DATABASE_URL "postgresql://localhost/demo"
Env LOG_LEVEL "debug"
Env NODE_ENV "development"
```

## Screenshot Capture

```tape
# Capture frame at specific point
Type "curl https://api.example.com/status"
Enter
Wait /200 OK/
Screenshot screenshots/success.png
Sleep 1s
```

## Comments

```tape
# This is a comment
Type "echo 'This is a command'"  # Inline comments work too
```

## Command Reference Table

| Command | Syntax | Description |
|---------|--------|-------------|
| `Output` | `Output file.gif` | Declare output file |
| `Type` | `Type "text"` | Type text |
| `Type@` | `Type@500ms "text"` | Type with custom speed |
| `Enter` | `Enter` | Press Enter key |
| `Wait` | `Wait` | Wait for prompt |
| `Wait` | `Wait /pattern/` | Wait for output text |
| `Wait+Screen` | `Wait+Screen /pattern/` | Wait for text on screen |
| `Wait@` | `Wait@5s /pattern/` | Wait with timeout |
| `Sleep` | `Sleep 2s` | Fixed pause |
| `Up/Down` | `Up 2` | Arrow keys |
| `Left/Right` | `Left 5` | Arrow keys |
| `Backspace` | `Backspace 10` | Delete characters |
| `Tab` | `Tab 2` | Tab key |
| `Space` | `Space 3` | Space key |
| `PageUp/PageDown` | `PageUp` | Page navigation |
| `Ctrl+` | `Ctrl+C` | Control key combo |
| `Copy` | `Copy "text"` | Copy to clipboard |
| `Paste` | `Paste` | Paste from clipboard |
| `Hide` | `Hide` | Stop recording |
| `Show` | `Show` | Resume recording |
| `Require` | `Require git` | Check dependency |
| `Env` | `Env VAR "value"` | Set environment variable |
| `Screenshot` | `Screenshot file.png` | Capture frame |
| `Set` | `Set Width 1200` | Configure setting |

## Multi-Stage Demonstrations Pattern

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
