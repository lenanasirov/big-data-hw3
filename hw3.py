import pymongo
import bcrypt
import ast
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class LoginManager:

    def __init__(self) -> None:
        # MongoDB connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["hw3"]
        self.collection = self.db["users"]
        self.salt = b"$2b$12$ezgTynDsK3pzF8SStLuAPO"  # TODO: if not working, generate a new salt

    def register_user(self, username: str, password: str) -> None:
        # TODO
        pass

    def login_user(self, username: str, password: str) -> object:
        # TODO
        pass


class DBManager:

    def __init__(self) -> None:
        # MongoDB connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["hw3"]
        self.user_collection = self.db["users"]
        self.game_collection = self.db["games"]

    def load_csv(self) -> None:
        # TODO
        pass

    def rent_game(self, user: dict, game_title: str) -> str:
        # TODO
        pass

    def return_game(self, user: dict, game_title: str) -> str:
        # TODO
        pass

    def recommend_games_by_genre(self, user: dict) -> list:
        # TODO
        pass

    def recommend_games_by_name(self, user: dict) -> list:
        # TODO
        pass

    def find_top_rated_games(self, min_score) -> list:
        # TODO
        pass

    def decrement_scores(self, platform_name) -> None:
        # TODO
        pass

    def get_average_score_per_platform(self) -> dict:
        # TODO
        pass

    def get_genres_distribution(self) -> dict:
        # TODO
        pass

