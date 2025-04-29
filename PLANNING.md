# Project Planning: Mathematical Talent Analyzer

## 1. Architecture Overview

- **Frontend:** Streamlit dashboard (MVP)
- **Backend:** Python (FastAPI for API, modular services)
- **Core Modules:**
  - Resume Parser
  - GitHub Analyzer
    - Mathematical Library Utilization (detects libraries such as numpy, scipy, pandas, matplotlib, etc. by scanning repo topics, description, and language) Scorer
    - Algorithm Complexity Analyzer
    - Optimization Approach Detector
    - Mathematical Documentation Quality Assessor
  - Math Skill Scorer
  - LLM Summarizer
  - Reporting/Export

## 2. File/Module Structure

```
/math-talent-analyzer
  /src
    resume_parser.py
    github_analyzer.py
    skill_scorer.py
    summarizer.py
    report_generator.py
    app.py (Streamlit UI)
  /tests
    test_resume_parser.py
    test_github_analyzer.py
    ...
  /sample_resumes
    FirstName_LastName_Resume.pdf  # Sample resumes for development/testing
  README.md
  PLANNING.md
  ROADMAP.md
  requirements.txt
```

## 3. Design Decisions

- Use spaCy for NLP and entity extraction
- Use radon for code complexity and algorithmic sophistication analysis
- Use plotly and seaborn for advanced visualizations (statistical distribution, radar charts)
- Use PyGithub for easier and more robust GitHub API access
- Use pypdf for extracting text from PDF resumes
- Use python-docx for parsing Word resumes
- Use GitHub API for repo analysis
- Analyze GitHub repos for:
  - Mathematical Library Utilization (detects libraries such as numpy, scipy, pandas, matplotlib, etc. by scanning repo topics, description, and language) (NumPy, SciPy, etc.)
  - Algorithm Complexity (detection of advanced algorithms)
  - Optimization Approaches (gradient descent, convex, etc.)
  - Mathematical Documentation Quality (docstrings, README, clarity)
- Use OpenAI or local LLM for summarization and documentation analysis
- All modules <500 lines, split as needed

### GitHub Analysis Workflow
1. User provides GitHub username or repo URL
2. Configuration panel allows selection of metrics (library utilization, algorithm complexity, optimization, documentation quality)
3. System fetches repos and analyzes codebase for signals for each metric
4. Scores and evidence (code snippets, explanations) are presented in a summary report
5. Visualizations and recruiter talking points generated

## 4. Naming Conventions & Style

- snake_case for files and functions
- Classes: PascalCase
- Tests mirror main modules in `/tests`
