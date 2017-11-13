Mdmail: Send emails written in Markdown
=======================================

Mdmail sends emails written in Markdown. It could be used as a standalone command-line script or as a python module. The features includes

- Have a sane default CSS style and support CSS customization
- Support local images as inline images

To install mdmail

```bash
$ pip install mdmail
```

Send Email in Command-line
--------------------------

When sending emails from command-line, the body of the email could be read from a file or stdin.

Email headers such as subject, from/to, cc etc could be specified at the beginning of the markdown file, Or be specified in command-line arguments.

Here is an example of Markdown file with email headers

```
Subject: Sample Email
From: foo@xyz.com
To: bar@xyz.com
Cc: baz@xyz.com

# Sample Email

-

![Embed local image](../assets/image.jpg)
```

To send this email with mdmail

```bash
$ mdmail sample_email.md
```

Here is an example of specifying subject, from/to in command-line

```bash
$ mdmail --from=foo@xyz.com --to=bar@xyz.com --subject='Sample' sample_email.md
```

To read email content from stdin, 

```bash
$ echo '# Sample Email' | mdmail --from=foo@xyz.com --to=bar@xyz.com --subject='Sample'
```

SMTP server configurations are read from the following environment variables

```bash
export MDMAIL_HOST="" # default: localhost
export MDMAIL_PORT="" # default: 25
export MDMAIL_USE_TLS="" # default: false
export MDMAIL_USE_SSL="" # default: false
export MDMAIL_USERNAME="" # default: None
export MDMAIL_PASSWORD="" # default: None
export MDMAIL_DEFAULT_SENDER="" # default: None
```

Send Email in Python Code
--------------------------

Sending emails in python is straight-forward.

```python
import mdmail

email="""
# Sample Email

- Python is awesome
- Markdown is cool

![Embed local image](../assets/image.jpg)
"""

mdmail.send(email, subject='Sample Email',
            from_email='foo@example.com', to_email='bar@example.com')
```
            
By default, it will use SMTP server on localhost. You could specify a SMTP server as well.

```
# Specify SMTP server
smtp = {
  'host: 'my-mailserver.com',
  'port': 25,
  'tls': False,
  'ssl': False,
  'user: '',
  'password': '',
}

mdmail.send(content, subject='Sample Email',
            from_email='foo@example.com', to_email='bar@example.com',
            smtp=smtp)
```
