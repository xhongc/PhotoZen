from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="1Moment API",
    description="1Moment API",
    urls_namespace="api",
)
api.auto_discover_controllers()
