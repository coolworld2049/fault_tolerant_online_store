import uvicorn

from app import factory
from app.api.v1.api import api_router
from app.lifespan import lifespan

app = factory.create_fastapi_app(
    _routers=[api_router],
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

if __name__ == "__main__":
    uvicorn.run(app)
