#!/usr/bin/env python
"""Send email written in Markdown.
"""
from __future__ import print_function

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from io import open

import mdmail
from mdmail.helpers import to_bool

def main(cli_args=None):
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("file", nargs="?",
                        help="Markdown file for email content. " \
                        "Default to STDIN.")
    parser.add_argument("--subject", "-s", help="Subject line")
    parser.add_argument("--from", "-f", dest='from_', help="From address")
    parser.add_argument("--to", "-t", help="To addresses, separated by comma")
    parser.add_argument("--cc", "-c", help="CC addresses, separated by comma")
    parser.add_argument("--bcc", "-b", help="Bcc address, separated by comma")
    parser.add_argument("--reply-to", "-r", help="Reply-to address")
    parser.add_argument("--css", help="Use a custom CSS file")
    parser.add_argument("--print-only", "-p", action='store_true',
                        help="Only print out rendered html")
    if cli_args:
        args = parser.parse_args(cli_args)
    else:
        args = parser.parse_args()

    if args.file:
        content = open(args.file, encoding='utf-8').read()
        image_root = os.path.dirname(args.file)
    else:
        content = sys.stdin.read()
        image_root = os.getcwd()

    if args.css:
        css = open(args.css, encoding='utf-8').read()
    else:
        css = None

    email_content = mdmail.EmailContent(content, css=css, image_root=image_root)

    if not args.from_:
        from_email = email_content.headers.get('from') or \
                     os.environ.get('MDMAIL_DEFAULT_SENDER')
    else:
        from_email = args.from_

    smtp = {
        'host': os.environ.get('MDMAIL_HOST', 'localhost'),
        'port': int(os.environ.get('MDMAIL_PORT', 25)),
        'tls': to_bool(os.environ.get('MDMAIL_USE_TLS')),
        'ssl': to_bool(os.environ.get('MDMAIL_USE_SSL')),
        'user': os.environ.get('MDMAIL_USERNAME',''),
        'password': os.environ.get('MDMAIL_PASSWORD',''),
    }

    if args.print_only:
        print("==========HTML Content===========")
        print(email_content.html + '\n')
        print("==========Plain-text Content===========")
        print(email_content.text + '\n')
    else:
        mdmail.send(email_content, subject=args.subject,
            from_email=from_email, to_email=args.to,
            cc=args.cc, bcc=args.bcc, reply_to=args.reply_to,
            smtp=smtp)

if __name__ == '__main__':
    main()
