# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Add
- Object display size configuration(LeftCtrl + ScrollWheel)
- Wire frame Mode(Left click)

### Fix
- Y-coordinate issue(https://github.com/yamato080915/3D-py/issues/2)

## [1.2.0] - 2024-08-13
### Added
- Show fps and render latency
- open filedialog(Control+O)

## Changed
- Calculation process optimization

## [1.1.1] - 2024-08-04
### Security
- Use ast.literal_eval() instead of eval()

### Fix
- Fix cursor

## [1.1.0] - 2024-07-31
### Added
- Support for STL file
- File selection
- stl_to_json.py
- to_scratchdata.py

### Fixed
- Calculation of mov function
- Use list comprehension instead of For loop

### Changed
- Update scratchdata_to_json.py

## [1.0.0]

タグ名変えたらcompareのURLダメになった(1.1.1以前)


[Unreleased]: https://github.com/yamato080915/3D-py/compare/v1.2.0...dev
[1.2.0]: https://github.com/yamato080915/3D-py/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/yamato080915/3D-py/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/yamato080915/3D-py/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/yamato080915/3D-py/releases/tag/v1.0.0
