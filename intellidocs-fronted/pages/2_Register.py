import streamlit as st
from services.api_service import register


st.set_page_config(
    page_title="Register",
    page_icon="📝"
)

st.title("📝 User Registration")

st.write("Create a new account.")

with st.form("register_form"):

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    submit = st.form_submit_button("Register")


if submit:

    if not name or not email or not password or not confirm_password:

        st.warning("Please fill all fields.")

    elif password != confirm_password:

        st.error("Passwords do not match.")

    else:

        response = register(
            name,
            email,
            password
        )

        if response["success"]:

            st.success(response["message"])

            st.info("Please login using your credentials.")

        else:

            st.error(response["message"])