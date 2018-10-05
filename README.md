<h1 align="center">Parsa</h1>

<div align="center">
  <strong>Textract-based multiformat text parser</strong>
</div>

<br />

<div align="center">
  <!-- Build Status -->
  <a href="https://travis-ci.com/rdimaio/parsa">
    <img src="https://travis-ci.com/rdimaio/parsa.svg?branch=master"
      alt="Build Status" />
  </a>
  <!-- Code Coverage -->
  <a href="https://codecov.io/gh/rdimaio/parsa">
    <img src="https://codecov.io/gh/rdimaio/parsa/branch/master/graph/badge.svg"
      alt="Code Coverage" />
  </a>
  <!-- SemVer Version -->
  <a href="https://github.com/rdimaio/parsa">
    <img src="https://img.shields.io/badge/Version-1.1.3-blue.svg"
      alt="SemVer Version" />
  </a>
</div>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">Usage</a> •
  <a href="#download">Download</a> •
  <a href="#related">Related</a> •
  <a href="https://github.com/rdimaio/parsa/blob/master/LICENSE">MIT License</a>
</p>

# parsa
Parsa is a [textract](https://github.com/deanmalmgren/textract)-based CLI text parser that supports most file extensions.
Parsa can parse multiple formats at once, writing them to .txt files in the directory of choice.
See also:
- [parsa-gui](https://github.com/rdimaio/parsa-gui) - Graphical version of parsa

# Supported formats
See [this list](https://textract.readthedocs.io/en/stable/#currently-supporting) from textract's documentation.

# Install
## Linux

# Usage
```bash
# Basic usage
$ parsa path/to/input

# Optional: add output path
$ parsa path/to/input path/to/output

# Optional: ignore files with no extension
$ parsa --noprompt path/to/input
```


## Related projects
- [xparsa](https://github.com/rdimaio/xparsa) - Extended parsa, with statistics like word frequency
- [xparsa-gui](https://github.com/rdimaio/xparsa-gui) - GUI for xparsa

## License
MIT