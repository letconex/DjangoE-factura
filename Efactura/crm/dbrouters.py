"""DB routers for Vendor"""
from crm.models import Vendor

class DBRouter(object):
    """Define db routes for reading/writing the model."""
    route_app_labels = {"crm"}
    def db_for_read(self, model, **hints):
        """reading vendor model from vendors db"""
        if model == Vendor:
            return "vendors"
        return None

    def db_for_write(self, model, **hints):
        """writing vendor model to vendors db"""
        if model == Vendor:
            return "vendors"
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure the apps only appear in the 'crm' database."""
        if app_label in self.route_app_labels:
            return db == "vendors"
        return None
