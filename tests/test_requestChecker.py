from unittest import TestCase
from flask import Flask
from flask_jwt_extended import (
    jwt_manager,
    create_access_token,
    create_refresh_token
)
from flask_restful import Api, Resource
from ..src.requestChecker import (
    RequestChecker,
    Path,
    SecurityPolicyEnum
)


class MyResource(Resource):
    def get(self):
        return True


class RequestCheckerTest(TestCase):
    def test_createWithApi(self):
        app = Flask("test")
        api = Api(app)
        requestChecker = RequestChecker(api)

        assert requestChecker.getApi() == api
        assert requestChecker.getApp() == api.app

    def test_createWithApp(self):
        app = Flask("test")
        requestChecker = RequestChecker(app)

        assert requestChecker.getApi() is None
        assert requestChecker.getApp() == app

    def test_createWithAnotherObject(self):
        with self.assertRaises(Exception):
            RequestChecker(object())

    def test_createPaths(self):
        app = Flask("test")
        api = Api(app)
        requestChecker = RequestChecker(api)

        assert requestChecker.getPaths() == list()

    def test_addPathWithApi(self):
        app = Flask("test")
        api = Api(app)
        requestChecker = RequestChecker(api)

        path = Path('/test')

        requestChecker.addPath(path, Resource)

        assert len(requestChecker.getPaths()) == 1
        assert requestChecker.getPaths()[0] == path

        api = requestChecker.getApi()

        # TODO : need to investicate
        # assert len(api.resources) == 1

    def test_addTwoPaths(self):
        app = Flask("test")
        api = Api(app)
        requestChecker = RequestChecker(api)

        path = Path('/test')
        requestChecker.addPath(path, Resource)
        requestChecker.addPath(path, Resource)

        assert len(requestChecker.getPaths()) == 1

    def test_JWTcheckRequestAnnonymous(self):
        app = Flask("test")
        api = Api(app)
        requestChecker = RequestChecker(api)

        path = Path('/test')

        requestChecker.addPath(path, MyResource)

        with app.test_client() as client:
            rv = client.get('/test')
            assert rv.status_code == 200

    def test_JWTcheckRequestNotFound(self):
        app = Flask("test")
        api = Api(app)
        RequestChecker(api)

        api.add_resource(MyResource, '/test')

        with app.test_client() as client:
            rv = client.get('/test')
            assert rv.status_code == 404

    def test_JWTcheckRequestJWTMissing(self):
        app = Flask("test")
        app.config['JWT_SECRET_KEY'] = "change_me_jwt"
        app.config['JWT_TOKEN_LOCATION'] = 'headers'
        app.config['JWT_HEADER_NAME'] = 'Authorization'
        app.config['JWT_HEADER_TYPE'] = 'Bearer'
        api = Api(app)
        requestChecker = RequestChecker(api)

        path = Path('/test', policy=SecurityPolicyEnum.JWT)

        requestChecker.addPath(path, MyResource)

        with app.test_client() as client:
            rv = client.get('/test')
            assert rv.status_code == 403

    def test_getJwtManager(self):
        app = Flask("test")
        app.config['JWT_SECRET_KEY'] = "change_me_jwt"
        app.config['JWT_TOKEN_LOCATION'] = 'headers'
        app.config['JWT_HEADER_NAME'] = 'Authorization'
        app.config['JWT_HEADER_TYPE'] = 'Bearer'
        api = Api(app)
        requestChecker = RequestChecker(api)

        assert type(requestChecker.getJwtManager()) == jwt_manager.JWTManager

    def test_JWTcheckRequestLogged(self):
        app = Flask("test")
        app.config['JWT_SECRET_KEY'] = "change_me_jwt"
        app.config['JWT_TOKEN_LOCATION'] = 'headers'
        app.config['JWT_HEADER_NAME'] = 'Authorization'
        app.config['JWT_HEADER_TYPE'] = 'Bearer'
        api = Api(app)
        requestChecker = RequestChecker(api)
        jwt_manager.JWTManager(app)

        path = Path('/test', policy=SecurityPolicyEnum.JWT)

        requestChecker.addPath(path, MyResource)
        with app.app_context():
            token = create_access_token(identity="toto")
        header = {"Authorization": "Bearer {0}".format(token)}

        with app.test_client() as client:
            rv = client.get('/test', headers=header)
            print(rv.data)
            assert rv.status_code == 200
