from import_export import resources
from employee.models import Data

class DataResource(resources.ModelResource):
    class Meta:
        model = Data