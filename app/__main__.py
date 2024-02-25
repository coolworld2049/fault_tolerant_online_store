import uvicorn

from app import factory
from app.api.v1.api import api_router
from app.lifespan import lifespan

app = factory.create(_routers=[api_router], lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(app)