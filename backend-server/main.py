from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.marketplace import router as marketplace_router
from routes.predict import router as predict_router
from routes.users import router as users_router
from routes.vendors import router as vendors_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Smart Agriculture AI",
        version="1.0.0",
        description="Backend server for Smart Agriculture AI (hackathon-ready).",
    )

    # Allow all origins for demo (lock down in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {
            "name": "Smart Agriculture AI",
            "docs": "/docs",
            "routes": [
                "POST /predict",
                "POST /sell-crop",
                "GET /buy-crops",
                "GET /vendors",
                "POST /users/register",
                "POST /users/login",
            ],
        }

    @app.get("/health")
    def health():
        return {"status": "ok"}

    # Routers
    app.include_router(predict_router)
    app.include_router(marketplace_router)
    app.include_router(vendors_router)
    app.include_router(users_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=False)