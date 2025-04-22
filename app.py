import streamlit as st
import fitz  # PyMuPDF

def extract_claims_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = "\n".join([page.get_text() for page in doc])

    # Detect start of the claims section
    claim_markers = ["what is claimed is:", "we claim:", "i claim:", "\nclaims\n", "\nclaims:"]
    lower_text = full_text.lower()

    for marker in claim_markers:
        index = lower_text.find(marker)
        if index != -1:
            full_text = full_text[index + len(marker):]
            break
    else:
        return []

    # Parse numbered claims (e.g., 1. xxx or 1 xxx)
    lines = full_text.splitlines()
    claims = []
    current_claim = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line[:2].isdigit() and (line[1:3] == ". " or line[1] == " " or line[1] == "."):
            if current_claim:
                claims.append(current_claim.strip())
            current_claim = line
        else:
            current_claim += " " + line

    if current_claim:
        claims.append(current_claim.strip())

    return claims


st.title("Patent Claims Extractor")

uploaded_file = st.file_uploader("Upload a patent PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting claims..."):
        claims = extract_claims_from_pdf(uploaded_file)

    if claims:
        st.subheader("Extracted Claims")
        for i, claim in enumerate(claims, 1):
            st.markdown(f"**Claim {i}:** {claim}")
    else:
        st.warning("No claims found. Please check if the document contains a recognizable claims section.")
