"""
Workshop Recommender Data Input Application

Single page application to read/enter review data!
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.settings import config

import app.utils as utils
import app.api as api
import app.models as models

app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def render_main_page(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "users": api.get_users()}
    )


@app.get("/")
async def display_splash(request: Request):
    return render_main_page(request)



@app.post("/users/update")
async def create_or_update_user(request: Request, userID: int, userGenre: str):
    # user_profile: models.RestaurantUser = models.RestaurantUser()
    # api.create_update_user(user_profile)
    return RedirectResponse(
        '/',
        status_code=200
    )