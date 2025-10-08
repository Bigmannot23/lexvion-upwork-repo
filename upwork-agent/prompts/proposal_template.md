# Proposal: {{ title }}

**Why Me**
- Direct experience:
{{ relevant_experience }}
- Proof: {{ proofs }}

**Plan**
{% for d in deliverables -%}
- {{ d }}
{% endfor %}

**Timeline & Milestones**
{{ timeline }}

**Price**
{{ price }}

**Assumptions / Risks**
{% for r in risks -%}
- {{ r }}
{% endfor %}

**Next Steps**
- Share sample data/access
- 15-min alignment call