# Changes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Categories:

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
-->

## 0.3.0 - 2025-03-21

### Added

* Recommend *uv* as another preferred method of installation/execution.
* Add `--config` option to specify `Zeal.conf` configuration file.

### Fixed

* Failure to find configuration folder for Flatpak. [#9](https://github.com/smsearcy/zeal-feeds/issues/9)


## 0.2.3 - 2024-09-13

### Fixed

* Resolving packaging issues and tagging mistake


## 0.2.2 - 2024-09-12

### Fixed

* Fix issue installing wxPython Docset due folder name with version. [#7](https://github.com/smsearcy/zeal-feeds/issues/7)

## 0.2.1 - 2023-02-10

### Fixed

* Packaging release to fix broken link to CI status in README.

## 0.2.0 - 2023-02-09

### Added

* Fuzzy search fallback if exact match does not find anything. [#2](https://github.com/smsearcy/zeal-feeds/pull/2)

## 0.1.0 - 2023-02-04

Initial release of *zeal-feeds* with basic `install` and `search` functionality.
