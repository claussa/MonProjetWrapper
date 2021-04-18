from typing import List

import attr
from marshmallow import Schema, fields, EXCLUDE, post_load


@attr.s(auto_attribs=True)
class Camp817Infos:
    previsionNbreParticipants: int
    previsionNbreAnimateurs: int


class Camp817InfosSchema(Schema):
    previsionNbreParticipants = fields.Integer(required=True)
    previsionNbreAnimateurs = fields.Integer(required=True)

    @post_load
    def _make_model(self, data, **kwargs):
        return Camp817Infos(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class Message:
    message: str
    level: str


class MessageSchema(Schema):
    message = fields.String(required=True)
    level = fields.String(required=True)

    @post_load
    def _make_model(self, data, **kwargs):
        return Message(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class Commune:
    libelle: str
    codePostale: str


class CommuneSchema(Schema):
    libelle = fields.String(required=True, allow_none=True)
    codePostale = fields.String(required=True, allow_none=True)

    @post_load
    def _make_model(self, data, **kwargs):
        return Commune(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class Lieu:
    adresseLigne1: str
    libelle: str
    tamRefCommune: Commune


class LieuSchema(Schema):
    adresseLigne1 = fields.String(required=True, allow_none=True)
    libelle = fields.String(required=True, allow_none=True)
    tamRefCommune = fields.Nested(nested=CommuneSchema, allow_none=True)

    @post_load
    def _make_model(self, data, **kwargs):
        return Lieu(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class CampAdherentStaff:
    id: int
    roleStaff: str
    nom: str
    prenom: str


class CampAdherentStaffSchema(Schema):
    id = fields.Integer(required=True)
    roleStaff = fields.String(required=True)
    adherent = fields.Dict()

    @post_load
    def _make_model(self, data, **kwargs):
        adherent = data["adherent"]
        del data["adherent"]
        data["nom"] = adherent.get("nom")
        data["prenom"] = adherent.get("prenom")
        return CampAdherentStaff(**data)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True)
class GeneralCamp:
    id: int = None
    camp817: Camp817Infos = None
    campAlertMessages: List[Message] = []
    campLieuPrincipal: Lieu = None
    campAdherentStaffs: List[CampAdherentStaff] = []


class GeneralCampSchema(Schema):
    id = fields.Integer(required=True)
    camp817 = fields.Nested(nested=Camp817InfosSchema, allow_none=True)
    _campAlertMessages = fields.Nested(nested=MessageSchema, many=True)
    campLieuPrincipal = fields.Nested(nested=LieuSchema, allow_none=True)
    campAdherentStaffs = fields.Nested(nested=CampAdherentStaffSchema, many=True)

    @post_load
    def _make_model(self, data, **kwargs):
        data["campAlertMessages"] = data["_campAlertMessages"]
        del data["_campAlertMessages"]
        return GeneralCamp(**data)

    class Meta:
        unknown = EXCLUDE


