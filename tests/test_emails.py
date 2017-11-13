# -*- coding: utf-8 -*-
import os
from io import open

from .context import mdmail

EMAIL_DIR = os.path.join(os.path.dirname(__file__), 'emails')

def validate_email_content(email_file, html=None, text=None):
    email_file = os.path.join(EMAIL_DIR, email_file)
    email_content = open(email_file, encoding='utf-8').read()
    image_root = os.path.dirname(email_file)
    email = mdmail.EmailContent(email_content, image_root=image_root)

    if html:
        html = open(os.path.join(EMAIL_DIR, html), encoding='utf-8').read()
        assert "HTML output mismatch", email.html == html

    if text:
        text = open(os.path.join(EMAIL_DIR, text), encoding='utf-8').read()
        assert "Plain text output mismatch", email.text == text

def test_basic():
    validate_email_content('basic.md', html='basic.html', text='basic.txt')

def test_inline_image():
    validate_email_content('inline_image.md', html='inline_image.html')

def test_unicode():
    validate_email_content('unicode.md', html='unicode.html', text='unicode.txt')
