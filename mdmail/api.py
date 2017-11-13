import os
import hashlib
from io import open

import emails
import markdown
from bs4 import BeautifulSoup

from mdmail.helpers import sanitize_email_address, is_string

def send(email, subject=None,
         from_email=None, to_email=None,
         cc=None, bcc=None, reply_to=None,
         smtp=None):
    """Send markdown email

    Args:
        email (str/obj): A markdown string or EmailContent object 
        subject (str): subject line
        from_email (str): sender email address
        to_email (str/list): recipient email addresses
        cc (str/list): CC email addresses (string or a list)
        bcc (str/list): BCC email addresses (string or a list)
        reply_to (str): Reply-to email address
        smtp (dict): SMTP configuration (dict)

    Schema of smtp dict:
        host (str): SMTP server host. Default: localhost
        port (int): SMTP server port. Default: 25
        tls (bool): Use TLS. Default: False
        ssl (bool): Use SSL. Default: False
        user (bool): SMTP login user. Default empty
        password (bool): SMTP login password. Default empty
    """
    if is_string(email):
        email = EmailContent(email)

    from_email = sanitize_email_address(from_email or email.headers.get('from'))
    to_email = sanitize_email_address(to_email or email.headers.get('to'))
    cc = sanitize_email_address(cc or email.headers.get('cc'))
    bcc = sanitize_email_address(bcc or email.headers.get('bcc'))
    reply_to = sanitize_email_address(reply_to or email.headers.get('reply-to'))

    message_args = {
        'html': email.html,
        'text': email.text,
        'subject': (subject or email.headers.get('subject', '')),
        'mail_from': from_email,
        'mail_to': to_email
    }
    if cc:
        message_args['cc'] = cc
    if bcc:
        message_args['bcc'] = bcc
    if reply_to:
        message_args['headers'] = {'reply-to': reply_to}

    message = emails.Message(**message_args)

    for filename, data in email.inline_images:
        message.attach(filename=filename, content_disposition='inline', data=data)

    message.send(smtp=smtp)

class EmailContent(object):
    def __init__(self, content, css=None, image_root='.'):
        """ Constructor

        Args:
            content (str): Markdown text
            css (str): Custom CSS style. If not set, use default CSS style.
            image_root (str): Root directory for inline images.
        """
        self._md = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.meta'])
        self._html = None
        self._inline_images = None
        self._convert(content, css, image_root)

    def _replace_inline_images(self, html, image_root):
        soup = BeautifulSoup(html, "lxml")
        imgs = soup.findAll('img')
        inlines = {}
        for img in imgs:
            src = img['src']
            if not src.startswith('http'):
                src_uid = '{}_{}'.format(
                    hashlib.md5(src.encode('utf-8')).hexdigest()[:6],
                    os.path.basename(src))
                if src_uid not in inlines:
                    img_path = os.path.join(image_root, src)
                    inlines[src_uid] = open(img_path, 'rb')
                img['src'] = 'cid:'+src_uid
        self._inline_images = inlines.items()
        return soup

    def _inline_css(self, html, css):
        if not css:
            default_css = os.path.join(os.path.dirname(__file__), 'default.css')
            css = open(default_css, encoding='utf-8').read()
        email_html_template = u"""
        <!doctype html>
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    {css}
                </style>
            </head>
            <body>
                {content}
            </body>
        </html>"""
        return email_html_template.format(css=css, content=html)

    def _convert(self, content, css, image_root):
        raw_html = self._md.convert(content)
        html = self._replace_inline_images(raw_html, image_root)
        html = self._inline_css(html, css)
        self._html = BeautifulSoup(html, "lxml").prettify()

    @property
    def html(self):
        return self._html

    @property
    def text(self):
        return u'\n'.join(self._md.lines)

    @property
    def headers(self):
        return {k.lower(): (v[0] if len(v) == 1 else v) for k,v in self._md.Meta.items()}

    @property
    def inline_images(self):
        return self._inline_images
