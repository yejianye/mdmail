# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_requires = [
    'markdown',
    'premailer',
    'emails',
    'beautifulsoup4',
    'lxml',
    'six'
]

setup(
    name='mdmail',
    version='0.1.0',
    description='Send email written in Markdown',
    long_description=readme,
    keywords=['markdown', 'html', 'email', 'inline css'],
    author='Jianye Ye',
    author_email='yejianye@gmail.com',
    url='https://github.com/yejianye/mdmail',
    license=license,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications :: Email :: Filters",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    entry_points={
        'console_scripts': [
            'mdmail = mdmail.cli:main',
            ]
    },
    packages=['mdmail'],
    tests_require=['nose', 'mock'],
    install_requires=install_requires,
)
