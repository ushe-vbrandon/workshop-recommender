"""
Workshop Recommender Data Input Application

Single page application to read/enter review data!
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from settings import config

import utils
import api
import models

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def render_main_page(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "users": api.get_users()}
    )


@app.get("/")
async def display_splash(request: Request):
    return render_main_page(request)



@app.post("/users/update")
async def create_or_update_user(request: Request, user_profile: models.RestaurantUser):
    api.create_update_user(user_profile)
    return RedirectResponse(
        '/',
        status_code=200
    )