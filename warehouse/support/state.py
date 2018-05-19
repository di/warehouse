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

import automat


class TicketStatuses(enum.Enum):

    Opened = "Opened"
    Accepted = "Accepted"
    Rejected = "Rejected"


class TicketStatus:

    _machine = automat.MethodicalMachine()

    def __init__(self, ticket):
        self._ticket = ticket

    # States
    @_machine.state(initial=True, serialized=TicketStatuses.Opened.value)
    def opened(self):
        """
        In this state, the ticket has been opened.
        """

    @_machine.state(serialized=TicketStatuses.Accepted.value)
    def accepted(self):
        """
        In this state, the ticket has been rejected.
        """

    @_machine.state(serialized=TicketStatuses.Rejected.value)
    def rejected(self):
        """
        In this state, the ticket has been rejected.
        """

    # Inputs
    @_machine.input()
    def open(self):
        """
        The ticket has been opened.
        """

    @_machine.input()
    def accept(self):
        """
        The ticket has been accepted.
        """

    @_machine.input()
    def reject(self):
        """
        The ticket has been rejected.
        """

    # Outputs
    @_machine.output()
    def _handle_accept(self):
        self._ticket.accept()

    @_machine.output()
    def _handle_reject(self):
        self._ticket.reject()

    # Transitions
    opened.upon(
        accept,
        enter=accepted,
        outputs=[_handle_accept],
        collector=lambda iterable: list(iterable)[-1],
    )
    opened.upon(
        reject,
        enter=rejected,
        outputs=[_handle_reject],
        collector=lambda iterable: list(iterable)[-1],
    )

    # Serialization / Deserialization
    @_machine.serializer()
    def _save(self, state):
        return state

    @_machine.unserializer()
    def _restore(self, state):
        return state

    def save(self):
        self._ticket.status = TicketStatuses(self._save())
        return self._ticket

    @classmethod
    def load(cls, ticket):
        self = cls(ticket)
        self._restore(ticket.status.value)
        return self
