# -*- coding: utf-8 -*-
"""
Camada Controller do SGA.

Os controllers são a única camada que lê e escreve em st.session_state.
Eles recebem chamadas das Views (em resposta a ações do usuário), buscam/
atualizam os dados na sessão delegando as regras de negócio para a camada
Model, e devolvem estruturas prontas para a View renderizar.
"""
