# Sistema de Gerenciamento de Estudantes

Este é um sistema de API REST desenvolvido com FastAPI para gerenciar informações de estudantes, incluindo seus dados pessoais e fotos.

## Tecnologias Utilizadas

- FastAPI (Framework Python para APIs)
- MongoDB (Banco de dados)
- Oracle Cloud Infrastructure (OCI) Object Storage (Armazenamento de fotos)
- Docker (Containerização)
- Python 3.8+

## Requisitos do Sistema

- Python 3.8 ou superior
- MongoDB
- Conta Oracle Cloud com acesso ao Object Storage
- Docker (opcional)

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd <nome-do-diretorio>
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` com as seguintes variáveis:
```
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
ORACLE_BUCKET_NAME=students-photos
ORACLE_NAMESPACE=seu-namespace
```

4. Configure o Oracle Cloud:
- Crie um arquivo `config` na raiz do projeto com suas credenciais OCI
- Certifique-se de que o bucket especificado existe no seu Object Storage

## Executando o Projeto

### Localmente
```bash
uvicorn main:app --reload
```

### Com Docker
```bash
docker build -t student-api .
docker run -p 8000:8000 student-api
```

## Endpoints da API

### POST /students/
Cria um novo estudante
- Parâmetros:
	- name (string): Nome do estudante
	- grade (float): Nota do estudante
	- photo (arquivo): Foto do estudante

### GET /students/
Lista todos os estudantes cadastrados

### GET /students/{student_id}
Retorna os dados de um estudante específico

### PUT /students/{student_id}
Atualiza os dados de um estudante
- Corpo da requisição: Dados do estudante (JSON)

### DELETE /students/{student_id}
Remove um estudante do sistema

## Estrutura do Projeto
```
.
├── main.py           # Arquivo principal com endpoints da API
├── models/
│   └── student.py    # Modelo de dados do estudante
├── .env              # Variáveis de ambiente
├── Dockerfile        # Configuração do Docker
└── README.md         # Documentação
```

## Testando a API

A documentação interativa da API está disponível em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Observações Importantes

1. Certifique-se de que o MongoDB está rodando antes de iniciar a aplicação