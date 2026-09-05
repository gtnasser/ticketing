# ticketing

## Proposta:

Criar um sistema simples para armazenar e consultar as ocorrências e as soluções adotadas, com o objetivo de formar uma base de conhecimento compartilhada. Tem que ser simples e leve o suficiente para que possa ser hospedado em um desktop, e ser utilizada por um pequeno grupo de usuários.

**Características principais:**
* Será registrada em cada ocorrência a análise da causa e a solução adotada.
* Deverá ter uma pesquisa por texto da ocorrência e algumas opções de filtro apra limitar o universo da pesquisa.
* Deverá ser multiusuário, e extremamente leve para ser executado em um desktop.

**Requisitos funcionais:**
* Multiusuário, com autenticação simples (apenas usuário/senha)
* Cadastro das ocorrências (CRUD)
* Pesquisa por texto nas ocorrências, com filtro
* Tela do administrador de usuários 
* Os atributas da ocorrência são:
    * Data da ocorrência
    * Título
    * Tipo (Erro de sistema, Erro de operação, Outros)
    * Solução provisória (texto)
    * Solução definitiva (texto)
    * Nome do usuário
    * Data/hora do registro da ocorrência
* Os atributos do usuário são:
    * username
    * password

**Requisitos Não Funcionais:**
* Banco de dados local
* Autenticação simples (usuário/senha), no mesmo banco
* Estimativa de usuários: 6
* Estimativa de ocorrências: 24/dia

## Solução:

Estrutura do projeto:
```text
sistema_ocorrencias/
├── app.py              # interface Streamlit (login, cadastro, pesquisa)
├── database.py         # camada de banco (SQLite)
├── auth.py             # autenticação com senha criptografada
├── create_user.py      # script para criar usuários
├── requirements.txt    # dependências
└── ocorrencias.db      # banco (criado automaticamente)
```



## TODO:

Lista de desejos:
* textos das soluções WYSIWYG
* lista de atualizações
* usuário redefinir a sua senha
* backup automatico
* forçar troca de senha periódica 
* login autenticacao AD
* exportar pesquisa
* execucao em docker


## To start developing

```bash
mkdir ticketing
cd ticketing
python -m venv venv
.\venv\Scripts\activate
git init
git add.
```

## To run this project

```bash
git clone...
cd ticketing
python -m venv venv                         # cria ambiente virtual
.\venv\Scripts\activate
pip install -r requirements.txt
python create_user.py admin senha123        # cria o primeiro usuário
python create_user.py john wick             # cria outro usuario
streamlit run app.py
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 # server.address habilita execucao remota no linux
```



