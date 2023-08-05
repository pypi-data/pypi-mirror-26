#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Pluggable Output Processor (main module)
#
# Copyright (c) 2013-2017 Alex Turbov <i.zaufi@gmail.com>
#
# Pluggable Output Processor is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pluggable Output Processor is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


# Project specific imports
import outproc.pp
from outproc.config import Config
from outproc.logger import log
from outproc.processing import Processor, report_error_with_backtrace, SYSCONFDIR

# Standard imports
import argparse
import exitstatus
import fcntl
import os
import pathlib
import pkgutil
import select
import subprocess
import sys
import traceback


class Application:

    def __init__(self):
        self.executable_name = pathlib.Path(sys.argv[0])
        self.real_executable_name = self.executable_name.resolve()
        self.basename = self.executable_name.name
        self.pipe_mode = False


    def _handle_command_line(self):
        parser = argparse.ArgumentParser(description='Pluggable Output Processor')
        parser.add_argument(
            '-l'
          , '--list-modules'
          , action='store_true'
          , help='List available modules'
          )
        parser.add_argument(
            '-m'
          , '--module'
          , metavar='NAME'
          , help='Choose module to process input from STDIN'
          )
        args = parser.parse_args()

        self.list_modules = args.list_modules

        # Override module name if running as `outproc`. I.e. in a command like this:
        #  $ /usr/bin/make 2>&1 | outproc -m make
        if args.module:
            self.basename = args.module
            self.pipe_mode = True


    def _find_wrapped_binary(self):
        # Try to find a wrapped executable
        self.binary = None
        for path in map(lambda p: pathlib.Path(p), os.environ['PATH'].split(os.pathsep)):
            binary = path / self.basename
            # If given binary exists and is not the same executable as the current one
            if binary.exists() and binary.resolve() != self.real_executable_name:
                self.binary = binary
                break

        if self.binary is None:
            raise RuntimeError('Command not found: {}'.format(self.basename))


    def _list_pp_modules(self):
        modules = [name for importer, name, ispkg in pkgutil.iter_modules(outproc.pp.__path__) if ispkg == False]

        print('List of available modules:')
        for m in modules:
            print('  {}'.format(m))


    def _load_pp_module(self):
        # Look for a plugin to post-process an output of the given command
        try:
            self.pp_mod = __import__(
                'outproc.pp.{}'.format(self.basename)
              , globals()
              , locals()
              , ['outproc.pp']
              )
        except:
            raise RuntimeError('Failed to import module {}'.format(self.basename))

        # Make sure the module found has a Processor class
        if not hasattr(self.pp_mod, 'Processor') or not issubclass(self.pp_mod.Processor, Processor):
            raise RuntimeError('Module {} does not provide class `Processor`'.format(self.pp_mod.__name__))


    def _load_config(self, config_file_name):
        # Try user config file first
        config_file_name_full = None
        if 'HOME' in os.environ:
            config_file_name_full = pathlib.Path.home() / '.outproc' / config_file_name
            # If no user config, then will try a system-wide
            if not config_file_name_full.exists():
                config_file_name_full = None

        # Set full config file name to the system-wide if still not inilialized
        if config_file_name_full is None:
            config_file_name_full = pathlib.Path(SYSCONFDIR) / config_file_name

        # Try to load configuration for selected plugin
        try:
            return Config(config_file_name_full)
        except:
            raise RuntimeError('Unable to load configuration data')


    def _create_output_processor(self, config):
        try:
            # Make an instance of an output processor
            return self.pp_mod.Processor(config, str(self.binary))
        except:
            raise RuntimeError('Unable to make a preprocessor instance')


    def _make_async(self, fd):
        '''Switch given file descriptor to asynchronous mode'''
        fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)


    def _start_wrapped_binary(self):
        try:
            # Execute wrapped (and found) binary
            return subprocess.Popen(
                [str(self.binary)] + sys.argv[1:]
              , bufsize=1                                   # Per line buffering
              , stdin=sys.stdin                             # TODO Need to pass input to subprocess as well
              , stdout=subprocess.PIPE
              , stderr=subprocess.STDOUT                    # NOTE Redirect STDERR to STDOUT
              , shell=False                                 # No shell needed
              )
        except:
            raise RuntimeError('Unable to start wrapped executable ({})'.format(self.binary))


    def _out_lines_list(self, lines):
        if lines:
            sys.stdout.write('\n'.join(lines) + '\n')
            sys.stdout.flush()


    def run(self):
        # Check the binary name
        if self.executable_name == self.real_executable_name:
            self._handle_command_line()
            if self.list_modules:
                self._list_pp_modules()
                return exitstatus.ExitStatus.success
            elif self.pipe_mode:
                # TODO
                log.eerror('Pipe mode not implemented')
                return exitstatus.ExitStatus.failure

        self._find_wrapped_binary()
        self._load_pp_module()
        if not self.pp_mod.Processor.want_to_handle_current_command():
            # Ok, replace self w/ wrapped executable
            os.execv(str(self.binary), [str(self.binary)] + sys.argv[1:])
            return exitstatus.ExitStatus.failure

        config = self._load_config(self.pp_mod.Processor.config_file_name(self.basename))
        processor = self._create_output_processor(config)
        process = self._start_wrapped_binary()

        po = select.epoll()                                 # Make a poll object
        self._make_async(process.stdout)                    # Switch STDOUT descriptor to asynchronous mode
        # Register descriptor for polling
        po.register(process.stdout, select.EPOLLIN | select.EPOLLHUP)

        eof = False
        while not eof:
            # Wait for data to become available
            events = None
            while events is None:
                try:
                    events = po.poll()
                    break
                except InterruptedError:                    # Handle EAGAIN:
                    continue                                # just try to poll() once again ;)

            # Analyze event
            for fileno, event in events:
                # Check if input available
                if event & select.EPOLLIN:
                    block = process.stdout.read()           # Read collected data
                    while block is not None and block:
                        self._out_lines_list(processor.handle_block(block))
                        block = process.stdout.read()       # Try to read more data
                elif event & select.EPOLLHUP:
                    eof = True
                    self._out_lines_list(processor.eof())   # Notify processor about EOF
                else:
                    assert False, 'Unexpected event {}'.format(event)

        result = None
        while result is None:
            result = process.poll()                         # Try to get child exit status

        return result


def main():
    try:
        a = Application()
        return a.run()

    except KeyboardInterrupt:
        return exitstatus.ExitStatus.failure

    except RuntimeError as ex:
        report_error_with_backtrace('Error: {}'.format(ex))
        return exitstatus.ExitStatus.failure

    return exitstatus.ExitStatus.success
