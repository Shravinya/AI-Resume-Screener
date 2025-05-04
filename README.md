
# AI-Powered Resume Screening System

## 📌 Overview
The AI-Powered Resume Screening System automates resume parsing and ranking using NLP and deep learning models. It extracts key sections such as skills, experience, and education, and ranks resumes based on job descriptions. This project enhances recruitment efficiency by quickly identifying the best candidates.

## 🚀 Features
- **Automated Resume Parsing**: Extracts key information from PDF and DOCX files.
- **NLP-Powered Analysis**: Uses spaCy for named entity recognition.
- **BERT-Based Ranking**: Matches resumes to job descriptions using a pre-trained BERT model.
- **User-Friendly Interface**: Built with Streamlit for easy resume uploads and evaluations.

## 🛠️ Tech Stack
- **Python**: Core programming language
- **spaCy**: Natural Language Processing for information extraction
- **PyMuPDF**: PDF text extraction
- **python-docx**: DOCX text extraction
- **Transformers (BERT)**: Resume ranking
- **Streamlit**: Web application framework
- **Flask**: Backend API for processing requests

## 📂 Installation
```bash
# Clone the repository
git clone https://github.com/Shravinya/AI-Resume-Screener.git
cd resume-screening

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## 🔍 Usage
1. Upload a resume (PDF/DOCX) via the web interface.
2. Enter a job description.
3. The system extracts skills, experience, and education from the resume.
4. A match score is generated based on how well the resume aligns with the job description.

## 🎯 Example Output
```json
{
  "parsed_data": {
    "skills": ["Python", "Machine Learning", "NLP"],
    "experience": ["5 years"],
    "education": ["MIT"]
  },
  "match_score": 0.85
}
```

## 📌 Future Enhancements
- Integrate LinkedIn profile parsing.
- Improve accuracy with domain-specific fine-tuning of BERT.
- Add multi-language support for global hiring.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📬 Contact
For any queries, reach out at [shravinyagoud@gmail.com](mailto:your-email@example.com).
