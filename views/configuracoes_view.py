# -*- coding: utf-8 -*-
"""[VIEW] Configurações — equivalente a src/pages/Configuracoes.tsx."""

import streamlit as st

from controllers import auth_controller
from models import seed_data as data
from views.components import PRIMARY, badge_html

MOCK_CURRENT_PASSWORD = "senha123"


def render():
    user = auth_controller.current_user()
    rc = data.ROLE_COLORS[user["role"]]

    st.markdown('<div class="sga-eyebrow">SISTEMA</div>', unsafe_allow_html=True)
    st.markdown("<div class='sga-title'>Configurações</div>", unsafe_allow_html=True)
    st.caption("Preferências e configurações da sua conta.")

    initials = "".join(w[0] for w in user["nome"].split(" ")[:2]).upper()
    with st.container(border=True):
        c1, c2 = st.columns([1, 5])
        c1.markdown(
            f"<div style='width:56px;height:56px;border-radius:16px;background:{PRIMARY};"
            f"color:white;display:flex;align-items:center;justify-content:center;"
            f"font-weight:800;font-size:1.2rem;'>{initials}</div>",
            unsafe_allow_html=True,
        )
        with c2:
            st.markdown(f"**{user['nome']}**")
            st.caption(user["email"])
            st.markdown(badge_html(user["role"], rc["bg"], rc["text"], rc["dot"]), unsafe_allow_html=True)

    st.write("")
    with st.form("profile_form"):
        st.markdown("###### Informações do Perfil")
        st.caption("Atualize seu nome e e-mail de contato.")
        nome = st.text_input("Nome completo", value=user["nome"])
        email = st.text_input("E-mail institucional", value=user["email"])
        st.text_input("Cargo / Função (somente ADM)", value=user["role"], disabled=True)
        st.caption("O cargo só pode ser alterado por um administrador na lista de membros.")
        if st.form_submit_button("Salvar perfil", type="primary"):
            err = auth_controller.update_current_user_profile(nome, email)
            if err:
                st.error(err)
            else:
                st.toast("Perfil atualizado com sucesso!", icon="✅")

    st.write("")
    with st.form("password_form"):
        st.markdown("###### Segurança")
        st.caption("Altere sua senha de acesso. A nova senha não pode ser igual à atual. "
                    "(dica: a senha simulada atual é `senha123`)")
        atual = st.text_input("Senha atual *", type="password")
        nova = st.text_input("Nova senha *", type="password", placeholder="Mínimo 6 caracteres")
        confirmar = st.text_input("Confirmar nova senha *", type="password")
        if st.form_submit_button("Alterar senha", type="primary"):
            if not atual:
                st.error("Informe sua senha atual.")
            elif atual != MOCK_CURRENT_PASSWORD:
                st.error("Senha atual incorreta.")
            elif not nova:
                st.error("Informe a nova senha.")
            elif len(nova) < 6:
                st.error("A nova senha deve ter pelo menos 6 caracteres.")
            elif nova == atual:
                st.error("A nova senha não pode ser igual à senha atual.")
            elif nova != confirmar:
                st.error("A confirmação não coincide com a nova senha.")
            else:
                st.toast("Senha alterada com sucesso!", icon="✅")
