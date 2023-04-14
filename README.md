# Sublime Format

A code formatting plugin for Sublime Text… because you have better things to worry about than manually formatting your code.

## Contents

- [Usage](#usage)
- [Installation](#installation)
- [Commands](#commands)
- [Keybindings](#keybindings)

## Usage

As this plugin merely acts as proxy for external formatters, each formatter will require its own tool and options for code formatting.

There are no default formatters included in the plugin, and each formatter must be manually enabled in the plugin preferences.
For example, this is the configuration for the formatting of Haskell and Rust source code:

```json
{
    "formatters": {
        "Haskell": {
            "command": ["fourmolu", "--indentation", "$tab_size", "--stdin-input-file", "-"],
            "selector": "source.haskell"
        },
        "Rust": {
            "command": ["rustfmt"],
            "selector": "source.rust",
            "format_on_save": true
        }
    }
}
```

The [Sublime Text documentation](https://www.sublimetext.com/docs/selectors.html) describes the concept of scopes and selector matching.
To find the scope at a given position, go to: Menu → Tools → Developer → Show Scope Name.

## Installation

### Package Control (coming soon…)

1. Install [Package Control](https://packagecontrol.io)
2. Run `Package Control: Install Package` in the Command Palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>)
3. Install `Format`

### Manual (via Package Control)

1. Install [Package Control](https://packagecontrol.io)
2. Run `Package Control: Add Repository` in the Command Palette
3. Add the repository: `https://github.com/Rypac/sublime-format.git`
4. Run `Package Control: Install Package` in the Command Palette
5. Install `sublime-format`

### Manual (via `git`)

1. Navigate to the Sublime Text package directory
2. Clone the repository:

    ```
    git clone https://github.com/Rypac/sublime-format.git Format
    ```

## Commands

- `Format: Format File`
    + Format the current file
- `Format: Format Selection`
    + Format the current selection
- `Format: Enable Formatter…`
    + Select source file types to enable formatting for
- `Format: Disable Formatter…`
    + Select source file types to disable formatting for
- `Format: Enable Format on Save…`
    + Select source file types to enable automatic formatting on save
- `Format: Disable Format on Save…`
    + Select source file types to disable automatic formatting on save

## Keybindings

- `Format: Format Selection`
    + macOS: (<kbd>Cmd</kbd>+<kbd>K</kbd>, <kbd>Cmd</kbd>+<kbd>S</kbd>)
    + Windows/Linux: (<kbd>Ctrl</kbd>+<kbd>K</kbd>, <kbd>Ctrl</kbd>+<kbd>S</kbd>)
- `Format: Format File`
    + macOS: (<kbd>Cmd</kbd>+<kbd>K</kbd>, <kbd>Cmd</kbd>+<kbd>F</kbd>)
    + Windows/Linux: (<kbd>Ctrl</kbd>+<kbd>K</kbd>, <kbd>Ctrl</kbd>+<kbd>F</kbd>)
