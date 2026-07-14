import streamlit as st
import requests

# Configure the browser tab and page layout
st.set_page_config(page_title="AI OCR App", layout="centered")

# Add a massive title to the top of the webpage
st.title("📄 AI Optical Character Recognition")

# A subtitle to explain what the app does
st.markdown("Upload an image (PNG, JPG) and our API will extract the text for you.")

# Create a drag-and-drop file uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 1. Show the image on the screen
    st.image(uploaded_file, caption="Your Uploaded Image", use_container_width=True)
    
    # 2. Add a button. When clicked, it connects to the backend!
    if st.button("Extract Text 🚀"):
        
        # Show a loading spinner while we wait for the backend
        with st.spinner("Talking to the backend API..."):
            
            # 3. Connect to FastAPI! We package the file exactly how FastAPI expects it
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            # We hit our LOCAL backend URL
            response = requests.post("http://localhost:8000/api/extract-text", files=files)
            
            # 4. Show the results on the screen
            if response.status_code == 200:
                result_data = response.json()
                st.success("Extraction Complete!")
                st.text_area("Extracted Text", result_data["extracted_text"], height=250)
            else:
                st.error("Backend Error! Is Uvicorn running?")
