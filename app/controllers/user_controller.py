from flask import Blueprint, request
from extensions import db
from app.models.user import User
from app.utils.response_handler import success_response, error_response

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return success_response(
            data=[user.to_dict() for user in users],
            message="Users retrieved successfully"
        )
    except Exception as e:
        return error_response(
            message="Failed to retrieve users",
            errors=str(e)
        )

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data:
            return error_response(
                message="Missing required fields",
                errors="Username and email are required"
            )
            
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return success_response(
            data=user.to_dict(),
            message="User created successfully",
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to create user",
            errors=str(e)
        )

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return success_response(
            data=user.to_dict(),
            message="User retrieved successfully"
        )
    except Exception as e:
        return error_response(
            message=f"User with id {user_id} not found",
            errors=str(e),
            status_code=404
        )

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
            
        db.session.commit()
        return success_response(
            data=user.to_dict(),
            message="User updated successfully"
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to update user",
            errors=str(e)
        )

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return success_response(
            message="User deleted successfully"
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to delete user",
            errors=str(e)
        ) 