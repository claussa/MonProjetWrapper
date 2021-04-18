import logging
from typing import List, Optional

import requests
from requests import Response

from schemas.camps_de_ma_structure import CampDeMaStructureSchema, CampDeMaStructure
from schemas.general_camp import GeneralCampSchema, GeneralCamp


class MonProjetApi:
    def __init__(self, token: str):
        self._token = token

    def les_camps_de_ma_structure(self) -> List[CampDeMaStructure]:
        url = "https://monprojet.sgdf.fr/api/camps?type-rattachement=indirect"
        response = self._make_api_call(url)
        if response.ok:
            schema = CampDeMaStructureSchema()
            camps = []
            for data in response.json():
                camps.append(
                    schema.load(data)
                )
            return camps
        else:
            return []

    def general_camp(self, id: int) -> Optional[GeneralCamp]:
        url = f"https://monprojet.sgdf.fr/api/camps/{id}?module=ENTETE"
        response = self._make_api_call(url)
        if response.ok:
            schema = GeneralCampSchema()
            return schema.load(
                response.json()
            )
        else:
            logging.error(f"Cannot load camp detail for id {id}, "
                          f"server respond with status code {response.status_code}")
            return None

    def _make_api_call(self, url: str) -> Response:
        headers_auth = {
            'Authorization': 'Bearer ' + self._token,
        }
        response = requests.get(url, headers=headers_auth)
        return response
