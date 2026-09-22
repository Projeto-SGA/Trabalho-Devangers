# -*- coding: utf-8 -*-
"""
controllers/auth_controller.py

Controller para autenticação.
Gerencia session state + chamadas para o model.
"""

import streamlit as st
from models import auth_model
from models import permissions_model
from controllers import session_controller


def init_auth_state():
    """Inicializa estado de autenticação na sessão"""
    if 'user_uid' not in st.session_state:
        st.session_state.user_uid = None
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    
    if 'user_nome' not in st.session_state:
        st.session_state.user_nome = None
    
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    
    if 'user_perfil' not in st.session_state:
        st.session_state.user_perfil = None

    if 'current_user' not in st.session_state:
        st.session_state.current_user = None


def is_logged_in():
    """Verifica se usuário está logado"""
    return st.session_state.get('user_uid') is not None


def fazer_login(email: str):
    """
    Processa login do usuário
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    init_auth_state()
    
    if not email:
        return False, "Email é obrigatório"
    
    sucesso, uid, mensagem = auth_model.fazer_login(email)
    
    if sucesso:
        # Obter perfil e armazenar em sessão
        perfil = auth_model.obter_perfil_usuario(uid)
        
        st.session_state.user_uid = uid
        st.session_state.user_email = email
        st.session_state.user_nome = perfil.get('nome')
        st.session_state.user_role = perfil.get('role')
        st.session_state.user_perfil = perfil
        st.session_state.current_user = perfil
        session_controller.goto("menu")
    
    return sucesso, mensagem


def login_demo(user: dict):
    """Entra com um perfil local de demonstração, sem exigir conta Firebase."""
    init_auth_state()
    demo_profile = dict(user)
    demo_profile["uid"] = f"demo:{user['email']}"
    demo_profile["ativo"] = True

    st.session_state.user_uid = demo_profile["uid"]
    st.session_state.user_email = demo_profile["email"]
    st.session_state.user_nome = demo_profile["nome"]
    st.session_state.user_role = demo_profile["role"]
    st.session_state.user_perfil = demo_profile
    st.session_state.current_user = demo_profile
    session_controller.goto("menu")


def fazer_registro(email: str, senha: str, nome: str):
    """
    Processa registro de novo usuário
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    init_auth_state()
    
    sucesso, uid, mensagem = auth_model.criar_nova_conta(email, senha, nome)
    
    if sucesso:
        st.session_state.user_uid = uid
        st.session_state.user_email = email
        st.session_state.user_nome = nome
        st.session_state.user_role = 'usuario'
    
    return sucesso, mensagem


def fazer_logout():
    """Faz logout do usuário"""
    st.session_state.user_uid = None
    st.session_state.user_email = None
    st.session_state.user_nome = None
    st.session_state.user_role = None
    st.session_state.user_perfil = None
    st.session_state.current_user = None


def logout():
    """Alias mantido para as views que usam a nomenclatura antiga."""
    fazer_logout()


def atualizar_perfil(dados: dict):
    """
    Atualiza perfil do usuário logado
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    if not is_logged_in():
        return False, "Usuário não está logado"
    
    uid = st.session_state.user_uid
    sucesso, mensagem = auth_model.atualizar_perfil(uid, dados)
    
    if sucesso:
        # Recarregar perfil
        st.session_state.user_perfil = auth_model.obter_perfil_usuario(uid)
    
    return sucesso, mensagem


def update_current_user_profile(nome: str, email: str):
    """Atualiza nome e e-mail no perfil usado pelas configurações."""
    nome = nome.strip()
    email = email.strip()
    if not nome or not email:
        return "Nome e e-mail são obrigatórios."

    user = current_user()
    if user.get('uid', '').startswith('demo:'):
        user.update({'nome': nome, 'email': email})
        st.session_state.user_nome = nome
        st.session_state.user_email = email
        st.session_state.user_perfil = user
        st.session_state.current_user = user
        return None

    sucesso, mensagem = atualizar_perfil({'nome': nome, 'email': email})
    if sucesso:
        st.session_state.user_nome = nome
        st.session_state.user_email = email
        st.session_state.user_perfil.update({'nome': nome, 'email': email})
        st.session_state.current_user = st.session_state.user_perfil
        return None
    return mensagem


def deletar_conta():
    """
    Deleta conta do usuário logado
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    if not is_logged_in():
        return False, "Usuário não está logado"
    
    uid = st.session_state.user_uid
    sucesso, mensagem = auth_model.deletar_conta_completa(uid)
    
    if sucesso:
        fazer_logout()
    
    return sucesso, mensagem


def tem_permissao(permissao: str) -> bool:
    """
    Verifica se usuário tem determinada permissão
    
    Args:
        permissao: Nome da permissão (ex: 'admin', 'professor')
    """
    if not is_logged_in():
        return False
    
    role = st.session_state.get('user_role', 'usuario')
    role = {
        'Aluno': 'usuario',
        'Professor': 'professor',
        'Coordenador': 'admin',
        'Administrador': 'admin',
    }.get(role, role)
    
    # Mapa de permissões por papel
    permissoes = {
        'usuario': ['ver_agenda', 'fazer_reservas'],
        'professor': ['ver_agenda', 'fazer_reservas', 'gerenciar_aulas'],
        'admin': ['ver_agenda', 'fazer_reservas', 'gerenciar_aulas', 'gerenciar_usuarios'],
    }
    
    return permissao in permissoes.get(role, [])


def permissions() -> dict:
    """Retorna as permissões do papel atual para as views do aplicativo."""
    role = st.session_state.get('user_role')
    if role in ('usuario', 'professor', 'admin'):
        role = {
            'usuario': 'Aluno',
            'professor': 'Professor',
            'admin': 'Administrador',
        }[role]
    return permissions_model.get_permissions(role)


def has_perm(permissao: str) -> bool:
    """Verifica uma permissão pelo nome usado na matriz de permissões."""
    role = st.session_state.get('user_role')
    return permissions_model.has_permission(role, permissao)


def is_admin() -> bool:
    """Indica se o usuário atual possui o papel de administrador."""
    return permissions_model.is_admin_role(st.session_state.get('user_role'))


def obter_info_usuario():
    """Retorna informações do usuário logado"""
    return {
        'uid': st.session_state.get('user_uid'),
        'email': st.session_state.get('user_email'),
        'nome': st.session_state.get('user_nome'),
        'role': st.session_state.get('user_role'),
    }


def current_user():
    """Retorna o perfil compatível com as views legadas do aplicativo."""
    return st.session_state.get('current_user') or st.session_state.get('user_perfil') or {}
