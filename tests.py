import time

import hw3

def main():
    # Initialize LoginManager
    user_manager = hw3.LoginManager()
    user_manager.collection.delete_many({})

    # Register multiple test users
    usernames = ["test_user1", "test_user2", "test_user3"]
    password = "secure_password"
    for username in usernames:
        user_manager.register_user(username, password)
        user = user_manager.login_user(username, password)
        assert user is not None, f"User {username} login failed after registration."

    # Attempt to log in with one of the test users
    user = user_manager.login_user(usernames[0], password)
    assert user is not None, f"Login failed for {usernames[0]}."
    print(f"Logged in as: {user['username']}")

    # Initialize DBManager and load game data
    db = hw3.DBManager()
    db.game_collection.delete_many({})
    db.load_csv()

    # Test game title
    game_title = "Pikmin 4"
    invalid_game_title = "Nonexistent Game"

    # Test renting a valid game
    print("\n--- Rent Game Test (Valid Game) ---")
    rent_result = db.rent_game(user, game_title)
    assert "rented successfully" in rent_result, "Failed to rent a valid game."
    print(f"Rent Result: {rent_result}")

    # Test renting an already rented game
    print("\n--- Rent Game Test (Already Rented) ---")
    rent_result = db.rent_game(user, game_title)
    assert "is already rented" in rent_result, "Rented game should not be rentable again."
    print(f"Rent Result: {rent_result}")

    user = db.user_collection.find_one({"username": usernames[0]})

    # Test renting an invalid game
    print("\n--- Rent Game Test (Invalid Game) ---")
    rent_result = db.rent_game(user, invalid_game_title)
    assert "not found" in rent_result, "Invalid game title should return 'not found'."
    print(f"Rent Result: {rent_result}")

    # Test recommend_games_by_genre function
    print("\n--- Recommended Games by Genre ---")
    recommended_games_by_genre = db.recommend_games_by_genre(user)
    assert isinstance(recommended_games_by_genre, list), "Recommendations by genre should return a list."
    print(recommended_games_by_genre)

    # Test recommend_games_by_name function
    print("\n--- Recommended Games by Name Similarity ---")
    recommended_games_by_name = db.recommend_games_by_name(user)
    assert isinstance(recommended_games_by_name, list), "Recommendations by name should return a list."
    print(recommended_games_by_name)

    # Test returning a valid game
    print("\n--- Return Game Test (Valid Game) ---")
    return_result = db.return_game(user, game_title)
    assert "returned successfully" in return_result, "Failed to return a valid game."
    print(f"Return Result: {return_result}")
    #
    #
    # Test returning a game not rented by the user
    print("\n--- Return Game Test (Not Rented) ---")
    return_result = db.return_game(user, game_title)
    assert "was not rented by you" in return_result, "Returning a non-rented game should fail."
    print(f"Return Result: {return_result}")
    #
    # Test recommend_games_by_genre function
    print("\n--- Recommended Games by Genre ---")
    recommended_games_by_genre = db.recommend_games_by_genre(user)
    assert isinstance(recommended_games_by_genre, list), "Recommendations by genre should return a list."
    print(recommended_games_by_genre)

    # Test recommend_games_by_name function
    print("\n--- Recommended Games by Name Similarity ---")
    recommended_games_by_name = db.recommend_games_by_name(user)
    assert isinstance(recommended_games_by_name, list), "Recommendations by name should return a list."
    print(recommended_games_by_name)

    # Test finding top-rated games
    print("\n--- Top Rated Games (User Score >= 9.1) ---")
    top_rated_games = db.find_top_rated_games(9.1)
    assert len(top_rated_games) > 0, "There should be top-rated games with a score >= 9.1."
    print(f"Top Rated Games Count: {len(top_rated_games)}")
    print(top_rated_games)

    # Test decrementing scores for a platform
    print("\n--- NO Decrement Scores  ---")
    # db.decrement_scores('Switch')
    updated_scores = db.get_average_score_per_platform()
    assert 'Switch' in updated_scores, "Switch platform should exist in average scores."
    print("Decrement completed. Verifying...")

    # Test getting average score per platform
    print("\n--- Average Scores Per Platform ---")
    average_scores = db.get_average_score_per_platform()
    assert isinstance(average_scores, dict), "Average scores should return a dictionary."
    print(average_scores)

    # Test getting genre distribution
    print("\n--- Genre Distribution ---")
    genre_distribution = db.get_genres_distribution()
    assert isinstance(genre_distribution, dict), "Genre distribution should return a dictionary."
    print(genre_distribution)

    # Clean up test data
    print("\n--- Cleaning Up ---")
    for username in usernames:
        db.user_collection.delete_one({"username": username})
    db.game_collection.update_one({"title": game_title}, {"$set": {"is_rented": False}})
    print("Test completed and data cleaned.")

    print("\n--- Decrement Scores (Platform: Switch) ---")
    db.decrement_scores('Switch')
    updated_scores = db.get_average_score_per_platform()
    assert 'Switch' in updated_scores, "Switch platform should exist in average scores."
    print("Decrement completed. Verifying...")

if __name__ == "__main__":
    main()