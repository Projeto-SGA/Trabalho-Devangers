# -*- coding: utf-8 -*-
"""
[CONTROLLER] Estrutura acadêmica (Núcleo > Curso > Turma > Disciplina).

Conecta a View "academico_view" (e o fluxo de cadastro do "login_view") ao
Model academico_model, lendo e persistindo as listas em st.session_state.
"""

import streamlit as st

from models import academico_model as m


# ── Consultas ─────────────────────────────────────────────────────────────────

def list_nucleos() -> list:
    return st.session_state.nucleos


def list_cursos(scoped_nucleo_id: int | None = None) -> list:
    cursos = st.session_state.cursos
    return [c for c in cursos if not scoped_nucleo_id or c["nucleoId"] == scoped_nucleo_id]


def list_turmas(scoped_nucleo_id: int | None = None) -> list:
    turmas = st.session_state.turmas
    return [t for t in turmas if not scoped_nucleo_id or t["nucleoId"] == scoped_nucleo_id]


def list_disciplinas(scoped_nucleo_id: int | None = None) -> list:
    discs = st.session_state.disciplinas
    return [d for d in discs if not scoped_nucleo_id or d["nucleoId"] == scoped_nucleo_id]


def get_nucleo_by_name(nome: str):
    return m.get_nucleo_by_name(st.session_state.nucleos, nome)


def get_nucleo_by_id(nid: int):
    return m.get_nucleo_by_id(st.session_state.nucleos, nid)


def get_curso_by_id(cid: int):
    return m.get_curso_by_id(st.session_state.cursos, cid)


def get_turma_by_id(tid: int):
    return m.get_turma_by_id(st.session_state.turmas, tid)


def cursos_by_nucleo(nucleo_id: int) -> list:
    return m.cursos_by_nucleo(st.session_state.cursos, nucleo_id)


def turmas_by_curso(curso_id: int) -> list:
    return m.turmas_by_curso(st.session_state.turmas, curso_id)


def disciplinas_by_turma(turma_id: int) -> list:
    return m.disciplinas_by_turma(st.session_state.disciplinas, turma_id)


def disciplinas_by_nucleo(nucleo_id: int) -> list:
    return m.disciplinas_by_nucleo(st.session_state.disciplinas, nucleo_id)


def turmas_do_nucleo(nucleo_id: int) -> list:
    return [t for t in st.session_state.turmas if t["nucleoId"] == nucleo_id]


# ── Núcleo ────────────────────────────────────────────────────────────────────

def nucleo_name_exists(nome: str) -> bool:
    return m.nucleo_name_exists(st.session_state.nucleos, nome)


def _next_id() -> int:
    ss = st.session_state
    ss._next_acad_id += 1
    return ss._next_acad_id


def add_nucleo(nome: str, descricao: str, ativo: bool = True) -> None:
    m.add_nucleo(st.session_state.nucleos, _next_id(), nome, descricao, ativo)
    # (a linha acima mantém o contador coerente com o padrão dos demais métodos)


def update_nucleo(nid: int, **kwargs) -> None:
    m.update_nucleo(st.session_state.nucleos, nid, **kwargs)


def delete_nucleo(nid: int) -> None:
    ss = st.session_state
    ss.nucleos = m.delete_nucleo(ss.nucleos, nid)


# ── Curso ─────────────────────────────────────────────────────────────────────

def add_curso(nome: str, nucleo_id: int, ativo: bool = True) -> None:
    ss = st.session_state
    m.add_curso(ss.cursos, ss.nucleos, _next_id(), nome, nucleo_id, ativo)


def update_curso(cid: int, **kwargs) -> None:
    m.update_curso(st.session_state.cursos, cid, **kwargs)


def delete_curso(cid: int) -> None:
    ss = st.session_state
    ss.cursos = m.delete_curso(ss.cursos, ss.nucleos, cid)


# ── Turma ─────────────────────────────────────────────────────────────────────

def add_turma(nome: str, curso_id: int, nucleo_id: int, turno: str, ativo: bool = True) -> None:
    ss = st.session_state
    m.add_turma(ss.turmas, ss.cursos, _next_id(), nome, curso_id, nucleo_id, turno, ativo)


def update_turma(tid: int, **kwargs) -> None:
    m.update_turma(st.session_state.turmas, tid, **kwargs)


def delete_turma(tid: int) -> None:
    ss = st.session_state
    ss.turmas = m.delete_turma(ss.turmas, ss.cursos, tid)


# ── Disciplina ────────────────────────────────────────────────────────────────

def add_disciplina(codigo: str, nome: str, nucleo_id: int, carga_horaria: int,
                    turmas_ids: list | None = None) -> None:
    ss = st.session_state
    m.add_disciplina(ss.disciplinas, _next_id(), codigo, nome, nucleo_id, carga_horaria, turmas_ids)


def update_disciplina(did: int, **kwargs) -> None:
    m.update_disciplina(st.session_state.disciplinas, did, **kwargs)


def delete_disciplina(did: int) -> None:
    ss = st.session_state
    ss.disciplinas = m.delete_disciplina(ss.disciplinas, did)
