# -*- coding: utf-8 -*-
import os
from io import open

from mock import patch

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

    return email

def test_basic():
    validate_email_content('basic.md', html='basic.html', text='basic.txt')

def test_unicode():
    validate_email_content('unicode.md', html='unicode.html', text='unicode.txt')

@patch('emails.Message')
def test_email_with_headers(message_mock):
    email = validate_email_content('email_headers.md',
                           html='email_headers.html', text='email_headers.txt')
    mdmail.send(email)
    message_args = message_mock.call_args[1]
    assert message_args['subject'] == 'Email Header Test'
    assert message_args['mail_from'] == 'from@test.com'
    assert message_args['mail_to'] == 'to@test.com'
    assert message_args['cc'] == ['cc1@test.com', 'cc2@test.com']
    assert message_args['bcc'] == 'bcc@test.com'
    assert message_args['headers'] == {'reply-to': 'reply-to@test.com'}
