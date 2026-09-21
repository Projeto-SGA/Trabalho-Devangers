# -*- coding: utf-8 -*-
"""
[MODEL] Dados simulados (seed data) e constantes de domínio do SGA.

Esta camada contém apenas dados estáticos e tabelas de apoio (cores,
rótulos, matriz de permissões, massa de dados inicial). Nenhuma dependência
de Streamlit ou de estado de sessão é permitida aqui — isso garante que o
Model seja independente de framework e testável isoladamente.
"""

# ── Papéis e permissões ──────────────────────────────────────────────────────

NUCLEOS = ["Saúde", "Engenharia", "Computação", "Administração", "Direito"]

PERMISSIONS_MATRIX = {
    "Aluno": {
        "canViewSalas": True, "canCheckAvailability": True, "canViewSalaResources": True,
        "canRequestReserva": True, "canMakeDirectReserva": False,
        "canApproveStudentRequests": False, "canApproveAuthRequests": False,
        "canViewAllReservas": False, "canViewOwnReservas": True,
        "canManageUsers": False, "canManageSalas": False, "canViewMembros": False,
        "canViewDashboard": False, "canViewConfig": True, "canManageAcademic": False,
    },
    "Professor": {
        "canViewSalas": True, "canCheckAvailability": True, "canViewSalaResources": True,
        "canRequestReserva": True, "canMakeDirectReserva": True,
        "canApproveStudentRequests": True, "canApproveAuthRequests": False,
        "canViewAllReservas": False, "canViewOwnReservas": True,
        "canManageUsers": False, "canManageSalas": False, "canViewMembros": False,
        "canViewDashboard": True, "canViewConfig": True, "canManageAcademic": False,
    },
    "Coordenador": {
        "canViewSalas": True, "canCheckAvailability": True, "canViewSalaResources": True,
        "canRequestReserva": False, "canMakeDirectReserva": True,
        "canApproveStudentRequests": False, "canApproveAuthRequests": True,
        "canViewAllReservas": True, "canViewOwnReservas": True,
        "canManageUsers": False, "canManageSalas": False, "canViewMembros": False,
        "canViewDashboard": True, "canViewConfig": True, "canManageAcademic": True,
    },
    "Administrador": {
        "canViewSalas": True, "canCheckAvailability": True, "canViewSalaResources": True,
        "canRequestReserva": False, "canMakeDirectReserva": True,
        "canApproveStudentRequests": False, "canApproveAuthRequests": False,
        "canViewAllReservas": True, "canViewOwnReservas": True,
        "canManageUsers": True, "canManageSalas": True, "canViewMembros": True,
        "canViewDashboard": True, "canViewConfig": True, "canManageAcademic": True,
    },
}

DEMO_USERS = [
    {"nome": "Ana Santos", "email": "ana.santos@inst.edu.br", "role": "Administrador",
     "initials": "AS", "depto": "TI"},
    {"nome": "Prof. André Lemos", "email": "andre.lemos@inst.edu.br", "role": "Professor",
     "initials": "AL", "depto": "Física", "nucleo": "Engenharia"},
    {"nome": "Prof. Carlos Silva", "email": "carlos.silva@inst.edu.br", "role": "Professor",
     "initials": "CS", "depto": "Computação", "nucleo": "Computação"},
    {"nome": "Dra. Fátima Ramos", "email": "fatima.ramos@inst.edu.br", "role": "Coordenador",
     "initials": "FR", "depto": "Engenharia", "nucleo": "Engenharia"},
    {"nome": "Mariana Costa", "email": "mariana.costa@inst.edu.br", "role": "Coordenador",
     "initials": "MC", "depto": "Computação", "nucleo": "Computação"},
    {"nome": "João Pedro", "email": "joao.pedro@aluno.inst.edu.br", "role": "Aluno",
     "initials": "JP", "depto": "Engenharia", "curso": "Engenharia Civil", "turno": "Noturno",
     "turma": "ENG-CIVIL-01",
     "disciplinas": ["Resistência dos Materiais", "Cálculo II", "Desenho Técnico"],
     "nucleo": "Engenharia"},
    {"nome": "Maria Clara", "email": "maria.clara@aluno.inst.edu.br", "role": "Aluno",
     "initials": "MC", "depto": "Computação", "curso": "Sistemas de Informação", "turno": "Noturno",
     "turma": "SI-04", "disciplinas": ["Programação", "Banco de Dados", "Cálculo II"],
     "nucleo": "Computação"},
    {"nome": "Dr. João Paulo", "email": "joao.paulo@inst.edu.br", "role": "Coordenador",
     "initials": "JP", "depto": "Saúde", "nucleo": "Saúde"},
    {"nome": "Lucas Ferreira", "email": "lucas.ferreira@aluno.inst.edu.br", "role": "Aluno",
     "initials": "LF", "depto": "Computação", "curso": "Sistemas de Informação", "turno": "Noturno",
     "turma": "SI-04", "disciplinas": ["Programação", "Banco de Dados", "Cálculo II"],
     "nucleo": "Computação"},
]

