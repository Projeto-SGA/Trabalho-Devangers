# -*- coding: utf-8 -*-
"""
SGA — Sistema de Gestão de Ambientes
Arquitetura MVC com Firebase Authentication:

    Model      -> models/      (dados + regras de negócio puras, sem Streamlit)
    View       -> views/       (apenas apresentação/Streamlit; nunca muta a sessão direto)
    Controller -> controllers/ (única camada que lê/grava st.session_state; orquestra
                                 os casos de uso chamados pelas Views)

Este arquivo é o Front Controller: inicializa Firebase, manage autenticação e rotas.
"""

import streamlit as st
import os

from controllers import auth_controller, session_controller
from views import auth_view, layout_view
from views.components import inject_css
from utils.firebase_utils import init_firestore

st.set_page_config(page_title="SGA — Sistema de Gestão de Ambientes", page_icon="🏫", layout="wide")

# Definir caminho correto do projeto (onde app.py está)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)  # Mudar diretório de trabalho para o projeto

# Inicializa Firebase Firestore
if 'firestore_db' not in st.session_state:
    try:
        st.session_state.firestore_db = init_firestore()
    except Exception as e:
        st.error(f"❌ Erro ao conectar Firebase: {e}")

# Inicializa autenticação
auth_controller.init_auth_state()

inject_css()

# Permissão necessária para acessar cada rota protegida (equivalente a ProtectedRoute)
ROUTE_PERMISSION = {
    "dashboard": "ver_agenda",
    "membros": "gerenciar_usuarios",
    "academico": "gerenciar_aulas",
    "reservas": "fazer_reservas",
}

# Mapa de rota -> módulo de View responsável por renderizá-la
VIEW_MODULES = {
    "dashboard": "dashboard_view",
    "reservas": "reservas_view",
    "membros": "membros_view",
    "academico": "academico_view",
    "configuracoes": "configuracoes_view",
    "perfil": "perfil_view",
}


def main():
    # Se não está logado, mostrar login
    if not auth_controller.is_logged_in():
        auth_view.render()
        return
    
    # Usuário logado - renderizar app principal
    route = session_controller.current_route()
    
    # Rotas públicas (apenas autenticado)
    if route == "menu":
        layout_view.render_sidebar()
        from views import menu_view
        menu_view.render()
        return
    
    if route == "perfil":
        layout_view.render_sidebar()
        from views import perfil_view
        perfil_view.render()
        return
    
    # Rotas protegidas (autenticado + permissão)
    layout_view.render_sidebar()
    
    required_perm = ROUTE_PERMISSION.get(route)
    if required_perm and not auth_controller.tem_permissao(required_perm):
        layout_view.render_unauthorized()
        return
    
    module_name = VIEW_MODULES.get(route, "menu")
    if module_name in VIEW_MODULES:
        try:
            module = __import__(f"views.{module_name}", fromlist=[module_name])
            module.render()
        except ImportError:
            session_controller.goto("menu")
            st.rerun()
    else:
        session_controller.goto("menu")
        st.rerun()


if __name__ == "__main__":
    main()
