# app.py
"""
Streamlit UI for the Mathematical Talent Analyzer.
Handles recruiter workflow: upload, analysis, visualization, and export.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.github_analyzer import GitHubAnalyzer
import pandas as pd

st.set_page_config(page_title="Mathematical Talent Analyzer", layout="wide")

# Sidebar with project info and instructions
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/brain.png", width=64)
    st.title("🧠 Math Talent Analyzer")
    st.markdown("""
    <span style='color:#555;'>v1.0 &mdash; Analyze a GitHub user's public repositories for:</span>
    <ul style='margin-bottom:0;'>
      <li>Mathematical library usage</li>
      <li>Code complexity signals</li>
      <li>Documentation quality</li>
    </ul>
    <span style='color:#888;'>Enter a username and click <b>Analyze</b>.</span>
    """, unsafe_allow_html=True)
    recruiter_mode = st.checkbox("Recruiter Mode", value=False, help="Show recruiter-focused summary and export tools.")
    if recruiter_mode:
        st.markdown("""
        <div style='background:#eaf6ff; color:#155fa0; border-radius:8px; padding:10px; margin-top:10px; margin-bottom:10px; text-align:center; font-weight:600;'>
        <span style='font-size:18px;'>Recruiter Mode Enabled</span><br>
        <span style='font-size:13px; color:#155fa0;'>This mode highlights candidate strengths, red flags, and provides a copyable summary for technical recruiters.</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <span style='color:#888; font-size:12px;'>
    <b>What is Recruiter Mode?</b><br>
    When enabled, the app:
    <ul style='margin-bottom:0;'>
    <li>Shows a plain-language candidate summary at the top</li>
    <li>Highlights strengths and red flags with colored badges</li>
    <li>Provides a copy-to-clipboard recruiter summary</li>
    <li>Makes all results more readable for non-engineers</li>
    </ul>
    </span>
    """, unsafe_allow_html=True)
    st.markdown("""---<br><span style='color:#aaa;'>Built with ❤️ by the Math Talent Analyzer Team</span>""", unsafe_allow_html=True)
    # Scaffold for batch analysis (future)
    # st.file_uploader("Batch Analyze (CSV of GitHub usernames)", type=["csv"])
st.title("Mathematical Talent Analyzer: GitHub Profile Analysis")

with st.form("github_form"):
    username = st.text_input("🔗 GitHub Username", "")
    submitted = st.form_submit_button("Analyze")

if submitted and username:
    try:
        analyzer = GitHubAnalyzer(username)
        with st.spinner(f"Fetching GitHub data for {username}..."):
            profile = analyzer.fetch_profile()
            repos = analyzer.fetch_repos()
        st.success(f"Fetched {len(repos)} repositories for {username}.")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("👤 Profile Summary")
            st.markdown(f"**Name:** {profile.get('name', 'N/A')}")
            st.markdown(f"**Bio:** {profile.get('bio', 'N/A')}")
            st.markdown(f"**Location:** {profile.get('location', 'N/A')}")
            st.markdown(f"**Public Repos:** {profile.get('public_repos', 'N/A')}")
            st.markdown(f"**Followers:** {profile.get('followers', 'N/A')}")
            st.markdown(f"[View on GitHub]({profile.get('html_url', '')})")

            # --- Math Talent Analyzer Summary ---
            math_libs = analyzer.analyze_math_libraries(repos)
            complexity = analyzer.analyze_repo_complexity(repos)
            documentation = analyzer.analyze_documentation(repos)
            unique_libs = len([lib for lib, v in math_libs.items() if v["count"] > 0])
            avg_complexity_level = 0
            if complexity:
                levels = []
                for v in complexity.values():
                    score = v["score"]
                    if score == 0:
                        levels.append(0)
                    elif score == 1:
                        levels.append(1)
                    elif 2 <= score <= 3:
                        levels.append(2)
                    else:
                        levels.append(3)
                avg_complexity_level = sum(levels) / len(levels)
            avg_doc_score = sum(v["score"] for v in documentation.values()) / max(1, len(documentation))

            # Summarize each metric
            def summarize_libs(n):
                if n >= 5:
                    return "Strong math library diversity"
                elif n >= 2:
                    return "Some math/science library experience"
                else:
                    return "Limited advanced math library usage"
            def summarize_complexity(level):
                if level >= 2.5:
                    return "Research-level code complexity"
                elif level >= 1.5:
                    return "Advanced code complexity"
                elif level >= 0.5:
                    return "Some algorithmic sophistication"
                else:
                    return "No advanced code complexity detected"
            def summarize_doc(score):
                if score >= 3.5:
                    return "Exceptional documentation"
                elif score >= 2.5:
                    return "Detailed documentation"
                elif score >= 1.5:
                    return "Some usage/examples"
                elif score >= 0.5:
                    return "Minimal documentation"
                else:
                    return "No documentation found"

            st.markdown("""
            <div style='background-color:#f2f6fc; padding:12px; border-radius:8px; margin-top:12px;'>
            <b>📝 Math Talent Analysis Summary</b><br>
            <ul style='margin-bottom:0;'>
                <li><b>Math Libraries:</b> {lib_summary}</li>
                <li><b>Code Complexity:</b> {complexity_summary}</li>
                <li><b>Documentation:</b> {doc_summary}</li>
            </ul>
            <b>Strengths:</b>
            <ul style='margin-bottom:0;'>
            {pros}
            </ul>
            <b>Areas for Improvement:</b>
            <ul style='margin-bottom:0;'>
            {cons}
            </ul>
            </div>
            <style>
            .badge-green {{ background:#c8f7c5; color:#217a3b; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:12px; }}
            .badge-yellow {{ background:#fff6c5; color:#b89b1c; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:12px; }}
            .badge-red {{ background:#ffd6d6; color:#b82c2c; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:12px; }}
            </style>
            """.format(
                lib_summary=summarize_libs(unique_libs),
                complexity_summary=summarize_complexity(avg_complexity_level),
                doc_summary=summarize_doc(avg_doc_score),
                pros="".join([
                    "<li><span class='badge-green'>✔</span>Strong library diversity</li>" if unique_libs >= 5 else "",
                    "<li><span class='badge-green'>✔</span>Advanced or research-level code complexity</li>" if avg_complexity_level >= 1.5 else "",
                    "<li><span class='badge-green'>✔</span>Exceptional or detailed documentation</li>" if avg_doc_score >= 2.5 else "",
                ]),
                cons="".join([
                    "<li><span class='badge-red'>✖</span>Limited advanced library usage</li>" if unique_libs < 2 else "",
                    "<li><span class='badge-red'>✖</span>No advanced code complexity detected</li>" if avg_complexity_level < 0.5 else "",
                    "<li><span class='badge-yellow'>⚠</span>Minimal or no documentation</li>" if avg_doc_score < 1.5 else "",
                ])
            ), unsafe_allow_html=True)

            # --- Export Buttons ---
            import io
            import pandas as pd
            summary_lines = [
                "Math Talent Analysis Summary",
                "",
                f"Math Libraries: {summarize_libs(unique_libs)}",
                f"Code Complexity: {summarize_complexity(avg_complexity_level)}",
                f"Documentation: {summarize_doc(avg_doc_score)}",
                "",
                "Strengths:",
            ]
            if unique_libs >= 5:
                summary_lines.append("- Strong library diversity")
            if avg_complexity_level >= 1.5:
                summary_lines.append("- Advanced or research-level code complexity")
            if avg_doc_score >= 2.5:
                summary_lines.append("- Exceptional or detailed documentation")
            summary_lines.append("")
            summary_lines.append("Areas for Improvement:")
            if unique_libs < 2:
                summary_lines.append("- Limited advanced library usage")
            if avg_complexity_level < 0.5:
                summary_lines.append("- No advanced code complexity detected")
            if avg_doc_score < 1.5:
                summary_lines.append("- Minimal or no documentation")
            summary_text = "\n".join(summary_lines)
            st.download_button("Download Profile Summary (txt)", summary_text, file_name="profile_summary.txt")

            # --- Recruiter Mode Block ---
            if recruiter_mode:
                # Visual recruiter summary banner
                st.markdown("""
                <div style='background:#eaf6ff; border-radius:8px; padding:16px; margin-top:8px; margin-bottom:16px; border-left: 6px solid #155fa0;'>
                <span style='font-size:17px; font-weight:700; color:#155fa0;'>Why Consider This Candidate?</span><br><br>
                <span style='font-size:15px; color:#222;'>
                {plain_summary}
                </span>
                <div style='margin-top:10px;'>
                  <span style='font-weight:600;'>Strengths:</span> {strength_badges}
                </div>
                <div style='margin-top:4px;'>
                  <span style='font-weight:600;'>Red Flags:</span> {flag_badges}
                </div>
                </div>
                """.format(
                    plain_summary=f"This candidate demonstrates {summarize_libs(unique_libs).lower()}, {summarize_complexity(avg_complexity_level).lower()}, and {summarize_doc(avg_doc_score).lower()}.",
                    strength_badges=" ".join([
                        "<span style='background:#c8f7c5; color:#217a3b; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:13px;'>Strong library diversity</span>" if unique_libs >= 5 else "",
                        "<span style='background:#c8f7c5; color:#217a3b; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:13px;'>Advanced/research-level code</span>" if avg_complexity_level >= 1.5 else "",
                        "<span style='background:#c8f7c5; color:#217a3b; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:13px;'>Exceptional/detailed docs</span>" if avg_doc_score >= 2.5 else "",
                    ]),
                    flag_badges=" ".join([
                        "<span style='background:#ffd6d6; color:#b82c2c; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:13px;'>Limited advanced library usage</span>" if unique_libs < 2 else "",
                        "<span style='background:#ffd6d6; color:#b82c2c; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:13px;'>No advanced code complexity</span>" if avg_complexity_level < 0.5 else "",
                        "<span style='background:#fff6c5; color:#b89b1c; border-radius:6px; padding:2px 8px; margin-right:4px; font-size:13px;'>Minimal/no documentation</span>" if avg_doc_score < 1.5 else "",
                    ]),
                ), unsafe_allow_html=True)
                recruiter_lines = [
                    f"Recruiter Summary for {profile.get('name', profile.get('login', 'Candidate'))}",
                    "",
                    f"- Math Library Experience: {summarize_libs(unique_libs)}",
                    f"- Code Complexity: {summarize_complexity(avg_complexity_level)}",
                    f"- Documentation: {summarize_doc(avg_doc_score)}",
                    "",
                    "Key Strengths:",
                ]
                if unique_libs >= 5:
                    recruiter_lines.append("- Strong library diversity")
                if avg_complexity_level >= 1.5:
                    recruiter_lines.append("- Advanced/research-level code")
                if avg_doc_score >= 2.5:
                    recruiter_lines.append("- Exceptional/detailed docs")
                recruiter_lines.append("Areas for Growth:")
                if unique_libs < 2:
                    recruiter_lines.append("- Limited advanced library usage")
                if avg_complexity_level < 0.5:
                    recruiter_lines.append("- No advanced code complexity")
                if avg_doc_score < 1.5:
                    recruiter_lines.append("- Minimal/no documentation")
                recruiter_summary = "\n".join(recruiter_lines)
                st.text_area("Copy Recruiter Summary", recruiter_summary, height=120)
                st.download_button("Download Recruiter Summary (txt)", recruiter_summary, file_name="recruiter_summary.txt")

            # --- Download buttons for tables ---
            if 'df_libs' in locals():
                libs_csv = df_libs.to_csv(index=False).encode('utf-8')
                st.download_button("Download Math Library Table (CSV)", libs_csv, file_name="math_libraries.csv")
            if 'df_complex' in locals():
                complex_csv = df_complex.to_csv(index=False).encode('utf-8')
                st.download_button("Download Complexity Table (CSV)", complex_csv, file_name="complexity.csv")
            if 'df_doc' in locals():
                doc_csv = df_doc.to_csv(index=False).encode('utf-8')
                st.download_button("Download Documentation Table (CSV)", doc_csv, file_name="documentation.csv")

            # --- Download radar chart as PNG ---
            try:
                import plotly.io as pio
                radar_bytes = None
                if 'radar_fig' in locals():
                    radar_bytes = io.BytesIO()
                    pio.write_image(radar_fig, radar_bytes, format='png')
                    radar_bytes.seek(0)
                if radar_bytes:
                    st.download_button("Download Radar Chart (PNG)", radar_bytes, file_name="radar_chart.png")
            except Exception as e:
                pass

        with col2:
            st.subheader("📊 Analysis Results")
            st.markdown("""
            <style>
            .stDataFrame tbody tr:nth-child(even) {background-color: #f8fafc;}
            .stDataFrame tbody tr:nth-child(odd) {background-color: #fff;}
            </style>
            """, unsafe_allow_html=True)
            st.markdown("<hr style='margin-top:0; margin-bottom:8px; border:none; border-top:1px solid #e0e0e0;'>", unsafe_allow_html=True)
            with st.expander("🔬 Mathematical Library Usage", expanded=True):
                st.markdown("""
                **Math Library Usage Metric:**
                - **Count**: Number of repositories where each mathematical or scientific library (e.g., numpy, scipy, sympy, networkx, etc.) is detected in topics, description, or repo name.
                - **Detection**: Uses keyword matching in repo metadata; avoids generic matches (e.g., excludes 'math' alone).
                - **Interpretation**: Higher counts indicate more experience with advanced math/science tools.
                ℹ️ <span style='color:#888;'>Tip: Click column headers to sort tables.</span>
                """, unsafe_allow_html=True)
                math_libs = analyzer.analyze_math_libraries(repos)
                if math_libs:
                    df_libs = pd.DataFrame([
                        {"Library": lib, "Count": v["count"], "Repos": ", ".join(v["repos"])}
                        for lib, v in math_libs.items() if v["count"] > 0
                    ])
                    st.dataframe(df_libs, use_container_width=True)
                    # Bar chart visualization
                    if not df_libs.empty:
                        st.markdown("**Library Usage Frequency**")
                        st.bar_chart(df_libs.set_index("Library")["Count"])
                else:
                    st.info("No mathematical libraries detected in public repositories.")

            st.markdown("<hr style='margin-top:0; margin-bottom:8px; border:none; border-top:1px solid #e0e0e0;'>", unsafe_allow_html=True)
            with st.expander("🧩 Code Complexity Analysis", expanded=True):
                st.markdown("""
                **Code Complexity Metric:**
                - **Signals**: Looks for keywords indicating advanced algorithms or mathematical sophistication (e.g., 'optimization', 'dynamic programming', 'graph', 'theory', etc.) in repo topics, description, or name.
                - **Score**: Number of unique complexity signals found per repository.
                - **Interpretation**: Higher scores indicate more sophisticated or research-level codebases.
                ℹ️ <span style='color:#888;'>Hover over column headers for more details.</span>
                """, unsafe_allow_html=True)
                complexity = analyzer.analyze_repo_complexity(repos)
                if complexity:
                    def complexity_level(score):
                        if score == 0:
                            return "None"
                        elif score == 1:
                            return "Basic"
                        elif 2 <= score <= 3:
                            return "Advanced"
                        else:
                            return "Research-level"
                    df_complex = pd.DataFrame([
                        {"Repository": repo, "Signals": ", ".join(v["complexity_signals"]), "Score": v["score"], "Complexity Level": complexity_level(v["score"])}
                        for repo, v in complexity.items()
                    ])
                    st.dataframe(df_complex, use_container_width=True)
                    st.info("""
                    **Complexity Level:**
                    - **None:** No advanced algorithmic or mathematical signals detected
                    - **Basic:** 1 signal (e.g., 'graph', 'regression', etc.)
                    - **Advanced:** 2-3 signals (multiple advanced concepts)
                    - **Research-level:** 4 or more signals (highly sophisticated or research-grade repository)
                    """)
                    # Bar chart visualization
                    if not df_complex.empty:
                        st.markdown("**Complexity Score per Repository**")
                        st.bar_chart(df_complex.set_index("Repository")["Score"])
                else:
                    st.info("No advanced complexity signals detected.")

            st.markdown("<hr style='margin-top:0; margin-bottom:8px; border:none; border-top:1px solid #e0e0e0;'>", unsafe_allow_html=True)
            with st.expander("📄 Documentation Quality Analysis", expanded=True):
                st.markdown("""
                **Documentation Quality Score Legend:**
                - **0**: No documentation detected (no README, no docstrings, no usage info)
                - **1**: Minimal documentation (basic README or short description only)
                - **2**: Some usage/examples (README with usage, install, or example sections)
                - **3**: Detailed API or function/class documentation (docstrings, API docs, or extensive README)
                - **4+**: Exceptional documentation (comprehensive guides, tutorials, diagrams, and API references)
                ℹ️ <span style='color:#888;'>Click pie slices for details.</span>
                <br>_Scores are heuristically assigned based on repo metadata, descriptions, topics, and README content._
                """, unsafe_allow_html=True)
                documentation = analyzer.analyze_documentation(repos)
                if documentation:
                    df_doc = pd.DataFrame([
                        {"Repository": repo, "Score": v["score"], "Notes": v["notes"]}
                        for repo, v in documentation.items()
                    ])
                    st.dataframe(df_doc, use_container_width=True)
                    # Pie chart visualization for documentation quality scores
                    import plotly.express as px
                    score_counts = df_doc['Score'].value_counts().sort_index()
                    pie_fig = px.pie(
                        names=score_counts.index.astype(str),
                        values=score_counts.values,
                        title="Documentation Quality Score Distribution",
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    st.plotly_chart(pie_fig, use_container_width=True)
                else:
                    st.info("No documentation quality signals detected.")

            # Time trend line chart
            with st.expander("Repository Score Over Time", expanded=False):
                import plotly.express as px
                if repos:
                    repo_scores = []
                    for repo in repos:
                        name = repo.get("name", "N/A")
                        created = repo.get("created_at", None)
                        complexity_score = complexity.get(name, {}).get("score", 0)
                        doc_score = documentation.get(name, {}).get("score", 0)
                        math_score = sum(1 for v in math_libs.values() if name in v["repos"])
                        total_score = complexity_score + doc_score + math_score
                        repo_scores.append({"Repository": name, "Created": created, "Total Score": total_score})
                    df_time = pd.DataFrame(repo_scores)
                    if not df_time.empty and df_time["Created"].notnull().any():
                        df_time = df_time[df_time["Created"].notnull()].copy()
                        df_time["Created"] = pd.to_datetime(df_time["Created"])
                        df_time = df_time.sort_values("Created")
                        st.line_chart(df_time.set_index("Created")["Total Score"])
                    else:
                        st.info("No repository creation dates available for trend analysis.")

        # Aggregate radar chart for overall profile (math, complexity, documentation)
        try:
            import plotly.graph_objects as go
            import plotly.express as px
            math_libs = analyzer.analyze_math_libraries(repos)
            complexity = analyzer.analyze_repo_complexity(repos)
            documentation = analyzer.analyze_documentation(repos)
            # Aggregate metrics for radar chart
            unique_libs = len([lib for lib, v in math_libs.items() if v["count"] > 0])
            avg_complexity_level = 0
            levels = []
            for v in complexity.values():
                score = v["score"]
                if score == 0:
                    levels.append(0)
                elif score == 1:
                    levels.append(1)
                elif 2 <= score <= 3:
                    levels.append(2)
                else:
                    levels.append(3)
            if levels:
                avg_complexity_level = sum(levels) / len(levels)
            avg_doc_score = sum(v["score"] for v in documentation.values()) / max(1, len(documentation))
            radar_metrics = {
                "Math Library Diversity": unique_libs,
                "Avg. Complexity Level (0-3)": avg_complexity_level,
                "Avg. Doc Quality (0-4+)": avg_doc_score,
            }
            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(
                r=list(radar_metrics.values()),
                theta=list(radar_metrics.keys()),
                fill='toself',
                name='Aggregate Profile'
            ))
            radar_fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=False,
                title="Aggregate Mathematical Profile (Radar Chart)"
            )
            st.markdown("""
            ### Aggregate Mathematical Profile
            This radar chart summarizes:
            - **Math Library Diversity:** Number of unique advanced libraries used
            - **Avg. Complexity Level:** 0=None, 1=Basic, 2=Advanced, 3=Research-level (across all repos)
            - **Avg. Documentation Quality:** 0=None, 1=Minimal, 2=Usage, 3=Detailed, 4+=Exceptional
            """)
            st.plotly_chart(radar_fig, use_container_width=True)

            # --- More aggregate visualizations ---
            st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
            st.markdown("#### Aggregate Metrics Bar Chart")
            agg_df = pd.DataFrame({
                "Metric": ["Math Library Diversity", "Avg. Complexity Level", "Avg. Doc Quality"],
                "Value": [unique_libs, avg_complexity_level, avg_doc_score],
            })
            st.bar_chart(agg_df.set_index("Metric")['Value'])

            # Pie chart: distribution of complexity levels
            st.markdown("#### Complexity Level Distribution")
            level_labels = {0: "None", 1: "Basic", 2: "Advanced", 3: "Research-level"}
            # Defensive: always define levels
            if 'levels' not in locals() or not isinstance(levels, list):
                levels = []
            if levels:
                level_counts = pd.Series([level_labels.get(l, "Other") for l in levels]).value_counts()
            else:
                level_counts = pd.Series(["None"]).value_counts()
            if level_counts.sum() == 0:
                st.info("No complexity data available for distribution chart.")
            else:
                pie1 = px.pie(
                    names=level_counts.index,
                    values=level_counts.values,
                    title="Complexity Level Distribution",
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                st.plotly_chart(pie1, use_container_width=True)

            # Pie chart: distribution of documentation quality
            st.markdown("#### Documentation Quality Distribution")
            doc_labels = {0: "None", 1: "Minimal", 2: "Some usage/examples", 3: "Detailed", 4: "Exceptional"}
            doc_scores = [min(int(v["score"]), 4) for v in documentation.values()]
            doc_counts = pd.Series([doc_labels.get(s, "Other") for s in doc_scores]).value_counts()
            pie2 = px.pie(
                names=doc_counts.index,
                values=doc_counts.values,
                title="Documentation Quality Distribution",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(pie2, use_container_width=True)

        except Exception as radar_exc:
            st.info(f"Radar chart could not be rendered: {radar_exc}")

    except Exception as e:
        st.error(f"Error analyzing GitHub profile: {e}")

st.markdown("""
<hr style='margin-top:32px; margin-bottom:8px; border: none; border-top: 1px solid #e0e0e0;'>
<div style='text-align:center; color:#888; font-size:13px; padding-bottom:12px;'>
  <span style='font-weight:600;'>Math Talent Analyzer</span> &copy; 2025 &mdash; All rights reserved.<br>
  <span style='font-size:11px;'>Questions? <a href='mailto:support@mathtalentanalyzer.com' style='color:#888;'>Contact Support</a></span>
</div>
""", unsafe_allow_html=True)
