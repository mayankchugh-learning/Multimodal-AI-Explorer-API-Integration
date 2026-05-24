"""Render Mermaid diagrams in Streamlit (visual + source)."""

from __future__ import annotations

import html
import re

import streamlit as st
import streamlit.components.v1 as components


def extract_mermaid(markdown_block: str) -> str:
    """Pull raw Mermaid from a ```mermaid fenced block or return as-is."""
    text = markdown_block.strip()
    match = re.search(r"```mermaid\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text


def render_mermaid_diagram(
    mermaid_source: str,
    *,
    height: int = 380,
    caption: str | None = None,
) -> None:
    """Render interactive Mermaid inside an iframe (works offline after first CDN load)."""
    body = html.escape(mermaid_source.strip())
    if caption:
        st.caption(caption)
    components.html(
        f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
  <style>
    body {{
      font-family: system-ui, sans-serif;
      margin: 0;
      padding: 12px;
      background: #fafafa;
    }}
    .mermaid {{
      display: flex;
      justify-content: center;
    }}
  </style>
</head>
<body>
  <pre class="mermaid">{body}</pre>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: "neutral",
      securityLevel: "loose",
      flowchart: {{ useMaxWidth: true, htmlLabels: true }}
    }});
  </script>
</body>
</html>
        """,
        height=height,
        scrolling=True,
    )


def render_diagram_block(
    mermaid_source: str,
    ascii_diagram: str,
    *,
    title: str,
    height: int = 380,
    source_expanded: bool = False,
) -> None:
    """Visual Mermaid + ASCII fallback + optional Mermaid source."""
    st.markdown(f"**{title}** — visual diagram")
    render_mermaid_diagram(mermaid_source, height=height)

    st.markdown("**ASCII diagram** (quick reference / slides)")
    st.code(ascii_diagram, language=None)

    with st.expander("View Mermaid source (edit in notebooks / GitHub)", expanded=source_expanded):
        st.code(mermaid_source, language="markdown")
