# SPDX-FileCopyrightText: 2023 Agustin Parmisano
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import dateutil
import re

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot

class AbusechFeodoTrackerParserBot2023(ParserBot):
    """Parse the Abuse.ch Feodo Tracker feed """

    def parse_line(self, line, report):
        line = line.strip()
        if line.startswith('# Last updated:'):
            self._lastupdated = line[16:36]
        elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line):
            event = self.new_event()
            if self._lastupdated:
                event.add('time.source', dateutil.parser.parse(self._lastupdated).isoformat())
            event.add('classification.type', 'malware-distribution')
            event.add('source.ip', line)
            
            yield event

BOT = AbusechFeodoTrackerParserBot2023