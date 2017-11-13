#!/usr/bin/env python
"""
A tool to generate html and txt file for a markdown file.

This is mainly used to generate test cases.
"""

import argparse
import os
from io import open

import mdmail

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("file", help="Markdown file for email content")
    args = parser.parse_args()
    content = open(args.file, encoding='utf-8').read()
    email = mdmail.EmailContent(content)
    base_fname = args.file.rsplit('.', 1)[0]
    html_fname = base_fname + '.html'
    with open(html_fname, 'w', encoding='utf-8') as f:
        f.write(email.html)

    text_fname = base_fname + '.txt'
    with open(text_fname, 'w', encoding='utf-8') as f:
        f.write(email.text)

if __name__ == '__main__':
    main()
