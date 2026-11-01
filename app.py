"""GenAI in Business: responsible customer-support draft evaluation dashboard.

No generative-AI API is called. All cases and replies are fictional examples.
"""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
CASES_FILE = OUT / "customer_support_cases_and_drafts.csv"
RUBRIC_FILE = OUT / "human_scoring_checklist.csv"
PROMPT_FILE = ROOT / "prompt_template.md"

st.set_page_config(
    page_title="SupportSense AI | GenAI in Business",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root {color-scheme: dark;}
.stApp {background: linear-gradient(150deg, #081126 0%, #101b39 55%, #11102c 100%); color: #edf3ff;}
[data-testid="stSidebar"] {background: #0b1630; border-right: 1px solid #303c63;}
h1, h2, h3, h4, p, label, [data-testid="stWidgetLabel"] {color: #edf3ff;}
[data-testid="stMarkdownContainer"] p {line-height: 1.65;}
[data-testid="stMetric"] {background: #152347; padding: 15px; border: 1px solid #3a4a77; border-radius: 14px;}
[data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * {color: #f2f6ff !important;}
[data-testid="stSelectbox"] label, [data-testid="stTextArea"] label,
[data-testid="stRadio"] label, [data-testid="stSlider"] label {color: #f2f6ff !important;}
div[data-baseweb="select"] > div {background: #172647; color: white; border-color: #4b5d89;}
.hero {background: linear-gradient(105deg, #263d90 0%, #5b35b0 100%); border: 1px solid #7c78e4;
       border-radius: 20px; padding: 22px 27px; margin: 0 0 18px 0;}
.hero h1 {font-size: 2.1rem; margin: 0 0 8px 0; color: #fff;}
.hero p {font-size: 1.02rem; margin: 0; color: #e8eafa;}
.casebox {background: #152346; border: 1px solid #3b4d7f; padding: 19px; border-radius: 14px; margin: 8px 0 15px;}
.casebox p {white-space: pre-wrap; margin: 0; color: #f3f6ff;}
.casebox .small {color: #bac8f7; font-weight: 700; margin-bottom: 7px; font-size: .86rem;}
.note {color: #b9c8e6; font-size: 0.92rem;}
[data-testid="stAlert"] {border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    if not CASES_FILE.exists() or not RUBRIC_FILE.exists():
        return None, None
    cases = pd.read_csv(CASES_FILE, dtype=str).fillna("")
    rubric = pd.read_csv(RUBRIC_FILE, dtype=str).fillna("")
    required_case_cols = {"id", "category", "customer_enquiry", "known_facts", "desired_action", "human_escalation", "draft_reply"}
    required_rubric_cols = {"case_id", "criterion", "what_to_check"}
    if not required_case_cols.issubset(cases.columns) or not required_rubric_cols.issubset(rubric.columns):
        raise ValueError("The CSV files do not contain the expected columns. Run customer_support_exercise.py again.")
    return cases, rubric

try:
    cases, rubric = load_data()
except (ValueError, pd.errors.ParserError) as exc:
    st.error(f"Unable to read project data: {exc}")
    st.stop()

if cases is None:
    st.error("Missing CSV files. In the VS Code terminal, first run: python customer_support_exercise.py")
    st.code("python customer_support_exercise.py", language="powershell")
    st.stop()

case_ids = cases["id"].tolist()
criteria = rubric["criterion"].drop_duplicates().tolist()
if "ratings" not in st.session_state:
    # Blank scores are intentional: the reviewer must decide each score.
    st.session_state.ratings = {}
if "review_notes" not in st.session_state:
    st.session_state.review_notes = {}

st.sidebar.markdown("## 💬 SupportSense AI")
st.sidebar.caption("GenAI in Business · Responsible AI Evaluation")
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Review customer drafts", "Scoring dashboard", "Prompt & governance"],
)
st.sidebar.divider()
st.sidebar.info("This is a simulated exercise. Drafts are pre-written examples; no AI API, customer accounts, or messaging service is connected.")

st.markdown("""
<div class="hero">
<h1>SupportSense AI</h1>
<p>Customer-support draft assistant · Five synthetic cases · Human-led responsible AI assessment</p>
</div>
""", unsafe_allow_html=True)

all_keys = [(cid, crit) for cid in case_ids for crit in criteria]
scored_count = sum(st.session_state.ratings.get(k) is not None for k in all_keys)
points = sum(v for v in st.session_state.ratings.values() if v is not None)
max_points = len(all_keys) * 2
completed_cases = sum(all(st.session_state.ratings.get((cid, crit)) is not None for crit in criteria) for cid in case_ids)

if page == "Overview":
    st.subheader("Exercise overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Synthetic enquiries", len(case_ids))
    m2.metric("Evaluation criteria", len(criteria))
    m3.metric("Cases fully reviewed", f"{completed_cases}/{len(case_ids)}")
    m4.metric("Scoring progress", f"{scored_count}/{len(all_keys)}")
    st.markdown("### The five customer enquiries")
    st.dataframe(cases[["id", "category", "customer_enquiry"]], hide_index=True, use_container_width=True)
    st.markdown("### How to complete the assessment")
    st.markdown("1. Open **Review customer drafts** and choose a case.\n"
                "2. Read the enquiry, verified facts and example draft.\n"
                "3. Score **accuracy, bias/fairness, privacy, transparency and human escalation** from 0 to 2.\n"
                "4. Add reviewer notes, particularly for weak or partial scores.\n"
                "5. Open **Scoring dashboard** and download your completed evaluation CSV.")
    st.caption("0 = does not meet requirement · 1 = partly meets · 2 = fully meets")

elif page == "Review customer drafts":
    st.subheader("Review and score a draft")
    selected_id = st.selectbox("Choose customer enquiry", case_ids,
                               format_func=lambda cid: f"{cid} — {cases.loc[cases['id'] == cid, 'category'].iloc[0]}")
    case = cases.loc[cases["id"] == selected_id].iloc[0]
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        st.markdown("#### Customer enquiry")
        st.markdown(f'<div class="casebox"><div class="small">{selected_id} · {case["category"]}</div><p>{case["customer_enquiry"]}</p></div>', unsafe_allow_html=True)
        st.markdown("**Known facts / constraints**")
        st.write(case["known_facts"])
        st.markdown("**Desired support action**")
        st.write(case["desired_action"])
        st.markdown("**Human escalation rule**")
        st.write(case["human_escalation"])
    with right:
        st.markdown("#### Example draft reply")
        st.text_area("Draft for evaluation (read-only)", value=case["draft_reply"], height=245,
                     disabled=True, key=f"draft_{selected_id}")
        st.caption("Prepared sample text; not generated live and not sent to a customer.")

    st.markdown("### Human reviewer scoring")
    st.caption("Select a score for each criterion. Scores start as Not scored and are not assigned automatically.")
    for _, row in rubric.loc[rubric["case_id"] == selected_id].iterrows():
        crit = row["criterion"]
        k = (selected_id, crit)
        options = ["Not scored", "0 — Not met", "1 — Partly met", "2 — Fully met"]
        existing = st.session_state.ratings.get(k)
        index = 0 if existing is None else int(existing) + 1
        lcol, rcol = st.columns([1.45, 1], gap="medium")
        with lcol:
            st.markdown(f"**{crit}**")
            st.caption(row["what_to_check"])
        with rcol:
            choice = st.selectbox(f"Score: {crit}", options, index=index, key=f"select_{selected_id}_{crit}")
            st.session_state.ratings[k] = None if choice == "Not scored" else int(choice[0])
        st.divider()
    notes = st.text_area("Reviewer notes and improvements", value=st.session_state.review_notes.get(selected_id, ""),
                         placeholder="Explain any score below 2 and any improvements needed before human approval.",
                         key=f"notes_{selected_id}", height=110)
    st.session_state.review_notes[selected_id] = notes
    this_scores = [st.session_state.ratings.get((selected_id, c)) for c in criteria]
    if all(x is not None for x in this_scores):
        st.success(f"Review completed: {sum(this_scores)} / {len(criteria)*2} points. Visit Scoring dashboard to export.")
    else:
        st.info(f"Review in progress: {sum(x is not None for x in this_scores)} of {len(criteria)} criteria scored.")

elif page == "Scoring dashboard":
    st.subheader("Human evaluation results")
    a, b, c = st.columns(3)
    a.metric("Points awarded", f"{points}/{max_points}")
    b.metric("Criteria scored", f"{scored_count}/{len(all_keys)}")
    c.metric("Completed cases", f"{completed_cases}/{len(case_ids)}")

    # Preserve blank/unscored entries in downloads. Never treat them as zero scores.
    results = rubric.copy()
    results["score_0_to_2"] = [
        "" if st.session_state.ratings.get((row.case_id, row.criterion)) is None
        else str(st.session_state.ratings[(row.case_id, row.criterion)])
        for row in results.itertuples(index=False)
    ]
    results["reviewer_notes"] = [st.session_state.review_notes.get(cid, "") for cid in results["case_id"]]

    per_case = []
    for cid in case_ids:
        scores = [st.session_state.ratings.get((cid, crit)) for crit in criteria]
        per_case.append({
            "case_id": cid,
            "category": cases.loc[cases["id"] == cid, "category"].iloc[0],
            "criteria_scored": sum(s is not None for s in scores),
            "points_awarded": sum(s for s in scores if s is not None),
            "max_points": len(criteria) * 2,
            "review_status": "Complete" if all(s is not None for s in scores) else "Incomplete",
        })
    summary = pd.DataFrame(per_case)
    st.dataframe(summary, hide_index=True, use_container_width=True)
    if scored_count:
        st.markdown("#### Points awarded so far by case")
        st.bar_chart(summary.set_index("case_id")["points_awarded"], y_label="Points (0–10)")
    else:
        st.info("No scores yet. Begin reviewing drafts to populate this chart.")
    st.markdown("#### Download evaluation")
    st.download_button(
        "⬇ Download human scoring checklist (CSV)",
        data=results.to_csv(index=False).encode("utf-8-sig"),
        file_name="completed_human_scoring_checklist.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.download_button(
        "⬇ Download case-by-case score summary (CSV)",
        data=summary.to_csv(index=False).encode("utf-8-sig"),
        file_name="customer_support_evaluation_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.warning("Scores are held only in this browser session. Download your CSV before restarting the app or closing the session. Incomplete ratings remain blank in the export.")
    st.caption("The dashboard records a human assessment; a high score does not approve a draft for real customer use.")

else:
    st.subheader("Reusable prompt and responsible-AI controls")
    if PROMPT_FILE.exists():
        st.code(PROMPT_FILE.read_text(encoding="utf-8"), language="markdown")
    else:
        st.warning("prompt_template.md was not found in the project folder.")
    st.markdown("### Responsible use")
    st.markdown("- **Accuracy:** No invented delivery updates, refunds or policy commitments.\n"
                "- **Bias and fairness:** Respectful, accessible, consistent treatment.\n"
                "- **Privacy:** No passwords, payment-card numbers, one-time codes or unnecessary personal data.\n"
                "- **Transparency:** Clearly state limitations and distinguish drafts from completed actions.\n"
                "- **Human escalation:** Security, billing disputes, safety and unresolved requests require authorised review.")
    st.info("This app is for training and demonstration with synthetic enquiries only. It does not use an API key, generate new model responses, or contact real customers.")
