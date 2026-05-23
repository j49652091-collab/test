from deepface import DeepFace
import numpy as np


def compare_faces(img1, img2):

    try:

        result = DeepFace.verify(
            img1_path=img1,
            img2_path=img2,
            model_name="Facenet",
            enforce_detection=False
        )

        similarity = round(
            (1 - result["distance"]) * 100,
            2
        )

        status = "Match Found" if result["verified"] else "No Match"

        return {
            "similarity": max(0, similarity),
            "status": status
        }

    except:

        return {
            "similarity": 0,
            "status": "Face Detection Failed"
        }
