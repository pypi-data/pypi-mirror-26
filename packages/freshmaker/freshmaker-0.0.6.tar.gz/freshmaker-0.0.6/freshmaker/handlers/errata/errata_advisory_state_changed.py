# -*- coding: utf-8 -*-
# Copyright (c) 2017  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from freshmaker import db, conf, log
from freshmaker.events import (
    ErrataAdvisoryStateChangedEvent, ErrataAdvisoryRPMsSignedEvent)
from freshmaker.models import Event, EVENT_TYPES
from freshmaker.handlers import BaseHandler
from freshmaker.errata import Errata


class ErrataAdvisoryStateChangedHandler(BaseHandler):
    """Mark Errata advisory as released

    When an advisory state is changed to SHIPPED_LIVE, mark it as released in
    associated event object of ``ErrataAdvisoryStateChangedHandler``.

    This is used to avoiding generating YUM repository to include RPMs
    inlcuded in a SHIPPED_LIVE advisory, because at that state, RPMs will be
    available in official YUM repositories.
    """

    name = 'ErrataAdvisoryStateChangedHandler'

    def can_handle(self, event):
        return isinstance(event, ErrataAdvisoryStateChangedEvent)

    def mark_as_released(self, errata_id):
        """
        Marks the Errata advisory with `errata_id` ID as "released", so it
        is not included in further container images rebuilds.
        """
        # check db to see whether this advisory exists in db
        db_event = db.session.query(Event).filter_by(
            event_type_id=EVENT_TYPES[ErrataAdvisoryRPMsSignedEvent],
            search_key=str(errata_id)).first()
        if not db_event:
            log.debug("Ignoring Errata advisory %d - it does not exist in "
                      "Freshmaker db.", errata_id)
            return []

        db_event.released = True
        db.session.commit()
        log.info("Errata advisory %d is now marked as released", errata_id)

    def rebuild_if_not_exists(self, event, errata_id):
        """
        Initiates rebuild of artifacts based on Errata advisory with
        `errata_id` id.

        :rtype: List of ErrataAdvisoryRPMsSignedEvent instances.
        :return: List of extra events generated to initiate the rebuild.
        """

        db_event = db.session.query(Event).filter_by(
            event_type_id=EVENT_TYPES[ErrataAdvisoryRPMsSignedEvent],
            search_key=str(errata_id)).first()
        if db_event:
            log.debug("Ignoring Errata advisory %d - it already exists in "
                      "Freshmaker db.", errata_id)
            return []

        # Get additional info from Errata to fill in the needed data.
        errata = Errata(conf.errata_tool_server_url)
        advisories = errata.advisories_from_event(event)
        if not advisories:
            log.error("Unknown Errata advisory %d" % errata_id)
            return []

        log.info("Generating ErrataAdvisoryRPMsSignedEvent for Errata "
                 "advisory %d, because its state changed to %s.", errata_id,
                 event.state)
        advisory = advisories[0]
        db_event = ErrataAdvisoryRPMsSignedEvent(
            event.msg_id + "." + str(advisory.name), advisory.name,
            advisory.errata_id, advisory.security_impact)
        return [db_event]

    def handle(self, event):
        errata_id = event.errata_id
        state = event.state

        extra_events = []

        if state in ["REL_PREP", "PUSH_READY", "IN_PUSH", "SHIPPED_LIVE"]:
            extra_events += self.rebuild_if_not_exists(event, errata_id)

        if state == "SHIPPED_LIVE":
            self.mark_as_released(errata_id)

        return extra_events
