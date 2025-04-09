from drf_yasg.generators import OpenAPISchemaGenerator

from backend.settings import SCHEME


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = [SCHEME]
        return schema
