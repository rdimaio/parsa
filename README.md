<div align="center">
&nbsp;&nbsp;
  <a href="https://github.com/rdimaio/parsa">
    <img src="parsa/img/logo.png?raw=true" alt="Logo"/>
  </a>

  <strong>A text parser that doesn't care about your file extensions</strong>

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
    <img src="https://img.shields.io/badge/Version-1.1.4-blue.svg"
      alt="SemVer Version" />
  </a>

  <a href="#key-features">Key Features</a> •
  <a href="#supported-formats">Supported Formats</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#related-projects">Related projects</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">MIT License</a>
</div>

![Demo GIF](parsa/img/demo.gif?raw=true "Demo GIF")

<p style="text-align: center;">
  <strong>
    Parsa is a <a href="https://github.com/deanmalmgren/textract">textract</a>-based CLI text parser that supports multiple file extensions.
    It takes any number of inputs, and outputs them to .txt files in a directory of choice, preserving the structure of the original text.
  </strong>
</p>

# Key features
- Extends [textract](https://github.com/deanmalmgren/textract)'s functionalities to work with multiple inputs and to automatically save the output
- Takes an arbitrary number of inputs of different filetypes, and processess them all equally when supported
- Outputs the parsed text from the input files individually to corresponding .txt files, with the option of selecting a custom output path
- Includes a naming system that always avoids overwriting existing files, instead naming new files in a simple manner
- Supports over 20 of the most common formats (see [Supported formats](#supported-formats) for more)
- Preserves the structure of document file formats (.docx, .pdf, ...)
- Supports audio formats (.wav, .mp3, ...) via the speech recognition tools [sox](https://github.com/chirlu/sox), [SpeechRecognition](https://github.com/Uberi/speech_recognition) and [pocketsphinx](https://github.com/cmusphinx/pocketsphinx/)
- Supports image formats (.jpg, .png, ...), via the optical character recognition (OCR) tool [tesseract-ocr](https://github.com/tesseract-ocr/tesseract)
- Prompts the user for an input file's extension if it's not explicitly present; this feature can be turned off via `--noprompt`

# Supported formats
See [this page](https://textract.readthedocs.io/en/stable/#currently-supporting) from textract's documentation for a full list of the supported formats and their linked dependencies.

# Installation
## System requirements
- Linux
- Python 2.7/3.x (any Python 3 version)
## Linux
Via `pip`:
```bash
$ pip install parsa
```

Or, if you prefer, you can install it from source:
```bash
# Clone the repository
$ git clone https://github.com/rdimaio/parsa

# Go into the parsa folder
$ cd parsa

# Install parsa
$ python setup.py install
```

### Tests
```bash
$ python -m unittest discover tests
```

# Usage
## Single input
```bash
# Basic usage
$ parsa path/to/input_file
# The output will be saved inside the input file's parent folder.
```

## Multi input
```bash
# Basic usage
$ parsa path/to/input_folder
# The output will be saved inside a folder named `parsaoutput` in the input folder.
```

### Optional: custom output folder
```bash
# Basic usage
$ parsa path/to/input -o path/to/output_folder
# Works with both single and multi input.
```

### Optional: ignore files without an explicit extension
```bash
# Basic usage
$ parsa --noprompt path/to/input
# Useful for situations where your input includes log/system files without an extension.
```

## Full help message
```
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
```

# Related projects
- [parsa-gui](https://github.com/rdimaio/parsa-gui) - Graphical version of parsa (WIP)
- [xparsa](https://github.com/rdimaio/xparsa) - Extended parsa, enhanced with statistics about the parsed files (WIP)
- [xparsa-gui](https://github.com/rdimaio/xparsa-gui) - GUI for xparsa (WIP)

# Contributing
Pull requests are welcome! If you would like to include/remove/change a major feature, please open an issue first.

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
