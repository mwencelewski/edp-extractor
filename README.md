# Desafio Técnico COGNI - Extração de Faturas da EDP

## Descrição

O projeto de _Extração de Faturas da EDP_ é uma solução automatizada para a extração de faturas do portal da EDP. A aplicação permite que o usuário forneça o número da instalação e selecione os meses desejados para download das faturas, agilizando o processo de obtenção desses documentos de forma eficiente e sem intervenção manual.

## Estrutura do Projeto

- `src/`: Contém todos os scripts Python que constituem a aplicação principal.
  - `src/main.py`: O script principal que inicia a aplicação.
  - `src/utils.py`: Funções utilitárias usadas pelo `main.py`.
  - `src/logs/`: Diretório onde os logs gerados pela aplicação são armazenados.
  - `src/downloads/`: Diretório onde são armazenados os arquivos baixados pela aplicação.
- `Pipfile`: Gerenciador de dependências utilizado no projeto.
- `dockerfile`: Configuração para a construção da imagem Docker do projeto.
- `docker-compose.yml`: Configuração para orquestrar contêineres Docker para o projeto.
- `.gitignore`: Arquivo que especifica quais arquivos ou diretórios devem ser ignorados pelo Git.
- `.dockerignore`: Arquivo que especifica quais arquivos ou diretórios devem ser ignorados pelo Docker.

## Instalação

### Pré-requisitos

- [Python 3.10.7](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/)

### Passos para Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/cogni.git
   cd cogni
   ```

2. Instale as dependências utilizando o Pipenv:

   ```bash
   pipenv install
   ```
3. Crie um arquivo .env dentro src/
    ``` bash
    URL = "https://www.edponline.com.br/para-sua-casa/login"
    EMAIL = <Email Cliente>
    PASSWORD = <Senha>
    SITEKEY = <Chave Captcha>
    APIKEY = <API Key 2Captcha>
    ```
3. Para executar a aplicação localmente:
   ```bash
     pipenv run python src/main.py --numero_instalcao <numero_instalacao> --meses <meses>
   ```

### Usando Docker

1. Construa a imagem Docker:

   ```bash
   docker build -t cogni .
   ```

2. Execute a aplicação com Docker Compose:
   ```bash
   docker-compose up
   ```

```

```
