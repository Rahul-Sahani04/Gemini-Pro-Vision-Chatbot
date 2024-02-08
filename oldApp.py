from dataclasses import dataclass

@dataclass
class Message:
    actor: str
    payload: str



import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GENAI_API_KEY"]
    except KeyError:
        if not api_key:
            api_key = st.text_input("Enter Gemini API Key")
            if not api_key:
                st.error("Please set the GENAI_API_KEY environment variable.")
                st.stop()

genai.configure(api_key=api_key)

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

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
st.title("Gemini Pro AI")

# Start a chat with a greeting and initial information
convo_text = text_model.start_chat(history=[])



if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi!How can I help you?")]
    
with st.container():
    msg: Message
    for msg in st.session_state[MESSAGES]:
        st.chat_message(msg.actor).write(msg.payload)

welcome_text = "Hello! 😊"
# Display the model's response using Streamlit

user_input = st.text_input("You:", value=welcome_text, key="placeholder")

SendButton = st.button("Send", key="SendButton")

img_file_buffer = st.file_uploader("Choose a file", type=["jpg", "jpeg"])



# Check if an image has been uploaded
if img_file_buffer is not None:
    # for i, img in enumerate(img_file_buffer):
    # Display the taken image
    # st.image(img_file_buffer, caption=f"Uploaded Image: {img_file_buffer.file_id}")

    # Convert the image to bytes
    img_pil = Image.open(img_file_buffer)
    img_io = BytesIO()
    img_pil.save(img_io, format="JPEG")
    img_bytes = img_io.getvalue()

    # Encode image bytes to base64
    encoded_img = base64.b64encode(img_bytes).decode("utf-8")

    # Set up image parts for the model
    image_parts = [{"mime_type": "image/jpeg", "data": encoded_img}]


if SendButton and img_file_buffer is not None:
    st.session_state[MESSAGES].append(Message(actor=USER, payload=user_input))
    with st.spinner("Thinking..."):
        # Prompt for the model
        prompt_parts = [user_input, image_parts[0]]
        st.chat_message(USER).write(f"{user_input}")
        st.markdown(f"![Image](data:image/jpeg;base64,{image_parts[0]['data']})")

        # Generate content using the image model
        response = vision_model.generate_content(prompt_parts)
        convo_text.history.append(response.text)

        # Display the model's response
        # st.write(response.text)
        st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response.text))
        st.chat_message(ASSISTANT).write(response.text)

elif SendButton:
    st.session_state[MESSAGES].append(Message(actor=USER, payload=user_input))
    st.chat_message(USER).write(user_input)
    with st.spinner("Thinking..."):
        convo_text.send_message(user_input)
        # st.caption("Bot's Response:")
        # st.write(convo_text.last.text)
        st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=convo_text.last.text))
        st.chat_message(ASSISTANT).write(convo_text.last.text)
