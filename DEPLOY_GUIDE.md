# 🚀 Guia de Deploy - Funcionalidade de Edição de Perfil

## 📋 Pré-requisitos
- Servidor com Docker e Docker Compose configurados
- Acesso SSH ao servidor
- Repositório sincronizado com as mudanças

## 🔄 Passos para Deploy

### 1. **Acessar o Servidor**
```bash
# Conectar via SSH
ssh user@seu-servidor

# Navegar para o diretório do projeto
cd /opt/1panel/docker/compose/evo-ai
```

### 2. **Atualizar o Código**
```bash
# Fazer backup do estado atual (opcional)
git stash

# Atualizar do fork
git pull origin main

# Verificar se as mudanças foram aplicadas
git log --oneline -5
```

### 3. **Aplicar a Migração**
```bash
# Parar os containers
docker-compose down

# Aplicar a migração
docker-compose run --rm api python -m alembic upgrade head

# Verificar se a migração foi aplicada
docker-compose run --rm api python -m alembic current
```

### 4. **Reiniciar os Serviços**
```bash
# Reiniciar todos os containers
docker-compose up -d

# Verificar se estão rodando
docker-compose ps

# Verificar logs da API
docker-compose logs -f api
```

### 5. **Testar a Funcionalidade**
```bash
# Copiar o script de teste para o servidor
# Executar o teste
python3 test_profile_api.py http://localhost:8000

# Ou se estiver acessível externamente:
python3 test_profile_api.py https://seu-dominio.com
```

## 🧪 Teste Manual da API

### **Endpoint Disponível:**
```
PUT /auth/profile
```

### **Exemplo com curl:**
```bash
# 1. Fazer login para obter token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@admin.com","password":"admin123"}' | jq -r '.access_token')

# 2. Atualizar perfil
curl -X PUT "http://localhost:8000/auth/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Novo Nome"}'

# 3. Verificar mudança
curl -X POST "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 Verificações de Funcionamento

### ✅ **Checklist de Verificação:**
- [ ] Migração aplicada sem erros
- [ ] Containers reiniciados com sucesso
- [ ] API responde no endpoint `/auth/profile`
- [ ] JWT authentication funciona
- [ ] Atualização de nome funciona
- [ ] Atualização de email funciona
- [ ] Validações de erro funcionam

### 🔍 **Logs para Monitorar:**
```bash
# Logs da API
docker-compose logs -f api

# Logs do banco
docker-compose logs -f postgres

# Status dos containers
docker-compose ps
```

## 🐛 Troubleshooting

### **Problema: Migração falha**
```bash
# Verificar conexão com banco
docker-compose exec postgres psql -U postgres -d evo_ai -c "\dt"

# Verificar status das migrações
docker-compose exec api python -m alembic history
```

### **Problema: API não responde**
```bash
# Verificar logs
docker-compose logs api

# Verificar se porta está aberta
netstat -tulpn | grep 8000
```

### **Problema: Campo name não existe**
```bash
# Verificar estrutura da tabela
docker-compose exec postgres psql -U postgres -d evo_ai -c "\d users"

# Aplicar migração específica
docker-compose exec api python -m alembic upgrade 4d1c657fd3a1
```

## 🎯 Resultado Esperado

Após aplicar todas as mudanças, você deve ter:

1. ✅ **Campo `name` na tabela `users`**
2. ✅ **Endpoint `PUT /auth/profile` funcionando**
3. ✅ **Validação de JWT ativa**
4. ✅ **Atualização de nome e email funcionando**
5. ✅ **Reset de verificação de email quando alterado**

## 📝 Notas Importantes

- **Backup:** Sempre faça backup antes de aplicar migrações
- **Downtime:** Os containers ficam offline durante a aplicação
- **Logs:** Monitore os logs após o deploy
- **Teste:** Use o script de teste fornecido para validar

## 🔗 Links Úteis

- **Fork do projeto:** https://github.com/tassomuniz/ecom-evo-ai
- **Commit da funcionalidade:** 3d28f4c9
- **Migração:** `4d1c657fd3a1_add_name_field_to_users_table.py` 