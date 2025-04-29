# Roadmap: Mathematical Talent Analyzer

## MVP (Phase 1)
- [ ] Resume parsing (PDF/DOCX/text)
- [ ] GitHub profile analysis
  - [x] Algorithm- Implement and test GitHubAnalyzer methods for math library detection, code complexity, and documentation quality. **(Complete, robust to edge/adversarial cases, comprehensively tested.)**
  - Math library detection avoids generic false positives (e.g., 'math' removed)
  - Complexity analysis includes 'theory' and uses robust word-boundary regex
  - Full test coverage in /tests/test_github_analyzer.py
  - [ ] Recruiter-facing configuration panel for metric selection
- [ ] Basic math skill extraction and scoring
- [ ] LLM-based summary and talking points
- [ ] Streamlit UI for recruiters
- [ ] Unit tests for all modules

## Phase 2
- [ ] Skill radar visualization
- [ ] Bulk resume analysis
- [ ] ATS/CRM integration
- [ ] Customizable scoring profiles

## Phase 3
- [ ] Comparison mode (multi-candidate)
- [ ] Feedback loop for summary improvement
- [ ] Advanced analytics (e.g., publication impact)

## Timeline
- MVP: 2–4 weeks
- Phase 2: +4 weeks
- Phase 3: +4 weeks