ROLE_COLORS = {
    "Aluno":         {"bg": "#E3ECEE", "text": "#1E5E60", "border": "#B0CDD2", "dot": "#1E5E60"},
    "Professor":     {"bg": "#E8EFE2", "text": "#3C5E53", "border": "#B0CEB8", "dot": "#3C5E53"},
    "Coordenador":   {"bg": "#FFF8E6", "text": "#805B00", "border": "#FFE19A", "dot": "#B08A00"},
    "Administrador": {"bg": "#FFF0F2", "text": "#8B0019", "border": "#FFD6D9", "dot": "#8B0019"},
}

ROLE_DESCRIPTIONS = {
    "Aluno": "Consulta salas e solicita reservas",
    "Professor": "Realiza reservas e aprova solicitações de alunos",
    "Coordenador": "Acompanha reservas e autoriza ambientes especiais",
    "Administrador": "Gerencia usuários, salas e todo o sistema",
}

# ── Salas / Ambientes ────────────────────────────────────────────────────────

INITIAL_SALAS = [
    {"id": 1, "nome": "Lab. de Informática", "bloco": "Bloco B", "numero": "102", "tipo": "Laboratório",
     "capacidade": 45, "recursos": ["Projetor", "Ar-cond.", "Computadores"], "exigeAutorizacao": False,
     "status": "Disponível"},
    {"id": 2, "nome": "Sala de Reuniões", "bloco": "Bloco A", "numero": "201", "tipo": "Reunião",
     "capacidade": 15, "recursos": ["TV", "Quadro branco"], "exigeAutorizacao": False, "status": "Disponível"},
    {"id": 3, "nome": "Auditório Central", "bloco": "Bloco C", "numero": "Térreo", "tipo": "Auditório",
     "capacidade": 200, "recursos": ["Projetor", "Som", "Ar-cond."], "exigeAutorizacao": True,
     "status": "Disponível"},
    {"id": 4, "nome": "Lab. de Química", "bloco": "Bloco D", "numero": "104", "tipo": "Laboratório",
     "capacidade": 30, "recursos": ["Capelas", "Bancadas"], "exigeAutorizacao": False, "status": "Manutenção"},
    {"id": 5, "nome": "Sala Multimídia", "bloco": "Bloco B", "numero": "305", "tipo": "Aula",
     "capacidade": 40, "recursos": ["Projetor", "Ar-cond."], "exigeAutorizacao": False, "status": "Disponível"},
    {"id": 6, "nome": "Sala de Estudos", "bloco": "Biblioteca", "numero": "2º andar", "tipo": "Estudo",
     "capacidade": 20, "recursos": ["Wi-Fi", "Tomadas"], "exigeAutorizacao": False, "status": "Disponível"},
]

TIPO_OPTIONS = ["Laboratório", "Reunião", "Auditório", "Aula", "Estudo", "Outro"]
RECURSO_OPTIONS = ["Projetor", "Ar-condicionado", "Computadores", "TV", "Quadro branco", "Som",
                    "Wi-Fi", "Tomadas", "Capelas", "Bancadas"]
PROFESSORS = ["Prof. André Lemos", "Dra. Fátima Ramos", "Mariana Costa", "Ana Santos"]

STATUS_SALA_STYLE = {
    "Disponível": {"bg": "#EAF5EA", "text": "#2B5E2B", "dot": "#4A9A4A"},
    "Manutenção": {"bg": "#FFF8E6", "text": "#805B00", "dot": "#B08A00"},
    "Inativa":    {"bg": "#F5F2EB", "text": "#776D5B", "dot": "#A8A09A"},
}

