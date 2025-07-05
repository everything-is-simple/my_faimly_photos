from app import db
from app.models import User

class UserExistsError(Exception):
    """Custom exception for when a user already exists."""
    pass

class UserService:
    @staticmethod
    def create_user(username, password, nickname=None):
        """
        Create a new user.
        :param username: User's username.
        :param password: User's plain text password.
        :param nickname: User's nickname. Defaults to username if not provided.
        :return: The new user object.
        :raises UserExistsError: If the username is already taken.
        """
        user_exists = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if user_exists:
            raise UserExistsError(f"User with username '{username}' already exists.")

        new_user = User(
            username=username,
            nickname=nickname or username  # Default nickname to username
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user

    @staticmethod
    def to_dict(user):
        """
        Serialize a User object to a dictionary.
        Excludes sensitive information like password_hash.
        """
        return {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'family_id': user.family_id,
            'created_at': user.created_at.isoformat() + 'Z' # ISO 8601 format
        } 