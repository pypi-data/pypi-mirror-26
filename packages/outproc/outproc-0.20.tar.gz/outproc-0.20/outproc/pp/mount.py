# -*- coding: utf-8 -*-
#
# Output processor for `mount`
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
#

# Project specific imports
from ..processing import Processor as ProcessorBase
from ..term import fg2bg, get_width, is_real_term

# Standard imports
import os
import sys

# TODO Add more?
KNOWN_NETWORK_FILESYSTEMS = ['nfs']


class Processor(ProcessorBase):

    @staticmethod
    def want_to_handle_current_command():
        '''Post-process output from `mount` only if executed w/o args
            and STDOUT is not already captured
        '''
        return sys.stdout.isatty() \
          and len(sys.argv) == 1 \
          and os.path.basename(sys.argv[0]) == 'mount'


    def __init__(self, config, binary):
        super().__init__(config, binary)
        self.mount_point_max_size = config.get_int('mountpoint-max-size', 0)
        self.trim_char = config.get_string('trim-char', '...')
        self.kernel_fs = config.get_color('kernel-fs', 'grey+bold')
        self.real_fs = config.get_color('real-fs', 'normal')
        self.net_fs = config.get_color('net-fs', 'blue+bold')
        self.rebind_fs = config.get_color('rebind-fs', 'magenta')
        self.odd_bg = config.get_color('odd-bg', 'normal', with_reset=False)
        if self.odd_bg == config.color.normal:
            self.odd_bg = ''
        else:
            self.odd_bg = fg2bg(self.odd_bg)
        self.even_bg = config.get_color('even-bg', 'normal', with_reset=False)
        if self.even_bg == config.color.normal:
            self.even_bg = ''
        else:
            self.even_bg = fg2bg(self.even_bg)

        self.max_fields = (0, 0, 0)
        self.records = []
        self.reminder = None


    def _update_max_lengths(self, current, record):
        assert len(record) == 4 and len(current) == 3
        return (
            max(current[0], len(record[0]))
          , max(current[1], len(record[1]))
          , max(current[2], len(record[2]))
          )


    def handle_block(self, block):
        if self.reminder is not None:
            block = self.reminder + block

        for line in block.splitlines():
            if block.endswith(line):
                self.reminder = line
                break

            columns = line.decode('utf-8').split(' ')
            # TODO ATTENTION Other locales will cause assertion fail
            assert columns[1] == 'on' and columns[3] == 'type'
            # TODO Unit tests for this piece of crap!
            if 0 < self.mount_point_max_size and self.mount_point_max_size < len(columns[2]):
                size = 0
                for i, p in enumerate(columns[2].split('/')[::-1]):
                    if self.mount_point_max_size < (size + len(p) + 1):
                        break
                    size += len(p) + 1
                truncate_point = len(columns[2]) - size
                columns[2] = self.trim_char + columns[2][truncate_point:]
            record = (columns[0], columns[2], columns[4], str(columns[5])[1:len(columns[5])-1])
            self.max_fields = self._update_max_lengths(self.max_fields, record)
            self.records.append(record)
        # NOTE Do not return anything... wait for all blocks (lines)...


    def eof(self):
        # Form a format line
        fmt = ('{{:<{}}} ' * len(self.max_fields)).format(*self.max_fields)

        # Format the output
        term_width = get_width()
        lines = []
        last_field_start_column = sum(self.max_fields) + 3  # 3 == spaces between columns
        for row, r in enumerate(self.records):
            # Colorize
            if r[0].startswith('/'):
                color = self.real_fs
            elif r[2] in KNOWN_NETWORK_FILESYSTEMS:
                color = self.net_fs
            else:
                color = self.kernel_fs
            bg_color = self.odd_bg if row % 2 else self.even_bg
            # Format leading 3 columns
            line = fmt.format(r[0], r[1], r[2])
            options = r[3].split(',')
            last = len(options) - 1
            for i, opt in enumerate(options):
                if opt == 'bind':
                    color = self.rebind_fs
                if (len(line) + 1 + len(opt)) < term_width:
                    line += opt + (',' if i != last else '')
                else:
                    # Overflow
                    if is_real_term():
                        line += ' ' * (term_width - len(line))
                    lines.append(color + bg_color + line + self.config.color.reset)
                    line = ' ' * last_field_start_column + opt + (',' if i != last else '')
            if is_real_term():
                line += ' ' * (term_width - len(line))
            lines.append(color + bg_color + line + self.config.color.reset)
        return lines
