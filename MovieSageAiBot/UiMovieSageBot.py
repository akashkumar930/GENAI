import json
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MovieSage AI",
    page_icon="🎬",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0D0D0F;
    color: #E8E4DC;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

/* Hero */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    border-bottom: 1px solid #2A2A30;
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #C9A84C;
    font-weight: 500;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.6rem, 5vw, 4rem);
    color: #F0EBE0;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #8A8680;
    font-weight: 300;
    letter-spacing: 0.01em;
}

/* Textarea + button */
[data-testid="stTextArea"] textarea {
    background: #16161A !important;
    border: 1px solid #2E2E36 !important;
    border-radius: 8px !important;
    color: #E8E4DC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 1rem !important;
    resize: vertical;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.18) !important;
}
[data-testid="stTextArea"] label {
    color: #A09A92 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

[data-testid="stButton"] > button {
    background: #C9A84C !important;
    color: #0D0D0F !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em;
    padding: 0.65rem 2.4rem !important;
    border: none !important;
    border-radius: 6px !important;
    transition: opacity 0.15s;
}
[data-testid="stButton"] > button:hover { opacity: 0.88; }

/* Result cards */
.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    margin-top: 0.5rem;
}
.card {
    background: #16161A;
    border: 1px solid #2A2A30;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
}
.card-label {
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #C9A84C;
    font-weight: 600;
    margin-bottom: 0.35rem;
}
.card-value {
    font-size: 0.95rem;
    color: #E8E4DC;
    font-weight: 400;
    line-height: 1.5;
}
.card-value.null-val { color: #4A4A52; font-style: italic; }

/* Summary block */
.summary-block {
    background: #16161A;
    border-left: 3px solid #C9A84C;
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
    font-family: 'DM Serif Display', serif;
    font-size: 1.08rem;
    color: #D8D2C6;
    line-height: 1.7;
}

/* Tag pills */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.3rem; }
.tag {
    background: #1E1E26;
    border: 1px solid #3A3A44;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem;
    color: #B0AAA0;
}

/* Section heading */
.section-heading {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #5A5A62;
    font-weight: 500;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1E1E26;
}

/* Error */
.error-box {
    background: #1A0D0D;
    border: 1px solid #5C2020;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    color: #E07070;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ── Prompt template ───────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are MovieSage AI, an expert movie summarization assistant.

Your task is to analyze a raw paragraph about a movie and extract the most important information.

Instructions:
1. Read the input carefully.
2. Identify the key details about the movie.
3. Ignore unnecessary descriptions, repetition, opinions, or marketing language.
4. Generate a concise, objective summary.
5. Return ONLY valid JSON.
6. Do not include Markdown, explanations, or code blocks.
7. Never hallucinate unknown parameters; return null when information is unavailable.

Extract the following fields whenever possible:
- title
- genre (array)
- director
- cast (array)
- release_year
- setting
- main_characters (array)
- plot
- conflict
- climax
- ending
- themes (array)
- mood
- rating (if mentioned)
- runtime (if mentioned)
- summary (2–4 sentences)

If any information is not available, use null for that field.

Output format:

{{
  "title": null,
  "genre": [],
  "director": null,
  "cast": [],
  "release_year": null,
  "setting": null,
  "main_characters": [],
  "plot": null,
  "conflict": null,
  "climax": null,
  "ending": null,
  "themes": [],
  "mood": null,
  "rating": null,
  "runtime": null,
  "summary": null
}}
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Analyze the following movie description and extract all relevant information.\n\nMovie Description:\n{movie_description}")
])


@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2603")


def analyze_movie(description: str) -> dict:
    model = get_model()
    final_prompt = prompt_template.invoke({"movie_description": description})
    res = model.invoke(final_prompt)
    return json.loads(res.content)


def fmt(val):
    """Format a value for display."""
    if val is None:
        return '<span class="null-val">—</span>'
    if isinstance(val, list):
        if not val:
            return '<span class="null-val">—</span>'
        return val
    return str(val)


def card(label, value):
    if isinstance(value, list):
        tags_html = "".join(f'<span class="tag">{v}</span>' for v in value) if value else '<span class="null-val">—</span>'
        inner = f'<div class="tag-row">{tags_html}</div>'
    else:
        inner = f'<div class="card-value">{fmt(value)}</div>'
    return f'<div class="card"><div class="card-label">{label}</div>{inner}</div>'


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by Mistral AI</div>
    <div class="hero-title">MovieSage AI</div>
    <div class="hero-sub">Paste any movie description — get a structured breakdown in seconds.</div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_gap = st.columns([3, 1])
with col_input:
    description = st.text_area(
        "Movie description",
        placeholder="Paste a synopsis, plot summary, or any paragraph about a movie…",
        height=180,
    )
    analyze_btn = st.button("Analyze →")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not description.strip():
        st.markdown('<div class="error-box">Please enter a movie description before analyzing.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Reading between the frames…"):
            try:
                data = analyze_movie(description)

                # Summary
                if data.get("summary"):
                    st.markdown(f'<div class="summary-block">{data["summary"]}</div>', unsafe_allow_html=True)

                # Identity row
                st.markdown('<div class="section-heading">Identity</div>', unsafe_allow_html=True)
                identity_cards = "".join([
                    card("Title", data.get("title")),
                    card("Release Year", data.get("release_year")),
                    card("Director", data.get("director")),
                    card("Rating", data.get("rating")),
                    card("Runtime", data.get("runtime")),
                    card("Mood", data.get("mood")),
                ])
                st.markdown(f'<div class="result-grid">{identity_cards}</div>', unsafe_allow_html=True)

                # Tags row
                st.markdown('<div class="section-heading">Tags</div>', unsafe_allow_html=True)
                tags_cards = "".join([
                    card("Genre", data.get("genre", [])),
                    card("Themes", data.get("themes", [])),
                    card("Cast", data.get("cast", [])),
                    card("Main Characters", data.get("main_characters", [])),
                ])
                st.markdown(f'<div class="result-grid">{tags_cards}</div>', unsafe_allow_html=True)

                # Narrative row
                st.markdown('<div class="section-heading">Narrative</div>', unsafe_allow_html=True)
                narrative_cards = "".join([
                    card("Setting", data.get("setting")),
                    card("Plot", data.get("plot")),
                    card("Conflict", data.get("conflict")),
                    card("Climax", data.get("climax")),
                    card("Ending", data.get("ending")),
                ])
                st.markdown(f'<div class="result-grid">{narrative_cards}</div>', unsafe_allow_html=True)

                # Raw JSON expander
                with st.expander("Raw JSON"):
                    st.json(data)

            except json.JSONDecodeError:
                st.markdown('<div class="error-box">The model returned an unexpected format. Try again or rephrase your description.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-box">Something went wrong: {e}</div>', unsafe_allow_html=True)