# `gfm-toc.py`

This was intended to be a Python port of Eugene Kalinin’s [`gh-md-toc` shell
script](https://github.com/ekalinin/github-markdown-toc), but I ended up
throwing out all of the original code / architecture, so I’m making a new
repository.

It works basically the same, but has a few more options, including numbered
lists with `-n`! Also, the input file defaults to `README.md`.

# Table of Contents

* [gfm-toc.py](#gfm-tocpy)
* [Usage](#usage)
* [Arguments](#arguments)
* [License](#license)

(I’m obligated to have this here, right?)

# Usage

```
usage: gh-md-toc [-h] [-] [--license] [-n] [-e] [--header HEADER]
                 [--no-header] [--encoding ENCODING]
                 [--header-depth HEADER_DEPTH] [-v]
                 [src_file [src_file ...]]
```

# Arguments

|Argument         |Description
|-----------------|------------
|`-h`, `--help`   |Show help and exit.
|`-`              |Read from STDIN instead of a file.
|`--license`      |Print license information (MIT) and exit.
|`-n`, `--number` |Generate a numbered list instead of bullets.
|`-e`, `--equals` |Notate header with equals signs rather than hashes. Purely cosmetic
|`--header`       |Custom text for the section header.  Default: `Table of Contents`.
|`--no-header`    |Don't generate a table header.
|`--encoding`     |Encoding of all input files. Frankly, there's no excuse to ever use this argument. Default: `utf-8`.
|`--header-depth` |Header depth; number of hashes to output before the header. Default: 1.
|`-v`, `--version`|show program's version number and exit

# License

MIT / Expat, see [`license.txt`](blob/master/license.txt).
