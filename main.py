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


if __name__ == "__main__":
    run_tests()
