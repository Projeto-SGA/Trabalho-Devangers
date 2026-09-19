# -*- coding: utf-8 -*-
"""
[VIEW] Estilos CSS globais e componentes visuais reutilizáveis do SGA.

Puramente apresentação: nenhuma função aqui lê ou grava em st.session_state
nem contém regra de negócio.
"""

import streamlit as st

PRIMARY = "#8B0019"
PRIMARY_DARK = "#700010"
BG = "#FAF9F6"
SIDEBAR_BG = "#14120D"
SIDEBAR_BORDER = "#2A2620"
TEXT_DARK = "#1E1B15"
TEXT_MED = "#3D382E"
TEXT_MUTED = "#776D5B"
TEXT_FAINT = "#A8A09A"
BORDER = "#E7E0D5"
CARD_BG = "#FFFFFF"
SOFT_BG = "#F5F2EB"
DIVIDER = "#F3EFEA"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {BG}; }}
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{ padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1200px; }}

        /* Sidebar look */
        section[data-testid="stSidebar"] {{
            background-color: {SIDEBAR_BG};
        }}
        section[data-testid="stSidebar"] * {{ color: #FAF9F6; }}
        section[data-testid="stSidebar"] .stButton button {{
            background-color: transparent;
            color: #C9C3B8;
            border: none;
            text-align: left;
            width: 100%;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.85rem;
            padding: 0.5rem 0.75rem;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background-color: rgba(255,255,255,0.06);
            color: #FAF9F6;
        }}
        section[data-testid="stSidebar"] .nav-active button {{
            background-color: {PRIMARY} !important;
            color: white !important;
        }}

        /* Generic card */
        .sga-card {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1.25rem 1.4rem;
        }}
        .sga-eyebrow {{
            color: {PRIMARY};
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 2px;
        }}
        .sga-title {{ color: {TEXT_DARK}; font-size: 1.5rem; font-weight: 800; margin: 0; }}
        .sga-subtitle {{ color: {TEXT_MUTED}; font-size: 0.85rem; margin-top: 4px; }}

        .badge {{
            display: inline-flex; align-items: center; gap: 6px;
            padding: 3px 10px; border-radius: 999px;
            font-size: 0.72rem; font-weight: 600;
        }}
        .badge-dot {{ width: 6px; height: 6px; border-radius: 50%; display: inline-block; }}

        div[data-testid="stMetric"] {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1rem 1.1rem;
        }}

        .stButton>button[kind="primary"] {{
            background-color: {PRIMARY};
            border-color: {PRIMARY};
        }}
        .stButton>button[kind="primary"]:hover {{
            background-color: {PRIMARY_DARK};
            border-color: {PRIMARY_DARK};
        }}
        hr {{ border-color: {DIVIDER}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def badge_html(label: str, bg: str, color: str, dot: str | None = None) -> str:
    dot_html = f'<span class="badge-dot" style="background-color:{dot}"></span>' if dot else ""
    return (
        f'<span class="badge" style="background-color:{bg};color:{color}">'
        f'{dot_html}{label}</span>'
    )


def page_header(eyebrow: str, title: str, subtitle: str = ""):
    st.markdown(f'<div class="sga-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sga-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sga-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.write("")


def card_open():
    st.markdown('<div class="sga-card">', unsafe_allow_html=True)


def card_close():
    st.markdown('</div>', unsafe_allow_html=True)


def toast_ok(msg: str):
    st.toast(msg, icon="✅")


def toast_err(msg: str):
    st.toast(msg, icon="⚠️")
