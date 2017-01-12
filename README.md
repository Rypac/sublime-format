# Format

Because you have better things to worry about than formatting your code.

## Supported Languages

- [Elm](#elm-elm-format)
- [JavaScript](#javascript-prettier)
- [Python](#python-yapf)
- [Rust](#rust-rustfmt)
- [Terraform](#terraform-terraform-format)

## Prerequisites

As this plugin merely acts as a proxy, each formatter will require it's own tool and options for code formatting.

#### Elm ([`elm-format`](https://github.com/avh4/elm-format))

Download [the latest release](https://github.com/avh4/elm-format/releases) from the repo and ensure the binary is available on your `$PATH`.

#### JavaScript ([`prettier`](https://github.com/jlongster/prettier))

    $ npm install -g prettier

#### Python ([`yapf`](https://github.com/google/yapf))

    $ pip install yapf

#### Rust ([`rustfmt`](https://github.com/rust-lang-nursery/rustfmt))

    $ cargo install rustfmt

#### Terraform ([`terraform fmt`](https://github.com/hashicorp/terraform))

Visit [the website](https://www.terraform.io/downloads.html) and follow the instructions to download and install.

## Installation

#### Package Control (coming soon...)

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
