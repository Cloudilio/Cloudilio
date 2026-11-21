import random
import time

import streamlit as st

st.title("Chat interface")
st.write(
    "Chat apps take a few lines: `st.chat_input` for the box, `st.chat_message` for the "
    "bubbles, and `st.write_stream` to type out the reply. This bot is a simple keyword "
    "matcher; swap `reply_to` for a call to any AI model's API to build a real assistant."
)

ANSWERS = {
    "deploy": "Push your code to Cloudilio and it detects Streamlit from requirements.txt, "
              "builds a container and gives you an HTTPS address.",
    "chart": "Streamlit has built-in line, bar, area, scatter and map charts, and it can "
             "show Altair, Plotly, Matplotlib and pydeck figures too.",
    "state": "`st.session_state` is a dictionary that survives reruns, one per browser "
             "tab. This chat history lives there.",
    "cache": "`@st.cache_data` remembers a function's result for each input, so slow "
             "data loading only happens once.",
    "save": "Write files to the folder in the APP_DATA_DIR environment variable and "
            "Cloudilio keeps them across restarts. The Guestbook page does exactly that.",
}
FALLBACK = [
    "Good question! Try asking me about deploying, charts, state, caching or saving data.",
    "I'm a tiny demo bot. Ask about deploy, chart, state, cache or save.",
]


def reply_to(message: str):
    """Yields the answer a word at a time, so it streams like an AI model's reply."""
    text = next((answer for key, answer in ANSWERS.items() if key in message.lower()),
                random.choice(FALLBACK))
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me how to deploy, chart, cache or save data with Streamlit."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        answer = st.write_stream(reply_to(prompt))
    st.session_state.messages.append({"role": "assistant", "content": answer})

if len(st.session_state.messages) > 1 and st.button("Clear chat"):
    del st.session_state.messages
    st.rerun()
