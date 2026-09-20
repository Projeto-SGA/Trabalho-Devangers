# -*- coding: utf-8 -*-
"""[VIEW] Reservas — equivalente a src/pages/Reservas.tsx."""

from datetime import date, datetime, time

import streamlit as st

from controllers import auth_controller, reservas_controller as rc
from models import seed_data as data
from views.components import TEXT_MUTED, badge_html


# ── Modal: Nova sala (Admin) ─────────────────────────────────────────────────

@st.dialog("Sala", width="large")
def sala_modal(sala=None):
    editing = sala is not None
    st.markdown(f"##### {'Editar Sala' if editing else 'Adicionar Sala'}")
    nome = st.text_input("Nome da sala *", value=sala["nome"] if editing else "")
    c1, c2 = st.columns(2)
    bloco = c1.text_input("Bloco *", value=sala["bloco"] if editing else "")
    numero = c2.text_input("Localização *", value=sala["numero"] if editing else "")
    c3, c4 = st.columns(2)
    tipo = c3.selectbox("Tipo", data.TIPO_OPTIONS,
                         index=data.TIPO_OPTIONS.index(sala["tipo"]) if editing and sala["tipo"] in data.TIPO_OPTIONS else 0)
    capacidade = c4.number_input("Capacidade (pessoas) *", min_value=1, value=sala["capacidade"] if editing else 30)
    recursos = st.multiselect("Recursos disponíveis", data.RECURSO_OPTIONS,
                               default=[r for r in (sala["recursos"] if editing else []) if r in data.RECURSO_OPTIONS])
    extra_recursos_raw = st.text_input(
        "Recursos personalizados (separe por vírgula)",
        value=", ".join([r for r in (sala["recursos"] if editing else []) if r not in data.RECURSO_OPTIONS]),
    )
    extra_recursos = [r.strip() for r in extra_recursos_raw.split(",") if r.strip()]
    exige_auth = st.checkbox("Exige autorização do coordenador para reserva",
                              value=sala.get("exigeAutorizacao", False) if editing else False)
    status = sala["status"] if editing else "Disponível"
    if editing:
        status = st.radio("Status da sala", ["Disponível", "Manutenção", "Inativa"],
                           index=["Disponível", "Manutenção", "Inativa"].index(sala["status"]), horizontal=True)

    if st.button("Salvar alterações" if editing else "Cadastrar Sala", type="primary", use_container_width=True):
        if not nome or not bloco or not numero:
            st.error("Preencha todos os campos obrigatórios.")
        elif capacidade < 1:
            st.error("Informe uma capacidade válida (mínimo 1 pessoa).")
        else:
            payload = {
                "nome": nome, "bloco": bloco, "numero": numero, "tipo": tipo,
                "capacidade": int(capacidade), "recursos": recursos + extra_recursos,
                "exigeAutorizacao": exige_auth, "status": status,
            }
            if editing:
                rc.update_sala(sala["id"], payload)
                st.toast(f'Sala "{nome}" atualizada!', icon="✅")
            else:
                rc.add_sala(payload)
                st.toast(f'Sala "{nome}" cadastrada!', icon="✅")
            st.rerun()


# ── Modal: Nova solicitação / reserva ────────────────────────────────────────

