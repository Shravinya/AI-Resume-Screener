import spacy
import fitz  # PyMuPDF for PDF parsing
import docx
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer, util

# Load NLP model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

# Load SBERT model for ranking resumes against job descriptions
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = " ".join([page.get_text("text") for page in doc])
        return text
    except Exception as e:
        return str(e)

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file using python-docx."""
    try:
        doc = docx.Document(docx_path)
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return str(e)

def extract_sections(text):
    """Extract skills, experience, and education from resume text using NLP."""
    doc = nlp(text)
    skills, experience, education = set(), set(), set()

    for ent in doc.ents:
        if ent.label_ == "ORG":
            education.add(ent.text)
        elif ent.label_ == "DATE" or "years" in ent.text.lower():
            experience.add(ent.text)
        elif ent.label_ in ["PRODUCT", "SKILL"]:
            skills.add(ent.text)

    return {
        "skills": list(skills),
        "experience": list(experience),
        "education": list(education)
    }

def rank_resume(resume_text, job_description):
    """Calculate similarity score between resume and job description using SBERT."""
    try:
        embeddings = sbert_model.encode([resume_text, job_description])
        similarity_score = util.cos_sim(embeddings[0], embeddings[1])
        return float(similarity_score[0][0])  # Convert tensor to float
    except Exception as e:
        return str(e)

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Handle resume file uploads and return extracted details and ranking score."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Extract text based on file format
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    job_desc = request.form.get("job_description", "Looking for a Python Developer with NLP experience")
    parsed_data = extract_sections(text)
    rank_score = rank_resume(text, job_desc)

    return jsonify({"parsed_data": parsed_data, "match_score": rank_score})

if __name__ == "__main__":
    app.run(debug=True)
