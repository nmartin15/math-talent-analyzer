# test_resume_parser.py
"""
Unit tests for resume_parser.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from resume_parser import ResumeParser, SAMPLE_RESUME_DIR

@pytest.fixture
def parser():
    return ResumeParser()

def test_get_pdf_files(parser):
    pdfs = parser.get_pdf_files()
    # Should find all .pdf files in sample_resumes/
    assert isinstance(pdfs, list)
    for f in pdfs:
        assert f.lower().endswith('.pdf')
        assert os.path.exists(f)

def test_extract_text(parser):
    pdfs = parser.get_pdf_files()
    if not pdfs:
        pytest.skip("No sample PDF resumes present for text extraction test.")
    text = parser.extract_text(pdfs[0])
    assert isinstance(text, str)
    assert len(text) > 0

def test_batch_parse_structure(parser):
    pdfs = parser.get_pdf_files()
    if not pdfs:
        pytest.skip("No sample PDF resumes present for batch parse test.")
    results = parser.batch_parse()
    assert isinstance(results, list)
    for r in results:
        assert 'name' in r
        assert 'education' in r
        assert 'experience' in r
        assert 'skills' in r
        assert 'raw_text' in r
        assert 'filename' in r

import pytest

def test_extract_name(parser):
    sample_text = "Ada Lovelace\nMathematician\n..."
    expected_name = "Ada Lovelace"
    assert parser.extract_name(sample_text) == expected_name

def test_extract_education(parser):
    sample_text = "Education\nB.S. Mathematics, University of London, 1841\n..."
    expected_education = ["B.S. Mathematics, University of London, 1841", "..."]
    assert parser.extract_education(sample_text) == expected_education

def test_extract_experience(parser):
    sample_text = "Experience\nAnalyst, Analytical Engines, 1842-1850\n..."
    expected_experience = ["Analyst, Analytical Engines, 1842-1850", "..."]
    assert parser.extract_experience(sample_text) == expected_experience

def test_extract_skills(parser):
    sample_text = "Skills\nMathematics, Programming, Algorithm Design\n..."
    expected_skills = ["Mathematics", "Programming", "Algorithm Design", "..."]
    assert parser.extract_skills(sample_text) == expected_skills

# --- EDGE CASE TESTS ---
def test_extract_experience_missing_section(parser):
    sample_text = "Education\nB.S. Math\nSkills\nPython, R"
    assert parser.extract_experience(sample_text) == []

def test_extract_skills_missing_section(parser):
    sample_text = "Education\nB.S. Math\nExperience\nEngineer, 2020-2022"
    assert parser.extract_skills(sample_text) == []

def test_extract_education_missing_section(parser):
    sample_text = "Experience\nEngineer, 2020-2022\nSkills\nPython"
    assert parser.extract_education(sample_text) == []

def test_extract_skills_multiline_and_spaces(parser):
    sample_text = "Skills\nPython,   R,\nMachine Learning , Data Science,\n , , SQL "
    expected_skills = ["Python", "R", "Machine Learning", "Data Science", "SQL"]
    assert parser.extract_skills(sample_text) == expected_skills

def test_extract_skills_nonstandard_header(parser):
    sample_text = "Core Competencies\nLeadership, Communication, Problem Solving"
    expected_skills = ["Leadership", "Communication", "Problem Solving"]
    assert parser.extract_skills(sample_text) == expected_skills
