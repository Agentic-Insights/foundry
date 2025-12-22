# VHS Settings Reference

Complete reference for VHS terminal appearance and configuration settings.

## Setting Syntax

All settings use the `Set` command:

```tape
Set <Setting> <Value>
```

**CRITICAL**: Configure all settings BEFORE any interactive commands. Settings cannot be changed mid-recording.

## Terminal Dimensions

```tape
Set Width 1200
Set Height 600
```

### Common Presets

| Use Case | Width | Height | FontSize | Padding |
|----------|-------|--------|----------|---------|
| README hero | 1200 | 600 | 32-46 | 40 |
| Tutorial detail | 1400 | 800 | 24-28 | 30 |
| Social media | 1920 | 1080 | 46-52 | 60 |
| Compact demo | 800 | 500 | 20-24 | 20 |

**Guidelines**:
- **1200x600** - Most common, works well for READMEs
- **1400x800** - More detail, tutorial mode
- **1920x1080** - Full HD for social media
- **800x500** - Compact, minimal demos

## Typography

```tape
Set FontSize 32
Set FontFamily "JetBrains Mono"
Set LetterSpacing 1
Set LineHeight 1.4
```

### Font Settings

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| `FontSize` | 32 | 12-72 | Text size in pixels |
| `FontFamily` | "JetBrains Mono" | Any font | Must be installed |
| `LetterSpacing` | 1 | 0.5-3 | Space between characters |
| `LineHeight` | 1.4 | 1.0-2.0 | Space between lines |

**Popular fonts**:
- "JetBrains Mono" (default)
- "Fira Code"
- "Monaco"
- "Menlo"
- "Source Code Pro"
- "Cascadia Code"

## Appearance

```tape
Set Theme "Catppuccin Mocha"
Set Padding 40
Set BorderRadius 8
Set WindowBar Colorful
```

### Themes

VHS includes many built-in themes:

```tape
Set Theme "Catppuccin Mocha"
Set Theme "Dracula"
Set Theme "GitHub Dark"
Set Theme "Nord"
Set Theme "Monokai"
Set Theme "Tokyo Night"
Set Theme "Gruvbox Dark"
```

**Popular choices**:
- **Catppuccin Mocha** - Modern, pleasant colors
- **Dracula** - High contrast, vibrant
- **GitHub Dark** - Familiar to developers
- **Nord** - Calm, professional

To see all available themes:
```bash
vhs themes
```

### Padding & Borders

```tape
Set Padding 40          # Space around terminal (pixels)
Set BorderRadius 8      # Corner rounding (pixels)
```

**Guidelines**:
- **20px** - Minimal, compact
- **40px** - Standard, comfortable (recommended)
- **60px** - Spacious, social media
- **BorderRadius 0** - Sharp corners
- **BorderRadius 8** - Subtle rounding (recommended)
- **BorderRadius 16** - Rounded appearance

### Window Bar

```tape
Set WindowBar Colorful    # macOS-style colored buttons
Set WindowBar Rings       # Colored rings
Set WindowBar RingsRight  # Rings on right side
Set WindowBar None        # No window bar
```

**Visual styles**:
- **Colorful** - macOS-style (red, yellow, green)
- **Rings** - Minimalist colored circles
- **RingsRight** - Rings aligned right
- **None** - Clean, no decoration

## Timing Settings

```tape
Set TypingSpeed 50ms
Set Framerate 60
Set PlaybackSpeed 1.0
```

See [timing-control.md](./timing-control.md) for complete timing documentation.

## Complete Configuration Example

### README Hero Configuration

```tape
Output demo.gif

# Optimized for GitHub README
Set Width 1200
Set Height 600
Set FontSize 36
Set FontFamily "JetBrains Mono"
Set Theme "Catppuccin Mocha"
Set Padding 40
Set BorderRadius 8
Set WindowBar Colorful
Set TypingSpeed 50ms
Set Framerate 60
```

### Tutorial Configuration

```tape
Output tutorial.mp4

# Detailed tutorial with more space
Set Width 1400
Set Height 800
Set FontSize 28
Set FontFamily "Fira Code"
Set Theme "GitHub Dark"
Set Padding 30
Set BorderRadius 8
Set WindowBar None
Set TypingSpeed 100ms     # Slower for teaching
Set Framerate 30
Set PlaybackSpeed 0.8     # 80% speed for clarity
```

### Social Media Configuration

```tape
Output social.mp4

# Full HD for Twitter/LinkedIn
Set Width 1920
Set Height 1080
Set FontSize 48
Set FontFamily "JetBrains Mono"
Set Theme "Dracula"
Set Padding 60
Set BorderRadius 16
Set WindowBar Colorful
Set TypingSpeed 50ms
Set Framerate 60
```

### Compact Demo Configuration

```tape
Output compact.gif

# Minimal size, embedded docs
Set Width 800
Set Height 500
Set FontSize 22
Set FontFamily "Monaco"
Set Theme "Nord"
Set Padding 20
Set BorderRadius 4
Set WindowBar None
Set TypingSpeed 25ms      # Faster pace
Set Framerate 30
```

## All Available Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `Width` | number | 1200 | Terminal width in pixels |
| `Height` | number | 600 | Terminal height in pixels |
| `FontSize` | number | 32 | Font size in pixels |
| `FontFamily` | string | "JetBrains Mono" | Font name (must be installed) |
| `LetterSpacing` | number | 1 | Space between characters |
| `LineHeight` | number | 1.4 | Space between lines |
| `Theme` | string | "Catppuccin Mocha" | Color theme |
| `Padding` | number | 40 | Space around terminal |
| `BorderRadius` | number | 8 | Corner rounding |
| `WindowBar` | string | "Colorful" | Window decoration style |
| `TypingSpeed` | duration | 50ms | Default typing speed |
| `Framerate` | number | 60 | Output framerate |
| `PlaybackSpeed` | number | 1.0 | Playback speed multiplier |

## Settings Best Practices

### Structure

```tape
# 1. Output declarations first
Output demo.gif
Output demo.mp4

# 2. All settings together
Set Width 1200
Set Height 600
Set FontSize 32
Set Theme "Catppuccin Mocha"
Set Padding 40
Set TypingSpeed 50ms

# 3. Requirements (if needed)
Require git

# 4. Then commands
Type "echo 'Hello'"
Enter
```

### Common Mistakes

#### ❌ Setting After Commands

```tape
Type "echo 'Hello'"
Enter
Set FontSize 32  # Too late! Settings must come first
```

#### ✅ Settings Before Commands

```tape
Set FontSize 32
Set Theme "Dracula"

Type "echo 'Hello'"
Enter
```

#### ❌ Font Not Installed

```tape
Set FontFamily "CustomFont"  # Will fail if not installed
```

#### ✅ Use Installed Fonts

```bash
# Check installed fonts first
fc-list | grep -i "jetbrains"

# Then use in tape file
Set FontFamily "JetBrains Mono"
```

## Testing Appearance

Use ASCII output for quick iteration:

```tape
Output test.ascii

Set Width 1200
Set Height 600
Set FontSize 32
# ... other settings

Type "test content"
Enter
```

Then view:
```bash
vhs test.tape && cat test.ascii
```

## Resources

- Main documentation: [SKILL.md](../SKILL.md)
- Timing controls: [timing-control.md](./timing-control.md)
- VHS syntax: [vhs-syntax.md](./vhs-syntax.md)
- List all themes: `vhs themes`
- VHS manual: `vhs manual`
