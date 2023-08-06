#!/usr/bin/env python3
# © 2016 James R. Barlow: github.com/jbarlow83

"""Wrappers to manage subprocess calls"""

import os


def get_program(name):
    "Check environment variables for overrides to this program"
    envvar = 'OCRMYPDF_' + name.upper()
    return os.environ.get(envvar, name)
