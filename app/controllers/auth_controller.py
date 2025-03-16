from flask import Blueprint, request, make_response
from extensions import db, jwt
from app.models.user import User
from app.utils.response_handler import success_response, error_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return error_response(
                    message=f"Field {field} harus diisi",
                    errors=f"Missing required field: {field}",
                    status_code=400
                )

        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return error_response(
                message="Username sudah terdaftar",
                errors="Username already exists",
                status_code=400
            )

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return error_response(
                message="Email sudah terdaftar",
                errors="Email already exists",
                status_code=400
            )

        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return success_response(
            data=user.to_dict(),
            message="User berhasil didaftarkan",
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal mendaftarkan user",
            errors=str(e)
        )

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return error_response(
                    message=f"Field {field} harus diisi",
                    errors=f"Missing required field: {field}",
                    status_code=400
                )

        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return error_response(
                message="Email atau password salah",
                errors="Invalid credentials",
                status_code=401
            )

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return success_response(
            data={
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer'
            },
            message="Login berhasil"
        )

    except Exception as e:
        return error_response(
            message="Gagal melakukan login",
            errors=str(e)
        )

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)

        return success_response(
            data={
                'access_token': access_token,
                'token_type': 'Bearer'
            },
            message="Token berhasil diperbarui"
        )

    except Exception as e:
        return error_response(
            message="Gagal memperbarui token",
            errors=str(e)
        )

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Get current user info"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return error_response(
                message="User tidak ditemukan",
                errors="User not found",
                status_code=404
            )

        return success_response(
            data=user.to_dict(),
            message="Data user berhasil diambil"
        )

    except Exception as e:
        return error_response(
            message="Gagal mengambil data user",
            errors=str(e)
        ) 