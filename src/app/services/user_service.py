from app.repositories.user_repository import UserRepository

class UserService:
    """
    Retrieves a list of all users from the database.
    Args:
        db: The SQLAlchemy session.
    Returns:
        list: A list of all users.
    """
    @staticmethod
    def get_all_users(db):
        return UserRepository.get_all_users(db)

    """
    Retrieves a user by their ID.
    Args:
        db: The SQLAlchemy session.
        user_id (int): The ID of the user.
    Returns:
        User: The user object, or None if the user is not found.
    """
    @staticmethod
    def get_user_by_id(db, user_id):
        return UserRepository.get_user_by_id(db, user_id)

    """
    Retrieves a user by their badge code.
    Args:
        db: The SQLAlchemy session.
        badge_code (str): The badge code of the user.
    Returns:
        User: The user object, or None if the user is not found.
    """
    @staticmethod
    def get_user_by_badge_code(db, badge_code):
        return UserRepository.get_user_by_badge_code(db, badge_code)

    """
    Updates a user's information.
    Args:
        db: The SQLAlchemy session.
        user_id (int): The ID of the user.
        update_data (dict): A dictionary of fields and values to update.
    Returns:
        User: The updated user object, or None if the user was not found.
    """
    @staticmethod
    def update_user(db, user_id, update_data):
        return UserRepository.update_user(db, user_id, update_data)