STATUS_SOL_STYLE = {
    "Pendente":     {"bg": "#FFF8E6", "text": "#805B00", "dot": "#B08A00"},
    "Em análise":   {"bg": "#E3ECEE", "text": "#1E5E60", "dot": "#1E5E60"},
    "Aprovado":     {"bg": "#EAF5EA", "text": "#2B5E2B", "dot": "#4A9A4A"},
    "Recusado":     {"bg": "#FDF0F2", "text": "#991B1B", "dot": "#C0303F"},
    "Cancelado":    {"bg": "#F5F2EB", "text": "#776D5B", "dot": "#A8A09A"},
}

# ── Solicitações / Reservas ──────────────────────────────────────────────────

INITIAL_SOLICITACOES = [
    {"id": 1, "tipo": "aluno_para_professor", "sala": "Lab. de Informática", "bloco": "Bloco B — 102",
     "data": "26/08/2026", "inicio": "14:00", "fim": "16:00", "pessoas": 25,
     "solicitante": "João Pedro", "solicitanteRole": "Aluno", "nucleoSolicitante": "Engenharia",
     "professorResponsavel": "Prof. André Lemos", "status": "Pendente", "createdAt": "25/08/2026 09:30"},
    {"id": 5, "tipo": "direta", "sala": "Sala de Reuniões", "bloco": "Bloco A — 201",
     "data": "26/08/2026", "inicio": "09:00", "fim": "10:30", "pessoas": 10,
     "solicitante": "Prof. André Lemos", "solicitanteRole": "Professor", "nucleoSolicitante": "Engenharia",
     "status": "Aprovado", "createdAt": "24/08/2026 08:00"},
    {"id": 6, "tipo": "aluno_para_professor", "sala": "Lab. de Química", "bloco": "Bloco D — 104",
     "data": "29/08/2026", "inicio": "08:00", "fim": "10:00", "pessoas": 18,
     "solicitante": "João Pedro", "solicitanteRole": "Aluno", "nucleoSolicitante": "Engenharia",
     "professorResponsavel": "Prof. André Lemos", "status": "Recusado", "aprovadoPor": "Prof. André Lemos",
     "dataAprovacao": "25/08/2026 15:00", "observacao": "Conflito de horário com outra turma.",
     "createdAt": "23/08/2026 14:00"},
    {"id": 3, "tipo": "auth_required", "sala": "Auditório Central", "bloco": "Bloco C — Térreo",
     "data": "28/08/2026", "inicio": "08:00", "fim": "12:00", "pessoas": 150,
     "solicitante": "Prof. André Lemos", "solicitanteRole": "Professor", "nucleoSolicitante": "Engenharia",
     "status": "Em análise", "createdAt": "25/08/2026 11:00"},
    {"id": 7, "tipo": "aluno_para_professor", "sala": "Sala Multimídia", "bloco": "Bloco B — 305",
     "data": "27/08/2026", "inicio": "10:00", "fim": "12:00", "pessoas": 30,
     "solicitante": "João Pedro", "solicitanteRole": "Aluno", "nucleoSolicitante": "Engenharia",
     "professorResponsavel": "Prof. André Lemos", "status": "Aprovado", "aprovadoPor": "Prof. André Lemos",
     "dataAprovacao": "25/08/2026 10:15", "createdAt": "24/08/2026 16:00"},
    {"id": 2, "tipo": "aluno_para_professor", "sala": "Lab. de Informática", "bloco": "Bloco B — 102",
     "data": "27/08/2026", "inicio": "14:00", "fim": "16:00", "pessoas": 20,
     "solicitante": "Maria Clara", "solicitanteRole": "Aluno", "nucleoSolicitante": "Computação",
     "professorResponsavel": "Prof. Carlos Silva", "status": "Pendente", "createdAt": "25/08/2026 10:00"},
    {"id": 8, "tipo": "direta", "sala": "Sala de Estudos", "bloco": "Bloco A — 103",
     "data": "26/08/2026", "inicio": "16:00", "fim": "18:00", "pessoas": 15,
     "solicitante": "Prof. Carlos Silva", "solicitanteRole": "Professor", "nucleoSolicitante": "Computação",
     "status": "Aprovado", "createdAt": "24/08/2026 12:00"},
    {"id": 9, "tipo": "auth_required", "sala": "Auditório Central", "bloco": "Bloco C — Térreo",
     "data": "02/09/2026", "inicio": "14:00", "fim": "18:00", "pessoas": 200,
     "solicitante": "Mariana Costa", "solicitanteRole": "Coordenador", "nucleoSolicitante": "Computação",
     "status": "Aprovado", "aprovadoPor": "Ana Santos", "dataAprovacao": "25/08/2026 14:30",
     "createdAt": "24/08/2026 09:00"},
    {"id": 10, "tipo": "auth_required", "sala": "Auditório Central", "bloco": "Bloco C — Térreo",
     "data": "10/09/2026", "inicio": "09:00", "fim": "12:00", "pessoas": 180,
     "solicitante": "Prof. Carlos Silva", "solicitanteRole": "Professor", "nucleoSolicitante": "Computação",
     "status": "Em análise", "createdAt": "26/08/2026 08:00"},
    {"id": 4, "tipo": "aluno_para_professor", "sala": "Sala Multimídia", "bloco": "Bloco B — 305",
     "data": "03/09/2026", "inicio": "10:00", "fim": "12:00", "pessoas": 35,
     "solicitante": "Maria Clara", "solicitanteRole": "Aluno", "nucleoSolicitante": "Computação",
     "professorResponsavel": "Prof. Carlos Silva", "status": "Pendente", "createdAt": "25/08/2026 14:00"},
]

