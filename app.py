import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


st.markdown("""
    <style>

        
        h1 {
            background: linear-gradient(90deg, #8a2be2, #da70d6); /* Button-like gradient */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* BUTTON NORMAL */
        div.stButton > button {
            background: linear-gradient(90deg, #8a2be2, #da70d6);
            color: white;
            padding: 8px 20px;
            border-radius: 10px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s ease;
        }

        /* BUTTON HOVER */
        div.stButton > button:hover {
            background: linear-gradient(90deg, #7a1fd1, #c45ed6);
            transform: scale(1.02);
        }

    </style>
""", unsafe_allow_html=True)



def get_gemini_response(input_prompt, image_parts):
    model = genai.GenerativeModel("models/gemini-2.5-flash-image")
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



st.set_page_config(page_title="Gemini Health App")


st.header("Gemini Health App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("Analyze Calories ")

input_prompt = """
You are an expert nutritionist. 
Identify the food items in the image and calculate the calories.

Provide output in this format:

1. Item 1 - calories
2. Item 2 - calories
---
Total calories: ____
Is this healthy? Yes/No (and explain why)
"""

if submit:
    if uploaded_file is None:
        st.error("Please upload an image before asking!")
    else:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("The Response is:")
        st.write(response)
