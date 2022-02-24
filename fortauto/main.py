from fastapi import FastAPI, status, responses
# from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware import cors
from fortauto.conf import config as base_config
from fortauto.database import database_dependencies as db_deps
from fortauto.api import api_base_router as base_router_v1

app = FastAPI(
    debug=base_config.settings.debug,
    title=base_config.settings.website_name,
    version=base_config.settings.api_version)
app.state.database = db_deps.database
app.include_router(router=base_router_v1.base_router)


@app.on_event("startup")
async def startup():
    await db_deps.connect_datatase(app=app)
    if base_config.settings.debug:
        print("database connected")


@app.on_event("shutdown")
async def shutdown():
    await db_deps.disconnect_datatase(app=app)
    if base_config.settings.debug:
        print("database disconnected")


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     return RedirectResponse("/docs")


@app.get("/", include_in_schema=False, status_code=status.HTTP_200_OK)
async def root():
    return responses.RedirectResponse(
        "/redoc", status_code=status.HTTP_302_FOUND)