# ── Membros ───────────────────────────────────────────────────────────────────

INITIAL_MEMBERS = [
    {"id": 1, "nome": "Ana Santos", "email": "ana.santos@inst.edu.br", "funcao": "Administrador",
     "depto": "TI", "nucleo": None, "status": "Ativo", "initials": "AS", "source": "existing"},
    {"id": 2, "nome": "Prof. André Lemos", "email": "andre.lemos@inst.edu.br", "funcao": "Professor",
     "depto": "Física", "nucleo": "Engenharia", "curso": "Engenharia Civil", "turno": "Noturno",
     "turma": "ENG-CIVIL-01",
     "disciplinas": ["Cálculo II", "Resistência dos Materiais", "Desenho Técnico"],
     "status": "Ativo", "initials": "AL", "source": "existing"},
    {"id": 3, "nome": "Dra. Fátima Ramos", "email": "fatima.ramos@inst.edu.br", "funcao": "Coordenador",
     "depto": "Engenharia", "nucleo": "Engenharia", "status": "Ativo", "initials": "FR", "source": "existing"},
    {"id": 4, "nome": "Mariana Costa", "email": "mariana.costa@inst.edu.br", "funcao": "Coordenador",
     "depto": "Computação", "nucleo": "Computação", "status": "Ativo", "initials": "MC", "source": "existing"},
    {"id": 5, "nome": "Prof. Carlos Silva", "email": "carlos.silva@inst.edu.br", "funcao": "Professor",
     "depto": "Computação", "nucleo": "Computação", "curso": "Sistemas de Informação", "turno": "Noturno",
     "turma": "SI-04", "disciplinas": ["Programação", "Banco de Dados", "Cálculo II"],
     "status": "Ativo", "initials": "CS", "source": "existing"},
    {"id": 6, "nome": "Beatriz Souza", "email": "beatriz.souza@inst.edu.br", "funcao": "Professor",
     "depto": "Matemática", "nucleo": "Saúde", "curso": "Enfermagem", "turno": "Matutino",
     "turma": "ENF-01", "disciplinas": ["Anatomia", "Fisiologia"],
     "status": "Ativo", "initials": "BS", "source": "existing"},
    {"id": 7, "nome": "João Pedro", "email": "joao.pedro@aluno.inst.edu.br", "funcao": "Aluno",
     "depto": "Engenharia", "nucleo": "Engenharia", "curso": "Engenharia Civil", "turno": "Noturno",
     "turma": "ENG-CIVIL-01",
     "disciplinas": ["Resistência dos Materiais", "Cálculo II", "Desenho Técnico"],
     "status": "Ativo", "initials": "JP", "source": "existing"},
    {"id": 8, "nome": "Maria Clara", "email": "maria.clara@aluno.inst.edu.br", "funcao": "Aluno",
     "depto": "Computação", "nucleo": "Computação", "curso": "Sistemas de Informação", "turno": "Noturno",
     "turma": "SI-04", "disciplinas": ["Programação", "Banco de Dados", "Cálculo II"],
     "status": "Ativo", "initials": "MC", "source": "existing"},
    {"id": 9, "nome": "Carlos Mendes", "email": "carlos.mendes@inst.edu.br", "funcao": "Aluno",
     "depto": "Administração", "nucleo": "Administração", "curso": "Administração", "turno": "Noturno",
     "turma": "ADM-01", "disciplinas": ["Gestão Empresarial", "Finanças Corporativas"],
     "status": "Inativo", "initials": "CM", "source": "existing"},
    {"id": 10, "nome": "Rafael Oliveira", "email": "rafael.oliveira@inst.edu.br", "funcao": "Aluno",
     "depto": "Computação", "nucleo": "Computação", "curso": "Ciências da Computação", "turno": "Vespertino",
     "turma": "CC-01", "disciplinas": ["Programação", "Banco de Dados"],
     "status": "Pendente", "initials": "RO", "source": "existing"},
    {"id": 11, "nome": "Lucas Silva", "email": "lucas.silva@inst.edu.br", "funcao": "Professor",
     "depto": "Ciências", "nucleo": "Administração", "curso": "Administração", "turno": "Noturno",
     "turma": "ADM-01", "disciplinas": ["Gestão Empresarial", "Finanças Corporativas", "Recursos Humanos"],
     "status": "Ativo", "initials": "LS", "source": "existing"},
    {"id": 12, "nome": "Dr. João Paulo", "email": "joao.paulo@inst.edu.br", "funcao": "Coordenador",
     "depto": "Saúde", "nucleo": "Saúde", "status": "Ativo", "initials": "JP", "source": "existing"},
    {"id": 13, "nome": "Lucas Ferreira", "email": "lucas.ferreira@aluno.inst.edu.br", "funcao": "Aluno",
     "depto": "Computação", "nucleo": "Computação", "curso": "Sistemas de Informação", "turno": "Noturno",
     "turma": "SI-04", "disciplinas": ["Programação", "Banco de Dados", "Cálculo II"],
     "status": "Ativo", "initials": "LF", "source": "existing"},
    {"id": 14, "nome": "Fernanda Lima", "email": "fernanda.lima@aluno.inst.edu.br", "cpf": "123.456.789-01",
     "funcao": "Aluno", "depto": "Saúde", "nucleo": "Saúde", "curso": "Enfermagem", "turno": "Matutino",
     "turma": "ENF-01", "disciplinas": ["Anatomia", "Fisiologia"],
     "status": "Pendente", "initials": "FL", "source": "request"},
    {"id": 15, "nome": "Pedro Alves", "email": "pedro.alves@inst.edu.br", "cpf": "987.654.321-00",
     "funcao": "Professor", "depto": "Engenharia", "nucleo": "Saúde", "curso": "Engenharia Civil",
     "turno": "Noturno", "turma": "ENG-CIVIL-01", "disciplinas": ["Cálculo II"],
     "status": "Pendente", "initials": "PA", "source": "request"},
    {"id": 16, "nome": "Amanda Rocha", "email": "amanda.rocha@aluno.inst.edu.br", "cpf": "456.123.789-55",
     "funcao": "Aluno", "depto": "Direito", "nucleo": "Direito", "curso": "Direito", "turno": "Vespertino",
     "turma": "DIR-01", "disciplinas": ["Direito Constitucional", "Direito Civil"],
     "status": "Aguardando Correção", "initials": "AR", "source": "request",
     "motivoCorrecao": "Confirme sua turma e núcleo corretos antes de prosseguir."},
]

