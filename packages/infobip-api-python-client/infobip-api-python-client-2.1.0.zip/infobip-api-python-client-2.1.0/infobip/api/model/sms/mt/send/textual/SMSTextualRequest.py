# -*- coding: utf-8 -*-
"""This is a generated class and is not intended for modification!
"""


from datetime import datetime
from infobip.util.models import DefaultObject, serializable
class SMSTextualRequest(DefaultObject):
    @property
    @serializable(name="operatorClientId", type=unicode)
    def operator_client_id(self):
        return self.get_field_value("operator_client_id")

    @operator_client_id.setter
    def operator_client_id(self, operator_client_id):
        self.set_field_value("operator_client_id", operator_client_id)

    def set_operator_client_id(self, operator_client_id):
        self.operator_client_id = operator_client_id
        return self

    @property
    @serializable(name="campaignId", type=unicode)
    def campaign_id(self):
        return self.get_field_value("campaign_id")

    @campaign_id.setter
    def campaign_id(self, campaign_id):
        self.set_field_value("campaign_id", campaign_id)

    def set_campaign_id(self, campaign_id):
        self.campaign_id = campaign_id
        return self

    @property
    @serializable(name="from", type=unicode)
    def from_(self):
        return self.get_field_value("from_")

    @from_.setter
    def from_(self, from_):
        self.set_field_value("from_", from_)

    def set_from_(self, from_):
        self.from_ = from_
        return self

    @property
    @serializable(name="to", type=unicode, list=True)
    def to(self):
        return self.get_field_value("to")

    @to.setter
    def to(self, to):
        self.set_field_value("to", to)

    def set_to(self, to):
        self.to = to
        return self

    def add_to(self, *to):
        if not self.to:
            self.to = []

        self.to.extend(to)
        return self

    def remove_to(self, *to):
        if not self.to:
            return self

        for i in to:
            self.to.remove(i)

        return self

    @property
    @serializable(name="text", type=unicode)
    def text(self):
        return self.get_field_value("text")

    @text.setter
    def text(self, text):
        self.set_field_value("text", text)

    def set_text(self, text):
        self.text = text
        return self

    @property
    @serializable(name="transliteration", type=unicode)
    def transliteration(self):
        return self.get_field_value("transliteration")

    @transliteration.setter
    def transliteration(self, transliteration):
        self.set_field_value("transliteration", transliteration)

    def set_transliteration(self, transliteration):
        self.transliteration = transliteration
        return self