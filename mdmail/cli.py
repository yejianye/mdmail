#!/usr/bin/env python
"""
"""
from __future__ import print_function

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from mdmail.api import send, EmailContent
from mdmail.helpers import to_bool

def main():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("file", nargs='?',
                        help="Markdown file for email content. " \
                        "Default to STDIN.")
    parser.add_argument("--subject", help="Subject line")
    parser.add_argument("--from", help="From address")
    parser.add_argument("--to", help="To address")
    parser.add_argument("--cc", help="CC address")
    parser.add_argument("--bcc", help="Bcc address")
    parser.add_argument("--reply-to", help="Reply-to address")
    args = parser.parse_args()

    if not args.file:
        content = sys.stdin.read()
    elif os.path.exists(args.file):
        content = open(args.file).read()
    else:
        print("No such file: {}".format(args.file))
        sys.exit(1)

    email_content = EmailContent(content)

    smtp = {
        'host': os.environ.get('MDMAIL_HOST', 'localhost'),
        'port': int(os.environ.get('MDMAIL_PORT', 25)),
        'tls': to_bool(os.environ.get('MDMAIL_USE_TLS')),
        'ssl': to_bool(os.environ.get('MDMAIL_USE_SSL')),
        'user': os.environ.get('MDMAIL_USERNAME',''),
        'password': os.environ.get('MDMAIL_PASSWORD',''),
    }

    send(email_content, subject=args.subject,
         from_email=args.from, to_email=args.to,
         cc=args.cc, bcc=args.bcc, reply_to=args.reply_to,
         smtp=smtp)

if __name__ == '__main__':
    main()
