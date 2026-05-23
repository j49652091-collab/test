from PIL import Image
import numpy as np
import cv2
from skimage.feature import local_binary_pattern


# ----------------------------
# Image preprocessing
# ----------------------------
def preprocess(image):

    img = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    gray = cv2.resize(gray, (256, 256))

    return img, gray


# ----------------------------
# Texture feature (real skin vs anime)
# ----------------------------
def texture_score(gray):

    lbp = local_binary_pattern(
        gray,
        P=24,
        R=3,
        method="uniform"
    )

    hist, _ = np.histogram(
        lbp.ravel(),
        bins=30,
        range=(0, 30)
    )

    hist = hist.astype("float")

    hist = hist / (hist.sum() + 1e-7)

    return np.var(hist)


# ----------------------------
# Edge detection (anime has strong edges)
# ----------------------------
def edge_score(gray):

    edges = cv2.Canny(gray, 100, 200)

    return np.mean(edges)


# ----------------------------
# FINAL DETECTION
# ----------------------------
def detect_image(uploaded_image):

    image = Image.open(uploaded_image)

    img, gray = preprocess(image)

    tex = texture_score(gray)

    edge = edge_score(gray)

    # ----------------------------
    # Decision logic
    # ----------------------------
    score = (
        (1 - min(tex * 120, 1)) * 50 +
        (1 - min(edge / 80, 1)) * 50
    )

    score = round(score, 2)

    # ----------------------------
    # Classification rules
    # ----------------------------
    if edge > 25 and tex < 0.01:
        status = "Anime / Cartoon (AI Generated Style)"

    elif score >= 65:
        status = "Real Human"

    else:
        status = "AI / Edited Image"

    # ----------------------------
    # Digital signature
    # ----------------------------
    signature = f"SIG-{int(tex*100000)}-{int(edge*100)}"

    return status, score, signature, image
