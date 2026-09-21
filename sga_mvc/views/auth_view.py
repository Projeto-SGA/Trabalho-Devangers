# -*- coding: utf-8 -*-
"""
views/auth_view.py

View para autenticação (Login / Registro)
"""

import streamlit as st
from controllers import auth_controller


def render_login():
    """Renderiza formulário de login"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔐 Login")
        st.markdown("---")
        
        with st.form("login_form"):
            email = st.text_input(
                "Email",
                placeholder="seu.email@example.com",
                help="Email da sua conta"
            )
            
            st.markdown("*Para demo, use: `admin@sga.local`*")
            
            submitted = st.form_submit_button("🔓 Entrar", use_container_width=True)
        
        if submitted:
            if not email:
                st.error("Preencha o email")
            else:
                with st.spinner("Verificando..."):
                    sucesso, msg = auth_controller.fazer_login(email)
                
                if sucesso:
                    st.success(msg)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)
        
        st.markdown("---")
        
        if st.button("📝 Criar Conta", use_container_width=True):
            st.session_state.auth_tab = "registro"
            st.rerun()


def render_registro():
    """Renderiza formulário de registro"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("📝 Criar Conta")
        st.markdown("---")
        
        with st.form("registro_form"):
            nome = st.text_input(
                "Nome Completo",
                placeholder="João Silva",
                help="Seu nome completo"
            )
            
            email = st.text_input(
                "Email",
                placeholder="seu.email@example.com",
                help="Será usado para login"
            )
            
            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Mínimo 6 caracteres",
                help="Escolha uma senha segura"
            )
            
            senha_confirma = st.text_input(
                "Confirmar Senha",
                type="password",
                placeholder="Repita a senha",
                help="Confirme a mesma senha"
            )
            
            st.markdown("""
            ℹ️ **Requisitos:**
            - Nome: mínimo 3 caracteres
            - Senha: mínimo 6 caracteres
            - Email: formato válido (ex: user@example.com)
            """)
            
            submitted = st.form_submit_button("✅ Criar Conta", use_container_width=True)
        
        if submitted:
            # Validações
            if not nome or not email or not senha:
                st.error("Preencha todos os campos")
            elif senha != senha_confirma:
                st.error("Senhas não conferem")
            else:
                with st.spinner("Criando conta..."):
                    sucesso, msg = auth_controller.fazer_registro(nome, email, senha)
                
                if sucesso:
                    st.success(msg)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)
        
        st.markdown("---")
        
        if st.button("🔓 Voltar ao Login", use_container_width=True):
            st.session_state.auth_tab = "login"
            st.rerun()


def render():
    """Renderiza página de autenticação"""
    
    # Inicializar tab
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = "login"
    
    st.set_page_config(
        page_title="SGA — Autenticação",
        page_icon="🔐",
        layout="centered"
    )
    
    # Banner
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🏫 SGA — Sistema de Gestão de Ambientes</h1>
        <p>Autenticação com Firebase</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs de autenticação
    if st.session_state.auth_tab == "login":
        render_login()
    else:
        render_registro()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 12px;">
        <p>© 2026 SGA — Sistema de Gestão de Ambientes</p>
        <p>Desenvolvido com Streamlit + Firebase</p>
    </div>
    """, unsafe_allow_html=True)


def render_user_menu():
    """Renderiza menu do usuário logado (usar na sidebar)"""
    
    if not auth_controller.is_logged_in():
        return
    
    info = auth_controller.obter_info_usuario()
    
    st.markdown("---")
    st.subheader(f"👤 {info['nome']}")
    st.caption(f"📧 {info['email']}")
    st.caption(f"👁️ Papel: **{info['role'].upper()}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚙️ Perfil", use_container_width=True):
            st.session_state.current_route = "perfil"
            st.rerun()
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            auth_controller.fazer_logout()
            st.session_state.current_route = "login"
            st.rerun()
