# -*- coding: utf-8 -*-
"""[VIEW] Acadêmico — equivalente a src/pages/Academico.tsx."""

import streamlit as st

from controllers import academico_controller as ac, auth_controller


@st.dialog("Núcleo")
def nucleo_modal(nucleo=None):
    editing = nucleo is not None
    nome = st.text_input("Nome *", value=nucleo["nome"] if editing else "", placeholder="Ex: Saúde")
    desc = st.text_area("Descrição", value=nucleo["descricao"] if editing else "")
    ativo = st.checkbox("Núcleo ativo", value=nucleo["ativo"] if editing else True)
    if st.button("Salvar", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Informe o nome do núcleo.")
        elif not editing and ac.nucleo_name_exists(nome):
            st.error("Já existe um núcleo com esse nome.")
        else:
            if editing:
                ac.update_nucleo(nucleo["id"], nome=nome.strip(), descricao=desc, ativo=ativo)
                st.toast("Núcleo atualizado!", icon="✅")
            else:
                ac.add_nucleo(nome.strip(), desc, ativo)
                st.toast("Núcleo criado!", icon="✅")
            st.rerun()


@st.dialog("Curso")
def curso_modal(curso=None, scoped_nucleo_id=None):
    editing = curso is not None
    nucleo_opts = {n["nome"]: n["id"] for n in ac.list_nucleos() if n["ativo"]}
    if scoped_nucleo_id:
        cur_nome = ac.get_nucleo_by_id(scoped_nucleo_id)["nome"]
        st.caption(f"Núcleo: {cur_nome}")
        nucleo_id = scoped_nucleo_id
    else:
        default_name = ac.get_nucleo_by_id(curso["nucleoId"])["nome"] if editing else list(nucleo_opts.keys())[0]
        nucleo_sel = st.selectbox("Núcleo *", list(nucleo_opts.keys()),
                                   index=list(nucleo_opts.keys()).index(default_name) if default_name in nucleo_opts else 0)
        nucleo_id = nucleo_opts[nucleo_sel]
    nome = st.text_input("Nome do curso *", value=curso["nome"] if editing else "")
    ativo = st.checkbox("Curso ativo", value=curso["ativo"] if editing else True)
    if st.button("Salvar", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Informe o nome do curso.")
        else:
            if editing:
                ac.update_curso(curso["id"], nome=nome.strip(), nucleoId=nucleo_id, ativo=ativo)
                st.toast("Curso atualizado!", icon="✅")
            else:
                ac.add_curso(nome.strip(), nucleo_id, ativo)
                st.toast("Curso criado!", icon="✅")
            st.rerun()


@st.dialog("Turma")
def turma_modal(turma=None, scoped_nucleo_id=None):
    editing = turma is not None
    cursos_visiveis = ac.list_cursos(scoped_nucleo_id)
    curso_opts = {c["nome"]: c for c in cursos_visiveis}
    default_curso = ac.get_curso_by_id(turma["cursoId"])["nome"] if editing else (list(curso_opts.keys())[0] if curso_opts else "")
    curso_sel = st.selectbox("Curso *", list(curso_opts.keys()),
                              index=list(curso_opts.keys()).index(default_curso) if default_curso in curso_opts else 0)
    curso_obj = curso_opts.get(curso_sel)
    nome = st.text_input("Nome da turma *", value=turma["nome"] if editing else "", placeholder="Ex: SI-06")
    turno = st.selectbox("Turno", ["Matutino", "Vespertino", "Noturno", "Integral"],
                          index=["Matutino", "Vespertino", "Noturno", "Integral"].index(turma["turno"]) if editing else 0)
    ativo = st.checkbox("Turma ativa", value=turma["ativo"] if editing else True)
    if st.button("Salvar", type="primary", use_container_width=True):
        if not nome.strip() or not curso_obj:
            st.error("Preencha todos os campos obrigatórios.")
        else:
            if editing:
                ac.update_turma(turma["id"], nome=nome.strip(), cursoId=curso_obj["id"],
                                 nucleoId=curso_obj["nucleoId"], turno=turno, ativo=ativo)
                st.toast("Turma atualizada!", icon="✅")
            else:
                ac.add_turma(nome.strip(), curso_obj["id"], curso_obj["nucleoId"], turno, ativo)
                st.toast("Turma criada!", icon="✅")
            st.rerun()


@st.dialog("Disciplina")
def disciplina_modal(disc=None, scoped_nucleo_id=None):
    editing = disc is not None
    nucleo_opts = {n["nome"]: n["id"] for n in ac.list_nucleos() if n["ativo"]}
    if scoped_nucleo_id:
        nucleo_id = scoped_nucleo_id
        st.caption(f"Núcleo: {ac.get_nucleo_by_id(scoped_nucleo_id)['nome']}")
    else:
        default_name = ac.get_nucleo_by_id(disc["nucleoId"])["nome"] if editing else list(nucleo_opts.keys())[0]
        nucleo_sel = st.selectbox("Núcleo *", list(nucleo_opts.keys()),
                                   index=list(nucleo_opts.keys()).index(default_name) if default_name in nucleo_opts else 0)
        nucleo_id = nucleo_opts[nucleo_sel]
    c1, c2 = st.columns(2)
    codigo = c1.text_input("Código *", value=disc["codigo"] if editing else "")
    carga = c2.number_input("Carga horária *", min_value=15, step=15, value=disc["cargaHoraria"] if editing else 60)
    nome = st.text_input("Nome da disciplina *", value=disc["nome"] if editing else "")
    turmas_do_nucleo = ac.turmas_do_nucleo(nucleo_id)
    turma_names = [t["nome"] for t in turmas_do_nucleo]
    default_turmas = [t["nome"] for t in turmas_do_nucleo if editing and t["id"] in disc["turmasIds"]]
    turmas_sel = st.multiselect("Turmas vinculadas", turma_names, default=default_turmas)
    if st.button("Salvar", type="primary", use_container_width=True):
        if not codigo.strip() or not nome.strip():
            st.error("Preencha todos os campos obrigatórios.")
        else:
            turmas_ids = [t["id"] for t in turmas_do_nucleo if t["nome"] in turmas_sel]
            if editing:
                ac.update_disciplina(disc["id"], codigo=codigo.strip(), nome=nome.strip(),
                                      nucleoId=nucleo_id, cargaHoraria=int(carga), turmasIds=turmas_ids)
                st.toast("Disciplina atualizada!", icon="✅")
            else:
                ac.add_disciplina(codigo.strip(), nome.strip(), nucleo_id, int(carga), turmas_ids)
                st.toast("Disciplina criada!", icon="✅")
            st.rerun()


def nucleos_tab():
    st.markdown("###### Núcleos institucionais")
    if st.button("➕ Novo Núcleo", type="primary"):
        nucleo_modal()
    for n in ac.list_nucleos():
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1.4])
            with c1:
                st.markdown(f"**{n['nome']}**" + ("" if n["ativo"] else " _(inativo)_"))
                st.caption(n["descricao"])
                st.caption(f"{len(n['cursosIds'])} curso(s) vinculado(s)")
            with c3:
                bc1, bc2 = st.columns(2)
                if bc1.button("Editar", key=f"editn_{n['id']}", use_container_width=True):
                    nucleo_modal(n)
                if bc2.button("Excluir", key=f"deln_{n['id']}", use_container_width=True):
                    ac.delete_nucleo(n["id"])
                    st.rerun()


