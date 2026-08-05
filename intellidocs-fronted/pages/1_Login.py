import streamlit as st
from services.api_service import login


# If already logged in
if st.session_state.get("logged_in", False):
    st.switch_page("pages/3_Chat.py")


st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)

st.title("🔐 Login")

st.write("Please login to continue.")

with st.form("login_form"):

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    submit = st.form_submit_button("Login")


if submit:

    if email == "" or password == "":

        st.warning("Please enter Email and Password.")

    else:

        response = login(email, password)

        if response["success"]:

            st.session_state["logged_in"] = True

            st.session_state["user"] = response["user"]

            st.success(response["message"])

            st.switch_page("pages/3_Chat.py")

        else:

            st.error(response["message"])