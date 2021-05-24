# Copyright (c) 2021 Works Applications Co., Ltd.
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

import argparse
import fileinput
import logging
import os
import sys
import time

from . import Chikkar
from .dictionarylib import Dictionary
from .dictionarylib.dictionarybuilder import DictionaryBuilder
from .dictionarylib.dictionaryheader import DictionaryHeader
from .dictionarylib.dictionaryversion import SYSTEM_DICT_VERSION_1


def _set_default_subparser(self, name, args=None):
    """Set a default subparser

    copy and modify code from https://bitbucket.org/ruamel/std.argparse
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)


argparse.ArgumentParser.set_default_subparser = _set_default_subparser


def print_version():
    from . import __version__
    print('chikkarpy {}'.format(__version__))


def search_synonyms(enable_verb, dictionaries, input_, stdout_logger):
    for word in input_:
        word = word.rstrip('\n')
        chikkar = Chikkar()
        if enable_verb:
            chikkar.enable_verb()
        for dictionary in dictionaries:
            dic = Dictionary(filename=dictionary)
            chikkar.add_dictionary(dic)
        stdout_logger.info("{}\t{}".format(word, ','.join(chikkar.find(word))))


def _command_search(args, print_usage):
    if args.version:
        print_version()
        return

    stdout_logger = logging.getLogger(__name__)

    output = open(args.fpath_out, "w", encoding="utf-8") if args.fpath_out else sys.stdout

    handler = logging.StreamHandler(output)
    handler.setLevel(logging.DEBUG)
    stdout_logger.addHandler(handler)
    stdout_logger.setLevel(logging.DEBUG)
    stdout_logger.propagate = False

    try:
        input_ = fileinput.input(args.in_files, openhook=fileinput.hook_encoded("utf-8"))
        search_synonyms(args.enable_verb, args.dictionaries, input_, stdout_logger)
    finally:
        if args.fpath_out:
            output.close()


def _input_files_checker(args, print_usage):
    for file in args.in_files:
        if not os.path.exists(file):
            print_usage()
            print('{}: error: {} doesn\'t exist'.format(__name__, file), file=sys.stderr)
            exit(1)


def build_dictionary(input_file, output_file, description):
    header = DictionaryHeader(SYSTEM_DICT_VERSION_1, int(time.time()), description)
    with open(output_file, 'wb') as wf:
        wf.write(header.to_byte())

        builder = DictionaryBuilder()
        builder.build(input_file, wf)


def _command_build(args, print_usage):
    build_dictionary(args.input_file, args.out_file, args.description)


def main():
    parser = argparse.ArgumentParser(description="Japanese Morphological Analyzer")

    subparsers = parser.add_subparsers(description='')

    # root, search synonyms
    parser_ss = subparsers.add_parser('search', help='(default) see `search -h`', description='Search synonyms')
    parser_ss.add_argument('-d', dest='dictionaries', metavar='file', nargs=argparse.ZERO_OR_MORE, default=[None],
                           help='synonym dictionary (default: system synonym dictionary)')
    parser_ss.add_argument('-ev', dest='enable_verb', action='store_true', default=False,
                           help='Enable verb and adjective synonyms.')
    parser_ss.add_argument('-o', dest='fpath_out', metavar='file', help='the output file')
    parser_ss.add_argument('in_files', metavar='file', nargs=argparse.ZERO_OR_MORE, help='text written in utf-8')
    parser_ss.add_argument('-v', '--version', action='store_true', dest='version', help='print chikkarpy version')
    parser_ss.set_defaults(handler=_command_search, print_usage=parser_ss.print_usage)

    # build dictionary parser
    parser_bd = subparsers.add_parser('build', help='see `build -h`', description='Build Synonym Dictionary')
    parser_bd.add_argument('-i', dest='input_file', metavar='file', required=True,
                           help='dictionary file (csv)')
    parser_bd.add_argument('-o', dest='out_file', metavar='file', default='synonym.dic', required=False,
                           help='output file (default: synonym.dic)')
    parser_bd.add_argument('-d', dest='description', metavar='string', default='', required=False,
                           help='description comment to be embedded on dictionary')

    parser_bd.set_defaults(handler=_command_build, print_usage=parser_bd.print_usage)

    parser.set_default_subparser('search')

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(args, args.print_usage)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
