from unittest import TestCase
from flask import Flask
from flask_restful import Api, Resource
from ..src.requestChecker import RequestChecker, Path, SecurityPolicyEnum


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

        requestChecker.addPath(Resource, path)

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
        requestChecker.addPath(Resource, path)
        requestChecker.addPath(Resource, path)

        assert len(requestChecker.getPaths()) == 1

    def test_checkRequestAnnonymous(self):
        app = Flask("test")
        api = Api(app)
        requestChecker = RequestChecker(api)

        path = Path('/test')

        requestChecker.addPath(MyResource, path)

        with app.test_client() as client:
            rv = client.get('/test')
            assert rv.status_code == 200

    def test_checkRequestNotFound(self):
        app = Flask("test")
        api = Api(app)
        RequestChecker(api)

        api.add_resource(MyResource, '/test')

        with app.test_client() as client:
            rv = client.get('/test')
            assert rv.status_code == 404

    def test_checkRequestJWTMissing(self):
        app = Flask("test")
        app.config['JWT_SECRET_KEY'] = "change_me_jwt"
        app.config['JWT_TOKEN_LOCATION'] = 'headers'
        app.config['JWT_HEADER_NAME'] = 'Authorization'
        app.config['JWT_HEADER_TYPE'] = 'Bearer'
        api = Api(app)
        requestChecker = RequestChecker(api)

        path = Path('/test', policy=SecurityPolicyEnum.JWT)

        requestChecker.addPath(MyResource, path)

        with app.test_client() as client:
            rv = client.get('/test')
            assert rv.status_code == 403
