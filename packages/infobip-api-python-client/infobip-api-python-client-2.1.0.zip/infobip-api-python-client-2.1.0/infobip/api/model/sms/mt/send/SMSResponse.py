# -*- coding: utf-8 -*-
"""This is a generated class and is not intended for modification!
"""


from datetime import datetime
from infobip.util.models import DefaultObject, serializable
from infobip.api.model.sms.mt.send.SMSResponseDetails import SMSResponseDetails

class SMSResponse(DefaultObject):
    @property
    @serializable(name="bulkId", type=unicode)
    def bulk_id(self):
        return self.get_field_value("bulk_id")

    @bulk_id.setter
    def bulk_id(self, bulk_id):
        self.set_field_value("bulk_id", bulk_id)

    def set_bulk_id(self, bulk_id):
        self.bulk_id = bulk_id
        return self

    @property
    @serializable(name="trackingProcessKey", type=unicode)
    def tracking_process_key(self):
        return self.get_field_value("tracking_process_key")

    @tracking_process_key.setter
    def tracking_process_key(self, tracking_process_key):
        self.set_field_value("tracking_process_key", tracking_process_key)

    def set_tracking_process_key(self, tracking_process_key):
        self.tracking_process_key = tracking_process_key
        return self

    @property
    @serializable(name="messages", type=SMSResponseDetails, list=True)
    def messages(self):
        return self.get_field_value("messages")

    @messages.setter
    def messages(self, messages):
        self.set_field_value("messages", messages)

    def set_messages(self, messages):
        self.messages = messages
        return self

    def add_messages(self, *messages):
        if not self.messages:
            self.messages = []

        self.messages.extend(messages)
        return self

    def remove_messages(self, *messages):
        if not self.messages:
            return self

        for i in messages:
            self.messages.remove(i)

        return self