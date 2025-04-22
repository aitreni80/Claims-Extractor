import streamlit as st
import fitz  # PyMuPDF

def extract_claims_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    # Find the "claims" section (case-insensitive)
    lower_text = full_text.lower()
    claims_start = lower_text.find("claims")
    if claims_start == -1:
        return "Could not find 'Claims' section."

    claims_text = full_text[claims_start:]

    # Break text into lines and detect claims
    lines = claims_text.splitlines()
    claims = []
    current_claim = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Make sure line is long enough before checking characters
        if len(line) > 1 and line[0].isdigit() and (
            line[1:3] == ". " or line[1] == " " or line[1] == "."
        ):
            if current_claim:
                claims.append(current_claim.strip())
            current_claim = line
        else:
            current_claim += " " + line

    if current_claim:
        claims.append(current_claim.strip())

    return claims

st.title("Patent Claims Extractor (Part 1)")

uploaded_file = st.file_uploader("Upload Patent PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting claims..."):
        claims = extract_claims_from_pdf(uploaded_file)

        if isinstance(claims, str):
            st.error(claims)
        else:
            st.success(f"Extracted {len(claims)} claims.")
            for i, claim in enumerate(claims, 1):
                st.markdown(f"**Claim {i}:** {claim}")
