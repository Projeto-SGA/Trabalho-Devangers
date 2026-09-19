# -*- coding: utf-8 -*-
"""[VIEW] Layout compartilhado — sidebar de navegação e tela de acesso negado.
Equivalente a components/Sidebar.tsx + components/ProtectedRoute.tsx."""

import streamlit as st

from controllers import auth_controller, session_controller
from models import seed_data as data

# Itens de navegação (equivalente a Sidebar.tsx navItems)
NAV_ITEMS = [
    {"key": "dashboard", "label": "📊 Dashboard", "roles": ["Professor", "Coordenador", "Administrador"]},
    {"key": "reservas", "label": "🗓️ Reservas", "roles": ["Aluno", "Professor", "Coordenador", "Administrador"],
     "label_aluno": "🗓️ Minhas Solicitações"},
    {"key": "academico", "label": "🎓 Acadêmico", "roles": ["Administrador", "Coordenador"]},
    {"key": "membros", "label": "👥 Membros", "roles": ["Administrador"]},
    {"key": "configuracoes", "label": "⚙️ Configurações", "roles": ["Aluno", "Professor", "Coordenador", "Administrador"]},
]


def render_sidebar():
    user = auth_controller.current_user()
    rc = data.ROLE_COLORS[user["role"]]

    with st.sidebar:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; padding: 4px 0 18px;
                        border-bottom: 1px solid #2A2620; margin-bottom: 14px;">
                <div style="width:38px;height:38px;border-radius:10px;background:#FAF9F6;
                            display:flex;align-items:center;justify-content:center;
                            color:{data.ROLE_COLORS['Administrador']['text']};font-weight:800;font-size:0.75rem;">
                    SGA
                </div>
                <div>
                    <div style="font-size:0.8rem;font-weight:700;color:#FAF9F6;">SGA</div>
                    <div style="font-size:0.7rem;color:#776D5B;">Gestão de Ambientes</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='font-size:0.68rem;color:#4A4540;letter-spacing:0.06em;'>NAVEGAÇÃO</div>",
                    unsafe_allow_html=True)

        visible = [item for item in NAV_ITEMS if user["role"] in item["roles"]]
        for item in visible:
            label = item.get("label_aluno") if (item["key"] == "reservas" and user["role"] == "Aluno") else item["label"]
            is_active = session_controller.current_route() == item["key"]
            btn_container = st.container()
            with btn_container:
                if is_active:
                    st.markdown('<div class="nav-active">', unsafe_allow_html=True)
                clicked = st.button(label, key=f"nav_{item['key']}", use_container_width=True)
                if is_active:
                    st.markdown('</div>', unsafe_allow_html=True)
            if clicked:
                session_controller.goto(item["key"])
                st.rerun()

        st.markdown("<div style='margin-top:auto;'></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<hr style='border-color:#2A2620;'/>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:30px;height:30px;border-radius:50%;background:{rc['text']};
                            display:flex;align-items:center;justify-content:center;color:white;
                            font-size:0.7rem;font-weight:700;flex-shrink:0;">{user['initials']}</div>
                <div style="min-width:0;">
                    <div style="font-size:0.78rem;font-weight:600;color:#FAF9F6;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;">{user['nome']}</div>
                    <div style="font-size:0.7rem;color:#776D5B;">{user['role']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("↩ Sair", use_container_width=True):
            auth_controller.logout()
            st.rerun()


def render_unauthorized():
    user = auth_controller.current_user()
    st.markdown(
        f"""
        <div style="text-align:center; padding: 4rem 0;">
            <h1 style="color:#1E1B15;">🔒 Acesso não autorizado</h1>
            <p style="color:#776D5B;">Você não tem permissão para acessar esta página com o perfil de
            <strong>{user['role']}</strong>. Entre em contato com o administrador caso precise de acesso.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Ir ao Menu", type="primary", use_container_width=True):
            session_controller.goto("menu")
            st.rerun()
