from starlette.schemas import SchemaGenerator

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Codsworth API", "version": "1.0"}}
)

def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)