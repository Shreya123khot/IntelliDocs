import streamlit as st

from services.api_service import (
    start_chat,
    get_chat_list,
    get_chat_messages,
    ask_question
)


# --------------------------------------------------
# Login Check
# --------------------------------------------------

if not st.session_state.get("logged_in"):

    st.warning("Please login first.")

    st.switch_page("pages/1_Login.py")


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

user = st.session_state["user"]


# --------------------------------------------------
# Session Variables
# --------------------------------------------------

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = ""


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("💬 Chats")

    # -----------------------------
    # New Chat
    # -----------------------------

    with st.expander("➕ New Chat", expanded=False):

        title = st.text_input("Chat Title")

        if st.button("Start Chat", use_container_width=True):

            if title.strip() == "":

                st.warning("Enter chat title.")

            else:

                response = start_chat(
                    user["id"],
                    title
                )

                if response["success"]:

                    st.session_state.chat_id = response["chatid"]
                    st.session_state.chat_title = response["title"]
                    st.session_state.messages = []

                    st.rerun()

                else:

                    st.error(response["message"])

    st.divider()

    # -----------------------------
    # Chat List
    # -----------------------------

    response = get_chat_list(user["id"])

    if response["success"]:

        chats = response["chats"]

        for chat in chats:

            if st.button(
                chat["title"],
                key=f"chat_{chat['id']}",
                use_container_width=True
            ):

                msg_response = get_chat_messages(chat["id"])

                if msg_response["success"]:

                    st.session_state.chat_id = chat["id"]
                    st.session_state.chat_title = chat["title"]
                    st.session_state.messages = msg_response["messages"]

                    st.rerun()

    st.divider()

    if st.button("Logout", use_container_width=True):

        st.session_state.clear()

        st.switch_page("pages/1_Login.py")


# --------------------------------------------------
# Main Page
# --------------------------------------------------

st.title("🤖 Enterprise Knowledge Assistant")

st.write(f"Welcome **{user['name']}**")

if st.session_state.chat_title != "":

    st.subheader(st.session_state.chat_title)

st.divider()


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["message_by"]):

        st.markdown(message["message"])


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

if st.session_state.chat_id is None:

    st.info("Create a new chat or select an existing chat.")

    st.stop()


question = st.chat_input("Ask a question...")


if question:

    # Display user message

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append({

        "role": "user",

        "content": question

    })

    # Ask backend

    with st.spinner("Thinking..."):

        response = ask_question(

            chatid=st.session_state.chat_id,

            userid=user["id"],

            question=question

        )

    if response["success"]:

        answer = response["answer"]

    else:

        answer = response["message"]

    with st.chat_message("assistant"):

        st.markdown(answer)

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })