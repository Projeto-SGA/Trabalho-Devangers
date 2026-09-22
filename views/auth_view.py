# -*- coding: utf-8 -*-
"""Tela unificada de autenticação do SGA."""

import streamlit as st

from controllers import auth_controller
from models import seed_data as data
from views.components import BORDER, PRIMARY, TEXT_DARK, TEXT_MUTED, badge_html


def _inject_auth_css():
    """Define os estilos locais da tela sem alterar o tema das páginas internas."""
    st.markdown(
        f"""
        <style>
        .block-container {{ max-width: none !important; padding: 0 !important; }}
        [data-testid="stAppViewContainer"] > .main {{ background: #FAF9F6; }}
        .auth-layout {{ min-height: 100vh; }}
        .auth-brand {{
            min-height: 100vh; box-sizing: border-box; padding: 3.4rem 3.5rem;
            background: {PRIMARY}; color: #FFFFFF; display: flex;
            flex-direction: column; justify-content: space-between; position: relative;
            overflow: hidden;
        }}
        .auth-brand::after {{
            content: ""; position: absolute; width: 260px; height: 260px;
            right: -55px; bottom: 60px; border-radius: 50%;
            background: rgba(255,255,255,0.05);
        }}
        .auth-brand-mark {{ display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 1rem; }}
        .auth-brand-icon {{
            width: 80px; height: 80px; display: inline-flex; align-items: center;
            justify-content: center; background: #FFFFFF; color: {PRIMARY};
            border-radius: 12px; font-weight: 900; font-size: 1.35rem;
        }}
        .auth-brand-copy {{ position: relative; z-index: 1; max-width: 530px; padding-bottom: 1rem; }}
        .auth-kicker {{
            display: inline-flex; padding: 0.45rem 0.8rem; border-radius: 999px;
            background: rgba(255,255,255,0.12); color: #FFFFFF; font-size: 0.72rem;
            font-weight: 700; margin-bottom: 1.5rem;
        }}
        .auth-brand h1 {{ color: #FFFFFF; font-size: clamp(2.25rem, 4vw, 3.25rem); line-height: 1.08; margin: 0 0 1.1rem; }}
        .auth-brand p {{ color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6; margin: 0; max-width: 440px; }}
        div[data-testid="column"]:has(.auth-panel-marker) {{
            padding: 3.5rem clamp(2rem, 8vw, 8rem) 4rem; box-sizing: border-box;
        }}
        .auth-label {{
            color: {TEXT_MUTED}; font-size: 0.72rem; font-weight: 700;
            letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.6rem;
        }}
        .auth-card-title {{ color: {TEXT_DARK}; font-size: 1.55rem; font-weight: 800; margin: 0; }}
        .auth-card-subtitle {{ color: {TEXT_MUTED}; font-size: 0.9rem; margin: 0.25rem 0 1.5rem; }}
        .auth-divider {{
            display: flex; align-items: center; gap: 10px; color: {TEXT_MUTED};
            font-size: 0.75rem; margin: 1.1rem 0;
        }}
        .auth-divider::before, .auth-divider::after {{ content: ""; flex: 1; height: 1px; background: {BORDER}; }}
        .demo-avatar {{
            width: 34px; height: 34px; border-radius: 10px; display: flex;
            align-items: center; justify-content: center; color: #FFFFFF;
            font-weight: 700; font-size: 0.78rem;
        }}
        .demo-name {{ color: {TEXT_DARK}; font-weight: 700; font-size: 0.88rem; margin: 0; }}
        .demo-sub {{ color: {TEXT_MUTED}; font-size: 0.76rem; margin: 0; }}
        .demo-section {{ margin-top: 2rem; }}
        .first-access {{ margin: 2.2rem 0 0.5rem; padding-top: 1.4rem; border-top: 1px solid {BORDER}; }}
        .first-access p {{ color: {TEXT_MUTED}; font-size: 0.82rem; margin: 0 0 0.7rem; }}
        div[data-testid="column"]:has(.auth-panel-marker) div[data-testid="stTextInput"] input {{ background: #F5F2EB; border-color: {BORDER}; }}
        div[data-testid="column"]:has(.auth-panel-marker) div[data-testid="stForm"] {{ border: 0; padding: 0; }}
        div[data-testid="column"]:has(.auth-panel-marker) .stButton button,
        div[data-testid="column"]:has(.auth-panel-marker) [data-testid="stFormSubmitButton"] button {{ min-height: 2.6rem; }}
        @media (max-width: 800px) {{
            .auth-brand {{ min-height: auto; padding: 2rem 1.5rem 3rem; gap: 5rem; }}
            .auth-brand h1 {{ font-size: 2.2rem; }}
            div[data-testid="column"]:has(.auth-panel-marker) {{ padding: 2.5rem 1.25rem 3rem; }}
        }}
        div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label,
        div[data-testid="stCheckbox"] label {{ color: {TEXT_DARK} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_brand():
    st.markdown(
        """
        <div class="auth-brand">
            <div class="auth-brand-mark"><span class="auth-brand-icon">SGA</span><span>SGA</span></div>
            <div class="auth-brand-copy">
                <div class="auth-kicker">&#8226;&nbsp; Sistema Institucional</div>
                <h1>Sistema de Gestão<br>de Ambientes</h1>
                <p>Plataforma integrada para gerenciamento de reservas, controle de ambientes e organização de membros da instituição.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_login():
    st.markdown('<div class="auth-label">Acesso à conta</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-card-title">Bem-vindo de volta</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-card-subtitle">Acesse sua conta para continuar.</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("E-mail", placeholder="seu@email.com")
        st.text_input("Senha", type="password", placeholder="Sua senha")
        st.checkbox("Lembrar de mim")
        submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)

    if submitted:
        if not email.strip():
            st.error("Preencha o e-mail.")
        else:
            with st.spinner("Verificando..."):
                sucesso, mensagem = auth_controller.fazer_login(email.strip())
            if sucesso:
                st.success(mensagem)
                st.rerun()
            else:
                st.error(mensagem)

def _render_registration():
    st.markdown('<div class="auth-label">Novo cadastro</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-card-title">Criar sua conta</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-card-subtitle">Seus dados serão salvos no Firebase para aprovação e acesso.</div>', unsafe_allow_html=True)

    with st.form("registro_form"):
        nome = st.text_input("Nome completo", placeholder="João Silva")
        email = st.text_input("E-mail", placeholder="seu@email.com")
        senha = st.text_input("Senha", type="password", placeholder="Mínimo de 6 caracteres")
        confirmar = st.text_input("Confirmar senha", type="password")
        submitted = st.form_submit_button("Criar conta", type="primary", use_container_width=True)

    if submitted:
        if not nome.strip() or not email.strip() or not senha:
            st.error("Preencha todos os campos.")
        elif senha != confirmar:
            st.error("As senhas não conferem.")
        else:
            with st.spinner("Criando conta..."):
                sucesso, mensagem = auth_controller.fazer_registro(email.strip(), senha, nome.strip())
            if sucesso:
                st.success(mensagem)
                st.session_state.auth_tab = "login"
                st.rerun()
            else:
                st.error(mensagem)

    if st.button("Voltar ao login", use_container_width=True):
        st.session_state.auth_tab = "login"
        st.rerun()


def _render_demo_users():
    st.markdown('<div class="auth-divider demo-section">Entrar como — Demonstração</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for index, user in enumerate(data.DEMO_USERS):
        role_color = data.ROLE_COLORS[user["role"]]
        initials = user.get("initials") or "".join(word[0] for word in user["nome"].split()[:2]).upper()
        with cols[index % 2]:
            with st.container(border=True):
                first, second = st.columns([1, 4])
                first.markdown(
                    f'<div class="demo-avatar" style="background:{role_color["dot"]}">{initials}</div>',
                    unsafe_allow_html=True,
                )
                with second:
                    st.markdown(f'<p class="demo-name">{user["nome"]}</p>', unsafe_allow_html=True)
                    st.markdown(
                        badge_html(user["role"], role_color["bg"], role_color["text"]),
                        unsafe_allow_html=True,
                    )
                if user.get("nucleo"):
                    st.markdown(f'<p class="demo-sub">Núcleo {user["nucleo"]}</p>', unsafe_allow_html=True)
                if st.button("Entrar", key=f"demo_{index}", use_container_width=True):
                    auth_controller.login_demo(user)
                    st.rerun()

    st.markdown(
        '<div class="first-access"><div class="auth-label">Primeiro acesso</div>'
        '<p>Ainda não possui uma conta institucional?</p></div>',
        unsafe_allow_html=True,
    )
    if st.button("Criar nova conta", use_container_width=True):
        st.session_state.auth_tab = "registro"
        st.rerun()


def render():
    """Renderiza a tela única de login e cadastro."""
    _inject_auth_css()

    left, right = st.columns([1, 1.03], gap="small")
    with left:
        _render_brand()

    with right:
        st.markdown('<span class="auth-panel-marker"></span>', unsafe_allow_html=True)
        if st.session_state.get("auth_tab", "login") == "login":
            _render_login()
            _render_demo_users()
        else:
            _render_registration()


def render_user_menu():
    """Renderiza o menu do usuário logado na barra lateral."""
    if not auth_controller.is_logged_in():
        return

    info = auth_controller.obter_info_usuario()
    st.markdown("---")
    st.subheader(info.get("nome") or "Usuário")
    st.caption(info.get("email") or "")
    st.caption(f"Papel: **{(info.get('role') or 'usuario').upper()}**")

    if st.button("Perfil", use_container_width=True):
        st.session_state.route = "perfil"
        st.rerun()
    if st.button("Sair", use_container_width=True):
        auth_controller.fazer_logout()
        st.session_state.route = "login"
        st.rerun()
