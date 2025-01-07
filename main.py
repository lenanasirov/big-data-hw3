from hw3 import LoginManager, DBManager


def run_tests():
    # Initialize managers
    login_manager = LoginManager()
    db_manager = DBManager()

    # Clear collections for clean test environment
    login_manager.collection.delete_many({})
    db_manager.game_collection.delete_many({})

    # Load CSV data into the database
    db_manager.load_csv()

    # Test data
    username = "testuser"
    password = "password123"
    game_title_existing = "Super Mario Odyssey"  # Replace with an actual title from your CSV
    game_title_nonexistent = "Nonexistent Game"

    # Test: Register and Login Success
    try:
        login_manager.register_user(username, password)
        print("Register Success: Passed")
    except ValueError as e:
        print(f"Register Success: Failed - {e}")

    try:
        user = login_manager.login_user(username, password)
        print("Login Success: Passed")
    except ValueError as e:
        print(f"Login Success: Failed - {e}")

    # Test: Register Duplicate User
    try:
        login_manager.register_user(username, password)
        print("Register Duplicate User: Failed")
    except ValueError:
        print("Register Duplicate User: Passed")

    # Test: Rent Game Success
    try:
        result = db_manager.rent_game(user, game_title_existing)

        if f"{game_title_existing} rented successfully" in result:
            print("Rent Game Success: Passed")
        else:
            print(f"Rent Game Success: Failed - {result}")
    except Exception as e:
        print(f"Rent Game Success: Failed - {e}")

    # Test: Rent Already Rented Game
    try:
        result = db_manager.rent_game(user, game_title_existing)
        if f"{game_title_existing} is already rented" in result:
            print("Rent Already Rented Game: Passed")
        else:
            print(f"Rent Already Rented Game: Failed - {result}")
    except Exception as e:
        print(f"Rent Already Rented Game: Failed - {e}")

    # Test: Rent Nonexistent Game
    try:
        result = db_manager.rent_game(user, game_title_nonexistent)
        if f"{game_title_nonexistent} not found" in result:
            print("Rent Nonexistent Game: Passed")
        else:
            print(f"Rent Nonexistent Game: Failed - {result}")
    except Exception as e:
        print(f"Rent Nonexistent Game: Failed - {e}")

    # Test: Return Game Success
    try:
        result = db_manager.return_game(user, game_title_existing)
        if f"{game_title_existing} returned successfully" in result:
            print("Return Game Success: Passed")
        else:
            print(f"Return Game Success: Failed - {result}")
    except Exception as e:
        print(f"Return Game Success: Failed - {e}")

    # Test: Return Not Rented Game
    try:
        result = db_manager.return_game(user, game_title_existing)
        if f"{game_title_existing} was not rented by you" in result:
            print("Return Not Rented Game: Passed")
        else:
            print(f"Return Not Rented Game: Failed - {result}")
    except Exception as e:
        print(f"Return Not Rented Game: Failed - {e}")

    # Nati's tests
    # Test: Decrement Scores
    try:
        # Set initial scores for testing
        db_manager.game_collection.update_many(
            {"platform": "Nintendo Switch"},
            {"$set": {"user_score": 5}}
        )

        # Decrement scores
        db_manager.decrement_scores("Nintendo Switch")

        # Verify scores were decremented
        games = db_manager.game_collection.find({"platform": "Nintendo Switch"})
        passed = all(game["user_score"] == 4 for game in games)

        if passed:
            print("Decrement Scores: Passed")
        else:
            print("Decrement Scores: Failed - Scores were not decremented correctly")
    except Exception as e:
        print(f"Decrement Scores: Failed - {e}")

    # Test: Get Average Score Per Platform
    try:
        # Set specific scores for testing
        db_manager.game_collection.update_many(
            {"platform": "Switch"},
            {"$set": {"user_score": 8}}
        )
        db_manager.game_collection.update_many(
            {"platform": "iOS"},
            {"$set": {"user_score": 7}}
        )

        averages = db_manager.get_average_score_per_platform()

        if averages.get("Switch") == 8 and averages.get("iOS") == 7:
            print("Get Average Score Per Platform: Passed")
        else:
            print(f"Get Average Score Per Platform: Failed - {averages}")
    except Exception as e:
        print(f"Get Average Score Per Platform: Failed - {e}")

    # Test: Get Genres Distribution
    try:
        # Set genres for testing
        db_manager.game_collection.update_many(
            {},
            {"$set": {"genres": ["Action", "Adventure"]}}
        )

        distribution = db_manager.get_genres_distribution()

        if distribution.get("Action") > 0 and distribution.get("Adventure") > 0:
            print("Get Genres Distribution: Passed")
        else:
            print(f"Get Genres Distribution: Failed - {distribution}")
    except Exception as e:
        print(f"Get Genres Distribution: Failed - {e}")


if __name__ == "__main__":
    run_tests()
