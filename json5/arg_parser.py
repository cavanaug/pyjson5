# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from json5.host import Host


class _Bailout(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, host=None, add_help=True):
        super(ArgumentParser, self).__init__(prog='json5', add_help=add_help)

        self._host = host or Host()
        self.exit_status = None

        self.usage = '%(prog)s [options] [file...]'
        self.add_argument('-V', '--version', action='store_true',
                          help='Print the json5 version and exit.')

        self.add_argument('-c', metavar='STR', dest='cmd',
                          help='inline json5 string'),

        self.add_argument('--json', dest='format_json', action='store_const', 
                          const=True, default=False, 
                          help='output as json'),

        self.add_argument('files', nargs='*', default=[],
                          help=argparse.SUPPRESS)

    def parse_args(self, args=None, namespace=None):
        try:
            rargs = super(ArgumentParser, self).parse_args(args=args,
                                                           namespace=namespace)
        except _Bailout:
            return None

        return rargs

    # Redefining built-in 'file' pylint: disable=W0622

    def _print_message(self, msg, file=None):
        self._host.print_(msg=msg, stream=file, end='\n')

    def print_help(self, file=None):
        self._print_message(msg=self.format_help(), file=file)

    def error(self, message, bailout=True):  # pylint: disable=W0221
        self.exit(2, '%s: error: %s\n' % (self.prog, message), bailout=bailout)

    def exit(self, status=0, message=None,  # pylint: disable=W0221
             bailout=True):
        self.exit_status = status
        if message:
            self._print_message(message, file=self._host.stderr)
        if bailout:
            raise _Bailout()
