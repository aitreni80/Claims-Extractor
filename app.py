>>> import streamlit as st
... import fitz  # PyMuPDF
... import re
... 
... def extract_claims_from_text(text):
...     # Normalize and clean up text
...     text = text.replace('\n', ' ').replace('\r', ' ')
...     
...     # Simple regex to split claims assuming they are numbered (e.g., 1., 2., etc.)
...     claims = re.split(r'(?<=\.)\s*(\d+)\.\s+', text)
...     
...     # Remove unwanted preamble and recombine numbers with content
...     structured_claims = []
...     for i in range(2, len(claims), 2):
...         number = claims[i - 1]
...         content = claims[i].strip()
...         if content:
...             structured_claims.append((number, content))
...     return structured_claims
... 
... def extract_text_from_pdf(uploaded_file):
...     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
...     full_text = ""
...     for page in doc:
...         full_text += page.get_text()
...     return full_text
... 
... st.set_page_config(page_title="Claims Extractor", layout="wide")
... 
... st.title("📄 Patent Claims Extractor")
... uploaded_pdf = st.file_uploader("Upload a claims PDF file", type=["pdf"])
... 
... if uploaded_pdf:
...     with st.spinner("Extracting text from PDF..."):
...         text = extract_text_from_pdf(uploaded_pdf)
...         claims = extract_claims_from_text(text)
... 
...     if claims:
...         st.success(f"{len(claims)} claims extracted.")
...         for number, content in claims:
...             st.markdown(f"**Claim {number}:**")
...             st.markdown(f"> {content}")
...     else:
...         st.warning("No claims found. Please make sure the PDF contains clearly numbered claims.")
