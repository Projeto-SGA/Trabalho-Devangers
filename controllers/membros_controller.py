# -*- coding: utf-8 -*-
"""
[CONTROLLER] Membros da instituição e aprovação de cadastros.

Conecta a View "membros_view" ao Model membro_model, lendo e persistindo
a lista em st.session_state.
"""

import streamlit as st

from models import membro_model as m


def list_members() -> list:
    return st.session_state.members


def filter_members(search: str, funcao: str, status: str, nucleo: str) -> list:
    return m.filter_members(st.session_state.members, search, funcao, status, nucleo)


def pending_requests() -> list:
    return m.pending_requests(st.session_state.members)


def add_member_directly(payload: dict) -> None:
    ss = st.session_state
    _, ss._next_member_id = m.add_member_directly(ss.members, ss._next_member_id, payload)


def update_member(member_id: int, payload: dict) -> None:
    m.update_member(st.session_state.members, member_id, payload)


def remove_member(member_id: int) -> None:
    ss = st.session_state
    ss.members = m.remove_member(ss.members, member_id)


def toggle_member_status(member_id: int) -> None:
    m.toggle_member_status(st.session_state.members, member_id)


def approve_member(member_id: int) -> None:
    m.approve_member(st.session_state.members, member_id)


def reject_member(member_id: int) -> None:
    ss = st.session_state
    ss.members = m.reject_member(ss.members, member_id)


def solicitar_correcao(member_id: int, motivo: str) -> None:
    m.solicitar_correcao(st.session_state.members, member_id, motivo)
