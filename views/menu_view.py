# -*- coding: utf-8 -*-
"""[VIEW] Menu inicial — equivalente a src/pages/Menu.tsx."""

import streamlit as st

from controllers import auth_controller, session_controller
from models import seed_data as data
from views.components import TEXT_DARK, TEXT_MUTED, badge_html

ALL_CARDS = [
    {
        "to": "dashboard", "roles": ["Professor", "Coordenador", "Administrador"],
        "icon": "📊", "label": "Dashboard",
        "desc": "Visualize informações e indicadores importantes do sistema.",
        "color": "#8B0019", "bg": "#FFF0F2",
    },
    {
        "to": "reservas", "roles": ["Aluno", "Professor", "Coordenador", "Administrador"],
        "icon": "🗓️",
        "label": lambda role: "Ambientes e Solicitações" if role == "Aluno" else "Reservas",
        "desc": lambda role: (
            "Consulte salas disponíveis e envie solicitações de reserva."
            if role == "Aluno" else
            "Consulte, crie e gerencie reservas de ambientes."
        ),
        "color": "#1E5E60", "bg": "#E3ECEE",
    },
    {
        "to": "membros", "roles": ["Administrador"],
        "icon": "👥", "label": "Membros",
        "desc": "Gerencie os membros e organize as informações da equipe.",
        "color": "#3C5E53", "bg": "#E8EFE2",
    },
]

WELCOME_MSG = {
    "Aluno": "Consulte ambientes disponíveis e envie suas solicitações.",
    "Professor": "Gerencie reservas e responda às solicitações dos seus alunos.",
    "Coordenador": "Acompanhe as reservas e autorize solicitações especiais.",
    "Administrador": "Gerencie reservas, ambientes e membros em um só lugar.",
}


def render():
    user = auth_controller.current_user()
    rc = data.ROLE_COLORS[user["role"]]

    st.markdown("<div style='text-align:center; padding-top:2rem;'>", unsafe_allow_html=True)
    st.markdown(badge_html(user["role"], rc["bg"], rc["text"], rc["dot"]), unsafe_allow_html=True)
    st.markdown(
        f"<h1 style='color:{TEXT_DARK}; font-weight:800; margin-top:0.8rem;'>"
        f"Olá, {user['nome'].split(' ')[0]}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color:{TEXT_MUTED};'>{WELCOME_MSG[user['role']]}</p></div>",
        unsafe_allow_html=True,
    )
    st.write("")

    cards = [c for c in ALL_CARDS if user["role"] in c["roles"]]
    cols = st.columns(len(cards)) if cards else []
    for col, card in zip(cols, cards):
        label = card["label"](user["role"]) if callable(card["label"]) else card["label"]
        desc = card["desc"](user["role"]) if callable(card["desc"]) else card["desc"]
        with col:
            with st.container(border=True):
                st.markdown(
                    f"<div style='width:48px;height:48px;border-radius:12px;background:{card['bg']};"
                    f"display:flex;align-items:center;justify-content:center;font-size:1.4rem;'>"
                    f"{card['icon']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{label}**")
                st.caption(desc)
                if st.button("Acessar →", key=f"menu_{card['to']}", use_container_width=True):
                    session_controller.goto(card["to"])
                    st.rerun()

    st.write("")
    st.markdown(
        f"<p style='text-align:center; color:{TEXT_MUTED}; font-size:0.75rem;'>SGA · v2.4.1</p>",
        unsafe_allow_html=True,
    )
