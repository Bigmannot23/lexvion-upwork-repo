import streamlit as st
from parser import llm_parse
from retriever import search
from generator import draft_proposal
from scoring import fit_score
from logger import log_event


st.set_page_config(page_title="Upwork Proposal Agent", layout="wide")
st.title("Upwork Proposal Agent (v2.2)")

job_text = st.text_area("Paste an Upwork job post:", height=300)
if st.button("Generate"):
    if not job_text.strip():
        st.warning("Please paste a job post.")
    else:
        job = llm_parse(job_text)
        query = f"{job.title} {' '.join(job.must_have)} {job.summary[:500]}"
        matches = search(query, k=5)
        proposal_md, tags = draft_proposal(job, matches)
        score = fit_score(job.must_have, tags)
        st.subheader(f"Fit Score: {score}/100")
        st.code(proposal_md, language="markdown")
        st.caption("Reminder: manually review before posting to Upwork.")
        # Log event for UI invocation
        log_event({
            "fit_score": score,
            "title": getattr(job, "title", ""),
            "must_have": getattr(job, "must_have", []),
            "response_chars": len(proposal_md),
            "source": "ui",
        })