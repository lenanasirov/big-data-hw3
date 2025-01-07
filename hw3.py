from locale import normalize

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
        # Check if the username and password are not empty strings
        if not username or not password:
            raise ValueError("Username and password are required.")

        # Check if the length of both username and password is at least 3 characters
        if len(username) < 3 or len(password) < 3:
            raise ValueError("Username and password must be at least 3 characters.")

        # Check if the username already exists in the database
        if self.collection.find_one({"username": username}):
            raise ValueError(f"User already exists: {username}.")

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)

        # Create a new user in the database
        self.collection.insert_one({"username": username, "password": hashed_password, "rented_games": []})


    def login_user(self, username: str, password: str) -> object:
        # Hash the provided password using bcrypt with the same salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)

        # Query the database for a matching username and hashed password
        user = self.collection.find_one({"username": username, "password": hashed_password})

        if user:
            print(f"Logged in successfully as: {username}")
            return user
        else:
            raise ValueError("Invalid username or password.")


class DBManager:

    def __init__(self) -> None:
        # MongoDB connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["hw3"]
        self.user_collection = self.db["users"]
        self.game_collection = self.db["games"]

    def load_csv(self) -> None:
        # Load the CSV file
        csv_file = "NintendoGames.csv"
        df = pd.read_csv(csv_file)

        # Ensure the "genres" field is stored as a list
        df["genres"] = df["genres"].apply(ast.literal_eval)

        # Add the "is_rented" field with the value False
        df["is_rented"] = False

        # Ensure an "_id" field exists by generating unique IDs if necessary
        if "_id" not in df.columns:
            df["_id"] = [str(i) for i in range(len(df))]  # Assign unique IDs as strings

        # Convert the DataFrame to a list of dictionaries
        records = df.to_dict(orient="records")

        # Insert records into the collection, avoiding duplicates
        for record in records:
            if not self.game_collection.find_one({"_id": record["_id"]}):
                self.game_collection.insert_one(record)


    def rent_game(self, user: dict, game_title: str) -> str:
        # Query the game collection for the provided game title
        game = self.game_collection.find_one({"title": game_title})

        if not game:
            return f"{game_title} not found"

        if game["is_rented"]:
            return f"{game_title} is already rented"

        # Mark the game as rented
        self.game_collection.update_one(
            {"_id": game["_id"]},
            {"$set": {"is_rented": True}}
        )

        # Add the game ID to the user's rented games list
        self.user_collection.update_one(
            {"_id": user["_id"]},
            {"$push": {"rented_games": game["_id"]}}
        )

        return f"{game_title} rented successfully"

    def return_game(self, user: dict, game_title: str) -> str:
        # Retrieve the updated user to check the rented_games list
        updated_user = self.user_collection.find_one({"_id": user["_id"]})

        # Get the list of rented game IDs from the user object
        rented_game_ids = updated_user.get("rented_games", [])

        # Query the game collection for the provided game title
        game = self.game_collection.find_one({"title": game_title})

        if game and game["_id"] in rented_game_ids:
            # Remove the game ID from the user's rented games list
            self.user_collection.update_one(
                {"_id": user["_id"]},
                {"$pull": {"rented_games": game["_id"]}}
            )

            # Mark the game as not rented
            self.game_collection.update_one(
                {"_id": game["_id"]},
                {"$set": {"is_rented": False}}
            )

            return f"{game_title} returned successfully"

        return f"{game_title} was not rented by you"

    def recommend_games_by_genre(self, user: dict) -> list:
        #get the list of games rented by the user
        rented_game_ids = user.get("rented_games", [])
        if not rented_game_ids:
            return ["No games rented"]
        rented_games = self.game_collection.find_one({"_id": {"$in": rented_game_ids}})
        genres = []
        for game in rented_games:
            genres.extend(game.get("geners",[]))

        genre_counts = {}
        for genre in genres:
            if genre in genre_counts:
                genre_counts[genre] += 1
            else:
                genre_counts[genre] = 1
        total_genres = len(genres)
        genre_probabilities = {genre: count / total_genres for genre, count in genre_counts.items()}

        genre_selected = random.choices(
            population=list(genre_probabilities.keys()),
            weights=list(genre_probabilities.values()),
            k=1
        )[0]

        pipeline = [
            {"$match": {
                #match games with the genre selected
                "genres": genre_selected,
                #exclude games that already rented by the user
                "_id": {"$nin": rented_game_ids}
            }},
            {"$sample": {"size": 5}}
        ]

        recommend_games = list(self.game_collection.aggregate(pipeline))

        return [game["title"] for game in recommend_games]



    def recommend_games_by_name(self, user: dict) -> list:
        #get the list of games rented by the user
        rented_games_ids = user.get("rented_games",[])

        if not rented_games_ids:
            return ["NO games rented"]

        #pick random game from the user's rented games
        rented_games = []
        for game_id in rented_games_ids:
            game = self.game_collection.find_one({"_id": game_id})
            rented_games.append(game)

        selected_game = random.choice(rented_games)

        #get the title of the selected game
        selected_title = selected_game["title"]

        #get all the games titles
        games_db = list(self.game_collection.find({},{"title":1,"_id":0}))
        all_titles = [game["title"] for game in games_db]

        #calculte TF-IDF for all the games titles
        vectorizer = TfidfVectorizer()
        tfidf_vectors = vectorizer.fit_transform(all_titles)

        #find the position of the selected game title
        chosen_index = all_titles.index(selected_title)

        #calculte cosine similarity between the selected game to the other games
        cosine_similarities = cosine_similarity(tfidf_vectors[chosen_index], tfidf_vectors).flatten()

        sorted_score  = cosine_similarities.argsort()[::-1]
        similar_score = []
        for i in sorted_score :
            if all_titles[i] != selected_title:
                similar_score.append(i)

        #list of titles for games that the user rented
        rented_titles = [game["title"] for game in rented_games]
        #list of recommended games exclude games that the user rented
        recommendations = [all_titles[i] for i in similar_score if all_titles[i] not in rented_titles]

        return recommendations[:5]

    def find_top_rated_games(self, min_score) -> list:
        top_rated_games = self.game_collection.find({"user_score": {"$gte": min_score}}, {"title": 1, "user_score": 1, "_id": 0})
        return list(top_rated_games)

    def decrement_scores(self, platform_name) -> None:
        self.game_collection.update_many(
            {"platform": platform_name},
            {"$inc": {"user_score": -1}}
        )

    def get_average_score_per_platform(self) -> dict:
        platform_average = {}  # Dict
        pl = [{
            "$group": {
                "_id": "$platform",
                "average_score": {"$avg": "$user_score"},
            }
        }]
        results = list(self.game_collection.aggregate(pl))
        # Append results into dict
        for value in results:
            platform_average[value["_id"]] = value["average_score"]
        return platform_average

    def get_genres_distribution(self) -> dict:
        genres_dist = {}
        pl = [
            {"$unwind": "$genres"},
            {"$group": {"_id": "$genres", "count": {"$sum": 1}}},
        ]
        results = list(self.game_collection.aggregate(pl))
        # Append results into dict
        for value in results:
            genres_dist[value["_id"]] = value["count"]
        return genres_dist


