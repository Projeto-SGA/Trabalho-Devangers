# -*- coding: utf-8 -*-
"""
models/usuario_model.py

Model para gerenciar usuários no Firestore.
Esta é a ÚNICA camada que fala com Firebase!
"""

import streamlit as st
from datetime import datetime


def criar_usuario(nome: str, email: str, role: str = "usuario"):
    """
    Cria um novo usuário no Firestore
    
    Args:
        nome: Nome completo
        email: Email único (usado como ID)
        role: Papel (usuario, professor, admin)
    
    Returns:
        dict: Dados do usuário criado
    """
    db = st.session_state.firestore_db
    
    usuario = {
        'nome': nome,
        'email': email,
        'role': role,
        'criado_em': datetime.now(),
        'ativo': True,
    }
    
    db.collection('usuarios').document(email).set(usuario)
    return usuario


def obter_usuario(email: str):
    """Busca um usuário por email"""
    db = st.session_state.firestore_db
    doc = db.collection('usuarios').document(email).get()
    
    if doc.exists:
        return doc.to_dict()
    return None


def listar_usuarios(role: str = None):
    """
    Lista todos os usuários
    
    Args:
        role: Filtrar por papel (opcional)
    """
    db = st.session_state.firestore_db
    
    usuarios = []
    query = db.collection('usuarios')
    
    if role:
        query = query.where('role', '==', role)
    
    for doc in query.stream():
        usuarios.append({**doc.to_dict(), 'id': doc.id})
    
    return usuarios


def atualizar_usuario(email: str, dados: dict):
    """Atualiza dados de um usuário"""
    db = st.session_state.firestore_db
    db.collection('usuarios').document(email).update({
        **dados,
        'atualizado_em': datetime.now()
    })


def deletar_usuario(email: str):
    """Deleta um usuário"""
    db = st.session_state.firestore_db
    db.collection('usuarios').document(email).delete()


def usuario_existe(email: str):
    """Verifica se usuário existe"""
    return obter_usuario(email) is not None
