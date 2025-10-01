# Changelog

## v0.1.0 – 2025‑10‑01

This release prepares the project pack for demonstration.  The Markdown
normalisation script (`scripts/fix_markdown.py`) was applied across all
variant folders (`base`, `sales`, `content`).  The changes focused on
formatting rather than content: fixing inconsistent line endings,
normalising unordered list markers, ensuring blank lines after headings,
replacing non‑breaking spaces with regular spaces and trimming trailing
whitespace.

### Fixed Markdown files

The following files were adjusted for consistency.  Diff snippets show the
structure of the changes; context is abbreviated for brevity.  Note that
spaces were added before the `+`/`-` markers to avoid confusion with this
changelog format.

<details>
<summary><code>base/Project_Summary.md</code></summary>

```diff
@@
   - …one focused revision, ensuring you get exactly what you need, quickly.
   + …one focused revision, ensuring you get exactly what you need, quickly.
```

The summary text was kept intact; only trailing spaces and non‑breaking
spaces were normalised.  A final newline was added.

</details>

<details>
<summary><code>base/Paste‑Into‑Upwork.md</code></summary>

```diff
@@
   - # Paste-Into-Upwork
   + # Paste-Into-Upwork

@@
   - **Search Tags:** AI Workflow, Process Documentation, SOP, Productivity, Automation
   + **Search Tags:** AI Workflow, Process Documentation, SOP, Productivity, Automation
```

Headings were followed by a blank line to conform to ATX heading spacing,
and non‑breaking spaces were replaced with standard spaces.  List markers
and spacing were normalised throughout.

</details>

<details>
<summary><code>sales/Project_Summary.md</code></summary>

```diff
@@
   - …My workflow is designed for speed, clarity and reuse.
   + …My workflow is designed for speed, clarity and reuse.
```

Only spacing normalisation was required; the text itself did not change.

</details>

<details>
<summary><code>sales/Paste‑Into‑Upwork.md</code></summary>

```diff
@@
   - # Paste-Into-Upwork
   + # Paste-Into-Upwork

@@
   - **Project Summary:** Need to transform a messy process into a reliable, **AI‑optimized standard operating procedure**?…
   + **Project Summary:** Need to transform a messy process into a reliable, **AI‑optimized standard operating procedure**?…
```

As with the base variant, headings were given a trailing blank line and
non‑breaking spaces were normalised.

</details>

<details>
<summary><code>content/Project_Summary.md</code></summary>

```diff
@@
   - …provides documentation/training only—no automation or tool setup.
   + …provides documentation/training only—no automation or tool setup.
```

Trailing whitespace and non‑breaking spaces were removed; the narrative
remains unchanged.

</details>

<details>
<summary><code>content/Paste‑Into‑Upwork.md</code></summary>

```diff
@@
   - # Paste-Into-Upwork
   + # Paste-Into-Upwork

@@
   - **FAQs:** Will this work if my process is unclear? Which tools are supported? What does the revision cover?
   + **FAQs:** Will this work if my process is unclear? Which tools are supported? What does the revision cover?
```

A blank line was added after the H1 heading and list markers were
normalised.  No textual content changed.

</details>

### QA summary

After normalisation, the `scripts/qa_check.py` script was run to verify
each variant meets the contract requirements.  The table below
summarises the counts per variant.

| Variant | Summary words | Steps | Deliverables | FAQs | Tags | Status |
|--------:|--------------:|------:|-------------:|-----:|-----:|:------|
| base    | 192           | 4     | 5           | 3    | 5    | pass   |
| sales   | 192           | 4     | 5           | 3    | 5    | pass   |
| content | 184           | 4     | 5           | 3    | 5    | pass   |

All variants fall within the 170–220 word range for the project summary,
include the required scope statement (“documentation/training only — no
automation/tool setup”), and maintain the exact counts for steps,
deliverables, FAQs and tags.  As a result, the QA gate reports **PASS**.