FUNCOES = ["Administrador", "Professor", "Coordenador", "Aluno"]
DEPTOS = ["TI", "Ciências", "Matemática", "Física", "Química", "Pedagogia", "Administração",
          "Computação", "Engenharia", "Outros"]

FUNCAO_BADGE = {
    "Administrador": {"bg": "#FFF0F2", "text": "#8B0019"},
    "Professor":     {"bg": "#E8EFE2", "text": "#3C5E53"},
    "Coordenador":   {"bg": "#E3ECEE", "text": "#154749"},
    "Aluno":         {"bg": "#EAF5EA", "text": "#2B5E2B"},
}

MEMBER_STATUS_BADGE = {
    "Ativo":                 {"bg": "#EAF5EA", "text": "#2B5E2B", "dot": "#4A9A4A"},
    "Inativo":               {"bg": "#F5F2EB", "text": "#776D5B", "dot": "#A8A09A"},
    "Pendente":              {"bg": "#FFF8E6", "text": "#805B00", "dot": "#B08A00"},
    "Aguardando Correção":   {"bg": "#FDF0F2", "text": "#991B1B", "dot": "#C0303F"},
}

AVATAR_COLORS = ["#8B0019", "#1E5E60", "#3C5E53", "#B82E3E", "#700010", "#154749", "#54000B"]


