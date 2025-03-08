# Multi-Modal RAG App

## Overview
The **Multi-Modal RAG App** is a **Streamlit-based** application that processes PDF documents using a **Retrieval-Augmented Generation (RAG) Multi-Modal Model**. The app indexes PDF content and enables users to query the document with text-based questions while utilizing **Ollama's vision-enabled chat model** for enhanced responses.

## Features
- **PDF Upload & Processing:** Converts PDF pages into indexed screenshots for retrieval.
- **Multi-Modal Search:** Uses **Byaldi's RAGMultiModalModel** for document-based information retrieval.
- **Chat Integration:** Queries the indexed content using **Ollama's vision model (Llama3.2-Vision)**.
- **Interactive UI:** Built with **Streamlit** for seamless user experience.

## Installation
### Prerequisites
Ensure you have ollama installed in your local machine 

```bash
pip install streamlit byaldi ollama
```

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/Wailsafi/multimodel_rag_app.git
   cd multimodel_rag_app
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open the app in your browser at:
   ```
   http://localhost:8501/
   ```

## Usage
1. **Upload a PDF:** Use the sidebar to upload a document.
2. **Processing:** The app will extract and index page screenshots.
3. **Query the Document:** Enter a text prompt and retrieve relevant information.
4. **Chat with the AI:** The system generates responses based on retrieved images and text.

## Project Structure
```
multimodel_rag_app/
│-- app.py                # Main Streamlit application
│-- uploaded_docs/        # Directory for uploaded PDFs
│-- requirements.txt      # Dependencies
│-- README.md             # Documentation
```



