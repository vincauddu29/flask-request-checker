# Request Checker

Flask module enable to check if a request can be allowed or not.

## Exemple
```
from flask import Flask
from flask_restful import Api, Resource
from ModuleSecurityChecker import ModuleSecurityChecker

app = Flask("test")
api = Api(app)

securityChecker = ModuleSecurityChecker(api)

def TestResource(Resource):
    def post(self):
        pass

security.addPath(TestResource, '/test')

```