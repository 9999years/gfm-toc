# `gfm-toc.py`

This was intended to be a Python port of Eugene Kalinin’s [`gh-md-toc` shell
script](https://github.com/ekalinin/github-markdown-toc), but I ended up
throwing out all of the original code / architecture, so I’m making a new
repository.

It works basically the same, but has a few more options, including numbered
lists with `-n`! Also, the input file defaults to `README.md`.

# Table of Contents

1. [`gfm-toc.py`](#gfm-tocpy)
2. [Table of Contents](#table-of-contents)
3. [Arguments and Usage](#arguments-and-usage)
    1. [Usage](#usage)
    2. [Arguments](#arguments)
        1. [Quick reference table](#quick-reference-table)
        2. [`-h`, `--help`](#-h---help)
        3. [`-`](#-)
        4. [`--license`](#--license)
        5. [`-n`, `--number`](#-n---number)
        6. [`-e`, `--equals`](#-e---equals)
        7. [`--header` (Default: 'Table of Contents')](#--header-default-table-of-contents)
        8. [`--no-header`](#--no-header)
        9. [`--encoding` (Default: 'utf-8')](#--encoding-default-utf-8)
        10. [`--header-depth` (Default: 1)](#--header-depth-default-1)
        11. [`-v`, `--version`](#-v---version)
3. [License](#license)

(I’m obligated to have this here, right?)

# Arguments and Usage

## Usage

```
usage: gh-md-toc [-h] [-] [--license] [-n] [-e] [--header HEADER]
                 [--no-header] [--encoding ENCODING]
                 [--header-depth HEADER_DEPTH] [-v]
                 [src_file [src_file ...]]
```

## Arguments

### Quick reference table

|Short|Long          |Description
|-----|--------------|--------------------------------------
|-h   |--help        |show this help message and exit
|-    |              |Read from STDIN instead of a file
|     |--license     |Print license information and exit
|-n   |--number      |Generate a numbered list instead of a bulleted one
|-e   |--equals      |Use equals signs (=) on the next line instead of hashes (#) for level one and two headers
|     |--header      |Custom text for the section header. Default: `Table of Contents`
|     |--no-header   |Don't generate a table header
|     |--encoding    |Encoding of all input files. Default: `utf-8`
|     |--header-depth|Header depth; number of hashes to output before the top. Default: `1`
|-v   |--version     |show program's version number and exit

### `-h`, `--help`

show this help message and exit

### `-`

Read from STDIN instead of a file.

### `--license`

Print license information (MIT) and exit.

### `-n`, `--number`

Generate a numbered list instead of a bulleted list.

### `-e`, `--equals`

Use equals signs (=) on the next line instead of hashes (#) in the header text.
Purely cosmetic, does not effect rendered HTML.

### `--header` (Default: 'Table of Contents')

Custom text for the section header. Default: `Table of Contents`.

### `--no-header`

Don't generate a table header.

### `--encoding` (Default: 'utf-8')

Encoding of all input files. Frankly, there's no excuse to ever use this
argument

### `--header-depth` (Default: 1)

Header depth; number of hashes to output before the header.

### `-v`, `--version`

show program's version number and exit

# License

MIT / Expat, see [`license.txt`](blob/master/license.txt).
