"""
Models

Data models for Foodie Workshop Recommender
"""

import dateutil
from pydantic import BaseModel, validator
import os
from typing import Any, List

import json

from app.settings import config



genres = {}


# User Data Utilities

def save_model_data(model: BaseModel, filename: str, format: str = 'json') -> str:
    
    def save_as_json(model, filename) -> str:
        with open(filename, 'w+') as file:
            json.dump(dict(model), file)
        return filename

    def save_as_text(model, filename) -> str:
        with open(filename ,'w+') as file:
            file.write(json.dumps(dict(model)))

    filename = os.path.join(os.getcwd(), config.DATADIR, filename)

    file_mode_fns = {
        'json': save_as_json,
        'txt': save_as_text,
    }    

    save_fn = file_mode_fns[format]
    return save_fn(model, filename)



# Genre Lookup Utilities

def create_empty_genres_file(filepath: str) -> None:
    with open(filepath, 'w+') as file:
        json.dump({}, file)
    return {}
        
        

def load_or_create_genres(genres_file='genres.json') -> dict:
    filepath = os.path.join(os.getcwd(), config.DATADIR, genres_file)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        print('file not found', filepath)
        return create_empty_genres_file(filepath)


    
def save_genres(genres: dict, genres_file='genres.json') -> dict:
    filepath = os.path.join(os.getcwd(), config.DATADIR, genres_file)
    with open(filepath, 'w+') as file:
        json.dump(genres, file)
    return genres

    
        
def add_element_to_genres(element: str, genres: dict) -> int:
    
    def is_num(x) -> bool:
        try:
            return int(x) != False
        except:
            return False
    
    dict_len = len(genres)
    
    if is_num(element):
        return element
    elif element not in genres:
        genres[element] = dict_len + 1
        genres = save_genres(genres)
    return genres[element]
        
        
        
def map_genre(genre_list: list) -> list:
    tmp = []
    genres = load_or_create_genres()
    for element in genre_list:
        tmp.append(add_element_to_genres(element, genres))
    return tmp
        


# Data Models

class RestaurantUser(BaseModel):
    user_birth_date: int
    user_genres: List[Any] = [0]
    user_id: int
    user_occupation: str
    user_gender: bool  # 0: male, 1: female
    user_zip_code: int
    
    
    @validator('user_genres')
    def index_or_add(cls, v):
        assert len(v) > 0, 'Must provide list of genre > 0'
        return map_genre(v)
    
    def save(self, prefix='user', format='json') -> None:
        name = prefix + f"_{self.user_id}"
        return save_model_data(self, name, format)

    
        
class Restaurant(BaseModel):
    restaurant_id: int
    restaurant_title: str
    restaurant_genres: List[Any]
    restaurant_zip_code: int
   
    @validator('restaurant_genres')
    def index_or_add(cls, v):
        assert len(v) > 0, 'Must provide list of genre > 0'
        return map_genre(v)
        
    def save(self, prefix='restaurant', format='json') -> str:
        name = prefix + f"_{self.restaurant_id}"
        return save_model_data(self, name, format)
    
    
    
class RestaurantRating(BaseModel):
    user: RestaurantUser
    restaurant: Restaurant
    timestamp: int  # Converting all date/time to posix integer
    restaurant_rating: int
    
    @validator('timestamp')
    def convert_valid_time(cls, v: str):
        return v
    
    def save(self, prefix='rating', format='json') -> str:
        name = prefix + f"_{self.restaurant}_{self.user}_{self.timestamp}"
        return save_model_data(self, name)
    
    def flatten(self) -> dict:
        tmp = {
            **self.user.dict(), **self.restaurant.dict(),
            'timestamp': self.timestamp,
            'restaurant_rating': self.restaurant_rating,
        }
        return tmp

    
    