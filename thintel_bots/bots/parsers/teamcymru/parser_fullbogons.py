# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
""" Single IntelMQ parser for TeamCymru FullBogons feeds """

import dateutil.parser

from intelmq.lib.bot import ParserBot


class TeamCymruFullBogonsParserBot(ParserBot):
    """Parse the TeamCymru FullBogons"""
    """ TeamCymru FullBogons Parser Bot """

    _lastgenerated = None

    def parse_line(self, line, report):

        if line.startswith(';') or len(line) == 0:
            self.tempdata.append(line)
            if 'Last-Modified:' in line:
                self._lastgenerated = line.strip('; ')[15:]
                self._lastgenerated = dateutil.parser.parse(self._lastgenerated).isoformat()

        else:
            event = self.new_event(report)
            if self._lastgenerated:
                event.add('time.source', self._lastgenerated)
            event.add('classification.type', 'bogons')
            event.add('raw', line)
            
            yield event


BOT = TeamCymruFullBogonsParserBot
