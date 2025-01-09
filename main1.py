import hw3

def main():
    # Initialize LoginManager
    
    user_manager = hw3.LoginManager()
    user_manager.collection.delete_many({})
    

    # Register a test user
    username = "test_user"
    password = "secure_password"
    user_manager.register_user(username, password)

    # Attempt to log in with the test user
    user = user_manager.login_user(username, password)
    if user:
        print(f"Logged in as: {user['username']}")
    else:
        print("Login failed.")
        return  # Exit if login fails

    # Initialize DBManager and load game data
    db = hw3.DBManager()
    db.game_collection.delete_many({})
    db.load_csv()



    # Test game title
    game_title = "Super Mario Sunshine"
    game_title_1 = "Meteos"

    # Test renting a game
    print("\n--- Rent Game Test 1 ---")
    rent_result = db.rent_game(user, game_title)
    print(f"Rent Result: {rent_result}")

        # Test renting a game
    print("\n--- Rent Game Test 2 ---")
    rent_result_1 = db.rent_game(user, game_title_1)
    print(f"Rent Result: {rent_result_1}")


    # Reload user to reflect changes in the database
    user = db.user_collection.find_one({"username": username})

    # Test recommend_games_by_genre function
    recommended_games_by_genre = db.recommend_games_by_genre(user)
    print("\n Recommended games by genre:")
    print(recommended_games_by_genre)

    # Test recommend_games_by_name function
    recommended_games_by_name = db.recommend_games_by_name(user)
    print("\n Recommended games by name similarity:")
    print(recommended_games_by_name)

    top_rated_games = db.find_top_rated_games(9.6)
    print("top_rated_games")
    print(len(top_rated_games))
    print(top_rated_games)

    # db.decrement_scores('Switch')
    average_scores = db.get_average_score_per_platform()
    print("avg scores")
    print(average_scores)


    
    print("genres destribution")
    print(len( db.get_genres_distribution().items()))
    print("-----------------START-------------")
    print(db.get_genres_distribution().items())
    print("-----------------END-------------")



    # Test returning the game
    print("\n--- Return Game Test ---")
    return_result = db.return_game(user, game_title)
    return_result = db.return_game(user, game_title_1)
    print(f"Return Result: {return_result}")

    # Clean up test data
    print("\n--- Cleaning Up ---")
    db.user_collection.delete_one({"_id": user["_id"]})
    db.game_collection.update_one({"title": game_title}, {"$set": {"is_rented": False}})
    db.game_collection.update_one({"title": game_title_1}, {"$set": {"is_rented": False}})
    print("Test completed and data cleaned.")

if __name__ == "__main__":
    main()