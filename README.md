# Format

Because you have better things to worry about than formatting your code.

## Prerequisites

As this plugin merely acts as a proxy, each formatter will require it's own tool and options for code formatting.

#### JavaScript

JavsScript formatting relies on the amazing [prettier](https://github.com/jlongster/prettier).

    $ npm install -g prettier

#### Rust

Rust formatting relies on the amazing [rustfmt](https://github.com/rust-lang-nursery/rustfmt).

    $ cargo install rustfmt

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
