import json

from flask import Flask
from flask_apispec import use_kwargs, marshal_with, doc

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, String

from marshmallow import Schema
from webargs import fields

from flask import make_response
from flask_apispec.views import MethodResource

from flask_restful import Api

app = Flask(__name__)
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="pets",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="3.0.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",
    }
)
api = Api(app)
docs = FlaskApiSpec(app)


class Pet(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    category = Column(String(80))
    size = Column(Integer)

    def toJson(self):
        return json.dump(
            {"name": self.name, "category": self.category, "size": self.size}
        )


class PetSchema(Schema):
    id = 1
    name = "hello"
    category = "hey"
    size = 10


@app.route("/pets")
@marshal_with(PetSchema(many=False))
def get_pets(**kwargs):
    return {"name": "hey", "category": "a", "size": 15}


@doc(description="a pet store", tags=["pets"])
class PetResource(MethodResource):
    @marshal_with(PetSchema)
    def get(self, pet_id):
        return Pet.query.filter(Pet.id == pet_id).one()

    @use_kwargs(PetSchema)
    @marshal_with(PetSchema, code=201)
    def post(self, **kwargs):
        return Pet(**kwargs)

    @use_kwargs(PetSchema)
    @marshal_with(PetSchema)
    def put(self, pet_id, **kwargs):
        pet = Pet.query.filter(Pet.id == pet_id).one()
        pet.__dict__.update(**kwargs)
        return pet

    @marshal_with(None, code=204)
    def delete(self, pet_id):
        pet = Pet.query.filter(Pet.id == pet_id).one()
        pet.delete()
        return make_response("", 204)


api.add_resource(PetResource, "/pet-resource/<int:pet_id>")

docs.register(get_pets)
docs.register(PetResource)
app.run(debug=True)
