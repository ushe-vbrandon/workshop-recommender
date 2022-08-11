"""
API for Foodie Recommender!
"""

import os
from typing import List

import json

import app.models as models
from app.settings import config



def read_user_profiles(data_dir: os.PathLike) -> List[models.RestaurantUser]:
    def read_profile(path: os.PathLike) -> dict:
        with open(path, 'r') as file:
            return models.RestaurantUser(**json.load(file))  ## Not sure why json load not working here

    user_files = [os.path.join(os.getcwd(), config.DATADIR, path) for path in os.listdir(data_dir) if path.startswith('user')]
    user_profiles = [read_profile(path) for path in user_files]
    
    print(user_profiles)
    return user_profiles



def get_users() -> dict:
    users: dict = read_user_profiles(data_dir=config.DATADIR)
    return users



def create_update_user(user_profile: models.RestaurantUser) -> dict:
    user_profile.save()

