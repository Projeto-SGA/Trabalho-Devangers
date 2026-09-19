# Sistema de Gestão de Ambientes

## DEVANGERS

Sistema Web de Gerenciamento e Reserva de Ambientes Acadêmicos, desenvolvido pela equipe **Devangers**, da software house **Devora**.

---

## 📋 Sobre o Projeto

O Sistema de Gestão de Ambientes tem como objetivo centralizar informações sobre ambientes acadêmicos, disponibilidade e reservas, organizando o processo de consulta, solicitação e autorização de utilização dos espaços.

A solução considera diferentes perfis de usuários, com permissões e fluxos específicos para cada tipo de acesso.

---

## 🎯 Objetivo

Desenvolver uma solução capaz de:

- Organizar informações sobre ambientes acadêmicos;
- Consultar ambientes e sua disponibilidade;
- Solicitar reservas;
- Evitar conflitos de horários;
- Organizar processos de aprovação e rejeição;
- Diferenciar permissões de acordo com o perfil do usuário.

---

## 👥 Perfis de Usuário

O sistema considera quatro perfis principais:

### 👨‍🎓 Aluno
- Consulta ambientes;
- Verifica disponibilidade;
- Realiza solicitações de reserva.

### 👨‍🏫 Professor
- Analisa solicitações de alunos;
- Pode realizar reservas quando permitido;
- Pode aprovar ou rejeitar solicitações sob sua responsabilidade.

### 👩‍💼 Coordenador
- Analisa solicitações que necessitam de autorização;
- Pode aprovar ou rejeitar solicitações.

### 🛠️ Administrador
- Gerencia usuários;
- Gerencia ambientes;
- Gerencia categorias e recursos;
- Controla os status dos ambientes.

---

## 🔄 Fluxo Principal

O fluxo principal previsto para a solução é:

```text
Login
  ↓
Consulta de Ambientes
  ↓
Seleção de Data e Horário
  ↓
Verificação de Disponibilidade
  ↓
Reserva ou Solicitação
  ↓
Análise / Autorização
  ↓
Atualização do Status
  ↓
Consulta do Resultado / Histórico
