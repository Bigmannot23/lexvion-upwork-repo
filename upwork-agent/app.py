import os, sys
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    # Fallback when python-dotenv is unavailable
    def load_dotenv(*args, **kwargs):
        return None
from parser import llm_parse
from retriever import search
from generator import draft_proposal
from scoring import fit_score
from logger import log_event

load_dotenv()


def main():
    job_text = sys.stdin.read() if not sys.argv[1:] else open(sys.argv[1]).read()
    job = llm_parse(job_text)
    query = f"{job.title} {' '.join(job.must_have)} {job.summary[:500]}"
    matches = search(query, k=5)
    proposal, tags = draft_proposal(job, matches)
    score = fit_score(job.must_have, tags)
    out = "proposal.md"
    # Write proposal to file with fit score appended
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(proposal + f"\n\n---\nFit Score: {score}/100\n")
    # Log event (CSV or Sheets)
    log_event({
        "fit_score": score,
        "title": getattr(job, "title", ""),
        "must_have": getattr(job, "must_have", []),
        "response_chars": len(proposal),
        "source": "cli",
    })
    print(f"[OK] Generated {out} | Fit Score: {score}/100")


if __name__ == "__main__":
    main()