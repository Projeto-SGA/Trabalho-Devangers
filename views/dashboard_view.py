# -*- coding: utf-8 -*-
"""[VIEW] Dashboard — equivalente a src/pages/Dashboard.tsx.

Toda a preparação de métricas/agregações vive em controllers.dashboard_controller;
aqui só acontece a montagem dos gráficos (Plotly) e a renderização Streamlit.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from controllers import auth_controller, dashboard_controller as dc
from models import seed_data as data
from views.components import PRIMARY, TEXT_MUTED, badge_html


def bar_chart(x, y, colors=None, height=260, horizontal=False):
    if horizontal:
        fig = go.Figure(go.Bar(y=x, x=y, orientation="h", marker_color=colors or PRIMARY))
    else:
        fig = go.Figure(go.Bar(x=x, y=y, marker_color=colors or PRIMARY))
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(color=TEXT_MUTED, size=11),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#F3EFEA"),
    )
    return fig


# ── Dashboard do Professor ───────────────────────────────────────────────────

def professor_dashboard(user_name, my_reservas):
    st.markdown('<div class="sga-eyebrow">VISÃO PESSOAL</div>', unsafe_allow_html=True)
    st.markdown("<div class='sga-title'>Meu Dashboard</div>", unsafe_allow_html=True)

    periodo = st.radio("Período", list(dc.PROF_PERIOD_MULT.keys()), horizontal=True, index=1,
                        label_visibility="collapsed")
    d = dc.professor_dashboard_data(user_name, my_reservas, periodo)

    st.caption(f"Acompanhe suas reservas, utilização dos ambientes e principais indicadores — "
               f"{d['user_first_names']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de reservas", d["total_reservas_card"])
    c2.metric("Sala mais utilizada", " ".join(d["sala_top"]["sala"].split(" ")[:2]))
    c3.metric("Média de participantes", f"{d['media_card']} pessoas")
    c4.metric("Total de horas utilizadas", d["total_horas_card"])

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("###### Próxima reserva")
        proxima = d["proxima"]
        if proxima:
            st.markdown(f"**{proxima['sala']}**")
            st.caption(proxima["bloco"])
            st.write(f"📅 {proxima['data']}")
            st.write(f"🕒 {proxima['inicio']}–{proxima['fim']}")
            st.write(f"👥 {proxima['pessoas']} participantes")
            st.markdown(badge_html(d["proxima_tag"], "#FFF0F2", PRIMARY), unsafe_allow_html=True)
        else:
            st.caption("Você não possui reservas futuras.")

    with col2:
        st.markdown("###### Horários mais utilizados")
        peak = d["peak_periodo"]
        pct = round(peak["reservas"] / d["total_chart_reservas"] * 100)
        st.caption(f"Horário preferido: **{peak['label']}** — {pct}% das suas reservas")
        for h in d["chart_hours"]:
            hp = round(h["reservas"] / d["total_chart_reservas"] * 100)
            st.write(f"{h['periodo']} ({h['label']}) — {h['reservas']} reservas")
            st.progress(hp / 100)

    st.markdown("###### Utilização por ambiente")
    df = pd.DataFrame(d["chart_rooms"])
    st.plotly_chart(bar_chart(df["sala"], df["reservas"]), use_container_width=True)

    st.markdown("###### Insights")
    for ins in d["insights"]:
        st.markdown(f"- {ins}")


# ── Dashboard do Admin / Coordenador ─────────────────────────────────────────

def admin_coord_dashboard(user, solicitacoes, pending_for_me, is_admin):
    st.markdown('<div class="sga-eyebrow">GESTÃO</div>', unsafe_allow_html=True)
    st.markdown("<div class='sga-title'>Dashboard</div>", unsafe_allow_html=True)
    st.caption("Visão geral das reservas, ambientes e principais indicadores do sistema.")

    d = dc.admin_coord_dashboard_data(solicitacoes)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de reservas", d["total_reservas"])
    c2.metric("Aprovadas", d["aprovadas"])
    c3.metric("Pendentes / Em análise", d["pendentes"])
    c4.metric("Participantes atendidos", d["total_pessoas"])

    if not is_admin and pending_for_me:
        st.warning(f"Você tem **{len(pending_for_me)}** solicitação(ões) de autorização aguardando sua decisão.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("###### Reservas por dia da semana")
        df = pd.DataFrame(data.WEEK_DATA)
        st.plotly_chart(bar_chart(df["day"], df["reservas"]), use_container_width=True)

    with col2:
        st.markdown("###### Horários de maior utilização")
        df = pd.DataFrame(data.ALL_PEAK_HOURS)
        max_val = df["reservas"].max()
        colors = ["#8B0019" if v == max_val else "#D47080" for v in df["reservas"]]
        st.plotly_chart(bar_chart(df["slot"], df["reservas"], colors=colors), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("###### Reservas por ambiente")
        df = pd.DataFrame(data.ALL_ROOM_STATS).sort_values("reservas", ascending=True)
        st.plotly_chart(bar_chart(df["sala"], df["reservas"], horizontal=True), use_container_width=True)

    with col4:
        st.markdown("###### Taxa de ocupação dos ambientes")
        st.caption("Horas reservadas ÷ horas disponíveis (considerando 10h/dia úteis)")
        for r in d["ocupacao"]:
            st.write(f"**{r['sala']}** — {r['taxa']}%")
            st.progress(r["taxa"] / 100)

    st.markdown("###### Reservas Recentes")
    st.dataframe(pd.DataFrame(d["recentes"]), hide_index=True, use_container_width=True)


def render():
    user = auth_controller.current_user()

    if not dc.can_view_dashboard():
        st.error("Você não tem permissão para acessar esta página.")
        return

    my_reservas = dc.minhas_reservas(user["nome"])

    if user["role"] == "Professor":
        professor_dashboard(user["nome"], my_reservas)
        return

    is_coordenador = user["role"] == "Coordenador"
    pending_for_me = dc.pending_auth_for_coordenador(user.get("nucleo")) if is_coordenador else []

    from controllers import reservas_controller
    admin_coord_dashboard(user, reservas_controller.list_solicitacoes(), pending_for_me, auth_controller.is_admin())
