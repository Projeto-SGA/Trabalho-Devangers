# -*- coding: utf-8 -*-
"""
[MODEL] Validações de domínio (dados de cadastro).

Funções puras de validação, sem nenhuma dependência de Streamlit. Recebem
um valor bruto e devolvem uma string de erro (vazia = válido). Podem ser
reutilizadas por qualquer Controller ou testadas isoladamente.
"""

import re


def validate_nome(nome: str) -> str:
    t = (nome or "").strip()
    if not t:
        return "Informe seu nome completo."
    if len(t) < 3:
        return "O nome deve ter ao menos 3 caracteres."
    if t.isdigit():
        return "O nome não pode conter apenas números."
    if not re.search(r"[a-zA-ZÀ-ÿ]", t):
        return "O nome deve conter letras."
    return ""


def validate_email(email: str) -> str:
    t = (email or "").strip()
    if not t:
        return "Informe seu e-mail."
    if " " in t:
        return "O e-mail não pode conter espaços."
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$", t):
        return "Informe um endereço de e-mail válido."
    return ""


def validate_cpf(cpf: str) -> str:
    digits = re.sub(r"\D", "", cpf or "")
    if not digits:
        return "Informe seu CPF."
    if len(digits) != 11:
        return "CPF inválido. Verifique os dados informados."
    if digits == digits[0] * 11:
        return "CPF inválido. Verifique os dados informados."

    s = sum(int(digits[i]) * (10 - i) for i in range(9))
    rem = (s * 10) % 11
    rem = 0 if rem in (10, 11) else rem
    if rem != int(digits[9]):
        return "CPF inválido. Verifique os dados informados."

    s = sum(int(digits[i]) * (11 - i) for i in range(10))
    rem = (s * 10) % 11
    rem = 0 if rem in (10, 11) else rem
    if rem != int(digits[10]):
        return "CPF inválido. Verifique os dados informados."

    return ""


def email_already_registered(email: str, members: list) -> bool:
    email_lower = (email or "").strip().lower()
    return any(m["email"].lower() == email_lower for m in members)


def cpf_already_registered(cpf: str, members: list) -> bool:
    cpf_digits = re.sub(r"\D", "", cpf or "")
    return any(
        re.sub(r"\D", "", m.get("cpf") or "") == cpf_digits and m.get("cpf")
        for m in members
    )
