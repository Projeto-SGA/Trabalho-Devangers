# -*- coding: utf-8 -*-
"""
views/perfil_view.py

View para gerenciar perfil do usuário
"""

import streamlit as st
from controllers import auth_controller


def render():
    """Renderiza página de perfil do usuário"""
    
    st.title("⚙️ Meu Perfil")
    
    if not auth_controller.is_logged_in():
        st.error("❌ Você precisa estar logado")
        return
    
    info = auth_controller.obter_info_usuario()
    perfil = st.session_state.get('user_perfil', {})
    
    # SEÇÃO 1: Informações
    st.header("📋 Informações da Conta")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Nome:** {info['nome']}")
        st.write(f"**Email:** {info['email']}")
    
    with col2:
        st.write(f"**Papel:** {info['role'].upper()}")
        st.write(f"**Criado em:** {perfil.get('criado_em', 'N/A')}")
    
    st.markdown("---")
    
    # SEÇÃO 2: Editar Perfil
    st.header("✏️ Editar Perfil")
    
    with st.form("editar_perfil_form"):
        novo_nome = st.text_input(
            "Nome",
            value=info['nome'],
            help="Seu nome completo"
        )
        
        submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
    
    if submitted:
        if novo_nome != info['nome']:
            sucesso, msg = auth_controller.atualizar_perfil({'nome': novo_nome})
            
            if sucesso:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        else:
            st.info("Nenhuma alteração foi feita")
    
    st.markdown("---")
    
    # SEÇÃO 3: Segurança
    st.header("🔒 Segurança")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 Alterar Senha", use_container_width=True):
            st.info("⚠️ Função de reset de senha será implementada com Firebase Client SDK")
            st.write("Por enquanto, use: Esqueceu a senha? no login")
    
    with col2:
        if st.button("📧 Verificar Email", use_container_width=True):
            st.info("Email de verificação será enviado (Firebase Email Verification)")
    
    st.markdown("---")
    
    # SEÇÃO 4: Zona de Perigo
    st.header("⚠️ Zona de Perigo")
    
    st.warning("Ações nesta seção não podem ser desfeitas!")
    
    if st.button("🗑️ Deletar Conta Permanentemente", use_container_width=True):
        st.session_state.confirm_delete = True
    
    if st.session_state.get('confirm_delete', False):
        st.error("Tem certeza? Isso vai deletar sua conta e TODOS os seus dados!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("❌ Confirmar Deleção", use_container_width=True):
                with st.spinner("Deletando conta..."):
                    sucesso, msg = auth_controller.deletar_conta()
                
                if sucesso:
                    st.success(msg)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)
        
        with col2:
            if st.button("✅ Cancelar", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()
