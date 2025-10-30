from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

# ✅ Function to process image into bytes
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# ✅ Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# ✅ Streamlit UI
st.set_page_config(page_title="🧾 Multi-Language Invoice Extractor", layout="centered")
st.title("🌍 Multi-Language Invoice Extractor")
st.caption("Extract information from invoices using **Gemini Pro Vision** and **LangChain**")

# Text input for user
input_text = st.text_input("✍️ Enter your input text (e.g., 'Extract total amount and date')", "")

# Optional prompt (extra instruction)
prompt = st.text_area("💡 Add an optional custom prompt", "Extract all important details from the invoice in English.")

# File uploader
uploaded_file = st.file_uploader("📤 Upload an invoice image", type=["jpg", "jpeg", "png"])

# Display and process image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 Uploaded Invoice", use_container_width=True)

    # Convert to bytes for Gemini
    image_parts = input_image_setup(uploaded_file)

    if st.button("🚀 Extract Information"):
        with st.spinner("Analyzing invoice... 🔍"):
            try:
                response = get_gemini_response(input_text, image_parts, prompt)
                st.success("✅ Extraction Successful!")
                st.subheader("🔍 Extracted Information:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

else:
    st.info("Please upload an invoice image to get started.")
