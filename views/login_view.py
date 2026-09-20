import streamlit as st

from controllers import academico_controller, auth_controller, session_controller
from models import seed_data as data
from views.components import BORDER, PRIMARY, TEXT_DARK, TEXT_MUTED, badge_html


@st.dialog("Criar nova conta", width="large")
def register_modal():
    ss = st.session_state
    if "_reg_step" not in ss:
        ss._reg_step = 1
        ss._reg_form = {
            "nome": "", "email": "", "cpf": "", "funcao": "Aluno",
            "nucleo": "", "curso": "", "turno": "", "turma": "",
            "senha": "", "confirmar": "",
        }
        ss._reg_disciplinas = []

    form = ss._reg_form

    if ss._reg_step == 1:
        st.caption("Etapa 1 de 2 — Dados pessoais e de acesso")
        form["nome"] = st.text_input("Nome completo *", value=form["nome"])
        form["email"] = st.text_input("E-mail *", value=form["email"])
        form["cpf"] = st.text_input("CPF *", value=form["cpf"], placeholder="000.000.000-00")
        form["funcao"] = st.selectbox(
            "Função", data.FUNCOES, index=data.FUNCOES.index(form["funcao"]) if form["funcao"] in data.FUNCOES else 3
        )
        c1, c2 = st.columns(2)
        form["senha"] = c1.text_input("Senha *", value=form["senha"], type="password")
        form["confirmar"] = c2.text_input("Confirmar senha *", value=form["confirmar"], type="password")

        if st.button("Continuar →", type="primary", use_container_width=True):
            err = auth_controller.validate_step1(form["nome"], form["email"], form["cpf"],
                                                  form["senha"], form["confirmar"])
            if err:
                st.error(err)
            else:
                ss._reg_step = 2
                st.rerun()

    else:
        st.caption("Etapa 2 de 2 — Vínculo acadêmico")
        nucleos_ativos = auth_controller.nucleos_ativos_nomes()
        form["nucleo"] = st.selectbox("Núcleo *", [""] + nucleos_ativos,
                                       index=([""] + nucleos_ativos).index(form["nucleo"]) if form["nucleo"] in nucleos_ativos else 0)
        nucleo_obj = academico_controller.get_nucleo_by_name(form["nucleo"]) if form["nucleo"] else None
        cursos_list = academico_controller.cursos_by_nucleo(nucleo_obj["id"]) if nucleo_obj else []
        curso_names = [c["nome"] for c in cursos_list]
        form["curso"] = st.selectbox("Curso *", [""] + curso_names,
                                      index=([""] + curso_names).index(form["curso"]) if form["curso"] in curso_names else 0)
        form["turno"] = st.selectbox("Turno *", [""] + data.TURNOS,
                                      index=([""] + data.TURNOS).index(form["turno"]) if form["turno"] in data.TURNOS else 0)

        curso_obj = next((c for c in cursos_list if c["nome"] == form["curso"]), None)
        all_turmas = academico_controller.turmas_by_curso(curso_obj["id"]) if curso_obj else []
        turma_list = [t for t in all_turmas if not form["turno"] or t["turno"] == form["turno"]]
        turma_names = [t["nome"] for t in turma_list]
        form["turma"] = st.selectbox("Turma *", [""] + turma_names,
                                      index=([""] + turma_names).index(form["turma"]) if form["turma"] in turma_names else 0)

        turma_obj = next((t for t in turma_list if t["nome"] == form["turma"]), None)
        disc_list = academico_controller.disciplinas_by_turma(turma_obj["id"]) if turma_obj else []
        if disc_list:
            disc_names = [d["nome"] for d in disc_list]
            ss._reg_disciplinas = st.multiselect("Disciplinas", disc_names, default=ss._reg_disciplinas)

        c1, c2 = st.columns(2)
        if c1.button("← Voltar", use_container_width=True):
            ss._reg_step = 1
            st.rerun()
        if c2.button("Enviar cadastro", type="primary", use_container_width=True):
            if not form["nucleo"] or not nucleo_obj:
                st.error("Selecione o Núcleo.")
            elif not form["curso"] or not curso_obj:
                st.error("Selecione o Curso.")
            elif not form["turno"]:
                st.error("Selecione o Turno.")
            elif not form["turma"] or not turma_obj:
                st.error("Selecione a Turma.")
            else:
                auth_controller.submit_registration(form, ss._reg_disciplinas)
                del ss._reg_step
                del ss._reg_form
                del ss._reg_disciplinas
                st.success("Cadastro enviado! Aguarde a aprovação de um administrador.")
                st.balloons()
                if st.button("Fechar"):
                    st.rerun()


