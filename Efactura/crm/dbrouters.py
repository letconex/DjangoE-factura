"""DB routers for Vendor"""
from crm.models import Vendor

class DBRouter(object):
    """Define db routes for reading/writing the model."""

    def db_for_read(self, model, **hints):
        """reading vendor model from vendors db"""
        if model == Vendor:
            return "vendors"
        return None

    def db_for_write(self, model, **hints):
        """writing vendor model from vendors db"""
        if model == Vendor:
            return "vendors"
        return None
