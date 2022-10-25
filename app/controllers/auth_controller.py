from functools import partial
from flask import Blueprint, request, Response, json
from app import db, jwt
from app.models.user_model import User, UserSchema
from app.models.revoked_token_model import RevokedToken



class AuthController:
    
    auth_controller = Blueprint(name='auth_controller', import_name=__name__)
    

    #Loading the jwt identity value
    @jwt.user_identity_loader
    def user_identity_lookup(login):
        return login

    #cheking if token is revoked
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_data):
        jti = jwt_data['jti']
        rt = RevokedToken.query.filter_by(jti=jti).first()
        return bool(rt)

    @auth_controller.route('/register', methods=['POST'])
    def register():
        
        user_schema = UserSchema()
        req_data = request.get_json()
        try:
            data = user_schema.load(req_data)
        except Exception:
            message = {'error': 'Missing data for required field.'}
            return custom_response(message, 401)
       
        #checking if user already exust in db
        user_in_db = User.get_user_by_email(data.get("email"))
        if user_in_db:
            message = {"error": "User already exist, please supply another email adress"}
            return custom_response(message, 400)

        user = User(data)
        user.save()
        ser_data = user_schema.dump(user)
        
        return custom_response(ser_data, 201)





def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )