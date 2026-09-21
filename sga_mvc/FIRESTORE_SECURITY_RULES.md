# 🔒 Regras de Segurança do Firestore

## 📋 Como Aplicar as Regras

1. Acesse [Firebase Console](https://console.firebase.google.com)
2. Selecione seu projeto **"projeto-devangers"**
3. Vá em **Firestore Database** → **Rules** (aba)
4. **Cole o código abaixo** na editor
5. **Publish**

---

## 🛡️ Regras de Segurança (Security Rules)

```firestore_rules
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    
    /**
     * Função auxiliar: Verifica se usuário está autenticado
     */
    function isAuthenticated() {
      return request.auth != null;
    }
    
    /**
     * Função auxiliar: Obtém papel do usuário
     */
    function getUserRole() {
      return get(/databases/$(database)/documents/usuarios/$(request.auth.uid)).data.role;
    }
    
    /**
     * Função auxiliar: Verifica se é admin
     */
    function isAdmin() {
      return getUserRole() == 'admin';
    }
    
    /**
     * Função auxiliar: Verifica se é professor
     */
    function isProfessor() {
      return getUserRole() == 'professor';
    }
    
    /**
     * Função auxiliar: Verifica se é dono do documento
     */
    function isOwner(uid) {
      return request.auth.uid == uid;
    }
    
    /**
     * ============================================
     * COLEÇÃO: usuarios
     * ============================================
     */
    match /usuarios/{uid} {
      // LEITURA
      allow read: if 
        isAuthenticated() && (
          isOwner(uid) ||        // Ler próprio perfil
          isAdmin()              // Admin lê todos
        );
      
      // CRIAÇÃO (via registro)
      allow create: if 
        isAuthenticated() &&
        request.data.uid == request.auth.uid &&
        request.data.role == 'usuario' &&  // User não pode criar admin
        request.data.ativo == true;
      
      // ATUALIZAÇÃO
      allow update: if 
        isAuthenticated() && (
          (isOwner(uid) && request.data.role == resource.data.role) ||  // User edita apenas own data
          isAdmin()  // Admin pode editar qualquer campo
        );
      
      // DELEÇÃO
      allow delete: if 
        isAuthenticated() && (
          isOwner(uid) ||        // User deleta própria conta
          isAdmin()              // Admin deleta usuários
        );
      
      // Sub-coleção: userSessions
      match /userSessions/{sessionId} {
        allow read: if isOwner(uid);
        allow create: if isOwner(uid);
        allow delete: if isOwner(uid);
      }
    }
    
    /**
     * ============================================
     * COLEÇÃO: ambientes
     * ============================================
     */
    match /ambientes/{doc} {
      // LEITURA
      allow read: if isAuthenticated();
      
      // CRIAÇÃO
      allow create: if 
        isAuthenticated() && (
          isProfessor() || isAdmin()
        ) &&
        request.data.criador_uid == request.auth.uid &&
        exists(/databases/$(database)/documents/usuarios/$(request.auth.uid));
      
      // ATUALIZAÇÃO
      allow update: if 
        isAuthenticated() && (
          (resource.data.criador_uid == request.auth.uid) ||  // Criador edita
          isAdmin()                                            // Admin edita
        );
      
      // DELEÇÃO
      allow delete: if 
        isAuthenticated() && (
          (resource.data.criador_uid == request.auth.uid) ||
          isAdmin()
        );
    }
    
    /**
     * ============================================
     * COLEÇÃO: reservas
     * ============================================
     */
    match /reservas/{doc} {
      // LEITURA
      allow read: if 
        isAuthenticated() && (
          resource.data.usuario_uid == request.auth.uid ||  // Ver próprias reservas
          isAdmin()                                          // Admin vê todas
        );
      
      // CRIAÇÃO
      allow create: if 
        isAuthenticated() &&
        request.data.usuario_uid == request.auth.uid &&
        request.data.status == 'pendente' &&
        exists(/databases/$(database)/documents/usuarios/$(request.auth.uid)) &&
        exists(/databases/$(database)/documents/ambientes/$(request.data.ambiente_id));
      
      // ATUALIZAÇÃO
      allow update: if 
        isAuthenticated() && (
          (resource.data.usuario_uid == request.auth.uid && request.data.status in ['cancelada']) ||
          isAdmin()
        );
      
      // DELEÇÃO
      allow delete: if 
        isAuthenticated() && (
          isAdmin()
        );
    }
    
    /**
     * ============================================
     * COLEÇÃO: logs (auditoria)
     * ============================================
     */
    match /logs/{doc} {
      // LEITURA
      allow read: if isAdmin();
      
      // CRIAÇÃO (apenas servidor/backend)
      allow create: if false;  // Apenas servidor pode criar logs
      
      // ATUALIZAÇÃO/DELEÇÃO
      allow update, delete: if false;
    }
    
    /**
     * ============================================
     * OUTROS - Negar por padrão
     * ============================================
     */
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

---

## 🧪 Testando as Regras

No Firebase Console, use a aba **Rules Simulator**:

### Teste 1: Usuário pode ler próprio perfil
```
Operação: read
Documento: usuarios/user123
Autenticado como: user123
✅ Esperado: Permitido
```

### Teste 2: Usuário NÃO pode ler perfil de outro
```
Operação: read
Documento: usuarios/outro_user
Autenticado como: user123
❌ Esperado: Bloqueado
```

### Teste 3: Admin pode ler qualquer perfil
```
Operação: read
Documento: usuarios/qualquer_user
Autenticado como: admin123 (com role='admin')
✅ Esperado: Permitido
```

### Teste 4: Usuário não pode criar reserva para outro
```
Operação: create
Documento: reservas/novo_doc
Dados: { usuario_uid: "outro_user", ... }
Autenticado como: user123
❌ Esperado: Bloqueado
```

---

## 📝 Regras por Papel

| Ação | Usuário | Professor | Admin |
|------|---------|-----------|-------|
| Ler próprio perfil | ✅ | ✅ | ✅ |
| Ler outro perfil | ❌ | ❌ | ✅ |
| Criar ambiente | ❌ | ✅ | ✅ |
| Fazer reserva | ✅ | ✅ | ✅ |
| Ver próprias reservas | ✅ | ✅ | ✅ |
| Ver todas as reservas | ❌ | ❌ | ✅ |
| Deletar usuário | ❌ | ❌ | ✅ |
| Acessar logs | ❌ | ❌ | ✅ |

---

## 🔍 Estrutura de Dados Esperada

### Coleção: `usuarios/{uid}`
```json
{
  "uid": "user123",
  "nome": "João Silva",
  "email": "joao@example.com",
  "role": "usuario|professor|admin",
  "ativo": true,
  "email_verificado": false,
  "criado_em": "2026-09-20T10:00:00Z",
  "atualizado_em": "2026-09-20T10:00:00Z"
}
```

### Coleção: `ambientes/{docId}`
```json
{
  "nome": "Sala 101",
  "localizacao": "Prédio A",
  "capacidade": 30,
  "criador_uid": "professor123",
  "ativo": true,
  "criado_em": "2026-09-20T10:00:00Z"
}
```

### Coleção: `reservas/{docId}`
```json
{
  "usuario_uid": "user123",
  "ambiente_id": "ambient123",
  "data_inicio": "2026-09-21T14:00:00Z",
  "data_fim": "2026-09-21T16:00:00Z",
  "status": "pendente|confirmada|cancelada",
  "observacoes": "Reunião de planejamento",
  "criado_em": "2026-09-20T10:00:00Z"
}
```

---

## 🚨 Importante

⚠️ **Estas regras são básicas. Para produção:**

- ✅ Adicione validação de timestamps
- ✅ Implemente quotas de reservas por usuário
- ✅ Use Firestore Triggers para computar dados
- ✅ Configure backups automáticos
- ✅ Use Google Cloud Armor para DDoS
- ✅ Monitore com Cloud Logging

---

## 🔗 Referências

- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/start)
- [Estrutura de Regras](https://firebase.google.com/docs/firestore/security/rules-structure)
- [Simulador de Regras](https://firebase.google.com/docs/firestore/security/test-rules-simulator)