def get_avatar_color(member_id: int) -> str:
    return AVATAR_COLORS[member_id % len(AVATAR_COLORS)]


# ── Estrutura Acadêmica (Núcleo > Curso > Turma > Disciplina) ────────────────

TURNOS = ["Matutino", "Vespertino", "Noturno", "Integral"]

SEED_NUCLEOS = [
    {"id": 1, "nome": "Saúde", "descricao": "Cursos da área da saúde",
     "cursosIds": [1, 2, 3], "coordenadoresIds": [12], "ativo": True},
    {"id": 2, "nome": "Engenharia", "descricao": "Cursos de engenharia e exatas",
     "cursosIds": [4, 5, 6], "coordenadoresIds": [3], "ativo": True},
    {"id": 3, "nome": "Computação", "descricao": "Cursos de tecnologia e computação",
     "cursosIds": [7, 8], "coordenadoresIds": [4], "ativo": True},
    {"id": 4, "nome": "Administração", "descricao": "Cursos de gestão e negócios",
     "cursosIds": [9, 10, 11], "coordenadoresIds": [], "ativo": True},
    {"id": 5, "nome": "Direito", "descricao": "Cursos jurídicos e legislação",
     "cursosIds": [12], "coordenadoresIds": [], "ativo": True},
]

SEED_CURSOS = [
    {"id": 1, "nome": "Enfermagem", "nucleoId": 1, "turmasIds": [1, 2], "ativo": True},
    {"id": 2, "nome": "Fisioterapia", "nucleoId": 1, "turmasIds": [3], "ativo": True},
    {"id": 3, "nome": "Medicina", "nucleoId": 1, "turmasIds": [4], "ativo": True},
    {"id": 4, "nome": "Engenharia Civil", "nucleoId": 2, "turmasIds": [5, 6], "ativo": True},
    {"id": 5, "nome": "Engenharia Mecânica", "nucleoId": 2, "turmasIds": [7], "ativo": True},
    {"id": 6, "nome": "Engenharia de Software", "nucleoId": 2, "turmasIds": [8], "ativo": True},
    {"id": 7, "nome": "Sistemas de Informação", "nucleoId": 3, "turmasIds": [9, 10], "ativo": True},
    {"id": 8, "nome": "Ciências da Computação", "nucleoId": 3, "turmasIds": [11], "ativo": True},
    {"id": 9, "nome": "Administração", "nucleoId": 4, "turmasIds": [12], "ativo": True},
    {"id": 10, "nome": "Recursos Humanos", "nucleoId": 4, "turmasIds": [13], "ativo": True},
    {"id": 11, "nome": "Contabilidade", "nucleoId": 4, "turmasIds": [14], "ativo": True},
    {"id": 12, "nome": "Direito", "nucleoId": 5, "turmasIds": [15], "ativo": True},
]

