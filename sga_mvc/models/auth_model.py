# -*- coding: utf-8 -*-
"""
models/auth_model.py

Model para gerenciar autenticação.
Integra Firebase Auth + Firestore.
"""

import streamlit as st
from datetime import datetime
from utils import auth_utils
from models import usuario_model


def criar_nova_conta(email: str, senha: str, nome: str):
    """
    Cria uma nova conta (Firebase Auth + Profile no Firestore)
    
    Returns:
        tuple: (sucesso: bool, uid: str, mensagem: str)
    """
    
    # Validar
    if not auth_utils.validar_email(email):
        return False, None, "Email inválido"
    
    if not auth_utils.validar_senha(senha):
        return False, None, "Senha deve ter no mínimo 6 caracteres"
    
    if len(nome) < 3:
        return False, None, "Nome deve ter no mínimo 3 caracteres"
    
    # Criar em Firebase Auth
    sucesso, uid, msg = auth_utils.registrar_usuario(email, senha)
    
    if not sucesso:
        return False, None, msg
    
    # Criar perfil no Firestore
    try:
        db = st.session_state.firestore_db
        
        perfil_usuario = {
            'uid': uid,
            'nome': nome,
            'email': email,
            'role': 'usuario',  # Papel padrão
            'criado_em': datetime.now(),
            'ativo': True,
            'email_verificado': False,
        }
        
        db.collection('usuarios').document(uid).set(perfil_usuario)
        
        return True, uid, f"✅ Conta criada com sucesso!"
    
    except Exception as e:
        # Rollback: deletar do Firebase Auth se falhar no Firestore
        auth_utils.deletar_usuario_auth(uid)
        return False, None, f"❌ Erro ao criar perfil: {str(e)}"


def fazer_login(email: str):
    """
    Faz login do usuário (apenas valida se existe)
    
    ⚠️ Em produção real, use Firebase Client SDK para autenticar
    Este exemplo simula login server-side.
    """
    
    usuario = auth_utils.obter_usuario_por_email(email)
    
    if not usuario:
        return False, None, "❌ Usuário não encontrado"
    
    if not usuario.email_verified and usuario.email != "admin@sga.local":
        return False, None, "⚠️ Email não verificado. Verifique seu email"
    
    # Obter dados do perfil no Firestore
    db = st.session_state.firestore_db
    doc = db.collection('usuarios').document(usuario.uid).get()
    
    if not doc.exists:
        return False, None, "❌ Perfil não encontrado"
    
    perfil = doc.to_dict()
    
    if not perfil.get('ativo'):
        return False, None, "❌ Usuário inativo"
    
    return True, usuario.uid, f"✅ Bem-vindo, {perfil.get('nome')}!"


def obter_perfil_usuario(uid: str):
    """Busca perfil completo no Firestore"""
    try:
        db = st.session_state.firestore_db
        doc = db.collection('usuarios').document(uid).get()
        
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        st.error(f"Erro ao buscar perfil: {e}")
        return None


def atualizar_perfil(uid: str, dados: dict):
    """Atualiza perfil do usuário no Firestore"""
    try:
        db = st.session_state.firestore_db
        
        dados['atualizado_em'] = datetime.now()
        
        db.collection('usuarios').document(uid).update(dados)
        return True, "✅ Perfil atualizado"
    
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def deletar_conta_completa(uid: str):
    """
    Deleta conta completamente (Firebase Auth + Firestore)
    """
    try:
        # Deletar de Firebase Auth
        sucesso, msg = auth_utils.deletar_usuario_auth(uid)
        if not sucesso:
            return False, msg
        
        # Deletar do Firestore
        db = st.session_state.firestore_db
        db.collection('usuarios').document(uid).delete()
        
        return True, "✅ Conta deletada completamente"
    
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"
