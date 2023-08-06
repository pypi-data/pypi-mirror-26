# -*- coding: utf-8 -*-
"""This is a generated class and is not intended for modification!
"""


from datetime import datetime
from infobip.util.models import DefaultObject, serializable
from infobip.api.model.nc.logs.NumberContextLog import NumberContextLog

class NumberContextLogsResponse(DefaultObject):
    @property
    @serializable(name="results", type=NumberContextLog, list=True)
    def results(self):
        return self.get_field_value("results")

    @results.setter
    def results(self, results):
        self.set_field_value("results", results)

    def set_results(self, results):
        self.results = results
        return self

    def add_results(self, *results):
        if not self.results:
            self.results = []

        self.results.extend(results)
        return self

    def remove_results(self, *results):
        if not self.results:
            return self

        for i in results:
            self.results.remove(i)

        return self