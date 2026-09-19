# -*- coding: utf-8 -*-
"""
[CONTROLLER] Preparação dos dados exibidos no Dashboard.

Aqui ficam os cálculos de métricas e agregações (quantas reservas, horas
utilizadas, picos de horário etc). A camada de apresentação (gráficos
Plotly, métricas do Streamlit) permanece na View — este controller só
entrega estruturas de dados prontas para renderizar.
"""

from datetime import datetime

import streamlit as st

from models import seed_data as data
from models import solicitacao_model

PROF_PERIOD_MULT = {"Última semana": 0.25, "Último mês": 1, "Últimos 3 meses": 3, "Todo o período": 5}
HOJE_REFERENCIA = datetime(2026, 8, 26)  # data-base da massa de dados simulada


def _parse_pt_date(d: str) -> datetime:
    return datetime.strptime(d, "%d/%m/%Y")


def _parse_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def diff_hours(inicio: str, fim: str) -> float:
    return max(0, (_parse_minutes(fim) - _parse_minutes(inicio)) / 60)


def format_horas(total: float) -> str:
    h = int(total)
    m = round((total - h) * 60)
    return f"{h}h {m}min" if m else f"{h}h"


def can_view_dashboard() -> bool:
    from controllers import auth_controller
    return auth_controller.has_perm("canViewDashboard")


def minhas_reservas(user_nome: str) -> list:
    return solicitacao_model.minhas_solicitacoes(st.session_state.solicitacoes, user_nome)


def pending_auth_for_coordenador(nucleo: str | None) -> list:
    reqs = solicitacao_model.auth_requests_do_nucleo(st.session_state.solicitacoes, nucleo)
    return solicitacao_model.pendentes(reqs)


# ── Dashboard do Professor ───────────────────────────────────────────────────

def professor_dashboard_data(user_name: str, my_reservas: list, periodo_label: str) -> dict:
    mult = PROF_PERIOD_MULT[periodo_label]

    valid = [r for r in my_reservas if r["status"] not in ("Cancelado", "Recusado")]
    total_horas_real = sum(diff_hours(r["inicio"], r["fim"]) for r in valid)
    media_partic_real = round(sum(r["pessoas"] for r in valid) / len(valid)) if valid else 0

    chart_rooms = sorted(
        [{**r, "reservas": max(1, round(r["reservas"] * mult)), "horas": round(r["horas"] * mult, 1),
          "pessoas": round(r["pessoas"] * mult)} for r in data.PROF_BASE_ROOMS],
        key=lambda r: -r["reservas"],
    )
    chart_hours = [{**h, "reservas": max(1, round(h["reservas"] * mult))} for h in data.PROF_BASE_HOURS]
    total_chart_reservas = sum(h["reservas"] for h in chart_hours)
    peak_periodo = max(chart_hours, key=lambda h: h["reservas"])
    sala_top = chart_rooms[0]

    total_reservas_card = len(valid) or round(sum(r["reservas"] for r in data.PROF_BASE_ROOMS) * mult)
    total_horas_card = format_horas(total_horas_real) if total_horas_real > 0 else format_horas(
        sum(r["horas"] for r in data.PROF_BASE_ROOMS) * mult)
    media_card = media_partic_real or round(
        sum(r["pessoas"] for r in data.PROF_BASE_ROOMS) / sum(r["reservas"] for r in data.PROF_BASE_ROOMS))

    future = sorted([r for r in valid if _parse_pt_date(r["data"]) >= HOJE_REFERENCIA],
                     key=lambda r: _parse_pt_date(r["data"]))
    proxima = future[0] if future else None
    proxima_tag = None
    if proxima:
        diff_days = (_parse_pt_date(proxima["data"]) - HOJE_REFERENCIA).days
        proxima_tag = "Hoje" if diff_days == 0 else "Amanhã" if diff_days == 1 else f"Faltam {diff_days} dias"

    insights = [
        f"Você utiliza mais o {sala_top['sala']} — {sala_top['reservas']} reservas no período.",
        f"Suas reservas acontecem principalmente no período da {peak_periodo['periodo'].lower()} "
        f"({peak_periodo['label']}).",
        f"Você realizou {round(sum(r['reservas'] for r in data.PROF_BASE_ROOMS) * mult)} reservas "
        f"no período selecionado.",
    ]

    return {
        "chart_rooms": chart_rooms,
        "chart_hours": chart_hours,
        "total_chart_reservas": total_chart_reservas,
        "peak_periodo": peak_periodo,
        "sala_top": sala_top,
        "total_reservas_card": total_reservas_card,
        "total_horas_card": total_horas_card,
        "media_card": media_card,
        "proxima": proxima,
        "proxima_tag": proxima_tag,
        "insights": insights,
        "user_first_names": " ".join(user_name.split(" ")[:2]),
    }


# ── Dashboard do Admin / Coordenador ─────────────────────────────────────────

def admin_coord_dashboard_data(solicitacoes: list) -> dict:
    ativos = [s for s in solicitacoes if s["status"] != "Cancelado"]
    aprovados = [s for s in solicitacoes if s["status"] == "Aprovado"]
    pendentes = [s for s in solicitacoes if s["status"] in ("Pendente", "Em análise")]
    total_pessoas = sum(s["pessoas"] for s in ativos)

    ocupacao = []
    for r in data.ALL_ROOM_STATS:
        taxa = min(100, round(r["horas"] / (22 * 10) * 100))
        cor = "#8B0019" if taxa >= 70 else ("#1E5E60" if taxa >= 50 else "#A8A09A")
        ocupacao.append({"sala": r["sala"], "taxa": taxa, "cor": cor})

    recentes = [
        {
            "Ambiente": s["sala"], "Solicitante": s["solicitante"], "Data": s["data"],
            "Horário": f"{s['inicio']}–{s['fim']}", "Status": s["status"],
        }
        for s in solicitacoes[:8]
    ]

    return {
        "total_reservas": len(ativos),
        "aprovadas": len(aprovados),
        "pendentes": len(pendentes),
        "total_pessoas": total_pessoas,
        "ocupacao": ocupacao,
        "recentes": recentes,
    }