SEED_TURMAS = [
    {"id": 1, "nome": "ENF-01", "cursoId": 1, "nucleoId": 1, "turno": "Matutino",
     "alunosIds": [7, 8], "professoresIds": [6], "disciplinasIds": [1, 2, 3], "ativo": True},
    {"id": 2, "nome": "ENF-02", "cursoId": 1, "nucleoId": 1, "turno": "Noturno",
     "alunosIds": [], "professoresIds": [6], "disciplinasIds": [1, 2, 3], "ativo": True},
    {"id": 3, "nome": "FISIO-01", "cursoId": 2, "nucleoId": 1, "turno": "Vespertino",
     "alunosIds": [], "professoresIds": [], "disciplinasIds": [4, 5], "ativo": True},
    {"id": 4, "nome": "MED-01", "cursoId": 3, "nucleoId": 1, "turno": "Integral",
     "alunosIds": [], "professoresIds": [], "disciplinasIds": [1, 4, 5], "ativo": True},
    {"id": 5, "nome": "ENG-CIVIL-01", "cursoId": 4, "nucleoId": 2, "turno": "Noturno",
     "alunosIds": [7], "professoresIds": [2], "disciplinasIds": [6, 7, 8], "ativo": True},
    {"id": 6, "nome": "ENG-CIVIL-02", "cursoId": 4, "nucleoId": 2, "turno": "Matutino",
     "alunosIds": [], "professoresIds": [2], "disciplinasIds": [6, 7, 8], "ativo": True},
    {"id": 7, "nome": "ENG-MEC-01", "cursoId": 5, "nucleoId": 2, "turno": "Vespertino",
     "alunosIds": [], "professoresIds": [], "disciplinasIds": [6, 9], "ativo": True},
    {"id": 8, "nome": "ENG-SW-01", "cursoId": 6, "nucleoId": 2, "turno": "Noturno",
     "alunosIds": [], "professoresIds": [5], "disciplinasIds": [10, 7], "ativo": True},
    {"id": 9, "nome": "SI-04", "cursoId": 7, "nucleoId": 3, "turno": "Noturno",
     "alunosIds": [8, 13], "professoresIds": [5, 2], "disciplinasIds": [10, 11, 7], "ativo": True},
    {"id": 10, "nome": "SI-05", "cursoId": 7, "nucleoId": 3, "turno": "Matutino",
     "alunosIds": [], "professoresIds": [5], "disciplinasIds": [10, 11], "ativo": True},
    {"id": 11, "nome": "CC-01", "cursoId": 8, "nucleoId": 3, "turno": "Vespertino",
     "alunosIds": [], "professoresIds": [2, 5], "disciplinasIds": [10, 11, 12], "ativo": True},
    {"id": 12, "nome": "ADM-01", "cursoId": 9, "nucleoId": 4, "turno": "Noturno",
     "alunosIds": [], "professoresIds": [11], "disciplinasIds": [13, 14], "ativo": True},
    {"id": 13, "nome": "RH-01", "cursoId": 10, "nucleoId": 4, "turno": "Matutino",
     "alunosIds": [], "professoresIds": [11], "disciplinasIds": [13, 15], "ativo": True},
    {"id": 14, "nome": "CONT-01", "cursoId": 11, "nucleoId": 4, "turno": "Noturno",
     "alunosIds": [], "professoresIds": [], "disciplinasIds": [14, 15], "ativo": True},
    {"id": 15, "nome": "DIR-01", "cursoId": 12, "nucleoId": 5, "turno": "Vespertino",
     "alunosIds": [], "professoresIds": [], "disciplinasIds": [16, 17], "ativo": True},
]

SEED_DISCIPLINAS = [
    {"id": 1, "codigo": "SAU001", "nome": "Anatomia", "nucleoId": 1, "cargaHoraria": 60,
     "professoresIds": [6], "turmasIds": [1, 2, 4]},
    {"id": 2, "codigo": "SAU002", "nome": "Fisiologia", "nucleoId": 1, "cargaHoraria": 60,
     "professoresIds": [6], "turmasIds": [1, 2]},
    {"id": 3, "codigo": "SAU003", "nome": "Bioquímica", "nucleoId": 1, "cargaHoraria": 45,
     "professoresIds": [], "turmasIds": [1, 2]},
    {"id": 4, "codigo": "SAU004", "nome": "Farmacologia", "nucleoId": 1, "cargaHoraria": 60,
     "professoresIds": [], "turmasIds": [3, 4]},
    {"id": 5, "codigo": "SAU005", "nome": "Patologia", "nucleoId": 1, "cargaHoraria": 60,
     "professoresIds": [], "turmasIds": [3, 4]},
    {"id": 6, "codigo": "ENG001", "nome": "Resistência dos Materiais", "nucleoId": 2, "cargaHoraria": 75,
     "professoresIds": [2], "turmasIds": [5, 6, 7]},
    {"id": 7, "codigo": "MAT001", "nome": "Cálculo II", "nucleoId": 2, "cargaHoraria": 75,
     "professoresIds": [2], "turmasIds": [5, 6, 8, 9]},
    {"id": 8, "codigo": "ENG002", "nome": "Desenho Técnico", "nucleoId": 2, "cargaHoraria": 45,
     "professoresIds": [2], "turmasIds": [5, 6]},
    {"id": 9, "codigo": "ENG003", "nome": "Termodinâmica", "nucleoId": 2, "cargaHoraria": 60,
     "professoresIds": [], "turmasIds": [7]},
    {"id": 10, "codigo": "COMP001", "nome": "Programação", "nucleoId": 3, "cargaHoraria": 60,
     "professoresIds": [5], "turmasIds": [8, 9, 10, 11]},
    {"id": 11, "codigo": "COMP002", "nome": "Banco de Dados", "nucleoId": 3, "cargaHoraria": 60,
     "professoresIds": [5], "turmasIds": [9, 10, 11]},
    {"id": 12, "codigo": "COMP003", "nome": "Redes de Computadores", "nucleoId": 3, "cargaHoraria": 45,
     "professoresIds": [5], "turmasIds": [11]},
    {"id": 13, "codigo": "ADM001", "nome": "Gestão Empresarial", "nucleoId": 4, "cargaHoraria": 60,
     "professoresIds": [11], "turmasIds": [12, 13]},
    {"id": 14, "codigo": "ADM002", "nome": "Finanças Corporativas", "nucleoId": 4, "cargaHoraria": 60,
     "professoresIds": [11], "turmasIds": [12, 14]},
    {"id": 15, "codigo": "ADM003", "nome": "Recursos Humanos", "nucleoId": 4, "cargaHoraria": 45,
     "professoresIds": [11], "turmasIds": [13, 14]},
    {"id": 16, "codigo": "DIR001", "nome": "Direito Constitucional", "nucleoId": 5, "cargaHoraria": 75,
     "professoresIds": [], "turmasIds": [15]},
    {"id": 17, "codigo": "DIR002", "nome": "Direito Civil", "nucleoId": 5, "cargaHoraria": 75,
     "professoresIds": [], "turmasIds": [15]},
]

