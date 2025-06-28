# 🐍 WORKALOVA CHALLENGE API

  Esse projeto faz parte do processo seletivo da Workalove.

  Uma API RESTFull que cuida do contexto de gerenciamento de receitas de pratos simples e rápidos para serem feitos no dia a dia.

  A API é capaz de cadastrar um novo chefe de cozinha (Chef), como Chefe de cozinha é possível, cadastrar uma receita (Recipe) contendo nome, descrição, ingredientes e modo de preparo, editar e remover as receitas cadastradas.

  Além disso é possível, pesquisar receitas por nome do prato e/ou nomedo chef e/ou qualquer outra informação disponível na receita(Ingredientes, Descrição, Modo de preparo).

  Também é possível visualizar todas as receitas de um Chef específico.


![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)
![Django REST](https://img.shields.io/badge/Django%20REST%20Framework-3.16%2B-092E20?logo=django&logoColor=white&style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

## 📦 Pré-requisitos

- Python 3.13+
- Poetry 2.1.3
- Docker
- Banco de dados (PostgreSQL)

## 🛠️ Configuração

1. **Clonar repositório:**
```bash
git clone https://github.com/vroxo/workalove_challenge.git
cd workalove_challenge
```

2. **Variáveis de Ambiente:**
```bash
mv .env.example .env
```

3. **Ativar ambiente virtual:**
```bash
poetry shell
```

4. **Instalar dependencias:**
```bash
poetry install
```

5. **Subir container do DB:**
```bash
docker run db -d
```

6. **Rodar as migrations:**
```bash
task migrate
```

## ⚙️ Local
### 🚀 Execução
```bash
task run
```

### 🧪 Testes
```bash
task test 
```

## 🐳 Docker
### 🚀 Execução
```bash
docker build --no-cache
docker compose up -d
```

### 🧪 Testes
```bash
docker run tests
```

## 📚 Documentação da API:
- Swagger UI: [http://localhost:8000/docs/](http://localhost:8000)
- Arquivo OpenAPI: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
