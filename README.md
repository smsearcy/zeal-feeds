# zeal-feeds

[![PyPI - Version](https://img.shields.io/pypi/v/zeal-feeds.svg)](https://pypi.org/project/zeal-feeds)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zeal-feeds.svg)](https://pypi.org/project/zeal-feeds)
[![GitHub CI](https://github.com/smsearcy/zeal-feeds/actions/workflows/ci.yml/badge.svg)](https://github.com/smsearcy/zeal-feeds/actions)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

-----

*zeal-feeds* is a command line application for adding user contributed docsets to [Zeal](https://zealdocs.org/),
as an alternative to looking up the URL of the XML feed and pasting in the *Add Feed* option.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Installation

The recommended way to install *zeal-feeds* is via
[uv](https://github.com/astral-sh/uv)
or [pipx](https://pypi.org/project/pipx/),
to provide an isolated installation.

```console
# install with uv
$ uv tool install zeal-feeds
$ zeal-feeds --help

# run without "installing"
$ uvx zeal-feeds

# install with pipx
$ pipx install zeal-feeds
$ zeal-feeds --help
```

Alternatively, *zeal-feeds* can be installed via `pip`,
either for the current user or into the current Python virtual environment.

> **Warning**
>
> This package will install several dependencies into the current environment.
> Consider using `uv` or `pipx` to avoid dependency conflicts.

```console
$ pip install --user zeal-feeds
```

or

```console
$ pip install zeal-feeds
```

## Usage

To search available feeds, use `zeal-feeds search`:

```console
$ zeal-feeds search alpine
⠴ Loading index of user contributed docsets
Matching docsets:
Alpinejs (3.7.x/5_2021-12-14)
```

To install feeds, use `zeal-feeds install`.
The docset name needs to match the name from the `search` results:

```console
$ zeal-feeds install alpinejs attrs
Using cached index of user contributed docsets
Downloading Alpinejs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
.   Installing Alpinejs
Downloading attrs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
.   Installing attrs
```

If a docset is already installed then it will be skipped.

## Acknowledgments

This project was inspired by [zeal-user-contrib](https://github.com/jmerle/zeal-user-contrib),
but the apparent lack of an `npm` equivalent of `pipx` for isolated installations prompted writing a Python version
(I didn't know about `npx` at the time).

This [article](https://hynek.me/articles/productive-fruit-fly-programmer/) by Hynek Schlawack for introducing Dash/Zeal.

https://zealusercontributions.vercel.app/ for providing the docset API with XML feeds for Zeal.

## Contributing

Please open an issue or pull request on GitHub if you have questions, ideas, or issues.

For local development,
[fork and clone](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
the Git repository.

You will need [uv](https://github.com/astral-sh/uv) installed.
[`just`](https://github.com/casey/just) is *recommended* for running local tests,
but you can copy the commands from `Justfile` and run them by hand.

```console
$ uv sync

# run zeal-feeds
$ uv run zeal-feeds

# run test suite
$ just
```

## License

`zeal-feeds` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