@st.dialog("Reserva", width="large")
def solicitacao_modal():
    user = auth_controller.current_user()
    is_aluno = user["role"] == "Aluno"

    salas_disp = rc.salas_disponiveis()
    st.markdown(f"##### {'Solicitar Reserva' if is_aluno else 'Nova Reserva'}")
    if is_aluno:
        st.caption("Necessita aprovação do professor responsável")

    opts = {f'{s["nome"]} — {s["bloco"]} {s["numero"]} · cap. {s["capacidade"]} pessoas'
            + (" ⚠ Autorização" if s.get("exigeAutorizacao") else ""): s for s in salas_disp}
    sel_label = st.selectbox("Sala *", [""] + list(opts.keys()))
    sala_sel = opts.get(sel_label)

    needs_auth = bool(sala_sel and sala_sel.get("exigeAutorizacao") and not is_aluno)
    if needs_auth:
        st.info("Este ambiente exige autorização do coordenador.")

    if sala_sel:
        with st.container(border=True):
            st.markdown(f"**{sala_sel['nome']}** — capacidade: {sala_sel['capacidade']} pessoas")
            st.caption(", ".join(sala_sel["recursos"]) if sala_sel["recursos"] else "Sem recursos cadastrados")

    c1, c2, c3 = st.columns(3)
    data_res = c1.date_input("Data *", min_value=date.today(), value=date.today())
    inicio = c2.time_input("Início *", value=time(8, 0))
    fim = c3.time_input("Término *", value=time(10, 0))

    time_error = ""
    if fim <= inicio:
        time_error = "O horário de término deve ser posterior ao de início."
    elif data_res == date.today() and inicio < datetime.now().time():
        time_error = "O horário de início já passou. Escolha um horário futuro."
    if time_error:
        st.error(time_error)

    if st.checkbox("Ver disponibilidade da sala nesta data") and sala_sel:
        data_ptbr = data_res.strftime("%d/%m/%Y")
        rows = rc.disponibilidade_da_sala(sala_sel["nome"], data_ptbr)
        st.dataframe(rows, hide_index=True, use_container_width=True)

    pessoas = st.number_input("Quantidade de pessoas *", min_value=1, value=1)
    capacity_error = ""
    if sala_sel and pessoas > sala_sel["capacidade"]:
        capacity_error = (f"A capacidade máxima desta sala é de {sala_sel['capacidade']} pessoas. "
                           f"Você informou {pessoas} — reduza o número de participantes ou escolha um ambiente maior.")
        st.error(capacity_error)

    professor = ""
    if is_aluno:
        professor = st.selectbox("Professor responsável *", [""] + data.PROFESSORS)

    obs = st.text_area("Observações", placeholder="Descreva o motivo da solicitação…" if is_aluno else "Informações adicionais…")

    can_submit = sala_sel and not time_error and not capacity_error and (not is_aluno or professor)
    btn_label = "Enviar Solicitação" if is_aluno else ("Solicitar Autorização" if needs_auth else "Confirmar Reserva")

    if st.button(btn_label, type="primary", disabled=not can_submit, use_container_width=True):
        tipo = "aluno_para_professor" if is_aluno else ("auth_required" if needs_auth else "direta")
        status_ini = "Pendente" if is_aluno else ("Em análise" if needs_auth else "Aprovado")
        rc.add_solicitacao(
            tipo=tipo, sala=sala_sel["nome"], bloco=f'{sala_sel["bloco"]} — {sala_sel["numero"]}',
            data=data_res.strftime("%d/%m/%Y"), inicio=inicio.strftime("%H:%M"), fim=fim.strftime("%H:%M"),
            pessoas=int(pessoas), solicitante=user["nome"], solicitanteRole=user["role"],
            nucleoSolicitante=user.get("nucleo"),
            professorResponsavel=professor if is_aluno else None,
            status=status_ini, motivo=obs,
        )
        if is_aluno:
            st.success("Solicitação enviada! Sua solicitação foi enviada ao professor responsável e aguarda aprovação.")
        elif needs_auth:
            st.success("Aguardando autorização — sua solicitação foi encaminhada ao coordenador.")
        else:
            st.success("Reserva confirmada com sucesso!")
        st.balloons()
        if st.button("Fechar"):
            st.rerun()


@st.dialog("Recusar solicitação")
def recusar_modal(sol):
    st.caption(f'{sol["sala"]} · {sol["data"]} · {sol["inicio"]}–{sol["fim"]}')
    motivo = st.text_area("Motivo da recusa *")
    if st.button("Confirmar recusa", type="primary", disabled=not motivo.strip(), use_container_width=True):
        rc.recusar_solicitacao(sol["id"], auth_controller.current_user()["nome"], motivo)
        st.rerun()


# ── Cards ─────────────────────────────────────────────────────────────────────

