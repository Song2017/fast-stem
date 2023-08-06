# coding: utf-8

"""
Demo server
"""

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from src.api.health_api import router as health_api
from src.api.user_api import router as user_api
from stem.pkg import APP_CONF, PROJECT_DIR

APP_VERSION_PATH = APP_CONF.APP_VERSION_PATH

app = FastAPI(
    title=APP_CONF.APP_NAME,
    description="This is the CBEC API",
    version=APP_CONF.APP_VERSION,
    docs_url=None,  # f"{APP_VERSION_PATH}/docs",
    openapi_url=f"{APP_VERSION_PATH}/openapi.json"
)

# static files
app.mount('/static', StaticFiles(
    directory=f"{PROJECT_DIR}/resources/static/swagger-ui"), name='static')


# swagger doc path
@app.get(f"{APP_VERSION_PATH}/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_api, prefix=APP_VERSION_PATH)
app.include_router(user_api, prefix=APP_VERSION_PATH)

if __name__ == "__main__":
    uvicorn.run("http_server:app", host='0.0.0.0', port=APP_CONF.PORT, reload=True)
