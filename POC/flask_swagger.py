import logging

from flasgger import Swagger
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields

logging.basicConfig(
    filemode="w",
    format="%(asctime)s-%(name)s-%(levelname)s--%(process)d-%(thread)d-%(threadName)s-%(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


class MobileSchema(Schema):
    model = fields.String(required=True, doc="手机型号")
    no = fields.String(required=True, doc="手机编号")

    class Meta:
        strict = True


class UserJsonSchema(Schema):
    username = fields.Str(required=True, doc="用户名")
    age = fields.Integer(required=False, default=0, doc="年龄")
    qq = fields.List(fields.String, required=False, doc="用户QQ号")
    email = fields.Email(required=False, doc="邮箱")
    image = fields.URL(required=False, doc="用户头像")
    mobile = fields.Nested(MobileSchema, many=False)

    class Meta:
        strict = True
        unknown = "EXCLUDE"  # 参数中对多余字段处理 EXCLUDE`-排除, `INCLUDE`-不处理 or `RAISE`-抛异常.


class CreateUserJsonSchema(UserJsonSchema):
    pass

    class Meta:
        strict = True


class CreateUserSuccessResponse(Schema):
    id = fields.Number(required=True)

    class Meta:
        strict = True


class QueryUserSchema(Schema):
    id = fields.Int(required=False, doc="用户ID")
    username = fields.String(required=False, doc="用户名")

    class Meta:
        strict = True


class GetUserResponseSchema(Schema):
    """
    返回符合条件的用户列表
    """

    users = fields.Nested(UserJsonSchema, many=True, doc="用户列表")
    count = fields.Integer(required=True, default=0, doc="用户数量")
    page = fields.Integer(required=True, default=1, doc="当前页码")

    class Meta:
        strict = True


class UserDetailResponseSchema(UserJsonSchema):
    """用户详情"""

    pass

    class Meta:
        strict = True


class responseHeadersSchema(Schema):
    Location = fields.String(required=True, default=1, doc="跳转地址")
    X_RateLimit_Limit = fields.Integer(
        required=True,
        default=1,
        doc="Request limit per hour",
        data_key="X-RateLimit-Limit",
    )

    class Meta:
        strict = True


class HeadersSchema(Schema):
    Login_Credential = fields.String(
        required=True, doc="登录凭证", data_key="Login-Credential"
    )

    class Meta:
        unknown = True


class RedirectResponseSchema(Schema):
    """
    重定向实例
    """

    class Meta:
        headers = responseHeadersSchema
        strict = True


class User(Resource):
    @swagger_decorator(
        json_schema=CreateUserJsonSchema,
        response_schema={200: CreateUserSuccessResponse},
    )
    def post(self):
        """
        创建一个用户
        """

        # 获取校验后的数据
        logger.info(type(request.json_schema), request.json_schema)
        return {"id": 1}

    @swagger_decorator(
        query_schema=QueryUserSchema,
        response_schema={200: GetUserResponseSchema},
        headers_schema=HeadersSchema,
    )
    def get(self):
        """
        查询用户
        """

        # 获取校验后的数据
        logger.info(type(request.query_schema), request.query_schema)
        return {"user_name": "陈小龙"}

    @swagger_decorator(
        query_schema=QueryUserSchema, response_schema={302: RedirectResponseSchema}
    )
    def put(self):
        """重定向实例"""
        return (
            None,
            302,
            {"Location": "http://www.baidu.com", "X-RateLimit-Limit": 2000},
        )


class UsernamePathSchema(Schema):
    username = fields.String(required=False, doc="用户名")

    class Meta:
        strict = True


class UpdateUserSchema(Schema):
    email = fields.Email(required=False, doc="用户邮箱")
    image = fields.Url(required=False, doc="用户头像")

    class Meta:
        strict = True


class Username(Resource):
    @swagger_decorator(
        path_schema=UsernamePathSchema, response_schema={200: UserDetailResponseSchema}
    )
    def get(self, username):
        """
        This examples uses FlaskRESTful Resource    # 这里是简介
        It works also with swag_from, schemas and spec_dict  # 这里是详情
        """

        # 获取校验后的数据
        logger.info(type(request.path_schema), request.path_schema)
        return {"username": username}, 200

    @swagger_decorator(
        path_schema=UsernamePathSchema,
        form_schema=UpdateUserSchema,
        response_schema={200: UserDetailResponseSchema},
    )
    def put(self, username):
        """
        更新用户信息
        """
        return {"username": username}, 200


api.add_resource(Username, "/username/<username>")
api.add_resource(User, "/users")

app.run(debug=True)
