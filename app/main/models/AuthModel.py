from functools import wraps

from flask_jwt_extended import jwt_required

from . import *
from . import User
from .. import make_res
from flask_jwt_extended import get_jwt_identity


class AuthModel(User):
    @classmethod
    @jwt_required(refresh=True)
    def refresh(cls):
        identity = get_jwt_identity()
        ct = create_access_token(identity)
        return make_res(success=1, res={"access_token": ct})

    @classmethod
    def user_by_phone(cls):
        data = request.json.get("data")
        if not data:
            return make_res(msg="access denied")
        user = cls.get_user_by_phone(data)
        return make_res(success=1, res=user if user else False)
