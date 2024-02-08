from dataclasses import dataclass
from io import BytesIO
import base64

import streamlit as st
from PIL import Image

from dotenv import load_dotenv
import google.generativeai as genai

import os


load_dotenv()

@dataclass
class Message:
    actor: str
    payload: str
    image: bool = False

def load_api_key():
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GENAI_API_KEY"]
        except KeyError:
            api_key = st.text_input("Enter Gemini API Key")
            if not api_key:
                st.error("Please set the GENAI_API_KEY environment variable.")
                st.stop()
    return api_key

api_key = load_api_key()
genai.configure(api_key=api_key)

def process_uploaded_image(img_file_buffer):
    img_pil = Image.open(img_file_buffer)
    img_io = BytesIO()
    img_pil.save(img_io, format="JPEG")
    img_bytes = img_io.getvalue()

    # Encode image bytes to base64
    encoded_img = base64.b64encode(img_bytes).decode("utf-8")

    # Set up image parts for the model
    return [{"mime_type": "image/jpeg", "data": encoded_img}], encoded_img

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
st.title("Gemini Pro AI")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Create text chat model
text_model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Create image chat model
vision_model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

container = st.container(border=True)

if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi! How can I help you?")]
    container.chat_message(ASSISTANT).write("Hi! How can I help you?")



welcome_text = "Hello! 😊"
user_input = st.text_input("You:", value=welcome_text, key="placeholder")
send_button = st.button("Send", key="SendButton")
img_file_buffer = st.file_uploader("Choose a file", type=["jpg", "jpeg"])

def update_msgs():
    for msg in st.session_state[MESSAGES]:
        if msg.image == True:
            container._html(msg.payload, width=218)
        else:
            container.chat_message(msg.actor).write(msg.payload)

if send_button:
    if img_file_buffer is not None:
        image_parts, base64Data = process_uploaded_image(img_file_buffer)
        st.session_state[MESSAGES].append(Message(actor=USER, payload=user_input))
        st.session_state[MESSAGES].append(Message(actor=USER, payload=f"<img src='data:image/jpeg;base64,{base64Data}' width='200' height='130'/>", image=True))

        with st.spinner("Thinking..."):
            prompt_parts = [user_input, image_parts[0]]
            response = vision_model.generate_content(prompt_parts)
            st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response.text))
            update_msgs()
            img_file_buffer.flush()
    else:
        st.session_state[MESSAGES].append(Message(actor=USER, payload=user_input))
        with st.spinner("Thinking..."):
            convo_text = text_model.start_chat(history=[])
            convo_text.send_message(user_input)
            response = convo_text.last.text
            st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
            update_msgs()

