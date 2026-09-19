# -*- coding: utf-8 -*-
"""
[CONTROLLER] Autenticação, permissões e auto-cadastro.

Faz a ponte entre as Views de Login/Configurações e os Models de
permissões, validação e membro.
"""

import copy

import streamlit as st

from models import seed_data as data
from models import membro_model, permissions_model, validators


# ── Sessão do usuário atual ──────────────────────────────────────────────────

def current_user() -> dict:
    return st.session_state.current_user


def permissions() -> dict:
    return permissions_model.get_permissions(current_user()["role"])


def has_perm(key: str) -> bool:
    return permissions_model.has_permission(current_user()["role"], key)


def is_admin() -> bool:
    return permissions_model.is_admin_role(current_user()["role"])


def login_as(user: dict) -> None:
    st.session_state.current_user = copy.deepcopy(user)
    st.session_state.logged_in = True
    st.session_state.route = "menu"


def logout() -> None:
    st.session_state.current_user = copy.deepcopy(data.DEMO_USERS[0])
    st.session_state.logged_in = False
    st.session_state.route = "login"


def demo_users() -> list:
    return data.DEMO_USERS


def role_description(role: str) -> str:
    return data.ROLE_DESCRIPTIONS.get(role, "")


def update_current_user_profile(nome: str, email: str) -> str:
    """Atualiza nome/e-mail do usuário logado. Devolve erro (vazio = ok)."""
    if not nome.strip():
        return "O nome não pode estar vazio."
    if "@" not in email:
        return "Informe um e-mail válido."
    user = current_user()
    user["nome"] = nome
    user["email"] = email
    return ""


# ── Cadastro de nova conta (registro em 2 etapas) ────────────────────────────

def validate_step1(nome: str, email: str, cpf: str, senha: str, confirmar: str) -> str:
    """Valida a etapa 1 do formulário de cadastro. Devolve erro (vazio = ok)."""
    err = validators.validate_nome(nome)
    if not err:
        err = validators.validate_email(email)
    if not err and validators.email_already_registered(email, st.session_state.members):
        err = "Este e-mail já está cadastrado no sistema."
    if not err:
        err = validators.validate_cpf(cpf)
    if not err and validators.cpf_already_registered(cpf, st.session_state.members):
        err = "Este CPF já está cadastrado no sistema."
    if not err and not senha:
        err = "Informe uma senha."
    if not err and len(senha) < 6:
        err = "A senha deve ter ao menos 6 caracteres."
    if not err and senha != confirmar:
        err = "As senhas não coincidem."
    return err


def nucleos_ativos_nomes() -> list:
    return [n["nome"] for n in st.session_state.nucleos if n["ativo"]]


def submit_registration(form: dict, disciplinas: list) -> None:
    """Envia o cadastro como membro pendente de aprovação (etapa 2)."""
    ss = st.session_state
    novo, ss._next_member_id = membro_model.add_pending_member(
        ss.members, ss._next_member_id,
        {
            "nome": form["nome"].strip(),
            "email": form["email"].strip(),
            "cpf": form["cpf"],
            "funcao": form["funcao"],
            "depto": form["nucleo"],
            "nucleo": form["nucleo"],
            "curso": form["curso"],
            "turno": form["turno"],
            "turma": form["turma"],
            "disciplinas": disciplinas,
        },
    )
