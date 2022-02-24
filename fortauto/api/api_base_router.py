import fastapi
from fortauto.api.user import user_router
from fortauto.api.user.auth import user_auth_router
from fortauto.api.user.property import user_property_router
from fortauto.api.user.address import user_address_router
from fortauto.api.payment import payment_router
from fortauto.conf import config as base_config
# from fortauto.api.service.category.service_category_router import category_router
from fortauto.api.service.listing import service_listing_router
from fortauto.api.service import service_router

base_router = fastapi.APIRouter(prefix=base_config.settings.api_prefix)
base_router.include_router(
    router=user_router.router, prefix="/users", tags=["Users Account"])
base_router.include_router(
    router=user_auth_router.router,
    prefix="/auth",
    tags=[" Users Authentication"])
base_router.include_router(
    router=user_property_router.router, prefix="/cars", tags=["User Car"])
base_router.include_router(
    router=user_address_router.router, prefix="/address", tags=["User Address"])

# base_router.include_router(
#     router=category_router, prefix="/categorys", tags=["Service category"]
# )
base_router.include_router(
    router=service_listing_router.router,
    prefix="/listings",
    tags=["Service listings"])
base_router.include_router(
    router=service_router.router, prefix="/services", tags=["Services"])

base_router.include_router(
    router=payment_router.router, prefix="/payments", tags=["Payment"])
