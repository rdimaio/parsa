<p align="center">
  <img src="parsa/img/logo.png?raw=true" alt="Logo"/>
</p>

<div align="center">
  <strong>The text parser that doesn't care about your file extensions</strong>
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

![Demo GIF](parsa/img/demo.gif?raw=true "Demo GIF")


Parsa is a [textract](https://github.com/deanmalmgren/textract)-based CLI text parser that supports multiple file extensions.
It takes any number of inputs, and outputs them to .txt files in a directory of choice, preserving the structure of the original text.

Use case scenario:
- You have many files of different kinds of formats all together, and you want to parse text from all of them

Parsa can parse multiple formats at once, writing them to .txt files in the directory of choice.
See also:
- [parsa-gui](https://github.com/rdimaio/parsa-gui) - Graphical version of parsa

## Supported formats
See [this page](https://textract.readthedocs.io/en/stable/#currently-supporting) from textract's documentation for a full list of the supported formats and their linked dependencies.

# Key features
- Takes an arbitrary of inputs


# Installation
## Requirements
- Linux
- Python 2.7/3.x 

## Linux
Python can be installed via `pip`.

```bash
$ pip install parsa
```

or clone from directory

# Usage
```bash
# Help message
$ parsa --help
usage: parsa [-h] [--noprompt] [--output [OUTPUT]] input

Textract-based text parser that supports most text file extensions. Parsa can
parse multiple formats at once, writing them to .txt files in the directory of
choice.

positional arguments:
  input                 input file or folder; if a folder is passed as input,
                        parsa will scan every file inside it recursively
                        (scanning subfolders as well)

optional arguments:
  -h, --help            show this help message and exit
  --noprompt, -n        ignore files without an extension and don't prompt the
                        user to input their extension
  --output [OUTPUT], -o [OUTPUT]
                        folder where the output files will be stored. The default folder is:
                        (a) the input file's parent folder, if the input is a file, or
                        (b) a folder named 'parsaoutput' located in the input folder, if the input is a folder.

# Basic usage
$ parsa path/to/input

# Optional: add output path
$ parsa path/to/input path/to/output

# Optional: ignore files with no extension
$ parsa --noprompt path/to/input
```

## Tests
```bash
$ python -m unittest discover tests
```

## Related projects
- [xparsa](https://github.com/rdimaio/xparsa) - Extended parsa, enhanced with statistics about the parsed files (WIP)
- [xparsa-gui](https://github.com/rdimaio/xparsa-gui) - GUI for xparsa (WIP)

## Contributing
Pull requests are welcome! If you would like to include/remove/change a major feature, please open an issue first.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.