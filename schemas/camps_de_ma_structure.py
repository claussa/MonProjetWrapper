from datetime import datetime
from typing import List

import attr
from marshmallow import fields, post_load, Schema, EXCLUDE


@attr.s(auto_attribs=True)
class TypeCamp:
    code: str


class TypeCampSchema(Schema):
    code = fields.String(required=True)

    @post_load
    def _make_model(self, data, **kwargs):
        return TypeCamp(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class CampStructure:
    id: int
    organisatrice: bool
    participante: bool
    code: str
    libelle: str


class CampStructureSchema(Schema):
    id = fields.Integer(required=True)
    organisatrice = fields.Bool(required=True)
    participante = fields.Bool(required=True)
    structure = fields.Dict(required=True)

    @post_load
    def _make_model(self, data, **kwargs):
        structure = data["structure"]
        del data["structure"]
        data["code"] = structure.get("code")
        data["libelle"] = structure.get("libelle")
        return CampStructure(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class CampDeMaStructure:
    id: int
    statut: int
    libelle: str
    typeCamp: TypeCamp
    dateDebut: datetime
    dateFin: datetime
    campStructures: List[CampStructure]


class CampDeMaStructureSchema(Schema):
    id = fields.Integer(required=True)
    statut = fields.Integer(required=True)
    libelle = fields.String(required=True)
    typeCamp = fields.Nested(nested=TypeCampSchema, required=True)
    dateDebut = fields.DateTime(required=True)
    dateFin = fields.DateTime(required=True)
    campStructures = fields.Nested(nested=CampStructureSchema, many=True)

    @post_load
    def _make_model(self, data, **kwargs):
        return CampDeMaStructure(**data)

    class Meta:
        unknown = EXCLUDE
