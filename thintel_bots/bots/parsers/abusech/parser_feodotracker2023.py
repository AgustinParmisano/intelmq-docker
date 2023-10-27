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

    def parse(self, report):
        raw_report = report.strip()

        if not len(raw_report):  # We depend on first line = date
            return

        first_row = raw_report.splitlines()[0]
        time_match = re.search(r'Last updated: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC)', first_row)
        
        if time_match:
            time_str = time_match.group(1)
            self.last_updated = dateutil.parser.parse(time_str).isoformat()
        else:
            return

        for row in raw_report.splitlines():
            if not row.startswith("#"):
                yield row.strip()

    def parse_line(self, val, report):
        if not val or val.startswith('#'):
            return

        event = self.new_event(report)

        if not event.add('source.ip', val, raise_failure=False):
            event.add('source.network', val)

        event.add('time.source', self.last_updated)
        event.add('classification.type', 'blacklist')
        event.add('raw', val)

        yield event

BOT = AbusechFeodoTrackerParserBot2023