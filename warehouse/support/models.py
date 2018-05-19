# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum

from sqlalchemy import sql, orm
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.mutable import MutableDict

from warehouse import db
from warehouse.packaging.models import Project
from warehouse.support.models import TicketStatuses


class Ticket(db.Model):

    __tablename__ = "support_tickets"

    created = Column(DateTime, nullable=False, server_default=sql.func.now())
    status = Column(
        Enum(TicketStatuses, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        server_default=TicketStatuses.Opened.value,
    )

    events = orm.relationship(
        "Event",
        backref="ticket",
        cascade="all, delete-orphan",
        lazy=False,
        order_by=lambda: Event.created,
    )

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'employee',
    }


class ProjectTicket(Ticket):

    project = orm.relationship(Project)


class FlagTicket(ProjectTicket):

    reason = Column(Text)
    details = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'project_flag'
    }

    def accept(self):
        print("accept flagticket")  # TODO

    def reject(self):
        print("reject flagticket")  # TODO


class UploadLimitTicket(ProjectTicket):

    requested_limit = Column(Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'upload_limit'
    }

    def accept(self):
        print("accept uploadlimitticket")  # TODO

    def reject(self):
        print("reject uploadlimitticket")  # TODO


class EventTypes(enum.Enum):

    Open = "Open"
    Accept = "Accept"
    Reject = "Reject"


class Event(db.Model):

    __tablename__ = "support_events"

    created = Column(DateTime, nullable=False, server_default=sql.func.now())

    ticket_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "support_tickets.id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
    )

    event_id = Column(Text, nullable=False, unique=True, index=True)
    event_type = Column(
        Enum(EventTypes, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )

    data = Column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        server_default=sql.text("'{}'"),
    )
