from flask import Blueprint, request, Response, json
from app.models.user_model import User, UserSchema
from flask_jwt_extended import jwt_required



class UserController:

    user_controller = Blueprint(name='user_controller', import_name=__name__)


    @user_controller.route('/user/<id>', methods=['GET'])
    @jwt_required()
    def get_one_user(id):
        user = User.get_one_user(id)

        if not user:
            return custom_response({'error': 'user not found'}, 404)

        serealized_user = user_schema.dump(user)

        return custom_response(serealized_user, 200)


    @user_controller.route('/user/update/<id>', methods=['PUT'])
    @jwt_required()
    def update_user(id):
        request_data = request.get_json()

        try:
            data = user_schema.load(request_data)
        except Exception:
            message = {'error': 'Missing data for required fields (name, email, password).'}
            return custom_response(message, 401)

        user = User.get_one_user(id)
        user.update(data)
        serealize_user = user_schema.dump(user)

        return custom_response(serealize_user, 200)

user_schema = UserSchema()

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )