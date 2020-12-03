from unittest import TestCase
from ..src.requestChecker import Path, SecurityPolicyEnum, MethodsEnum


class PathTest(TestCase):
    def test_createJWT(self):
        path = Path(
            "/url1",
            [MethodsEnum.GET, MethodsEnum.POST],
            SecurityPolicyEnum.JWT
        )

        assert path.getUrl() == "/url1"
        assert len(path.getMethods()) == 2
        assert path.getMethods()[0] == MethodsEnum.GET
        assert path.getMethods()[1] == MethodsEnum.POST
        assert path.getPolicy() == SecurityPolicyEnum.JWT

    def test_createWithDefaultValues(self):
        path = Path("/url2")

        assert path.getUrl() == "/url2"
        assert len(path.getMethods()) == 1
        assert path.getMethods() == [MethodsEnum.ALL]
        assert path.getPolicy() == SecurityPolicyEnum.ANNONYMOUS
