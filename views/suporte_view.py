# -*- coding: utf-8 -*-
"""[VIEW] Central de Ajuda — equivalente a src/pages/Suporte.tsx."""

import streamlit as st

from controllers import session_controller

FAQS = [
    ("Como faço para solicitar uma reserva de sala?",
     'Acesse a seção "Reservas" no menu lateral, clique em "Nova Reserva" (ou "Solicitar Reserva" '
     'se você for Aluno), preencha os dados da sala, data, horário e número de participantes e '
     'confirme. Alunos precisam indicar um professor responsável — a reserva fica pendente até a aprovação.'),
    ("Por que não consigo alterar meu cargo no perfil?",
     "Por questões de segurança, somente administradores podem alterar o cargo de um usuário. "
     "Essa alteração é feita na página de Membros."),
    ("Minha solicitação de reserva ficou como Pendente. O que isso significa?",
     "Solicitações enviadas por alunos aguardam aprovação do professor responsável indicado. "
     "Solicitações para ambientes que exigem autorização aguardam aprovação do coordenador."),
    ("Como cancelo uma reserva já feita?",
     'Acesse "Reservas" e abra a aba "Minhas Reservas/Solicitações". Clique em "Cancelar" no card '
     'da reserva desejada.'),
    ("Por que uma sala aparece como Em Manutenção?",
     "O administrador do sistema pode colocar uma sala em manutenção temporariamente. Nesse estado "
     "ela não aparece na lista de seleção ao fazer uma reserva."),
    ("Esqueci minha senha. Como recupero o acesso?",
     "Entre em contato com o suporte pelo e-mail abaixo informando seu nome completo e e-mail "
     "institucional."),
    ("Como faço para cadastrar um novo usuário no sistema?",
     'Qualquer pessoa pode clicar em "Criar conta" na tela de login e preencher o formulário de '
     'cadastro. A solicitação ficará pendente até aprovação de um administrador.'),
]

CONTACTS = [
    ("📧 E-mail de suporte", "suporte@sga.inst.edu.br"),
    ("📱 Telefone / WhatsApp", "(11) 3456-7890"),
    ("🕐 Horário de atendimento", "Segunda a sexta, das 8h às 18h"),
    ("📍 Localização do suporte", "Bloco A — Sala 110, Campus Principal"),
]


def render():
    if st.button("← Voltar ao login"):
        session_controller.goto("login")
        st.rerun()

    st.markdown('<div class="sga-eyebrow">SUPORTE</div>', unsafe_allow_html=True)
    st.markdown("<div class='sga-title'>Central de Ajuda</div>", unsafe_allow_html=True)
    st.caption("Encontre respostas para dúvidas frequentes ou entre em contato com nossa equipe de suporte.")

    st.markdown("###### Contato")
    cols = st.columns(2)
    for i, (label, value) in enumerate(CONTACTS):
        with cols[i % 2]:
            with st.container(border=True):
                st.caption(label)
                st.markdown(f"**{value}**")

    st.write("")
    st.markdown("###### Dúvidas Frequentes")
    for q, a in FAQS:
        with st.expander(q):
            st.write(a)

    st.write("")
    with st.container(border=True):
        st.markdown("**Não encontrou o que procurava?**")
        st.caption("Nossa equipe de suporte está disponível para ajudar você.")
        st.link_button("Enviar e-mail para o suporte", "mailto:suporte@sga.inst.edu.br", type="primary")
