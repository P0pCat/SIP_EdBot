import openai
import streamlit as st
import time

assistant_id = "asst_9RaySopKchAbeky2SwUCHqE4"

client = openai
    
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="CatGPT", page_icon=":speech_balloon:")

openai.api_key = "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"

st.markdown(
    """
    <style>
        div.stTitle {
            text-align: center;
        }
        div.stMarkdown {
            text-align: center;
        }
        .eye-catching-title {
            color: #FF5733;
            font-size: 4em;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Eye-catching title
st.markdown("<h1 class='eye-catching-title'>EdBot👨‍💻</h1>", unsafe_allow_html=True)

# Text
st.write("_Your Personal Calculus Tutor_")

st.markdown(
    """
    <style>
        div.stButton > button {
            width: 100%;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Button 1
if st.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# Button 2
if st.button("_Reset_"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask EdBot..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are an expert in calculus, you focuses on the topic Derive trigonometric identities, Solving problems involving trigonometric identities, Converting degree measure to radian measure and vice versa, Determining whether an equation is an identity or conditional equation. You act like socrates and response as socrates. You teach using socratic method. you do not give the exact answer until the user get the correct answer. you response based on the users question and use secratic method with it. you keep the response as short as possible."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")