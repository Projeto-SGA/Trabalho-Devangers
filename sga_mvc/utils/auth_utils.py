"""
utils/auth_utils.py

Utilitários para autenticação com Firebase Authentication.
"""

import streamlit as st
import firebase_admin
from firebase_admin import auth, credentials


def registrar_usuario(email: str, senha: str):
    """
    Registra um novo usuário no Firebase Auth
    
    Args:
        email: Email do usuário
        senha: Senha (mínimo 6 caracteres)
    
    Returns:
        tuple: (sucesso: bool, uid: str, mensagem: str)
    """
    try:
        user = auth.create_user(email=email, password=senha)
        return True, user.uid, f"✅ Usuário registrado: {email}"
    
    except auth.EmailAlreadyExistsError:
        return False, None, "❌ Este email já está registrado"
    
    except auth.InvalidPasswordError:
        return False, None, "❌ Senha muito fraca (mínimo 6 caracteres)"
    
    except auth.InvalidEmailError:
        return False, None, "❌ Email inválido"
    
    except Exception as e:
        return False, None, f"❌ Erro ao registrar: {str(e)}"


def deletar_usuario_auth(uid: str):
    """Deleta usuário do Firebase Auth"""
    try:
        auth.delete_user(uid)
        return True, "✅ Usuário deletado"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def resetar_senha(email: str):
    """Envia email de reset de senha"""
    try:
        auth.send_password_reset_email(email)
        return True, f"✅ Email de reset enviado para {email}"
    except auth.UserNotFoundError:
        return False, "❌ Usuário não encontrado"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def atualizar_email(uid: str, novo_email: str):
    """Atualiza email de um usuário"""
    try:
        auth.update_user(uid, email=novo_email)
        return True, f"✅ Email atualizado para {novo_email}"
    except auth.EmailAlreadyExistsError:
        return False, "❌ Este email já está em uso"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def atualizar_senha(uid: str, nova_senha: str):
    """Atualiza senha de um usuário"""
    try:
        auth.update_user(uid, password=nova_senha)
        return True, "✅ Senha atualizada"
    except auth.InvalidPasswordError:
        return False, "❌ Senha muito fraca"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def obter_usuario_por_email(email: str):
    """Busca usuário por email"""
    try:
        user = auth.get_user_by_email(email)
        return user
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        st.warning(f"Erro ao buscar usuário: {e}")
        return None


def listar_usuarios():
    """Lista todos os usuários (usar com cuidado)"""
    try:
        usuarios = []
        for user in auth.list_users().users:
            usuarios.append({
                'uid': user.uid,
                'email': user.email,
                'email_verificado': user.email_verified,
                'criado_em': user.user_metadata.creation_timestamp,
            })
        return usuarios
    except Exception as e:
        st.error(f"Erro ao listar usuários: {e}")
        return []


def validar_email(email: str) -> bool:
    """Valida formato de email - simples"""
    # Validação básica: Tem @ e tem um ponto após o @
    if not email:
        return False
    
    email = email.strip()
    
    # Verificar @ e extensão
    if '@' not in email:
        return False
    
    local, domain = email.rsplit('@', 1)
    
    # Local não pode ser vazio
    if not local:
        return False
    
    # Domain deve ter um ponto
    if '.' not in domain:
        return False
    
    # Não pode ter espaços
    if ' ' in email:
        return False
    
    return True


def validar_senha(senha: str) -> bool:
    """Valida força da senha"""
    return len(senha) >= 6
