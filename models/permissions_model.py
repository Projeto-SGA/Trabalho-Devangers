# -*- coding: utf-8 -*-
"""
[MODEL] Regras de permissão por papel (role).

Funções puras: recebem o papel do usuário e devolvem informações de
permissão, sem tocar em st.session_state. Quem decide "qual é o papel do
usuário logado" é responsabilidade do Controller (auth_controller).
"""

from models import seed_data as data


def get_permissions(role: str) -> dict:
    """Devolve o dicionário de permissões associado a um papel."""
    return data.PERMISSIONS_MATRIX.get(role, {})


def has_permission(role: str, key: str) -> bool:
    """Verifica se um papel possui a permissão `key`."""
    return bool(get_permissions(role).get(key, False))


def is_admin_role(role: str) -> bool:
    return role == "Administrador"