# ── Dashboard: dados estáticos simulados ─────────────────────────────────────

WEEK_DATA = [
    {"day": "Seg", "reservas": 18}, {"day": "Ter", "reservas": 27}, {"day": "Qua", "reservas": 31},
    {"day": "Qui", "reservas": 24}, {"day": "Sex", "reservas": 29}, {"day": "Sáb", "reservas": 9},
    {"day": "Dom", "reservas": 4},
]

ALL_ROOM_STATS = [
    {"sala": "Lab. de Informática", "tipo": "laboratorios", "bloco": "bloco_b", "reservas": 42,
     "horas": 84, "pessoas": 1344, "capacidade": 45},
    {"sala": "Sala Multimídia", "tipo": "salas_aula", "bloco": "bloco_b", "reservas": 35,
     "horas": 70, "pessoas": 980, "capacidade": 40},
    {"sala": "Auditório Central", "tipo": "auditorios", "bloco": "bloco_c", "reservas": 28,
     "horas": 112, "pessoas": 3360, "capacidade": 300},
    {"sala": "Sala de Reuniões", "tipo": "salas_reuniao", "bloco": "bloco_a", "reservas": 21,
     "horas": 31.5, "pessoas": 210, "capacidade": 20},
    {"sala": "Sala de Estudos", "tipo": "salas_aula", "bloco": "bloco_a", "reservas": 17,
     "horas": 34, "pessoas": 306, "capacidade": 30},
    {"sala": "Lab. de Química", "tipo": "laboratorios", "bloco": "bloco_d", "reservas": 14,
     "horas": 28, "pessoas": 252, "capacidade": 25},
]

ALL_PEAK_HOURS = [
    {"slot": "08–10h", "reservas": 28}, {"slot": "10–12h", "reservas": 45},
    {"slot": "12–14h", "reservas": 12}, {"slot": "14–16h", "reservas": 52},
    {"slot": "16–18h", "reservas": 38}, {"slot": "18–22h", "reservas": 22},
]

PROF_BASE_ROOMS = [
    {"sala": "Lab. de Informática", "capacidade": 45, "reservas": 8, "horas": 16, "pessoas": 256},
    {"sala": "Sala Multimídia", "capacidade": 40, "reservas": 5, "horas": 10, "pessoas": 130},
    {"sala": "Sala de Estudos", "capacidade": 30, "reservas": 3, "horas": 6, "pessoas": 45},
    {"sala": "Auditório Central", "capacidade": 300, "reservas": 1, "horas": 4, "pessoas": 120},
]

PROF_BASE_HOURS = [
    {"periodo": "Manhã", "label": "08:00–12:00", "reservas": 4},
    {"periodo": "Tarde", "label": "12:00–18:00", "reservas": 10},
    {"periodo": "Noite", "label": "18:00–22:00", "reservas": 3},
]

MONTH_NAMES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
               "Setembro", "Outubro", "Novembro", "Dezembro"]