def cursos_tab(scoped_nucleo_id):
    st.markdown("###### Cursos")
    if st.button("➕ Novo Curso", type="primary"):
        curso_modal(scoped_nucleo_id=scoped_nucleo_id)
    visiveis = ac.list_cursos(scoped_nucleo_id)
    for c in visiveis:
        nucleo = ac.get_nucleo_by_id(c["nucleoId"])
        with st.container(border=True):
            cc1, cc2 = st.columns([3, 1.4])
            with cc1:
                st.markdown(f"**{c['nome']}**" + ("" if c["ativo"] else " _(inativo)_"))
                st.caption(f"Núcleo {nucleo['nome'] if nucleo else '—'} · {len(c['turmasIds'])} turma(s)")
            with cc2:
                bc1, bc2 = st.columns(2)
                if bc1.button("Editar", key=f"editc_{c['id']}", use_container_width=True):
                    curso_modal(c, scoped_nucleo_id=scoped_nucleo_id)
                if bc2.button("Excluir", key=f"delc_{c['id']}", use_container_width=True):
                    ac.delete_curso(c["id"])
                    st.rerun()
    if not visiveis:
        st.caption("Nenhum curso cadastrado.")


def turmas_tab(scoped_nucleo_id):
    st.markdown("###### Turmas")
    if st.button("➕ Nova Turma", type="primary"):
        turma_modal(scoped_nucleo_id=scoped_nucleo_id)
    visiveis = ac.list_turmas(scoped_nucleo_id)
    for t in visiveis:
        curso = ac.get_curso_by_id(t["cursoId"])
        with st.container(border=True):
            tc1, tc2 = st.columns([3, 1.4])
            with tc1:
                st.markdown(f"**{t['nome']}**" + ("" if t["ativo"] else " _(inativa)_"))
                st.caption(f"{curso['nome'] if curso else '—'} · {t['turno']} · "
                           f"{len(t['alunosIds'])} aluno(s) · {len(t['disciplinasIds'])} disciplina(s)")
            with tc2:
                bc1, bc2 = st.columns(2)
                if bc1.button("Editar", key=f"editt_{t['id']}", use_container_width=True):
                    turma_modal(t, scoped_nucleo_id=scoped_nucleo_id)
                if bc2.button("Excluir", key=f"delt_{t['id']}", use_container_width=True):
                    ac.delete_turma(t["id"])
                    st.rerun()
    if not visiveis:
        st.caption("Nenhuma turma cadastrada.")