def _inject_login_css():
    st.markdown(
        f"""
        <style>
        .login-hero {{
            text-align: center;
            padding: 1.75rem 0 0.5rem;
        }}
        .login-emblem {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 60px; height: 60px; border-radius: 18px;
            background: linear-gradient(135deg, {PRIMARY} 0%, #5C0011 100%);
            color: white; font-weight: 800; font-size: 1.05rem; letter-spacing: 0.02em;
            box-shadow: 0 8px 20px -6px rgba(139,0,25,0.45);
            margin-bottom: 1.1rem;
        }}
        .login-hero h1 {{
            color: {TEXT_DARK}; font-weight: 800; font-size: 1.9rem;
            margin: 0 0 0.35rem 0; letter-spacing: -0.01em;
        }}
        .login-hero p {{
            color: {TEXT_MUTED}; font-size: 0.92rem; max-width: 460px;
            margin: 0 auto; line-height: 1.5;
        }}
        .login-section-label {{
            color: {TEXT_MUTED}; font-size: 0.72rem; font-weight: 700;
            letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.6rem;
        }}
        .login-divider {{
            display: flex; align-items: center; gap: 10px;
            color: {TEXT_MUTED}; font-size: 0.75rem; margin: 1.1rem 0;
        }}
        .login-divider::before, .login-divider::after {{
            content: ""; flex: 1; height: 1px; background: {BORDER};
        }}
        .login-help {{
            text-align: center; font-size: 0.8rem; color: {TEXT_MUTED}; margin-top: 0.4rem;
        }}
        .login-help a {{ color: {PRIMARY}; font-weight: 600; text-decoration: none; }}
        .demo-avatar {{
            width: 34px; height: 34px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 700; font-size: 0.78rem; flex-shrink: 0;
        }}
        .demo-name {{ color: {TEXT_DARK}; font-weight: 700; font-size: 0.88rem; margin: 0; }}
        .demo-sub {{ color: {TEXT_MUTED}; font-size: 0.76rem; margin: 0; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render():
    _inject_login_css()

    st.markdown(
        f"""
        <div class="login-hero">
            <div class="login-emblem">SGA</div>
            <h1>Sistema de Gestão de Ambientes</h1>
            <p>Plataforma integrada para gerenciamento de reservas, controle de ambientes
               e organização de membros da instituição.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    left, right = st.columns([1, 1.15], gap="large")

    with left:
        with st.container(border=True):
            st.markdown('<div class="login-section-label">ACESSO À CONTA</div>', unsafe_allow_html=True)
            st.markdown("#### Bem-vindo de volta 👋")
            st.caption("Entre com suas credenciais para continuar")

            with st.form("login_form"):
                st.text_input("E-mail", placeholder="seu@email.com")
                st.text_input("Senha", type="password", placeholder="••••••••")
                fc1, fc2 = st.columns([1, 1])
                fc1.checkbox("Lembrar de mim")
                fc2.markdown(
                    f'<div style="text-align:right; padding-top:6px;">'
                    f'<a href="#" style="font-size:0.8rem; color:{PRIMARY}; font-weight:600; '
                    f'text-decoration:none;">Esqueci a senha</a></div>',
                    unsafe_allow_html=True,
                )
                submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)
                if submitted:
                    st.info("Use uma das contas de demonstração ao lado para entrar no sistema.")

            st.markdown('<div class="login-divider">ou</div>', unsafe_allow_html=True)

            if st.button("Criar nova conta", use_container_width=True):
                register_modal()

            st.markdown(
                '<p class="login-help">Problemas de acesso? <a href="#">Contate o suporte</a></p>',
                unsafe_allow_html=True,
            )
            if st.button("→ Central de Ajuda", use_container_width=True):
                session_controller.goto("suporte")
                st.rerun()

    with right:
        st.markdown('<div class="login-section-label">ENTRAR COMO — DEMONSTRAÇÃO</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, u in enumerate(auth_controller.demo_users()):
            rc = data.ROLE_COLORS[u["role"]]
            initials = "".join(w[0] for w in u["nome"].split(" ")[:2]).upper()
            with cols[i % 2]:
                with st.container(border=True):
                    hc1, hc2 = st.columns([1, 4])
                    hc1.markdown(
                        f'<div class="demo-avatar" style="background:{rc["dot"] or rc["text"]}">{initials}</div>',
                        unsafe_allow_html=True,
                    )
                    with hc2:
                        st.markdown(f'<p class="demo-name">{u["nome"]}</p>', unsafe_allow_html=True)
                        st.markdown(badge_html(u["role"], rc["bg"], rc["text"]), unsafe_allow_html=True)
                    if u.get("nucleo"):
                        st.markdown(f'<p class="demo-sub">Núcleo {u["nucleo"]}</p>', unsafe_allow_html=True)
                    st.markdown(
                        f'<p class="demo-sub">{auth_controller.role_description(u["role"])}</p>',
                        unsafe_allow_html=True,
                    )
                    st.write("")
                    if st.button("Entrar →", key=f"demo_{i}", use_container_width=True):
                        auth_controller.login_as(u)
                        st.rerun()

    st.write("")
    st.markdown("<hr/>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("🏫 Ambientes", "200+")
    c2.metric("🗓️ Reservas/mês", "1.4k")
    c3.metric("⭐ Satisfação", "98%")