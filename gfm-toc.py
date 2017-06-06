import urllib.request
import re
import argparse
from html.parser import HTMLParser
import sys
import codecs

version = '1.1.0'

useragent = f'gh-md-toc v{version}'

def mdtohtml(md, encoding='utf-8'):
    """ Get HTML from GitHub, return it """
    response = urllib.request.urlopen(
        urllib.request.Request('https://api.github.com/markdown/raw',
        data=bytes(md, encoding=encoding),
        headers={'User-Agent': useragent, 'Content-Type': 'text/plain'}))
    return response.read().decode('utf-8')

# arguments

argparser = argparse.ArgumentParser(
    description='Render a TOC for GFM from a .md file',
    epilog='More info: github.com/9999years/github-markdown-toc',
    prog='gh-md-toc'
)

argparser.add_argument('src_file', nargs='*', default=['README.md'],
    help='The filename of a Markdown file to extract the TOC from.')

argparser.add_argument('-', action='store_true', dest='use_stdin',
    help='Read from STDIN instead of a file.')

argparser.add_argument('--license', action='store_true',
    help='Print license information (MIT) and exit.')

argparser.add_argument('-n', '--number', action='store_true',
    help='Generate a numbered list instead of a bulleted list.')

argparser.add_argument('-e', '--equals', action='store_true',
    help='Use equals signs (=) on the next line instead of hashes (#) in the '
    'header text. Purely cosmetic, does not effect rendered HTML.')

argparser.add_argument('--header', type=str, default='Table of Contents',
    help='Custom text for the section header. Default: `Table of Contents`.')

argparser.add_argument('--no-header', action='store_true',
    help='''Don't generate a table header.''')

argparser.add_argument('--encoding', type=str, default='utf-8',
    help='Encoding of all input files. Frankly, there\'s no excuse to ever use '
    'this argument')

argparser.add_argument('--header-depth', type=int, default=1,
    help='''Header depth; number of hashes to output before the header.''')

argparser.add_argument('-v', '--version', action='version',
    version=f'%(prog)s {version}')

args = argparser.parse_args()

if args.license:
    print('''Copyright (c) 2017 Rebecca Turner

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''')
    exit()

class headerExtracter(HTMLParser):
    # stolen from github.com/python/cpython/blob/3.6/Lib/html/parser.py
    def __init__(self, *, convert_charrefs=True):
        """Initialize and reset this instance.
        If convert_charrefs is True (the default), all character references
        are automatically converted to the corresponding Unicode characters.
        """
        self.convert_charrefs = convert_charrefs
        self.inheader = False
        self.currenthead = ''
        self.lasthref = ''
        self.parsed_data = []
        self.reset()

    def handle_tag(self, tag):
        if tag[0] == 'h' and len(tag) > 1:
            if (# messy but easier / faster than regular expressions
                tag[1] == '1' or
                tag[1] == '2' or
                tag[1] == '3' or
                tag[1] == '4' or
                tag[1] == '5' or
                tag[1] == '6'):
                if self.inheader is False:
                    # reset currenthead, in header now
                    self.currenthead = ''
                    self.inheader = True
                else:
                    # if this isn't the first header start tag we see, append a
                    # tuple to the parsed data list (text, href, depth)
                    if len(self.currenthead) != 0:
                        self.parsed_data.append(
                            (self.currenthead.replace('\n', ''),
                            self.lasthref,
                            int(tag[1])))
                    # switch inheader off
                    self.inheader = False
                return True
        else:
            if tag == 'code':
                self.currenthead += '`'
            elif tag == 'i':
                self.currenthead += '*'
            elif tag == 'b':
                self.currenthead += '**'
            # not a header tag
            return False

    def handle_starttag(self, tag, attrs):
        # if we’re in a header, we need the href
        if not self.handle_tag(tag):
            if tag == 'a' and self.inheader:
                for attr in attrs:
                    if attr[0] == 'href':
                        self.lasthref = attr[1]

    def handle_endtag(self, tag):
        self.handle_tag(tag)

    def handle_data(self, data):
        # cat data if in a header
        if self.inheader:
            self.currenthead += data

def treetomd(tree, numbering='bullet', sep='.'):
    ret = ''
    if numbering is 'bullet':
        get_number = lambda depth: '*'
    else: # numbering
        # array of numbers, one per 'depth', for persistent numbering
        # list        | value of `number`
        # ------------|-------------------
        # 1.          | [1]
        #   1.1       | [1, 1]
        #       1.1.1 | [1, 1, 1]
        #   1.2       | [1, 2]
        #       1.2.1 | [1, 2, 1]
        #       1.2.2 | [1, 2, 2]
        #       1.2.3 | [1, 2, 3]
        # 2.          | [2]
        #   2.1       | [2, 1]
        # we append() and pop() the array as needed (if the lastdepth changes
        # from the current depth)
        number = [0]
        lastdepth = 1
        get_number = lambda depth: f'{number[depth - 1]}{sep}'

    for header in tree:
        (text, href, depth) = header
        if numbering is not 'bullet':
            # if numbering, push for a new depth, pop for losing a depth,
            # and increment for the same depth
            if depth > lastdepth:
                number.append(1)
            elif depth < lastdepth:
                number.pop()
            else:
                number[depth - 1] += 1
        # output current header with indent and link
        ret += (' ' * (4 * int(depth) - 4)
            + get_number(depth)
            + f' [{text}]({href})\n')
        lastdepth = depth
    return ret

# create parser
parser = headerExtracter()

if not args.no_header:
    # use
    #    header
    #    ======
    # syntax if requested & possible,
    # but default to hash syntax if not
    if args.equals and args.header_depth <= 2:
        print(args.header + '\n'
            + (('=' if args.header_depth is 1 else '-')
            * len(args.header)))
    else:
        print(args.header_depth * '#' + ' ' + args.header)
    print('')

numbering = 'number' if args.number else 'bullet'

if args.use_stdin:
    # catenate stdinput, parse / render
    md = ''
    for line in sys.stdin:
        md += line + '\n'
    parser.feed(mdtohtml(md))
    print(treetomd(parser.parsed_data, numbering=numbering))

# process each file, respecting encoding, although i really hope nobody ever
# uses that argument and to be quite frank i haven't tested it
for fname in args.src_file:
    with open(fname, 'r', encoding=args.encoding) as f:
        parser.feed(mdtohtml(f.read(), encoding=args.encoding))
        tree = parser.parsed_data
        print(treetomd(tree, numbering=numbering))

parser.close()
