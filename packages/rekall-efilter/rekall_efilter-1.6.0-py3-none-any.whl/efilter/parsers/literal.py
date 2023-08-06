# EFILTER Forensic Query Language
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
EFILTER special syntaxes.

Syntaxs in this module don't really implement a language - they're special
cases for just passing through literals and stuff.
"""

__author__ = "Adam Sindelar <adamsh@google.com>"

from efilter import ast
from efilter import syntax


class LiteralSyntax(syntax.Syntax):
    """This is basically and identity function for literals."""

    @property
    def root(self):
        return ast.Literal(self.original)


syntax.Syntax.register_parser(LiteralSyntax, shorthand="literal")


class PassthroughSyntax(syntax.Syntax):
    """This is basically and identity function for expressions."""

    @property
    def root(self):
        return self.original


syntax.Syntax.register_parser(LiteralSyntax, shorthand="expression")