def solicitacao_card(s, can_approve, can_reject, can_cancel, current_user):
    st_style = data.STATUS_SOL_STYLE.get(s["status"], data.STATUS_SOL_STYLE["Pendente"])
    is_pending = s["status"] in ("Pendente", "Em análise")
    with st.container(border=True):
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"**{s['sala']}**")
            st.caption(s["bloco"])
        with c2:
            st.markdown(badge_html(s["status"], st_style["bg"], st_style["text"], st_style["dot"]),
                        unsafe_allow_html=True)
            if s["tipo"] == "auth_required":
                st.caption("Exige autorização")

        cc1, cc2, cc3, cc4 = st.columns(4)
        cc1.markdown(f"<small style='color:{TEXT_MUTED}'>Data</small><br/><b>{s['data']}</b>", unsafe_allow_html=True)
        cc2.markdown(f"<small style='color:{TEXT_MUTED}'>Horário</small><br/><b>{s['inicio']}–{s['fim']}</b>", unsafe_allow_html=True)
        cc3.markdown(f"<small style='color:{TEXT_MUTED}'>Solicitante</small><br/><b>{s['solicitante']}</b>", unsafe_allow_html=True)
        cc4.markdown(f"<small style='color:{TEXT_MUTED}'>Pessoas</small><br/><b>{s['pessoas']}</b>", unsafe_allow_html=True)

        if s.get("professorResponsavel"):
            st.caption(f"Professor: {s['professorResponsavel']}")
        if s.get("aprovadoPor"):
            st.caption(f"Decisão por: {s['aprovadoPor']} · {s.get('dataAprovacao', '')}")
        if s.get("observacao"):
            st.caption(f"Observação: _{s['observacao']}_")

        bc1, bc2, bc3 = st.columns(3)
        if is_pending and can_approve:
            if bc1.button("Aprovar", key=f"aprov_{s['id']}", use_container_width=True):
                rc.aprovar_solicitacao(s["id"], current_user)
                st.rerun()
        if is_pending and can_reject:
            if bc2.button("Recusar", key=f"rec_{s['id']}", use_container_width=True):
                recusar_modal(s)
        if can_cancel and s["status"] != "Cancelado":
            if bc3.button("Cancelar", key=f"canc_{s['id']}", use_container_width=True):
                rc.cancelar_solicitacao(s["id"])
                st.rerun()


