from jinja2 import Template
from typing import List, Tuple


def summarize_matches(matches: List[Tuple[dict,float]]):
    lines, proofs, tags = [], [], set()
    for rec, score in matches:
        lines.append(f"- {rec['title']} ({int(score*100)}% match): {rec['impact']}")
        if rec.get("link"): proofs.append(rec["link"])
        for t in rec.get("tags", []): tags.add(t)
    return "\n".join(lines), ", ".join(proofs[:3]), sorted(tags)


def draft_proposal(job, matches, price="Fixed bid after scope call", timeline="1–2 weeks"):
    match_summary, proofs, tags = summarize_matches(matches)
    # Resolve the template relative to this file
    import os
    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, "prompts", "proposal_template.md")
    with open(template_path) as f:
        tmpl = Template(f.read())
    rendered = tmpl.render(
        title=job.title,
        relevant_experience=match_summary or "- Relevant prior work available on request",
        proofs=proofs or "Portfolio available on request",
        deliverables=job.deliverables,
        timeline=job.timeline or timeline,
        price=price,
        risks=job.risks or ["Scope risk if access/data delayed"]
    )
    return rendered, tags