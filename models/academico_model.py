# -*- coding: utf-8 -*-
"""
[MODEL] Estrutura acadêmica: Núcleo > Curso > Turma > Disciplina.

Funções puras de CRUD e consulta. O Controller (academico_controller)
conecta estas funções às listas guardadas em st.session_state.
"""


# ── Lookups ───────────────────────────────────────────────────────────────────

def get_nucleo_by_name(nucleos: list, nome: str):
    return next((n for n in nucleos if n["nome"] == nome), None)


def get_nucleo_by_id(nucleos: list, nid: int):
    return next((n for n in nucleos if n["id"] == nid), None)


def get_curso_by_id(cursos: list, cid: int):
    return next((c for c in cursos if c["id"] == cid), None)


def get_turma_by_id(turmas: list, tid: int):
    return next((t for t in turmas if t["id"] == tid), None)


def cursos_by_nucleo(cursos: list, nucleo_id: int) -> list:
    return [c for c in cursos if c["nucleoId"] == nucleo_id and c["ativo"]]


def turmas_by_curso(turmas: list, curso_id: int) -> list:
    return [t for t in turmas if t["cursoId"] == curso_id and t["ativo"]]


def disciplinas_by_turma(disciplinas: list, turma_id: int) -> list:
    return [d for d in disciplinas if turma_id in d["turmasIds"]]


def disciplinas_by_nucleo(disciplinas: list, nucleo_id: int) -> list:
    return [d for d in disciplinas if d["nucleoId"] == nucleo_id]


# ── Núcleo ────────────────────────────────────────────────────────────────────

def add_nucleo(nucleos: list, new_id: int, nome: str, descricao: str, ativo: bool = True) -> dict:
    novo = {
        "id": new_id, "nome": nome, "descricao": descricao,
        "cursosIds": [], "coordenadoresIds": [], "ativo": ativo,
    }
    nucleos.append(novo)
    return novo


def update_nucleo(nucleos: list, nid: int, **kwargs) -> None:
    for n in nucleos:
        if n["id"] == nid:
            n.update(kwargs)
            return


def delete_nucleo(nucleos: list, nid: int) -> list:
    return [n for n in nucleos if n["id"] != nid]


def nucleo_name_exists(nucleos: list, nome: str) -> bool:
    return any(n["nome"].lower() == nome.strip().lower() for n in nucleos)


# ── Curso ─────────────────────────────────────────────────────────────────────

def add_curso(cursos: list, nucleos: list, new_id: int, nome: str, nucleo_id: int, ativo: bool = True) -> dict:
    novo = {"id": new_id, "nome": nome, "nucleoId": nucleo_id, "turmasIds": [], "ativo": ativo}
    cursos.append(novo)
    n = get_nucleo_by_id(nucleos, nucleo_id)
    if n:
        n["cursosIds"].append(new_id)
    return novo


def update_curso(cursos: list, cid: int, **kwargs) -> None:
    for c in cursos:
        if c["id"] == cid:
            c.update(kwargs)
            return


def delete_curso(cursos: list, nucleos: list, cid: int) -> list:
    novos_cursos = [c for c in cursos if c["id"] != cid]
    for n in nucleos:
        n["cursosIds"] = [x for x in n["cursosIds"] if x != cid]
    return novos_cursos


# ── Turma ─────────────────────────────────────────────────────────────────────

def add_turma(turmas: list, cursos: list, new_id: int, nome: str, curso_id: int,
              nucleo_id: int, turno: str, ativo: bool = True) -> dict:
    novo = {
        "id": new_id, "nome": nome, "cursoId": curso_id, "nucleoId": nucleo_id, "turno": turno,
        "alunosIds": [], "professoresIds": [], "disciplinasIds": [], "ativo": ativo,
    }
    turmas.append(novo)
    c = get_curso_by_id(cursos, curso_id)
    if c:
        c["turmasIds"].append(new_id)
    return novo


def update_turma(turmas: list, tid: int, **kwargs) -> None:
    for t in turmas:
        if t["id"] == tid:
            t.update(kwargs)
            return


def delete_turma(turmas: list, cursos: list, tid: int) -> list:
    novas_turmas = [t for t in turmas if t["id"] != tid]
    for c in cursos:
        c["turmasIds"] = [x for x in c["turmasIds"] if x != tid]
    return novas_turmas


# ── Disciplina ────────────────────────────────────────────────────────────────

def add_disciplina(disciplinas: list, new_id: int, codigo: str, nome: str,
                    nucleo_id: int, carga_horaria: int, turmas_ids: list | None = None) -> dict:
    novo = {
        "id": new_id, "codigo": codigo, "nome": nome, "nucleoId": nucleo_id,
        "cargaHoraria": carga_horaria, "professoresIds": [], "turmasIds": turmas_ids or [],
    }
    disciplinas.append(novo)
    return novo


def update_disciplina(disciplinas: list, did: int, **kwargs) -> None:
    for d in disciplinas:
        if d["id"] == did:
            d.update(kwargs)
            return


def delete_disciplina(disciplinas: list, did: int) -> list:
    return [d for d in disciplinas if d["id"] != did]
