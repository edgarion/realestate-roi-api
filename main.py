from fastapi import FastAPI
from adapters.entrypoints.api import router as roi_router

app = FastAPI(title="Real Estate ROI Engine")

app.include_router(roi_router, prefix="/v1")
