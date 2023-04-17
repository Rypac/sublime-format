# Sublime Format

A code formatting plugin for Sublime Text… because you have better things to worry about than manually formatting your code.

## Contents

- [Usage](#usage)
- [Installation](#installation)
- [Commands](#commands)
- [Key Bindings](#keybindings)

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

- `Format: Format File` – Format the current file
- `Format: Format Selection` – Format the current selection(s)
- `Format: Enable Formatter` – Select source file types to enable formatting for
- `Format: Disable Formatter` – Select source file types to disable formatting for
- `Format: Enable Format on Save` – Select source file types to enable automatic formatting on save
- `Format: Disable Format on Save` – Select source file types to disable automatic formatting on save
- `Preferences: Format Settings` – Edit plugin settings
- `Preferences: Format Key Bindings` – Edit plugin key bindings

## Key Bindings

To avoid potential conflicts, this plugin does not enable key bindings by default.

The following is an example that uses a single key binding to format either the entire file or a selection, based on the `selection_empty` context.

```json
[
    {
        "keys": ["primary+k", "primary+f"],
        "command": "format_file",
        "context": [
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true }
        ]
    },
    {
        "keys": ["primary+k", "primary+f"],
        "command": "format_selection",
        "context": [
            { "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }
        ]
    }
]
