import streamlit as st
import tempfile

from login import login
from detector import detect_image
from face_recognition import compare_faces


st.set_page_config(
    page_title="AI Forensic System",
    layout="wide"
)

# ----------------------------
# STYLE
# ----------------------------
with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("🧬 AI Deepfake & Face Forensics System")

# ----------------------------
# LOGIN STATE
# ----------------------------
if "logged" not in st.session_state:
    st.session_state.logged = False

# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.logged:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login(username, password):
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Wrong Credentials")

# ----------------------------
# MAIN APP
# ----------------------------
else:

    tab1, tab2 = st.tabs([
        "🧬 Detection",
        "👤 Face Match"
    ])

    # =========================
    # TAB 1 - DETECTION
    # =========================
    with tab1:

        img = st.file_uploader("Upload Image")

        if img:

            result = detect_image(img)
            print("The function output is:", result)

            col1, col2 = st.columns(2)

            with col1:
                st.image(img, caption="Uploaded Image")

            with col2:
                st.write("Result:", result)

                # st.metric(
                #     "Confidence Score",
                #     str(score) + "%"
                # )

                # st.subheader("Digital Signature")
                # st.code(signature)


    # =========================
    # TAB 2 - FACE MATCH
    # =========================
    with tab2:

        col1, col2 = st.columns(2)

        img1 = col1.file_uploader("First Image")
        img2 = col2.file_uploader("Second Image")

        if img1 and img2:

            col1.image(img1, caption="Image 1")
            col2.image(img2, caption="Image 2")

            def save(file):
                t = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                t.write(file.read())
                t.close()
                return t.name

            path1 = save(img1)
            path2 = save(img2)

            result_match = compare_faces(path1, path2)

            st.metric(
                "Similarity",
                str(result_match["similarity"]) + "%"
            )

            st.success(result_match["status"])
