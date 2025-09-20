from fastapi import FastAPI
from app.api.routers.router import router
from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title="GENAI api platform",
    summary="Api platform providing api to interact with llms",
    # used to redirect endpoint with slashes to actual endpoint example
    # /item is same as /item/ when set to true
    redirect_slashes=True,
    version="v0.1.0.0"
)

app.include_router(router=router)

#  IMP : apply something to all endpoint here auth

def custom_api():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    #  add security schema
    openapi_schema["components"]["securitySchema"]={
        "APIKeyAuth":{
            "type":"apiKey",
            "in": "header",
            "name" : "Authorization"
        }
    }

    # apply global security
    openapi_schema["security"] = [{"APIKeyAuth":[]}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_api