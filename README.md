# Format

Because you have better things to worry about than formatting your code.

## Contents

- [Supported Languages](#supported-languages)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Commands](#commands)
- [Keybindings](#keybindings)

## Supported Languages

- [Clang](#clang-clang-format)
- [Elm](#elm-elm-format)
- [Go](#go-gofmt)
- [Haskell](#haskell-hindent)
- [JavaScript](#javascript-prettier)
- [JSON](#json-json)
- [Python](#python-yapf)
- [Rust](#rust-rustfmt)
- [Swift](#swift-swiftformat)
- [Terraform](#terraform-terraform-fmt)

## Prerequisites

As this plugin merely acts as a proxy, each formatter will require it's own tool and options for code formatting.

#### Clang ([`clang-format`](http://clang.llvm.org/docs/ClangFormat.html))

Supports the C family of languages (C, C++, Objective-C, Objective-C++).

Download `clang-format` via you package manager or from [the LLVM website](http://releases.llvm.org/download.html).

#### Elm ([`elm-format`](https://github.com/avh4/elm-format))

    npm install -g elm-format

#### Go ([`gofmt`](https://golang.org/cmd/gofmt))

Installed with `Go` by default. Download `go` via your package manager or from [the website](https://golang.org/dl).

#### Haskell ([`hindent`](https://github.com/commercialhaskell/hindent))

    stack install hindent

#### JavaScript ([`prettier`](https://github.com/jlongster/prettier))

    npm install -g prettier

#### JSON ([`json`](https://docs.python.org/3.3/library/json.html))

Uses the JSON encoder and decoder from the Python standard library.

#### Python ([`yapf`](https://github.com/google/yapf))

    pip install yapf

#### Rust ([`rustfmt`](https://github.com/rust-lang-nursery/rustfmt))

    cargo install rustfmt

#### Swift ([`swiftformat`](https://github.com/nicklockwood/SwiftFormat))

    brew install swiftformat

#### Terraform ([`terraform fmt`](https://github.com/hashicorp/terraform))

Visit [the website](https://www.terraform.io/downloads.html) and follow the instructions to download and install.

## Installation

#### Package Control (coming soon...)

1. Install [Package Control](https://packagecontrol.io)
2. Run `Package Control: Install Package` in the Command Palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>)
3. Install `Format`

#### Manual (via Package Control)

1. Install [Package Control](https://packagecontrol.io)
2. Run `Package Control: Add Repository` in the Command Palette
3. Add the repository: `https://github.com/Rypac/sublime-format.git`
4. Run `Package Control: Install Package` in the Command Palette
5. Install `sublime-format`

#### Manual

1. Navigate to the Sublime Text package directory
2. Clone the repository

        git clone https://github.com/Rypac/sublime-format.git Format

## Commands

- `Format: Format Selection`
    + Format the current selection
- `Format: Format File`
    + Format the current file
- `Format: Toggle Format on Save`
    + Toggle formatting on save for all supported source file types
- `Format: Enable Format on Save...`
    + Select source file types to enable automatic formatting on save
- `Format: Disable Format on Save...`
    + Select source file types to disable automatic formatting on save

## Keybindings

- `Format: Format Selection`
    + OSX: (<kbd>Cmd</kbd>+<kbd>K</kbd>, <kbd>Cmd</kbd>+<kbd>S</kbd>)
    + Windows/Linux: (<kbd>Ctrl</kbd>+<kbd>K</kbd>, <kbd>Ctrl</kbd>+<kbd>S</kbd>)
- `Format: Format File`
    + OSX: (<kbd>Cmd</kbd>+<kbd>K</kbd>, <kbd>Cmd</kbd>+<kbd>F</kbd>)
    + Windows/Linux: (<kbd>Ctrl</kbd>+<kbd>K</kbd>, <kbd>Ctrl</kbd>+<kbd>F</kbd>)
