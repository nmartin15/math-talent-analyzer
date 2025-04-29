# github_analyzer.py
"""
Module for analyzing GitHub repositories for mathematical sophistication using custom metrics:
- Mathematical Library Utilization
- Algorithm Complexity Analysis
- Optimization Approach Detection
- Mathematical Documentation Quality
"""


import requests
from typing import List, Dict, Any

class GitHubAnalyzer:
    """
    Analyze GitHub profiles and repositories for mathematical and technical sophistication.
    """
    def __init__(self, username: str):
        self.username = username

    def _get_json(self, url: str) -> Any:
        """Helper to GET a URL and return JSON or None on error."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

    def fetch_profile(self) -> Dict[str, Any]:
        """Fetch the user's public GitHub profile data using the GitHub REST API."""
        url = f"https://api.github.com/users/{self.username}"
        data = self._get_json(url)
        return data if isinstance(data, dict) else {}

    def fetch_repos(self) -> List[Dict[str, Any]]:
        """Fetch the user's public repositories and metadata using the GitHub REST API."""
        url = f"https://api.github.com/users/{self.username}/repos"
        data = self._get_json(url)
        return data if isinstance(data, list) else []

    def analyze_math_libraries(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze use of mathematical libraries across repos.
        Scans repo metadata (topics, description, language) for common libraries.
        Returns a dict: {library: {count: int, repos: [repo_names]}}
        """
        math_libs = [
            'numpy', 'scipy', 'sympy', 'pandas', 'matplotlib', 'networkx',
            'statsmodels', 'sklearn', 'tensorflow', 'pytorch', 'jax', 'theano',
            'cvxpy', 'numba', 'sage', 'gmpy2', 'mpmath', 'random', 'itertools'
        ]
        result = {lib: {'count': 0, 'repos': []} for lib in math_libs}
        for repo in repos:
            text = ''
            # Combine topics, description, and language for simple matching
            if 'topics' in repo and isinstance(repo['topics'], list):
                text += ' '.join(repo['topics']).lower() + ' '
            if 'description' in repo and repo['description']:
                text += repo['description'].lower() + ' '
            if 'language' in repo and repo['language']:
                text += str(repo['language']).lower() + ' '
            import re
            for lib in math_libs:
                if re.search(r'\b' + re.escape(lib) + r'\b', text):
                    result[lib]['count'] += 1
                    result[lib]['repos'].append(repo.get('name', ''))
        # Remove unused libraries for cleaner output
        filtered = {lib: data for lib, data in result.items() if data['count'] > 0}
        return filtered

    def analyze_repo_complexity(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze code complexity and algorithmic sophistication.
        Scans repo metadata (topics, description, name) for advanced algorithm/complexity keywords.
        Returns a dict: {repo_name: {complexity_signals: [keywords], score: int}}
        """
        keywords = [
            "dynamic programming", "graph", "optimization", "gradient", "convex",
            "neural network", "regression", "classification", "clustering", "bayesian",
            "simulation", "eigenvalue", "sparse", "differential", "stochastic",
            "combinatorial", "cryptography", "probabilistic", "reinforcement",
            "theory"
        ]
        result = {}
        for repo in repos:
            topics = repo.get('topics', [])
            if not isinstance(topics, list):
                topics = []
            text = ' '.join(str(topic).lower() for topic in topics) + ' '
            if 'description' in repo and repo['description']:
                text += repo['description'].lower() + ' '
            if 'name' in repo and repo['name']:
                text += str(repo['name']).lower() + ' '
            import re
            cleaned_text = re.sub(r'[^a-z0-9 ]', ' ', text)
            signals = list({kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_text)})
            if signals:
                result[repo.get('name', 'unknown')] = {
                    'complexity_signals': signals,
                    'score': len(signals)
                }
        return result

    def analyze_documentation(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze mathematical documentation quality in repos.
        Uses metadata fields (has_readme, description length, keywords) to estimate quality.
        Returns a dict: {repo_name: {score: int, notes: str}}
        """
        doc_keywords = [
            'theory', 'algorithm', 'proof', 'complexity', 'references',
            'equation', 'formula', 'notation', 'background', 'analysis', 'derivation',
            'convergence', 'optimization', 'statistical', 'probability', 'model', 'objective'
        ]
        result = {}
        for repo in repos:
            notes = []
            score = 0
            # Heuristic: longer description = better docs
            desc = repo.get('description', '')
            if desc and len(desc) > 40:
                score += 1
                notes.append('Long description')
            # Heuristic: presence of doc-related keywords
            desc_l = desc.lower() if desc else ''
            found = [kw for kw in doc_keywords if kw in desc_l]
            if found:
                score += len(found)
                notes.append(f"Keywords: {', '.join(found)}")
            # Heuristic: has_wiki or has_pages flags
            if repo.get('has_wiki'):
                score += 1
                notes.append('Wiki enabled')
            if repo.get('has_pages'):
                score += 1
                notes.append('Pages enabled')
            # Heuristic: README presence (if available in repo data)
            if repo.get('has_readme', False):
                score += 2
                notes.append('README detected')
            if score > 0:
                result[repo.get('name', 'unknown')] = {
                    'score': score,
                    'notes': '; '.join(notes)
                }
        return result

# Implementation will be modular and tested in /tests/test_github_analyzer.py
