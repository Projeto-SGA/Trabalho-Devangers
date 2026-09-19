# -*- coding: utf-8 -*-
"""
[CONTROLLER] Sessão e navegação.

Responsável por inicializar o "banco de dados" em memória (st.session_state)
a partir do Model de seed data, e por controlar a rota atual (equivalente
ao roteador de uma aplicação MVC tradicional).
"""

import copy

import streamlit as st

from models import seed_data as data


def init_state() -> None:
    """Inicializa o estado da sessão uma única vez (bootstrap do 'banco')."""
    ss = st.session_state
    if "_sga_initialized" in ss:
        return

    ss.current_user = copy.deepcopy(data.DEMO_USERS[0])  # default: Admin
    ss.route = "login"
    ss.logged_in = False

    ss.salas = copy.deepcopy(data.INITIAL_SALAS)
    ss.solicitacoes = copy.deepcopy(data.INITIAL_SOLICITACOES)
    ss._next_sol_id = 100

    ss.members = copy.deepcopy(data.INITIAL_MEMBERS)
    ss._next_member_id = 200

    ss.nucleos = copy.deepcopy(data.SEED_NUCLEOS)
    ss.cursos = copy.deepcopy(data.SEED_CURSOS)
    ss.turmas = copy.deepcopy(data.SEED_TURMAS)
    ss.disciplinas = copy.deepcopy(data.SEED_DISCIPLINAS)
    ss._next_acad_id = 100

    ss._sga_initialized = True


def current_route() -> str:
    return st.session_state.route


def is_logged_in() -> bool:
    return bool(st.session_state.logged_in)


def goto(route: str) -> None:
    st.session_state.route = route
