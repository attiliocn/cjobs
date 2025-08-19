#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from cjobs.tools.arguments import create_argument_parser
import argcomplete
def main():
    parser = create_argument_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()