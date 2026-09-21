# -*- coding: utf-8 -*-
"""
controllers/usuario_controller.py

Controller para gerenciar ações relacionadas a usuários.
Orquestra Model + Session State
"""

import streamlit as st
from models import usuario_model


def handle_criar_usuario(nome: str, email: str, role: str = "usuario"):
    """
    Processa a criação de um novo usuário
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    
    # Validação
    if not nome or not email:
        return False, "Nome e email são obrigatórios"
    
    if "@" not in email or "." not in email:
        return False, "Email inválido"
    
    if len(nome) < 3:
        return False, "Nome deve ter pelo menos 3 caracteres"
    
    # Verificar se já existe
    if usuario_model.usuario_existe(email):
        return False, "Este email já está cadastrado"
    
    # Criar
    try:
        usuario_model.criar_usuario(nome, email, role)
        return True, f"✅ Usuário {nome} criado com sucesso!"
    
    except Exception as e:
        return False, f"❌ Erro ao criar usuário: {str(e)}"


def handle_listar_usuarios(role: str = None):
    """
    Carrega lista de usuários
    
    Returns:
        list: Lista de usuários
    """
    try:
        return usuario_model.listar_usuarios(role)
    except Exception as e:
        st.error(f"Erro ao carregar usuários: {e}")
        return []


def handle_deletar_usuario(email: str):
    """
    Processa exclusão de usuário
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    try:
        usuario_model.deletar_usuario(email)
        return True, "✅ Usuário deletado"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def handle_atualizar_usuario(email: str, dados: dict):
    """
    Processa atualização de usuário
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    
    if not email or not dados:
        return False, "Email e dados são obrigatórios"
    
    try:
        usuario_model.atualizar_usuario(email, dados)
        return True, "✅ Usuário atualizado"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"
