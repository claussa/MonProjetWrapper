import logging
from typing import Optional, Dict

from progress.bar import Bar
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from mon_projet_api import MonProjetApi
from schemas.camps_de_ma_structure import CampDeMaStructure
from schemas.general_camp import GeneralCamp


class XLSWriter:
    HEADERS = [
        "Tranche d'âge",  # 0
        "Unité",  # 1
        "Libellé du camp",  # 2
        "Date de début",  # 3
        "Date de fin",  # 4
        "Lieu",  # 5
        "Nombre de jeunes",  # 6
        "Nombre de chefs",  # 7
        "Directeur",  # 8
        "Alertes",  # 9
        "Warning",  # 10
        "État de récupération des infos"  # 11
    ]

    def __init__(self, filename: str, groups: Dict[int, str], api: MonProjetApi):
        self._filename = filename
        self._groups = groups
        self._api = api
        self._workbook: Optional[Workbook] = None
        self._worksheets: Dict[int, Worksheet] = {}
        self._worksheets_lines: Dict[int, int] = {}
        self._date_format = None

    def create(self):
        self._workbook = Workbook(self._filename, {'remove_timezone': True})
        self._date_format = self._workbook.add_format({'num_format': 'dd/mm/yy'})
        for group_id, group_name in self._groups.items():
            worksheet = self._workbook.add_worksheet(group_name)
            self._write_headers(worksheet)
            self._worksheets[group_id] = worksheet
            self._worksheets_lines[group_id] = 1

    def close(self):
        self._workbook.close()

    def _write_headers(self, worksheet: Worksheet):
        bold = self._workbook.add_format({'bold': True})
        for i in range(len(self.HEADERS)):
            worksheet.write(0, i, self.HEADERS[i], bold)

    def write(self):
        logging.info("Récupération des camps de ma structure")
        camps = self._api.les_camps_de_ma_structure()
        logging.info("Récupération des camps de ma structure terminé")
        bar = Bar('Processing', max=len(camps))
        for i in range(len(camps)):
            self._write_camp(
                camps[i]
            )
            bar.next()
        bar.finish()

    def _write_camp(self, camp: CampDeMaStructure):
        if camp.statut != 1:
            return
        structure_du_territoire = None
        for structure in camp.campStructures:
            if int(structure.code[:-2]) in list(self._groups.keys()):
                structure_du_territoire = structure
                pass
        if structure_du_territoire is None:
            logging.warning(f"Aucune structure trouvé pour le camps d'id {camp.id}, de libellé {camp.libelle}")
            return
        detail = self._api.general_camp(camp.id)
        worksheet = self._worksheets[int(structure_du_territoire.code[:-2])]
        line = self._worksheets_lines[int(structure_du_territoire.code[:-2])]
        self._worksheets_lines[int(structure_du_territoire.code[:-2])] = line + 1
        worksheet.write(line, 0, camp.typeCamp.code)
        worksheet.write(line, 1, structure_du_territoire.libelle)
        worksheet.write(line, 2, camp.libelle)
        worksheet.write(line, 3, camp.dateDebut, self._date_format)
        worksheet.write(line, 4, camp.dateFin, self._date_format)

        worksheet.write(line, 11, "OK" if detail else "ERROR")

        if detail:
            self._write_camp_detail(detail, worksheet, line)

    @staticmethod
    def _write_camp_detail(detail: GeneralCamp, worksheet: Worksheet, line: int):
        if detail.campLieuPrincipal:
            worksheet.write(
                line,
                5,
                f"{detail.campLieuPrincipal.adresseLigne1}, "
                f"{detail.campLieuPrincipal.tamRefCommune.codePostale if detail.campLieuPrincipal.tamRefCommune else None} "
                f"{detail.campLieuPrincipal.tamRefCommune.libelle if detail.campLieuPrincipal.tamRefCommune else None}"
            )
        if detail.camp817:
            worksheet.write(line, 6, detail.camp817.previsionNbreParticipants)
            worksheet.write(line, 7, detail.camp817.previsionNbreAnimateurs)
        for adherent in detail.campAdherentStaffs:
            if adherent.roleStaff == "D":
                worksheet.write(
                    line,
                    8,
                    f"{adherent.prenom} {adherent.nom}"
                )
        worksheet.write(
            line,
            9,
            "\n".join(message.message for message in detail.campAlertMessages if message.level == "error")
        )
        worksheet.write(
            line,
            10,
            "\n".join(message.message for message in detail.campAlertMessages if message.level == "warn")
        )
