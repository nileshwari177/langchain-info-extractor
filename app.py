from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
import streamlit as st
import streamlit.components.v1 as components
import os

load_dotenv()

from langchain_mistralai import ChatMistralAI

st.set_page_config(page_title="Movie Info Extractor", page_icon="🎬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #0d0d0d; color: #f0ebe3; }
.stButton > button {
    background: #f5c842 !important;
    color: #0d0d0d !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 8px !important;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stTextArea textarea {
    background-color: #1a1a1a !important;
    color: #f0ebe3 !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: #f5c842 !important;
    box-shadow: 0 0 0 1px #f5c842 !important;
}
label { color: #aaa !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding: 2rem 0 0.5rem 0;">
    <h1 style="font-family:'Playfair Display',serif; font-size:2.8rem; color:#f5c842; margin-bottom:0.3rem;">🎬 Movie Info Extractor</h1>
    <p style="color:#888; font-size:1rem; font-weight:300;">Paste a paragraph about any movie and get structured details instantly</p>
</div>
<div style="height:1px; background:linear-gradient(to right, transparent, #f5c842, transparent); margin:1.2rem 0 1.8rem 0;"></div>
""", unsafe_allow_html=True)


class MovieInfo(BaseModel):
    movie_name: Optional[str] = None
    director: Optional[str] = None
    release_year: Optional[str] = None
    genre: Optional[str] = None
    main_cast: Optional[List[str]] = None
    plot_overview: Optional[str] = None
    key_themes: Optional[List[str]] = None
    rating: Optional[str] = None
    soundtrack_composer: Optional[str] = None
    notable_features: Optional[List[str]] = None


parser = PydanticOutputParser(pydantic_object=MovieInfo)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Extract the most useful information about a movie from the given paragraph.
     Do NOT generate a summary. {format_instructions}"""),
    ("human", "Here is the paragraph: {paragraph}")
])


def render_value(val):
    not_mentioned = '<span style="color:#555; font-size:0.9rem; font-style:italic;">Not Mentioned</span>'
    if val is None:
        return not_mentioned
    if isinstance(val, list):
        if not val:
            return not_mentioned
        tags = "".join(
            '<span style="display:inline-block; background:#252525; border:1px solid #383838;'
            'border-radius:20px; padding:3px 14px; font-size:0.82rem; color:#d4cfc8; margin:2px 3px;">'
            + item + '</span>'
            for item in val
        )
        return '<div style="margin-top:3px; flex:1;">' + tags + '</div>'
    return '<span style="color:#e0d8ce; font-size:0.93rem; line-height:1.6; flex:1;">' + str(val) + '</span>'


def field_row(label, icon, val):
    return (
        '<div style="display:flex; align-items:flex-start; gap:12px; padding:12px 0;'
        'border-bottom:1px solid #1e1e1e;">'
        '<div style="min-width:180px; display:flex; align-items:center; gap:6px;">'
        '<span style="font-size:0.95rem;">' + icon + '</span>'
        '<span style="color:#f5c842; font-weight:500; font-size:0.75rem; text-transform:uppercase;'
        'letter-spacing:0.06em;">' + label + '</span>'
        '</div>'
        + render_value(val) +
        '</div>'
    )


paragraph = st.text_area(
    "Movie Paragraph",
    placeholder="e.g. Interstellar is a 2014 sci-fi film directed by Christopher Nolan...",
    height=160
)

extract_btn = st.button("Extract Information")

if extract_btn:
    if not paragraph.strip():
        st.warning("Please enter a paragraph to extract information from.")
    else:
        with st.spinner("Extracting movie details..."):
            try:
                model = ChatMistralAI(model='mistral-small-2506')
                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })
                response = model.invoke(final_prompt)
                movie: MovieInfo = parser.parse(response.content)

                fields = [
                    ("Movie Name",            "🎬", movie.movie_name),
                    ("Director",              "🎥", movie.director),
                    ("Release Year",          "📅", movie.release_year),
                    ("Genre",                 "🎭", movie.genre),
                    ("Main Cast",             "🌟", movie.main_cast),
                    ("Plot / Story Overview", "📖", movie.plot_overview),
                    ("Key Themes",            "💡", movie.key_themes),
                    ("Rating",                "⭐", movie.rating),
                    ("Soundtrack Composer",   "🎵", movie.soundtrack_composer),
                    ("Notable Features",      "🏆", movie.notable_features),
                ]

                rows_html = "".join(field_row(label, icon, val) for label, icon, val in fields)

                full_html = """
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: transparent; font-family: 'DM Sans', sans-serif; padding: 4px 2px; }
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #111; border-radius: 10px; }
  ::-webkit-scrollbar-thumb { background: #f5c842; border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: #e0b830; }
</style>
</head>
<body>
<div style="background:#161616; border:1px solid #272727; border-radius:14px; padding:1.6rem 1.8rem; box-shadow:0 4px 32px rgba(0,0,0,0.4);">
  <div style="display:flex; align-items:center; gap:10px; margin-bottom:1.2rem; padding-bottom:1rem; border-bottom:2px solid #f5c842;">
    <span style="font-size:1.4rem;">🎞️</span>
    <h3 style="font-family:'Playfair Display',serif; color:#f5c842; font-size:1.4rem; font-weight:700;">Extracted Details</h3>
  </div>
""" + rows_html + """
</div>
<script>
  // Auto-resize: tell parent iframe to match content height
  window.onload = function() {
    var h = document.body.scrollHeight;
    window.parent.postMessage({type: 'streamlit:setFrameHeight', height: h + 20}, '*');
  };
</script>
</body>
</html>
"""

                components.html(full_html, height=700, scrolling=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")