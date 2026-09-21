# SGA — Sistema de Gestão de Ambientes (arquitetura MVC)

Este projeto é a reestruturação do app Streamlit original em **MVC** (Model –
View – Controller). O comportamento funcional é o mesmo; o que mudou foi a
organização do código.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura de pastas

```
app.py                  Front Controller: inicializa o estado e roteia cada
                         página para a View correspondente.

models/                 MODEL — dados e regras de negócio puras.
                         Nenhum arquivo aqui importa `streamlit` nem toca em
                         st.session_state. São funções que recebem listas/
                         dicionários e devolvem o resultado da operação.
  seed_data.py             Massa de dados inicial + constantes de domínio
                            (cores de badge, matriz de permissões, listas de
                            opções etc). Equivale aos Context providers do
                            protótipo React original.
  validators.py            Validação de nome, e-mail e CPF.
  permissions_model.py     Regras de permissão por papel (role).
  sala_model.py             Entidade Sala: criar, editar, alternar manutenção.
  solicitacao_model.py      Entidade Solicitação/Reserva: criar, aprovar,
                             recusar, cancelar, checar disponibilidade.
  membro_model.py           Entidade Membro: CRUD + fluxo de aprovação de
                             cadastro (aprovar / rejeitar / pedir correção).
  academico_model.py        Núcleo > Curso > Turma > Disciplina: CRUD e
                             consultas (lookups).

controllers/             CONTROLLER — única camada que lê/grava
                         st.session_state. Fazem a ponte entre a View
                         (ação do usuário) e o Model (regra de negócio),
                         devolvendo dados prontos para a View renderizar.
  session_controller.py    Inicialização do "banco" em memória e navegação
                            (rota atual).
  auth_controller.py       Login/logout, permissões do usuário logado e
                            fluxo de auto-cadastro (2 etapas).
  reservas_controller.py   Casos de uso de Salas e Solicitações/Reservas.
  membros_controller.py    Casos de uso de Membros.
  academico_controller.py  Casos de uso da estrutura acadêmica.
  dashboard_controller.py  Cálculo das métricas/agregações exibidas nos
                            dashboards (professor e admin/coordenador).

views/                   VIEW — apenas apresentação (Streamlit). Uma View
                         nunca lê/grava st.session_state diretamente para
                         mutações de dados; toda ação de usuário (clique de
                         botão, envio de formulário) é delegada a uma função
                         de Controller.
  components.py            CSS global + componentes visuais reutilizáveis
                            (badge, cabeçalho de página etc). Equivale ao
                            antigo ui.py.
  layout_view.py           Sidebar de navegação e tela de "acesso não
                            autorizado" (equivalente a Sidebar.tsx +
                            ProtectedRoute.tsx).
  login_view.py             Tela de login + modal de cadastro de conta.
  menu_view.py               Menu inicial (cards por papel).
  dashboard_view.py          Dashboard do professor e do admin/coordenador
                              (monta os gráficos Plotly a partir dos dados já
                              calculados pelo dashboard_controller).
  reservas_view.py           Ambientes, nova reserva/solicitação, aprovações.
  membros_view.py            Lista de membros + solicitações de cadastro.
  academico_view.py          Núcleos, cursos, turmas e disciplinas.
  configuracoes_view.py      Perfil do usuário e troca de senha.
  suporte_view.py            Central de ajuda / FAQ.
```

## Fluxo de uma ação típica (exemplo: aprovar uma reserva)

1. **View** (`reservas_view.py`): o usuário clica no botão "Aprovar" dentro
   de `solicitacao_card()`.
2. A View chama `reservas_controller.aprovar_solicitacao(sol_id, nome_do_aprovador)`
   — ela não sabe *como* a aprovação é feita, só que precisa acontecer.
3. **Controller** (`reservas_controller.py`): busca a lista de solicitações em
   `st.session_state.solicitacoes` e delega a regra de negócio para o Model.
4. **Model** (`solicitacao_model.py`): função pura `aprovar_solicitacao(...)`
   atualiza o dicionário da solicitação (status, quem aprovou, data) — sem
   nenhuma dependência de Streamlit.
5. O Controller devolve o controle para a View, que chama `st.rerun()` para
   re-renderizar a tela com o novo estado.

## Por que separar assim?

- **Testabilidade**: os Models são funções puras (entra lista, sai lista) —
  dá para testar toda a regra de negócio com `pytest` puro, sem subir o
  Streamlit.
- **Reuso**: a mesma função de Model/Controller pode ser chamada por
  diferentes Views sem duplicar lógica (ex.: `dashboard_controller` é usado
  tanto no dashboard do professor quanto no do admin/coordenador).
- **Legibilidade**: cada View fica pequena e focada em desenhar a tela;
  quem quiser entender "como funciona a aprovação de reserva" olha direto
  no `solicitacao_model.py`, sem precisar ler 800 linhas de código Streamlit.

## Observação sobre o paradigma do Streamlit

O Streamlit é reativo (a cada interação o script inteiro roda de novo), o que
é diferente do ciclo request/response de um MVC "clássico" (ex.: Django/
Rails). Para manter a separação de responsabilidades dentro desse modelo:

- **Nenhuma View acessa `st.session_state` para leitura de listas de dados
  de negócio** (salas, solicitações, membros, estrutura acadêmica) — sempre
  passa por um Controller.
- O único estado que uma View pode manipular diretamente é o estado
  *transitório da própria UI* (ex.: `ss._reg_step` do wizard de cadastro em
  `login_view.py`), que não é dado de negócio persistente.
- `app.py` atua como *Front Controller*: decide, a partir da rota atual e das
  permissões do usuário, qual View deve ser renderizada.
