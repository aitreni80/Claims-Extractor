import streamlit as st
import fitz  # PyMuPDF

def extract_claims_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    lower_text = full_text.lower()

    # Try several known phrases that mark the true start of the claims section
    for marker in ["what is claimed is:", "we claim:", "i claim:", "\nclaims\n"]:
        index = lower_text.find(marker)
        if index != -1:
            full_text = full_text[index + len(marker):]
            break
    else:
        return "Could not reliably find start of claims section."

    # Now parse the claims themselves from this point onward
    lines = full_text.splitlines()
    claims = []
    current_claim = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect start of a new claim: starts with number and optional ". " or " "
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
