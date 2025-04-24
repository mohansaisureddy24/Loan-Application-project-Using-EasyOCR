import streamlit as st
import easyocr
from PIL import Image
import re
import tempfile

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to extract text using EasyOCR
def extract_text(image):
    result = reader.readtext(image)
    full_text = " ".join([item[1] for item in result])
    return full_text

# Function to extract key fields using regex or keyword matching
def extract_fields(text):
    name_match = re.search(r'Name[:\-]?\s*([A-Za-z\s]+)', text)
    address_match = re.search(r'Address[:\-]?\s*([\w\s,.-]+)', text)
    income_match = re.search(r'Income[:\-]?\s*([\d,]+)', text)
    loan_amount_match = re.search(r'Loan Amount[:\-]?\s*([\d,]+)', text)

    return {
        "Name": name_match.group(1).strip() if name_match else "",
        "Address": address_match.group(1).strip() if address_match else "",
        "Income": income_match.group(1).strip() if income_match else "",
        "Loan Amount": loan_amount_match.group(1).strip() if loan_amount_match else ""
    }

# Streamlit UI
st.set_page_config(page_title="Loan Document OCR", layout="centered")
st.title("📄 Automated Personal Loan Document Processing")

uploaded_file = st.file_uploader("Upload a scanned loan document", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)

    # Save uploaded image to a temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_path = tmp_file.name

    # Extract text
    with st.spinner("Running OCR..."):
        extracted_text = extract_text(temp_path)
        fields = extract_fields(extracted_text)

    st.subheader("📝 Extracted Information (Editable)")

    # Editable form for review
    with st.form("form_review"):
        name = st.text_input("Applicant Name", fields["Name"])
        address = st.text_area("Address", fields["Address"])
        income = st.text_input("Income", fields["Income"])
        loan_amount = st.text_input("Loan Amount", fields["Loan Amount"])

        submitted = st.form_submit_button("Submit Application")

        if submitted:
            st.success("✅ Application Submitted Successfully!")
            st.json({
                "Name": name,
                "Address": address,
                "Income": income,
                "Loan Amount": loan_amount
            })

    st.subheader("📃 Raw OCR Output")
    st.text_area("OCR Text", extracted_text, height=250)
