import streamlit as st
from byaldi import RAGMultiModalModel
import os
from pathlib import Path
from ollama import chat
from ollama import ChatResponse
import base64

# Cache model loading
@st.cache_resource
def load_model():
    return RAGMultiModalModel.from_pretrained('vidore/colpali-v1.2', verbose=0)

# Initialize session state for PDF processing
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
    st.session_state.pdf_name = None  # Track the last processed PDF

st.set_page_config(layout="wide")
st.title("PDF MultiRAG App")
model0 = load_model()

with st.sidebar:
    uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])
    st.info("This app will create screenshots of PDF pages and index them for multi-modal search.")

    os.makedirs("uploaded_docs", exist_ok=True)

    # Process the PDF only if it has changed
    if uploaded_file is not None:
        if not st.session_state.pdf_processed or uploaded_file.name != st.session_state.pdf_name:
            st.write(f"Processing PDF: {uploaded_file.name}")
            
            try:
                file_path = os.path.join("uploaded_docs", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.info("PDF saved successfully. Creating and indexing page screenshots...")

                with st.spinner('Processing PDF pages...'):
                    model0.index(
                        input_path=Path("uploaded_docs"),
                        index_name="colpali",  # Fixed index name
                        store_collection_with_index=True,
                        overwrite=True  # Ensure it gets updated if a new PDF is uploaded
                    )

                    # Store processing state
                    st.session_state.pdf_processed = True
                    st.session_state.pdf_name = uploaded_file.name  # Save processed PDF name

                st.success("PDF has been successfully processed and indexed!")

            except Exception as e:
                st.error(f"Error during processing: {str(e)}")

            finally:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    st.warning(f"Could not remove temporary file: {str(e)}")

# Text input and chat button
user_input = st.text_input("Enter your message:", "")

if st.button("Chat"):
    if user_input.strip():
        if not st.session_state.pdf_processed:
            st.warning("Please upload and process a PDF first.")
        else:
            results = model0.search(user_input, k=1)  # Fixed index name
            if results:
                image_data = base64.b64decode(results[0].base64)
                with open("decoded_image.png", "wb") as image_file:
                    image_file.write(image_data)

                response: ChatResponse = chat(model='llama3.2-vision', messages=[
                    {
                        'role': 'user',
                        'content': user_input,
                        'images': ['decoded_image.png']
                    }
                ])
               
                st.write("**Ollama:**", response['message']['content'])
            else:
                st.warning("No relevant information found in the indexed PDF.")
    else:
        st.warning("Please enter a message before clicking the button.")
