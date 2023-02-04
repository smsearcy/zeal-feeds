# zeal-feeds

[![PyPI - Version](https://img.shields.io/pypi/v/zeal-feeds.svg)](https://pypi.org/project/zeal-feeds)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zeal-feeds.svg)](https://pypi.org/project/zeal-feeds)
[![GitHub CI - Tests](https://github.com/smsearcy/zeal-feeds/actions/workflows/test.yml/badge.svg)](https://github.com/smsearcy/zeal-feeds/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

-----

*zeal-feeds* is a command line application for adding user contributed docsets to [Zeal](https://zealdocs.org/),
as an alternative to looking up the URL of the XML feed and pasting in the *Add Feed* option.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Installation

The recommended way to install *zeal-feeds* is via [pipx](https://pypi.org/project/pipx/),
to provide an isolated installation.

```console
$ pipx install zeal-feeds
```

Alternatively, *zeal-feeds* can be installed via `pip`,
either for the current user or into the current Python virtual environment.

> **Warning**
>
> This package will install several dependencies into the current environment.
> Consider using `pipx` to avoid dependency conflicts.

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

## Acknowledgements

This project was inspired by [zeal-user-contrib](https://github.com/jmerle/zeal-user-contrib),
but the apparent lack of an `npm` equivalent of `pipx` for isolated installations prompted writing a Python version.

This [article](https://hynek.me/articles/productive-fruit-fly-programmer/) by Hynek Schlawack for introducing Dash/Zeal.

https://zealusercontributions.vercel.app/ for providing the docset API with XML feeds for Zeal.

## Contributing

Please open an issue or pull request on GitHub if you have questions, ideas, or issues.

*zeal-feeds* uses [hatch](https://hatch.pypa.io/).
Run `hatch run lint` to run checks (Black, Ruff, and mypy) and `hatch run test:pytest` to run unit tests.

## License

`zeal-feeds` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
