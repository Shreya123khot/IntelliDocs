import streamlit as st

from services.api_service import upload_document


# ----------------------------------
# Login Check
# ----------------------------------

if not st.session_state.get("logged_in"):

    st.warning("Please login first.")

    st.switch_page("pages/1_Login.py")

# -----------------------------
# Authorization Check
# -----------------------------
user = st.session_state["user"]

if user["usertype"] != "admin":

    st.error("You are not authorized to access this page.")

    st.stop()

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Documents",
    page_icon="📄",
    layout="wide"
)


# ----------------------------------
# Title
# ----------------------------------

st.title("📄 Upload Documents")

st.write("Upload PDF or TXT documents to the Knowledge Base.")

st.divider()


# ----------------------------------
# Upload Form
# ----------------------------------

with st.form("upload_form"):

    title = st.text_input("Document Title")

    document_type = st.selectbox(
        "Document Type",
        [
            "pdf",
            "txt"
        ]
    )

    uploaded_file = st.file_uploader(
        "Choose Document",
        type=["pdf", "txt"]
    )

    submit = st.form_submit_button("Upload Document")


# ----------------------------------
# Upload Action
# ----------------------------------

if submit:

    if title == "":

        st.warning("Please enter document title.")

    elif uploaded_file is None:

        st.warning("Please choose a document.")

    else:

        with st.spinner("Uploading document..."):

            response = upload_document(
                title,
                document_type,
                uploaded_file
            )

        if response["success"]:

            st.success(response["message"])

        else:

            st.error(response["message"])