def render():
    user = auth_controller.current_user()
    perms = auth_controller.permissions()
    is_aluno = user["role"] == "Aluno"
    is_professor = user["role"] == "Professor"
    is_coordenador = user["role"] == "Coordenador"
    is_admin = auth_controller.is_admin()

    salas = rc.list_salas()
    minhas = rc.minhas_solicitacoes(user["nome"])
    pend_professor = rc.pendentes_para_professor(user["nome"])
    coord_nucleo = user.get("nucleo")
    todas_auth_coord = rc.auth_requests_do_nucleo(coord_nucleo)
    pend_coord = rc.pendentes(todas_auth_coord)

    st.markdown('<div class="sga-eyebrow">GESTÃO</div>', unsafe_allow_html=True)
    hc1, hc2 = st.columns([3, 2])
    with hc1:
        st.markdown(f"<div class='sga-title'>{'Ambientes e Solicitações' if is_aluno else 'Reservas'}</div>",
                    unsafe_allow_html=True)
        st.caption("Consulte a disponibilidade dos ambientes e gerencie suas reservas."
                   if not is_aluno else "Consulte os ambientes disponíveis e envie solicitações de reserva.")
    with hc2:
        b1, b2 = st.columns(2)
        if is_admin:
            if b1.button("➕ Adicionar Sala", use_container_width=True):
                sala_modal()
        if perms["canRequestReserva"] or perms["canMakeDirectReserva"]:
            if b2.button("Solicitar Reserva" if is_aluno else "Nova Reserva", type="primary", use_container_width=True):
                solicitacao_modal()

    if is_aluno:
        st.info("Como **Aluno**, você pode consultar salas e enviar solicitações. "
                "As reservas precisam ser aprovadas pelo professor responsável.")

    tab_labels = ["Ambientes", "Minhas Solicitações" if is_aluno else "Minhas Reservas"]
    show_aprov = perms["canApproveStudentRequests"] or perms["canApproveAuthRequests"] or perms["canViewAllReservas"]
    if show_aprov:
        tab_labels.append("Solicitações de Alunos" if is_professor else
                           "Autorizações" if is_coordenador else "Todas as Reservas")

    tabs = st.tabs(tab_labels)

    # ── Ambientes ──
    with tabs[0]:
        cols = st.columns(3)
        for i, s in enumerate(salas):
            style = data.STATUS_SALA_STYLE[s["status"]]
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{s['nome']}**")
                    st.caption(f"{s['bloco']} — {s['numero']} · {s['tipo']}")
                    st.markdown(badge_html(s["status"], style["bg"], style["text"], style["dot"]),
                                unsafe_allow_html=True)
                    st.caption(f"Capacidade: {s['capacidade']} pessoas")
                    if s["recursos"]:
                        st.caption(" · ".join(s["recursos"]))
                    if s.get("exigeAutorizacao"):
                        st.caption("⚠ Exige autorização do coordenador")
                    if is_admin:
                        ac1, ac2 = st.columns(2)
                        if ac1.button("Editar", key=f"editsala_{s['id']}", use_container_width=True):
                            sala_modal(s)
                        manut_label = "✓ Reativar" if s["status"] == "Manutenção" else "⚠ Manutenção"
                        if ac2.button(manut_label, key=f"manut_{s['id']}", use_container_width=True):
                            rc.toggle_manutencao(s["id"])
                            st.rerun()
        if is_admin:
            if st.button("+ Nova Sala", use_container_width=True):
                sala_modal()

    # ── Minhas reservas ──
    with tabs[1]:
        if not minhas:
            st.info("Nenhuma solicitação encontrada." if is_aluno else "Nenhuma reserva encontrada.")
        else:
            cols = st.columns(2)
            for i, s in enumerate(minhas):
                with cols[i % 2]:
                    solicitacao_card(s, can_approve=False, can_reject=False,
                                      can_cancel=s["status"] not in ("Cancelado", "Recusado"),
                                      current_user=user["nome"])

    # ── Aprovações / Todas ──
    if show_aprov:
        with tabs[2]:
            if is_admin:
                todas = rc.list_solicitacoes()
                st.markdown(f"**Todas as Reservas e Solicitações** ({len(todas)} total)")
                cols = st.columns(2)
                for i, s in enumerate(todas):
                    with cols[i % 2]:
                        solicitacao_card(s, can_approve=False, can_reject=False,
                                          can_cancel=s["status"] != "Cancelado", current_user=user["nome"])
            elif is_professor:
                minhas_alunos = rc.solicitacoes_de_alunos_do_professor(user["nome"])
                st.markdown(f"**Solicitações de Alunos** " +
                            (f"({len(pend_professor)} pendente(s))" if pend_professor else ""))
                if not minhas_alunos:
                    st.info("Nenhuma solicitação recebida.")
                else:
                    cols = st.columns(2)
                    for i, s in enumerate(minhas_alunos):
                        with cols[i % 2]:
                            can_act = s["status"] in ("Pendente", "Em análise")
                            solicitacao_card(s, can_approve=can_act, can_reject=can_act,
                                              can_cancel=False, current_user=user["nome"])
            elif is_coordenador:
                label = f"**Solicitações que exigem autorização**"
                if coord_nucleo:
                    label += f" — Núcleo {coord_nucleo}"
                if pend_coord:
                    label += f" · {len(pend_coord)} aguardando"
                st.markdown(label)
                if not todas_auth_coord:
                    st.info(f"Nenhuma solicitação de autorização" + (f" para o Núcleo {coord_nucleo}" if coord_nucleo else "") + ".")
                else:
                    cols = st.columns(2)
                    for i, s in enumerate(todas_auth_coord):
                        with cols[i % 2]:
                            can_act = s["status"] in ("Pendente", "Em análise")
                            solicitacao_card(s, can_approve=can_act, can_reject=can_act,
                                              can_cancel=False, current_user=user["nome"])
