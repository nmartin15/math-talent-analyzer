# resume_parser.py
"""
Module for parsing resumes in PDF, DOCX, or text format and extracting relevant information such as education, experience, projects, publications, and skills.
"""

import os
from typing import List, Dict, Any
import pypdf

SAMPLE_RESUME_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_resumes')

class ResumeParser:
    """
    Batch parser for resumes in PDF format.
    Extracts structured information for downstream analysis.
    """
    def __init__(self, resume_dir: str = SAMPLE_RESUME_DIR):
        self.resume_dir = resume_dir

    def get_pdf_files(self) -> List[str]:
        """Return list of PDF file paths in the resume directory."""
        try:
            files = os.listdir(self.resume_dir)
        except Exception as e:
            raise
        return [
            os.path.join(self.resume_dir, f)
            for f in files
            if f.lower().endswith('.pdf')
        ]

    def extract_text(self, pdf_path: str) -> str:
        """Extract all text from a PDF file using pypdf."""
        text = ""
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def parse_resume(self, text: str) -> Dict[str, Any]:
        """
        Stub: Parse resume text into structured data.
        Returns a dictionary with keys: name, education, experience, skills, etc.
        """
        return {
            'name': self.extract_name(text),
            'education': self.extract_education(text),
            'experience': self.extract_experience(text),
            'skills': self.extract_skills(text),
            'raw_text': text
        }

    def extract_name(self, text: str) -> str:
        """
        Extract candidate name from resume text.
        Uses the first non-empty line as the name.
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            return lines[0]
        return ""

    def extract_education(self, text: str) -> List[str]:
        """
        Extract education section from resume text.
        Looks for 'Education' header and grabs lines until the next section header or end.
        """
        lines = [line.strip() for line in text.split('\n')]
        education_headers = ["education", "academic background", "degrees"]
        all_headers = education_headers + ["experience", "skills", "projects", "publications", "work experience", "professional experience"]
        # Find the start of the education section
        start = None
        for i, line in enumerate(lines):
            if any(h in line.lower() for h in education_headers):
                start = i + 1
                break
        if start is None:
            return []
        # Find the end of the education section
        end = None
        for j in range(start, len(lines)):
            if any(h in lines[j].lower() for h in all_headers if h not in education_headers):
                end = j
                break
        section = lines[start:end] if end else lines[start:]
        # Filter out empty lines
        return [l for l in section if l.strip()]

    def extract_experience(self, text: str) -> List[str]:
        """
        Extract experience section from resume text.
        Looks for 'Experience' header and grabs lines until the next section header or end.
        """
        lines = [line.strip() for line in text.split('\n')]
        experience_headers = ["experience", "work experience", "professional experience"]
        all_headers = experience_headers + ["education", "skills", "projects", "publications", "academic background", "degrees"]
        start = None
        for i, line in enumerate(lines):
            if any(h in line.lower() for h in experience_headers):
                start = i + 1
                break
        if start is None:
            return []
        end = None
        for j in range(start, len(lines)):
            if any(h in lines[j].lower() for h in all_headers if h not in experience_headers):
                end = j
                break
        section = lines[start:end] if end else lines[start:]
        return [l for l in section if l.strip()]
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills section from resume text.
        Looks for 'Skills' header and grabs lines until the next section header or end.
        Splits comma-separated lists.
        """
        lines = [line.strip() for line in text.split('\n')]
        skills_headers = ["skills", "technical skills", "core competencies"]
        all_headers = skills_headers + ["education", "experience", "projects", "publications", "work experience", "professional experience", "academic background", "degrees"]
        start = None
        for i, line in enumerate(lines):
            if any(h in line.lower() for h in skills_headers):
                start = i + 1
                break
        if start is None:
            return []
        end = None
        for j in range(start, len(lines)):
            if any(h in lines[j].lower() for h in all_headers if h not in skills_headers):
                end = j
                break
        section = lines[start:end] if end else lines[start:]
        # Split comma-separated skills and flatten
        skills = []
        for l in section:
            for skill in l.split(","):
                s = skill.strip()
                if s:
                    skills.append(s)
        return skills

    def batch_parse(self) -> List[Dict[str, Any]]:
        """
        Parse all PDF resumes in the directory and return a list of structured results.
        """
        results = []
        for pdf_path in self.get_pdf_files():
            text = self.extract_text(pdf_path)
            parsed = self.parse_resume(text)
            parsed['filename'] = os.path.basename(pdf_path)
            results.append(parsed)
        return results

# For unit testing and CLI usage, see tests/test_resume_parser.py
