# -*- coding: utf-8 -*-
"""[VIEW] Membros — equivalente a src/pages/Membros.tsx."""

import streamlit as st

from controllers import academico_controller, auth_controller, membros_controller as mc
from models import seed_data as data
from views.components import badge_html


@st.dialog("Membro")
def member_modal(member=None):
    editing = member is not None
    st.markdown(f"##### {'Editar Membro' if editing else 'Adicionar Membro'}")
    nome = st.text_input("Nome completo *", value=member["nome"] if editing else "")
    email = st.text_input("E-mail *", value=member["email"] if editing else "")
    c1, c2 = st.columns(2)
    funcao = c1.selectbox("Função", data.FUNCOES,
                           index=data.FUNCOES.index(member["funcao"]) if editing else 3)
    depto = c2.selectbox("Departamento", data.DEPTOS,
                          index=data.DEPTOS.index(member["depto"]) if editing and member["depto"] in data.DEPTOS else 0)
    nucleo_opts = ["— Global (sem restrição) —"] + [n["nome"] for n in academico_controller.list_nucleos() if n["ativo"]]
    cur_nucleo = member.get("nucleo") if editing else None
    nucleo_sel = st.selectbox("Núcleo", nucleo_opts,
                               index=nucleo_opts.index(cur_nucleo) if cur_nucleo in nucleo_opts else 0)
    status = st.radio("Status", ["Ativo", "Inativo"],
                       index=0 if not editing or member["status"] == "Ativo" else 1, horizontal=True)

    if st.button("Salvar" if editing else "Adicionar", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("O nome é obrigatório.")
        elif "@" not in email:
            st.error("Informe um e-mail válido.")
        else:
            payload = {
                "nome": nome, "email": email, "funcao": funcao, "depto": depto,
                "nucleo": None if nucleo_sel.startswith("—") else nucleo_sel, "status": status,
            }
            if editing:
                mc.update_member(member["id"], payload)
                st.toast("Membro atualizado com sucesso!", icon="✅")
            else:
                mc.add_member_directly(payload)
                st.toast(f"{nome} adicionado(a) com sucesso!", icon="✅")
            st.rerun()


@st.dialog("Remover membro?")
def confirm_delete_modal(member):
    st.warning(f"**{member['nome']}** será removido permanentemente do sistema. Esta ação não pode ser desfeita.")
    c1, c2 = st.columns(2)
    if c1.button("Cancelar", use_container_width=True):
        st.rerun()
    if c2.button("Remover", type="primary", use_container_width=True):
        mc.remove_member(member["id"])
        st.toast("Membro removido.", icon="✅")
        st.rerun()


@st.dialog("Analisar Solicitação de Cadastro", width="large")
def registration_review_modal(member):
    st.caption(member["nome"])
    if member.get("motivoCorrecao"):
        st.error(f"**Motivo da correção solicitada:** {member['motivoCorrecao']}")

    with st.container(border=True):
        st.markdown(f"**Nome:** {member['nome']}")
        st.markdown(f"**E-mail:** {member['email']}")
        if member.get("cpf"):
            st.markdown(f"**CPF:** {member['cpf']}")
        st.markdown(f"**Função:** {member['funcao']}")
        st.markdown(f"**Núcleo:** {member.get('nucleo') or '—'}")
        st.markdown(f"**Curso:** {member.get('curso') or '—'}")
        st.markdown(f"**Turno:** {member.get('turno') or '—'}")
        st.markdown(f"**Turma:** {member.get('turma') or '—'}")
        if member.get("disciplinas"):
            st.markdown(f"**Disciplinas:** {', '.join(member['disciplinas'])}")

    action = st.radio("Ação", ["Aprovar", "Solicitar correção", "Rejeitar"], horizontal=True)
    motivo = ""
    if action in ("Solicitar correção", "Rejeitar"):
        motivo = st.text_area("Motivo *")

    if st.button("Confirmar", type="primary", use_container_width=True):
        if action in ("Solicitar correção", "Rejeitar") and not motivo.strip():
            st.error("Informe o motivo.")
        else:
            if action == "Aprovar":
                mc.approve_member(member["id"])
                st.toast(f"{member['nome']} aprovado(a)!", icon="✅")
            elif action == "Solicitar correção":
                mc.solicitar_correcao(member["id"], motivo)
                st.toast("Correção solicitada.", icon="✅")
            else:
                mc.reject_member(member["id"])
                st.toast("Cadastro rejeitado.", icon="⚠️")
            st.rerun()


def render():
    is_admin = auth_controller.is_admin()

    st.markdown('<div class="sga-eyebrow">EQUIPE</div>', unsafe_allow_html=True)
    hc1, hc2 = st.columns([3, 1])
    hc1.markdown("<div class='sga-title'>Organização de Membros</div>", unsafe_allow_html=True)
    hc1.caption("Gerencie os membros e organize as informações da equipe.")

    pending_requests = mc.pending_requests()

    if is_admin:
        tab_labels = ["Membros", f"Solicitações de Cadastro ({len(pending_requests)})"]
        tabs = st.tabs(tab_labels)
    else:
        tabs = [st.container()]

    with tabs[0]:
        if is_admin:
            if st.button("➕ Adicionar Membro", type="primary"):
                member_modal()

        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        search = c1.text_input("Buscar por nome ou e-mail", key="mem_search")
        filtro_funcao = c2.selectbox("Função", ["Todos"] + data.FUNCOES, key="mem_funcao")
        filtro_status = c3.selectbox("Status", ["Todos", "Ativo", "Inativo", "Pendente"], key="mem_status")
        filtro_nucleo = c4.selectbox("Núcleo", ["Todos", "Global"] + data.NUCLEOS, key="mem_nucleo") if is_admin else "Todos"

        filtered = mc.filter_members(search, filtro_funcao, filtro_status, filtro_nucleo)

        st.caption(f"{len(filtered)} membro(s)")

        for m in filtered:
            f_badge = data.FUNCAO_BADGE.get(m["funcao"], {"bg": "#F3EFEA", "text": "#776D5B"})
            s_badge = data.MEMBER_STATUS_BADGE.get(m["status"], data.MEMBER_STATUS_BADGE["Pendente"])
            with st.container(border=True):
                c1, c2, c3, c4, c5 = st.columns([2.2, 1, 1, 1, 1.4])
                with c1:
                    st.markdown(f"**{m['nome']}**")
                    st.caption(m["email"])
                with c2:
                    st.markdown(badge_html(m["funcao"], f_badge["bg"], f_badge["text"]), unsafe_allow_html=True)
                with c3:
                    st.caption(m.get("nucleo") or "Global")
                with c4:
                    st.caption(m.get("turma") or "—")
                with c5:
                    st.markdown(badge_html(m["status"], s_badge["bg"], s_badge["text"], s_badge["dot"]),
                                unsafe_allow_html=True)
                if is_admin:
                    ac1, ac2, ac3 = st.columns(3)
                    if ac1.button("Editar", key=f"editm_{m['id']}", use_container_width=True):
                        member_modal(m)
                    toggle_label = "Desativar" if m["status"] == "Ativo" else "Ativar"
                    if ac2.button(toggle_label, key=f"togm_{m['id']}", use_container_width=True):
                        mc.toggle_member_status(m["id"])
                        st.rerun()
                    if ac3.button("Remover", key=f"delm_{m['id']}", use_container_width=True):
                        confirm_delete_modal(m)

        if not filtered:
            st.info("Nenhum membro encontrado. Tente ajustar os filtros de busca.")

    if is_admin:
        with tabs[1]:
            if not pending_requests:
                st.success("Nenhuma solicitação pendente. Todas as solicitações de cadastro foram processadas.")
            for m in pending_requests:
                s_badge = data.MEMBER_STATUS_BADGE.get(m["status"], data.MEMBER_STATUS_BADGE["Pendente"])
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**{m['nome']}**")
                        st.caption(m["email"])
                        st.caption(f"{m['funcao']} · {m.get('nucleo') or '—'} · {m.get('curso') or '—'}")
                    with c2:
                        st.markdown(badge_html(m["status"], s_badge["bg"], s_badge["text"], s_badge["dot"]),
                                    unsafe_allow_html=True)
                    if m.get("motivoCorrecao"):
                        st.caption(f"⚠ {m['motivoCorrecao']}")
                    if st.button("Analisar", key=f"review_{m['id']}", use_container_width=True):
                        registration_review_modal(m)
