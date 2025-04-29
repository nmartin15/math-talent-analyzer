# test_github_analyzer.py
"""
Unit tests for github_analyzer.py
"""

import pytest
from src.github_analyzer import GitHubAnalyzer

@pytest.fixture
def analyzer():
    return GitHubAnalyzer(username="octocat")

import socket

@pytest.mark.skipif(socket.gethostbyname('api.github.com') is None, reason="No internet connection.")
def test_fetch_profile(analyzer):
    """Integration test: fetch_profile should return expected keys for a real user."""
    profile = analyzer.fetch_profile()
    assert isinstance(profile, dict)
    assert 'login' in profile and profile['login'] == 'octocat'
    assert 'public_repos' in profile

@pytest.mark.skipif(socket.gethostbyname('api.github.com') is None, reason="No internet connection.")
def test_fetch_repos(analyzer):
    """Integration test: fetch_repos should return a list of repos with expected keys."""
    repos = analyzer.fetch_repos()
    assert isinstance(repos, list)
    if repos:
        assert 'name' in repos[0]
        assert 'html_url' in repos[0]

def test_analyze_math_libraries(analyzer):
    # Edge: empty repo list
    assert analyzer.analyze_math_libraries([]) == {}
    # Topics only
    repos = [{
        'name': 'networks', 'topics': ['networkx'], 'description': '', 'language': ''
    }]
    out = analyzer.analyze_math_libraries(repos)
    assert 'networkx' in out and out['networkx']['count'] == 1
    # Description only
    repos = [{
        'name': 'mathfun', 'topics': [], 'description': 'Uses numpy and pandas.', 'language': ''
    }]
    out = analyzer.analyze_math_libraries(repos)
    assert 'numpy' in out and 'pandas' in out
    # Language only
    repos = [{
        'name': 'ml', 'topics': [], 'description': '', 'language': 'pytorch'
    }]
    out = analyzer.analyze_math_libraries(repos)
    assert 'pytorch' in out
    # No matches
    repos = [{
        'name': 'plain', 'topics': [], 'description': 'No math libs.', 'language': 'python'
    }]
    assert analyzer.analyze_math_libraries(repos) == {}
    # Advanced: multiple libraries in one repo, mixed case, duplicate in topics/description
    repos = [{
        'name': 'combo',
        'topics': ['NumPy', 'scipy'],
        'description': 'Uses numpy, scipy, and matplotlib. numpy is great.',
        'language': 'Python'
    }]
    out = analyzer.analyze_math_libraries(repos)
    assert out['numpy']['count'] == 1
    assert out['scipy']['count'] == 1
    assert out['matplotlib']['count'] == 1

def test_analyze_repo_complexity(analyzer):
    # Edge: empty repo list
    assert analyzer.analyze_repo_complexity([]) == {}
    # Case-insensitivity and partial word (should not match 'algorithms' for 'algorithm')
    repos = [{
        'name': 'algo', 'description': 'Contains algorithms', 'topics': []
    }]
    out = analyzer.analyze_repo_complexity(repos)
    assert out == {}  # 'algorithm' should not match 'algorithms'
    # Overlapping keywords (should count each only once)
    repos = [{
        'name': 'overlap',
        'description': 'Optimization and optimization theory.',
        'topics': ['optimization', 'theory']
    }]
    out = analyzer.analyze_repo_complexity(repos)
    assert out['overlap']['score'] == 2
    # Keywords in name only
    repos = [{
        'name': 'gradient',
        'description': 'A repo.',
        'topics': []
    }]
    out = analyzer.analyze_repo_complexity(repos)
    assert 'gradient' in out['gradient']['complexity_signals']
    # Similar words (should not match)
    repos = [{
        'name': 'deep',
        'description': 'Gradiently improving.',
        'topics': []
    }]
    out = analyzer.analyze_repo_complexity(repos)
    assert out == {}
    # Multiple signals in topics/description
    repos = [{
        'name': 'bigrepo',
        'description': 'Uses convex optimization and combinatorial algorithms.',
        'topics': ['convex', 'combinatorial', 'optimization']
    }]
    out = analyzer.analyze_repo_complexity(repos)
    assert out['bigrepo']['score'] >= 3

def test_analyze_documentation(analyzer):
    # Edge: empty repo list
    assert analyzer.analyze_documentation([]) == {}
    # Only wiki/pages
    repos = [{
        'name': 'wikirepo', 'description': '', 'has_wiki': True, 'has_pages': True
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['wikirepo']['score'] == 2
    # Only README
    repos = [{
        'name': 'readmerepo', 'description': '', 'has_readme': True
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['readmerepo']['score'] == 2
    # Multiple doc keywords and long description
    repos = [{
        'name': 'mathrepo',
        'description': 'This repo provides math proofs, analysis, and references for algorithms. Background and theory included.',
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['mathrepo']['score'] >= 5
    notes = out['mathrepo']['notes']
    assert 'Long description' in notes and 'Keywords:' in notes
    # All heuristics present
    repos = [{
        'name': 'superdoc',
        'description': 'Extensive documentation with theory, proof, analysis, and references. Covers background and optimization. Very detailed and long for demonstration purposes.',
        'has_wiki': True, 'has_pages': True, 'has_readme': True
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['superdoc']['score'] >= 7
    # Long but irrelevant description
    repos = [{
        'name': 'boring',
        'description': 'This is a very long description but contains nothing about math or documentation keywords. It is just verbose.'
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['boring']['score'] == 1
    # Only keywords (case-insensitive)
    repos = [{
        'name': 'case',
        'description': 'PROOF and THEORY are discussed here.'
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['case']['score'] == 2
    # Only wiki
    repos = [{
        'name': 'justwiki', 'description': '', 'has_wiki': True
    }]
    out = analyzer.analyze_documentation(repos)
    assert out['justwiki']['score'] == 1
    # No signals (should not be included)
    repos = [{
        'name': 'empty', 'description': ''
    }]
    out = analyzer.analyze_documentation(repos)
    assert out == {}
