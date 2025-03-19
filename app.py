import os
import streamlit as st
import spacy
import fitz  # PyMuPDF for PDF parsing
import docx
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np

# Ensure the 'uploads' folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load pre-trained BERT model for classification
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_sections(text):
    """Extracts key sections like skills, experience, and education."""
    doc = nlp(text)
    skills, experience, education = [], [], []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            education.append(ent.text)
        elif ent.label_ == "DATE" or "years" in ent.text.lower():
            experience.append(ent.text)
        elif ent.label_ == "PRODUCT" or ent.label_ == "SKILL":
            skills.append(ent.text)
    
    return {
        "skills": list(set(skills)),
        "experience": list(set(experience)),
        "education": list(set(education))
    }

def rank_resume(resume_text, job_description):
    """Ranks the resume against the job description using BERT."""
    try:
        inputs = tokenizer(resume_text, job_description, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1).detach().numpy()
        return round(scores[0][1] * 100, 2)  # Convert score to percentage
    except Exception as e:
        return f"Error ranking resume: {str(e)}"

# Streamlit UI
st.title("📄 AI-Driven Resume Screening System")
st.write("Upload your resume (PDF or DOCX) and enter a job description to evaluate match score.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_description = st.text_area("Enter Job Description", "Looking for a Python Developer with NLP experience")

if uploaded_file is not None:
    # Save uploaded file to 'uploads' directory
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text from uploaded file
    if uploaded_file.name.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    elif uploaded_file.name.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    else:
        st.error("❌ Unsupported file format. Please upload a PDF or DOCX.")
        st.stop()

    # Extract key sections
    parsed_data = extract_sections(extracted_text)
    match_score = rank_resume(extracted_text, job_description)

    # Display extracted information
    st.subheader("📌 Extracted Information:")
    st.json(parsed_data)

    # Display match score
    st.subheader(f"✅ Match Score: {match_score}%")

    # Cleanup: Optionally remove the file after processing
    os.remove(file_path)
