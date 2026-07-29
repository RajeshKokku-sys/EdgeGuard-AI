import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from config.settings import Settings


class FaceMatcher:

    def __init__(self, db):

        self.db = db

    def identify(self, embedding):

        employees = self.db.get_employee_embeddings()

        if len(employees) == 0:
            return {
                "authorized": False,
                "employee_id": None,
                "name": "Unknown",
                "department": None,
                "designation": None,
                "score": 0.0
            }

        best_employee = None
        best_score = -1

        for emp in employees:

            score = cosine_similarity(

                [embedding],

                [emp["embedding"]]

            )[0][0]

            if score > best_score:

                best_score = score

                best_employee = emp

        if (
            best_score >=
            Settings.FACE_MATCH_THRESHOLD
        ):

            return {

                "authorized": True,

                "employee_id":
                    best_employee["employee_id"],

                "name":
                    best_employee["name"],

                "department":
                    best_employee["department"],

                "designation":
                    best_employee["designation"],

                "score":
                    float(best_score)

            }

        return {

            "authorized": False,

            "employee_id": None,

            "name": "Unknown",

            "department": None,

            "designation": None,

            "score": float(best_score)

        }