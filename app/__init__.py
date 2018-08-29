from flask import Flask
from flask_restful import Api
from app.views import Questions,SingleQuestion,PostAnswer,UpdateAnswer
from app.views import UserSignup, UserLogin
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'sharifah' 
jwt = JWTManager(app)


"""initializing an API"""
api = Api(app)

api.add_resource(UserSignup,'/api/v1/auth/signup')
api.add_resource(UserLogin,'/api/v1/auth/login')
api.add_resource(Questions,'/api/v1/questions')
api.add_resource(SingleQuestion,'/api/v1/questions/<questionId>')
api.add_resource(PostAnswer,'/api/v1/questions/<questionId>/answers')
api.add_resource(UpdateAnswer,'/api/v1/questions/<questionId>/answers/<answerId>')
