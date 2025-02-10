from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_all_users(db):
        return UserRepository.get_all_users(db)

    @staticmethod
    def get_user_by_id(db, user_id):
        return UserRepository.get_user_by_id(db, user_id)

    @staticmethod
    def get_user_by_badge_code(db, badge_code):
        return UserRepository.get_user_by_badge_code(db, badge_code)

    @staticmethod
    def update_user(db, user_id, update_data):
        return UserRepository.update_user(db, user_id, update_data)
