# -*- coding: utf-8 -*-
"""
[MODEL] Entidade Sala (ambiente).

Todas as funções são puras: recebem a lista de salas (e demais argumentos)
e devolvem o resultado da operação, sem nunca acessar st.session_state.
Quem guarda o estado é o Controller (reservas_controller).
"""


def add_sala(salas: list, sala: dict) -> dict:
    """Cria uma nova sala com id autoincremental e a insere na lista."""
    new_id = (max((s["id"] for s in salas), default=0)) + 1
    novo = dict(sala)
    novo["id"] = new_id
    salas.append(novo)
    return novo


def update_sala(salas: list, sala_id: int, data_new: dict) -> None:
    for i, s in enumerate(salas):
        if s["id"] == sala_id:
            salas[i] = {**data_new, "id": sala_id}
            return


def toggle_manutencao(salas: list, sala_id: int) -> None:
    for s in salas:
        if s["id"] == sala_id:
            s["status"] = "Disponível" if s["status"] == "Manutenção" else "Manutenção"
            return


def get_sala_by_id(salas: list, sala_id: int) -> dict | None:
    return next((s for s in salas if s["id"] == sala_id), None)


def salas_disponiveis(salas: list) -> list:
    return [s for s in salas if s["status"] == "Disponível"]
