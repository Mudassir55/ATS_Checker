import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.parser import extract_text_from_pdf
from utils.scorer import calculate_ats_score


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ATS Resume Checker | Professional Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS STYLING
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ── Global ── */
    .main { background-color: #0f172a; }
    .stApp { background-color: #0f172a; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] p {
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
    }

    /* ── Typography ── */
    h1 { color: #f8fafc !important; font-weight: 700 !important; }
    h2 { color: #e2e8f0 !important; font-weight: 600 !important; }
    h3 { color: #cbd5e1 !important; font-weight: 600 !important; }
    p, span, div { color: #94a3b8 !important; }

    /* ── Cards ── */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-card h3 {
        color: #94a3b8 !important;
        font-size: 14px !important;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-card .value {
        color: #f8fafc !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
    }

    /* ── Input Fields ── */
    .stTextArea textarea, .stFileUploader {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

    /* ── Success/Error/Info ── */
    .stSuccess { background-color: rgba(34, 197, 94, 0.15) !important; border-color: #22c55e !important; }
    .stError { background-color: rgba(239, 68, 68, 0.15) !important; border-color: #ef4444 !important; }
    .stInfo { background-color: rgba(59, 130, 246, 0.15) !important; border-color: #3b82f6 !important; }
    .stWarning { background-color: rgba(234, 179, 8, 0.15) !important; border-color: #eab308 !important; }

    /* ── Skill Tags ── */
    .skill-tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin: 4px;
    }
    .skill-matched { background-color: rgba(34, 197, 94, 0.2); color: #22c55e !important; border: 1px solid #22c55e; }
    .skill-missing { background-color: rgba(239, 68, 68, 0.2); color: #ef4444 !important; border: 1px solid #ef4444; }
    .skill-resume { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6 !important; border: 1px solid #3b82f6; }

    /* ── Dividers ── */
    hr { border-color: #334155 !important; margin: 30px 0 !important; }

    /* ── Status Badge ── */
    .status-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
    }
    .status-excellent { background-color: rgba(34, 197, 94, 0.2); color: #22c55e !important; }
    .status-good { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6 !important; }
    .status-low { background-color: rgba(239, 68, 68, 0.2); color: #ef4444 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<h1 style='color:#f8fafc; font-size:22px;'>📄 ATS Resume Checker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:13px;'>Professional Resume Analysis Dashboard</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<h3 style='color:#e2e8f0; font-size:16px;'>📋 How It Works</h3>", unsafe_allow_html=True)

    steps = [
        ("1", "Upload Resume", "Upload your resume in PDF format"),
        ("2", "Paste Job Description", "Copy & paste the job description"),
        ("3", "Click Analyze", "Hit the Analyze button to process"),
        ("4", "Review Results", "Get detailed ATS score & insights"),
    ]

    for num, title, desc in steps:
        st.markdown(f"""
        <div style="background:#0f172a; border-left:3px solid #3b82f6; padding:12px; margin:8px 0; border-radius:0 8px 8px 0;">
            <span style="color:#3b82f6; font-weight:700;">{num}.</span>
            <span style="color:#e2e8f0; font-weight:600;">{title}</span><br>
            <span style="color:#64748b; font-size:12px;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#475569; font-size:11px;'>v2.0 | Built with Streamlit & Plotly</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# MAIN HEADER
# ═══════════════════════════════════════════════════════════════
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown("<h1 style='font-size:36px; margin-bottom:0;'>📄 ATS Resume Checker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:15px;'>Upload your resume and compare it against any job description to optimize your ATS compatibility.</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# INPUT SECTION
# ═══════════════════════════════════════════════════════════════
st.markdown("---")

input_col1, input_col2 = st.columns(2)

with input_col1:
    st.markdown("<h3 style='margin-bottom:16px;'>📤 Upload Resume</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=["pdf"],
        label_visibility="collapsed",
        help="Upload your resume in PDF format"
    )

    if uploaded_file:
        st.markdown(f"""
        <div style="background:rgba(34,197,94,0.1); border:1px solid #22c55e; border-radius:8px; padding:10px; margin-top:8px;">
            <span style="color:#22c55e;">✅</span> <span style="color:#e2e8f0;">{uploaded_file.name}</span>
            <span style="color:#64748b; font-size:12px;">({uploaded_file.size/1024:.1f} KB)</span>
        </div>
        """, unsafe_allow_html=True)

with input_col2:
    st.markdown("<h3 style='margin-bottom:16px;'>📝 Job Description</h3>", unsafe_allow_html=True)
    job_description = st.text_area(
        "",
        height=200,
        placeholder="Paste the complete job description here...",
        label_visibility="collapsed",
        help="Paste the full job description for comparison"
    )

    if job_description.strip():
        word_count = len(job_description.split())
        st.markdown(f"""
        <div style="text-align:right; color:#64748b; font-size:12px; margin-top:4px;">
            {word_count} words
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ANALYZE BUTTON
# ═══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

# Center the button
col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
with col_btn_center:
    analyze_clicked = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# MAIN LOGIC
# ═══════════════════════════════════════════════════════════════
if analyze_clicked:

    if uploaded_file is None:
        st.error("⚠️ Please upload a resume PDF before analyzing.")
    elif job_description.strip() == "":
        st.error("⚠️ Please paste a job description before analyzing.")
    else:

        # ── Processing Indicator ──
        with st.status("🔍 Analyzing your resume...", expanded=True) as status:
            st.write("Extracting text from PDF...")
            st.write("Processing keywords and skills...")
            st.write("Calculating ATS compatibility score...")
            st.write("Generating insights and recommendations...")

            try:
                # Extract Resume Text
                resume_text = extract_text_from_pdf(uploaded_file)

                # Calculate ATS Results
                results = calculate_ats_score(resume_text, job_description)

                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="❌ Analysis Failed", state="error")
                st.error(f"Error: {str(e)}")
                st.stop()

        # ═══════════════════════════════════════════════════════
        # RESULTS DASHBOARD
        # ═══════════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("<h2 style='text-align:center; margin-bottom:30px;'>📊 ATS Analysis Dashboard</h2>", unsafe_allow_html=True)

        # ── Top Metrics Row ──
        ats_score = results['ats_score']
        similarity = results['similarity_score']
        matched_count = len(results['matched_skills'])
        missing_count = len(results['missing_skills'])
        total_skills = matched_count + missing_count

        # Determine status
        if ats_score >= 80:
            status_text = "EXCELLENT"
            status_class = "status-excellent"
            gauge_color = "#22c55e"
        elif ats_score >= 60:
            status_text = "GOOD"
            status_class = "status-good"
            gauge_color = "#3b82f6"
        else:
            status_text = "NEEDS IMPROVEMENT"
            status_class = "status-low"
            gauge_color = "#ef4444"

        m1, m2, m3, m4, m5 = st.columns(5)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>ATS Score</h3>
                <div class="value" style="color:{gauge_color} !important;">{ats_score}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Similarity</h3>
                <div class="value">{similarity}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Matched</h3>
                <div class="value" style="color:#22c55e !important;">{matched_count}</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Missing</h3>
                <div class="value" style="color:#ef4444 !important;">{missing_count}</div>
            </div>
            """, unsafe_allow_html=True)

        with m5:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Status</h3>
                <div style="margin-top:8px;">
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Gauge Chart ──
        gauge_col1, gauge_col2, gauge_col3 = st.columns([1, 2, 1])
        with gauge_col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ats_score,
                number={'suffix': "%", 'font': {'size': 48, 'color': '#f8fafc'}},
                title={'text': "ATS Compatibility Score", 'font': {'size': 18, 'color': '#94a3b8'}},
                delta={'reference': 80, 'increasing': {'color': "#22c55e"}, 'decreasing': {'color': "#ef4444"}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#334155', 'tickfont': {'color': '#64748b'}},
                    'bar': {'color': gauge_color, 'thickness': 0.75},
                    'bgcolor': '#0f172a',
                    'borderwidth': 2,
                    'bordercolor': '#334155',
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(239,68,68,0.1)'},
                        {'range': [40, 60], 'color': 'rgba(234,179,8,0.1)'},
                        {'range': [60, 80], 'color': 'rgba(59,130,246,0.1)'},
                        {'range': [80, 100], 'color': 'rgba(34,197,94,0.1)'},
                    ],
                    'threshold': {
                        'line': {'color': "#f8fafc", 'width': 3},
                        'thickness': 0.85,
                        'value': 80
                    }
                }
            ))
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Skills Analysis ──
        st.markdown("<h2 style='margin-bottom:20px;'>🔍 Skills Analysis</h2>", unsafe_allow_html=True)

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:
            st.markdown("<h3 style='color:#22c55e !important; margin-bottom:12px;'>✅ Matched Skills</h3>", unsafe_allow_html=True)
            if results['matched_skills']:
                matched_html = " ".join([f'<span class="skill-tag skill-matched">{skill}</span>' for skill in results['matched_skills']])
                st.markdown(f"<div>{matched_html}</div>", unsafe_allow_html=True)
            else:
                st.warning("No matched skills found")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("<h3 style='color:#3b82f6 !important; margin-bottom:12px;'>📋 Skills in Resume</h3>", unsafe_allow_html=True)
            if results['resume_skills']:
                resume_html = " ".join([f'<span class="skill-tag skill-resume">{skill}</span>' for skill in results['resume_skills']])
                st.markdown(f"<div>{resume_html}</div>", unsafe_allow_html=True)
            else:
                st.warning("No skills detected in resume")

        with skill_col2:
            st.markdown("<h3 style='color:#ef4444 !important; margin-bottom:12px;'>❌ Missing Skills</h3>", unsafe_allow_html=True)
            if results['missing_skills']:
                missing_html = " ".join([f'<span class="skill-tag skill-missing">{skill}</span>' for skill in results['missing_skills']])
                st.markdown(f"<div>{missing_html}</div>", unsafe_allow_html=True)
            else:
                st.success("No missing skills — great job!")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Suggestions ──
        st.markdown("---")
        st.markdown("<h2 style='margin-bottom:20px;'>💡 Recommendations</h2>", unsafe_allow_html=True)

        if ats_score >= 80:
            st.markdown("""
            <div style="background:rgba(34,197,94,0.1); border:1px solid #22c55e; border-radius:12px; padding:20px;">
                <h3 style="color:#22c55e !important; margin-bottom:8px;">🎉 Excellent ATS Compatibility</h3>
                <p style="color:#e2e8f0 !important;">Your resume is well-optimized and matches strongly with the job description. You're ready to apply!</p>
            </div>
            """, unsafe_allow_html=True)
        elif ats_score >= 60:
            st.markdown("""
            <div style="background:rgba(59,130,246,0.1); border:1px solid #3b82f6; border-radius:12px; padding:20px;">
                <h3 style="color:#3b82f6 !important; margin-bottom:8px;">👍 Good Match — Room for Improvement</h3>
                <p style="color:#e2e8f0 !important;">Your resume has a decent match. Consider adding more relevant keywords, tools, and skills mentioned in the job description to boost your score above 80%.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(239,68,68,0.1); border:1px solid #ef4444; border-radius:12px; padding:20px;">
                <h3 style="color:#ef4444 !important; margin-bottom:8px;">⚠️ Low ATS Score — Needs Significant Improvement</h3>
                <p style="color:#e2e8f0 !important;">Your resume needs substantial updates. Focus on incorporating the missing skills and keywords from the job description. Tailor your resume specifically for this role.</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Actionable Tips ──
        tips = []
        if missing_count > 0:
            tips.append(f"• Add <b>{missing_count} missing skill(s)</b> to your resume if you have experience with them.")
        if similarity < 70:
            tips.append("• Increase keyword density by mirroring language from the job description.")
        if not results['resume_skills']:
            tips.append("• Your resume may not be parsing correctly. Ensure it's a text-based PDF, not an image.")
        if ats_score < 60:
            tips.append("• Use standard section headings (Experience, Education, Skills) for better parsing.")
            tips.append("• Avoid tables, columns, and graphics that ATS systems can't read.")

        if tips:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#cbd5e1; margin-bottom:12px;'>Quick Actions:</h4>", unsafe_allow_html=True)
            for tip in tips:
                st.markdown(f"<p style='color:#94a3b8; margin:4px 0;'>{tip}</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Resume Preview ──
        st.markdown("---")
        st.markdown("<h2 style='margin-bottom:20px;'>📝 Extracted Resume Text</h2>", unsafe_allow_html=True)

        with st.expander("Click to view extracted resume content", expanded=False):
            st.text_area(
                "Resume Content",
                resume_text,
                height=300,
                label_visibility="collapsed"
            )

        # ── Download Report ──
        st.markdown("<br>", unsafe_allow_html=True)
        report_text = f"""
ATS Resume Analysis Report
{'='*50}

ATS Score: {ats_score}%
Similarity Score: {similarity}%
Status: {status_text}

Matched Skills ({matched_count}):
{chr(10).join(results['matched_skills']) if results['matched_skills'] else 'None'}

Missing Skills ({missing_count}):
{chr(10).join(results['missing_skills']) if results['missing_skills'] else 'None'}

Skills Found in Resume ({len(results['resume_skills'])}):
{', '.join(results['resume_skills']) if results['resume_skills'] else 'None'}

Recommendation:
{'Excellent ATS compatibility. Your resume matches well with the job description.' if ats_score >= 80 else 'Good resume match. Add more relevant keywords and skills to improve your ATS score.' if ats_score >= 60 else 'Low ATS score. Improve your resume by adding more job-relevant keywords, tools, and skills.'}
"""

        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            st.download_button(
                label="📥 Download Analysis Report",
                data=report_text,
                file_name="ats_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )

else:
    # ── Empty State ──
    st.markdown("<br><br>", unsafe_allow_html=True)

    empty_col1, empty_col2, empty_col3 = st.columns([1, 2, 1])
    with empty_col2:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; background:#1e293b; border-radius:16px; border:1px dashed #334155;">
            <div style="font-size:48px; margin-bottom:16px;">📄</div>
            <h3 style="color:#e2e8f0 !important; margin-bottom:8px;">Ready to Analyze</h3>
            <p style="color:#64748b;">Upload your resume and paste a job description,<br>then click <b>Analyze Resume</b> to get started.</p>
        </div>
        """, unsafe_allow_html=True)