def disciplinas_tab(scoped_nucleo_id):
    st.markdown("###### Disciplinas")
    if st.button("➕ Nova Disciplina", type="primary"):
        disciplina_modal(scoped_nucleo_id=scoped_nucleo_id)
    visiveis = ac.list_disciplinas(scoped_nucleo_id)
    for d in visiveis:
        with st.container(border=True):
            dc1, dc2 = st.columns([3, 1.4])
            with dc1:
                st.markdown(f"**{d['codigo']} — {d['nome']}**")
                st.caption(f"{d['cargaHoraria']}h · {len(d['turmasIds'])} turma(s) vinculada(s)")
            with dc2:
                bc1, bc2 = st.columns(2)
                if bc1.button("Editar", key=f"editd_{d['id']}", use_container_width=True):
                    disciplina_modal(d, scoped_nucleo_id=scoped_nucleo_id)
                if bc2.button("Excluir", key=f"deld_{d['id']}", use_container_width=True):
                    ac.delete_disciplina(d["id"])
                    st.rerun()
    if not visiveis:
        st.caption("Nenhuma disciplina cadastrada.")


def render():
    user = auth_controller.current_user()
    is_admin = auth_controller.is_admin()

    st.markdown('<div class="sga-eyebrow">GESTÃO ACADÊMICA</div>', unsafe_allow_html=True)
    st.markdown("<div class='sga-title'>Estrutura Acadêmica</div>", unsafe_allow_html=True)

    scoped_nucleo = None
    if not is_admin and user.get("nucleo"):
        scoped_nucleo = ac.get_nucleo_by_name(user["nucleo"])

    if is_admin:
        st.caption("Gerencie núcleos, cursos, turmas e disciplinas da instituição.")
    else:
        st.caption(f"Gerencie cursos, turmas e disciplinas do Núcleo {user.get('nucleo', '')}.")

    scoped_id = scoped_nucleo["id"] if scoped_nucleo else None

    labels = (["Núcleos"] if is_admin else []) + ["Cursos", "Turmas", "Disciplinas"]
    tabs = st.tabs(labels)
    idx = 0
    if is_admin:
        with tabs[idx]:
            nucleos_tab()
        idx += 1
    with tabs[idx]:
        cursos_tab(scoped_id)
    with tabs[idx + 1]:
        turmas_tab(scoped_id)
    with tabs[idx + 2]:
        disciplinas_tab(scoped_id)
