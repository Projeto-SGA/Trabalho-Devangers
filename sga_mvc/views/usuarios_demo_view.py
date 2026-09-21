# -*- coding: utf-8 -*-
"""
views/usuarios_demo_view.py

View de exemplo para gerenciar usuários.
Usa Controller para toda lógica, nunca acessa Firebase direto!
"""

import streamlit as st
import pandas as pd
from controllers import usuario_controller


def render():
    """Renderiza página de gerenciamento de usuários"""
    
    st.title("👥 Gerenciar Usuários (Demo)")
    st.markdown("---")
    
    # SEÇÃO 1: Criar novo usuário
    st.header("➕ Criar Novo Usuário")
    
    with st.form("novo_usuario_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo", placeholder="Ex: João Silva")
        
        with col2:
            email = st.text_input("Email", placeholder="Ex: joao@example.com")
        
        role = st.selectbox("Papel", ["usuario", "professor", "admin"])
        
        submitted = st.form_submit_button("💾 Criar Usuário", use_container_width=True)
        
        if submitted:
            sucesso, mensagem = usuario_controller.handle_criar_usuario(nome, email, role)
            
            if sucesso:
                st.success(mensagem)
                st.session_state.rerun_flag = True
            else:
                st.error(mensagem)
    
    st.markdown("---")
    
    # SEÇÃO 2: Listar usuários
    st.header("📋 Usuários Cadastrados")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_role = st.selectbox("Filtrar por papel:", ["Todos", "usuario", "professor", "admin"])
    
    # Carregar dados
    role_filter = None if filtro_role == "Todos" else filtro_role
    usuarios = usuario_controller.handle_listar_usuarios(role_filter)
    
    if usuarios:
        # Exibir em tabela
        df = pd.DataFrame(usuarios)
        df = df[['nome', 'email', 'role', 'ativo']].copy()
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Seção de ações
        st.subheader("⚙️ Ações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_deletar = st.selectbox(
                "Selecionar usuário para deletar:",
                [u['email'] for u in usuarios]
            )
            
            if st.button("🗑️ Deletar Usuário", use_container_width=True):
                sucesso, mensagem = usuario_controller.handle_deletar_usuario(email_deletar)
                
                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)
        
        with col2:
            email_atualizar = st.selectbox(
                "Selecionar usuário para atualizar:",
                [u['email'] for u in usuarios],
                key="email_atualizar"
            )
            
            novo_role = st.selectbox(
                "Novo papel:",
                ["usuario", "professor", "admin"],
                key="novo_role"
            )
            
            if st.button("✏️ Atualizar", use_container_width=True):
                sucesso, mensagem = usuario_controller.handle_atualizar_usuario(
                    email_atualizar,
                    {"role": novo_role}
                )
                
                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)
    
    else:
        st.info("📭 Nenhum usuário cadastrado ainda. Crie um acima!")
    
    # Debug info
    st.markdown("---")
    with st.expander("🔧 Debug - Info Firebase"):
        if 'firestore_db' in st.session_state:
            st.success("✅ Firestore conectado")
            st.write(f"Total de usuários: {len(usuarios)}")
        else:
            st.error("❌ Firestore não inicializado")
