# -*- coding: utf-8 -*-
"""
[MODEL] Entidade Solicitação / Reserva.

Funções puras de criação, aprovação, recusa e cancelamento. O Controller
(reservas_controller) é responsável por buscar a lista em st.session_state,
chamar estas funções e persistir o resultado de volta na sessão.
"""

from datetime import datetime

SLOTS = [("08:00", "10:00"), ("10:00", "12:00"), ("12:00", "14:00"),
         ("14:00", "16:00"), ("16:00", "18:00"), ("18:00", "20:00")]


def _now_str() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def add_solicitacao(solicitacoes: list, next_id: int, **kwargs) -> tuple[dict, int]:
    """Cria uma nova solicitação. Devolve (solicitação criada, próximo id livre)."""
    sol = dict(kwargs)
    sol["id"] = next_id
    sol["createdAt"] = _now_str()
    solicitacoes.append(sol)
    return sol, next_id + 1


def aprovar_solicitacao(solicitacoes: list, sol_id: int, aprovado_por: str, obs: str | None = None) -> None:
    for s in solicitacoes:
        if s["id"] == sol_id:
            s["status"] = "Aprovado"
            s["aprovadoPor"] = aprovado_por
            s["dataAprovacao"] = _now_str()
            if obs:
                s["observacao"] = obs
            return


def recusar_solicitacao(solicitacoes: list, sol_id: int, aprovado_por: str, obs: str) -> None:
    for s in solicitacoes:
        if s["id"] == sol_id:
            s["status"] = "Recusado"
            s["aprovadoPor"] = aprovado_por
            s["dataAprovacao"] = _now_str()
            s["observacao"] = obs
            return


def cancelar_solicitacao(solicitacoes: list, sol_id: int) -> None:
    for s in solicitacoes:
        if s["id"] == sol_id:
            s["status"] = "Cancelado"
            return


# ── Consultas ─────────────────────────────────────────────────────────────────

def minhas_solicitacoes(solicitacoes: list, nome_usuario: str) -> list:
    return [s for s in solicitacoes if s["solicitante"] == nome_usuario]


def pendentes_para_professor(solicitacoes: list, nome_professor: str) -> list:
    return [s for s in solicitacoes if s["tipo"] == "aluno_para_professor"
            and s.get("professorResponsavel") == nome_professor
            and s["status"] in ("Pendente", "Em análise")]


def solicitacoes_de_alunos_do_professor(solicitacoes: list, nome_professor: str) -> list:
    return [s for s in solicitacoes if s.get("professorResponsavel") == nome_professor]


def auth_requests_do_nucleo(solicitacoes: list, nucleo: str | None) -> list:
    return [s for s in solicitacoes if s["tipo"] == "auth_required"
            and (not nucleo or not s.get("nucleoSolicitante") or s.get("nucleoSolicitante") == nucleo)]


def pendentes(lista: list) -> list:
    return [s for s in lista if s["status"] in ("Pendente", "Em análise")]


def disponibilidade_da_sala(solicitacoes: list, sala_nome: str, data_ptbr: str) -> list:
    """Devolve, para cada slot padrão do dia, se está ocupado ou disponível."""
    rows = []
    for si, fi in SLOTS:
        ocupado = next(
            (s for s in solicitacoes
             if s["sala"] == sala_nome and s["data"] == data_ptbr
             and s["status"] not in ("Cancelado", "Recusado") and s["inicio"] == si),
            None,
        )
        rows.append({
            "Horário": f"{si}–{fi}",
            "Status": f"Ocupado · {ocupado['solicitante']}" if ocupado else "Disponível",
        })
    return rows
