from flask import Blueprint, request, jsonify
from app.services.user_service import UserService, UserExistsError

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint.
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "code": 400,
            "message": "Invalid JSON",
            "data": None
        }), 400

    username = data.get('username')
    password = data.get('password')

    errors = {}
    if not username:
        errors['username'] = ['This field is required.']
    if not password:
        errors['password'] = ['This field is required.']

    if errors:
        return jsonify({
            "code": 422,
            "message": "Validation Error",
            "data": {"errors": errors}
        }), 422

    try:
        new_user = UserService.create_user(username=username, password=password)
        # The API doc asks for a simpler user object on return
        user_data = {
            'id': new_user.id,
            'username': new_user.username
        }
        return jsonify({
            "code": 201,
            "message": "User registered successfully.",
            "data": {"user": user_data}
        }), 201
    except UserExistsError:
        return jsonify({
            "code": 422,
            "message": "Validation Error",
            "data": {"errors": {"username": ["This username is already taken."]}}
        }), 422
    except Exception as e:
        # Generic error handler
        return jsonify({
            "code": 500,
            "message": f"An unexpected error occurred: {e}",
            "data": None
        }), 500
