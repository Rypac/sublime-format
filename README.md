# Format

A simple plugin to format JavaScript code.

## Prerequisites

This package relies on the amazing [prettier](https://github.com/jlongster/prettier) to format JavaScript source code files.

Install with `npm install -g prettier`.

## Installation

#### Package Control

1. Install [Package Control](https://packagecontrol.io/)
2. Run `Package Control: Install Package` in the Command Palette (<kbd>Super+Shift+P</kbd>)
3. Install `Format`

#### Manual

1. Navigate to the Sublime Text package directory
2. Clone the repository

        $ git clone https://github.com/Rypac/sublime-format.git Format

## Commands

- `Format: Format Selection`
    + Format the current selection
- `Format: Format File` (<kbd>Ctrl+k</kbd>, <kbd>Ctrl+f</kbd>)
    + Format the current file
- `Format: Enable Format on Save`
    + Enable automatic formatting of JavaScript source files on save
- `Format: Disable Format on Save`
    + Disable automatic formatting of JavaScript source files on save

## Configuration

- `prettier_format_on_save`
    + Automatically format files on save
- `prettier_binary`
    + Full path to `prettier` binary (if not on `PATH`)
