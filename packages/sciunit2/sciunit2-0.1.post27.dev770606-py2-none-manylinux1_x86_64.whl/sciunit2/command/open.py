from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError
import sciunit2.workspace

from getopt import getopt


class OpenCommand(AbstractCommand):
    name = 'open'

    @property
    def usage(self):
        return [('open <name>|<token#>|<path-to-sciunit.zip>',
                 'Open a sciunit by its <name>, through a token obtained '
                 "from 'sciunit copy', or from a ZIP file"),
                ('open -m <name>',
                 'Reopen the sciunit after renaming it to <name>')]

    def run(self, args):
        optlist, args = getopt(args, 'm:')
        if optlist:
            if args:
                raise CommandLineError
            _, v = optlist[0]
            sciunit2.workspace.rename(v)
        elif len(args) == 1:
            v = args[0]
        else:
            raise CommandLineError
        sciunit2.workspace.open(v)
