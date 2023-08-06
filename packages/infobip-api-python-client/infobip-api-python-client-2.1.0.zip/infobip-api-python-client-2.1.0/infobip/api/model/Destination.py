# -*- coding: utf-8 -*-
"""This is a generated class and is not intended for modification!
"""


from datetime import datetime
from infobip.util.models import DefaultObject, serializable
class Destination(DefaultObject):
    @property
    @serializable(name="messageId", type=unicode)
    def message_id(self):
        return self.get_field_value("message_id")

    @message_id.setter
    def message_id(self, message_id):
        self.set_field_value("message_id", message_id)

    def set_message_id(self, message_id):
        self.message_id = message_id
        return self

    @property
    @serializable(name="to", type=unicode)
    def to(self):
        return self.get_field_value("to")

    @to.setter
    def to(self, to):
        self.set_field_value("to", to)

    def set_to(self, to):
        self.to = to
        return self