from flask import Blueprint, request, Response, json, jsonify, g
from app import jwt
from app.models.user_model import User, UserSchema
from app.models.revoked_token_model import RevokedToken
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, get_jwt



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
        request_data = request.get_json()
        try:
            data = user_schema.load(request_data)
        except Exception:
            message = {'error': 'Missing data for required fields (name, email, password).'}
            return custom_response(message, 401)
       
        #checking if user already exust in db
        user_in_db = User.get_user_by_email(data.get("email"))
        if user_in_db:
            message = {"error": "User already exist, please supply another email adress"}
            return custom_response(message, 400)

        user = User(data)
        user.save()
        serealized_data = user_schema.dump(user)
        
        return custom_response(serealized_data, 201)


    @auth_controller.route('/login', methods=['POST'])
    def login():
        request_data = request.get_json()
        data = user_schema.load(request_data, partial=True)
        user = User.get_user_by_email(data.get('email'))

        if not data.get("email") or not data.get('password'):
            return custom_response({'error': 'you need a email and passoword to sing in'}, 400)

        if not user:
            return custom_response({'error': 'invalid credentials'}, 400)
        
        if not user.verify_password(data.get('password')):
            return custom_response({'error': 'invalid credentials'}, 400)

        g.user = user.id_user()

        
        serealize_data = user_schema.dump(user)
        access_token = create_access_token(serealize_data)
        refresh_token = create_refresh_token(serealize_data)
        message = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        
        return custom_response(message, 200)


    @auth_controller.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        access_token = create_access_token(current_user)
        message = {"acess_token": access_token}
        set_access_cookies(jsonify(message), access_token)

        return custom_response(message, 200)

    
    @auth_controller.route('/logout', methods=['DELETE'])
    @jwt_required()
    def logout():
        jti = get_jwt()['jti']
        revoked_token = RevokedToken(jti=jti)
        revoked_token.save()
        return custom_response('Succesfully logged out', 200)
    
user_schema = UserSchema()

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )