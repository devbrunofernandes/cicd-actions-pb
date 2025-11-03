# CI/CD com o Github Actions (Em progresso)
Este é um projeto que busca implementar todas as etapas do ciclo de desenvolvimento de software, partindo do ambiente local para repositorios de código remoto com automação em processos de build, e então atualização automatica de manifestos de infraestrutura (Kubernetes) com praticas de GitOps integradas para o deploy automatizado.

O objetivo desse texto é documentar todo o passo a passo realizado durante o processo.

ATENÇÃO! Os comandos utilizados e documentados aqui são para a shell `bash` que é utilizada nos sistemas Linux/MacOS.

## ⚠️ Requisitos
- Minikube (v1.37.0)
- ArgoCD (v3.1.9)
- Git (2.43.0+)
- Docker Engine (28.5.1)
- Kubectl (v1.34.1)
- Python (3.12.3)
- Pip (24.0)
- Conta no GitHub
- Conta no DockerHub

## 1️⃣ – Criar a aplicação FastAPI
Nessa etapa do projeto o objetivo é criar nossos repositórios que serão utilizados futuramente, introduzir a aplicação de modelo que será utilizada e criar o Dockerfile para permitir o `build` da imagem da aplicação.

A aplicação modelo é uma API escrita Python utilizando a biblioteca/framework FastAPI, esse por sua vez é uma biblioteca do Python para criação de APIs de forma simples e rápida.

- ### Criação dos repositórios do projeto
    Antes da própria aplicação vamos criar os repositorios locais e remotos que serão utilizados no projeto.

    Crie no github dois repositórios, um com a finalidade de ser o repositório do código fonte da nossa aplicação e o outro para práticas de GitOps.

    Caso precise de ajuda na criação, acesse a [documentação do GitHub](https://docs.github.com/pt/repositories/creating-and-managing-repositories/quickstart-for-repositories) sobre esse assunto.

    Após isso crie também os repositórios localmente, isso é crie duas pastas no seu sistema operacional, e dentro de cada uma utilize o comando `git init`.

    Faça a conexão dos repositórios remotos e locais seguindo as instruções fornecidas pelo GitHub ao criar os repositórios.

- ### Criação da aplicação Python
    Acesse via linha de comando a pasta para o código fonte que foi criada nos passos anteriores.

    Dentro da pasta vamos criar um `venv` do Python. Isso é uma ferramente que permite utilizar um "ambiente virtual" de desenvolvimento para gerenciar as dependências do projeto sem que precisem ser instaladas diretamente na nossa máquina inteira, ficam contidas no projeto especifico, dessa forma ao desenvolver multiplos projetos grandes com diversas dependências, a possibilidade de conflitos de versão é evitada.

    Essa é uma boa prática de desenvolvimento no ambiente Python. Para criar um `venv` utilize o seguinte comando:

    ``` bash
    python3 -m venv .venv
    ```

    Com o `venv` criado, para começar a utiliza-lo execute também:

    ``` bash
    source .venv/bin/activate
    ```
    
    Agora sim podemos instalar o FastAPI utilizando o gerenciador de pacotes `pip`, dentro do ambiente virtual esse pacote de dependência do projeto vai ficar contido sem gerar conflitos. Execute o seguinte comando para realizar a instalação:

    (baixe junto o pacote `uvicorn` que vai permitir a gente testar a nossa aplicação)

    ``` bash
    pip install fastapi uvicorn
    ```

    **Lembrando de utilizar o interpretador Python que está dentro da pasta `.venv`, não o comum do sistema.**

    Crie o arquivo contendo o código fonte da aplicação:

    ``` python
    from fastapi import FastAPI 

    app = FastAPI() 

    @app.get("/")
    async def root(): 
        return {"message": "Hello World"}
    ```

- ### Criação do Dockerfile e building
    A criação dos arquivos necessarios para fazer o build da imagem do Docker são fundamentais para o funcionamento da pipeline, pois nosso aplicação vai ser executada por meio de um cluster Kubernetes e precisamos prover as imagens que ele usará.


    Crie um arquivo `.dockerignore` com o seguinte conteúdo para ignorar arquivos desnecessarios de entrarem no processo de build.
    ``` .dockerignore
    .venv/
    __pycache__/
    .git
    .gitignore
    .vscode/
    ```

    Agora o arquivo `Dockerfile` com as instruções de como o Docker deve fazer o build, usaremos a imagem base do python 3.12, fazemos o `COPY` do requirements.txt para conseguir instalar as dependências por meio de um comando `pip`. Copiamos o conteúdo do nosso repositório para a imagem, definimos a porta de escuta do container como 8000 e por ultimo o comando `uvicorn` para servir a aplicação.
    ``` Dockerfile
    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

    Para testar se a nossa imagem está funcional, vamos fazer o build dela e executar como container. Utilize o seguinte comando para o build:
    ``` bash
    docker build -t fastapi .
    ```

    Depois de terminar o build da imagem, com esse outro comando podemos executar um container e testar se a aplicação está funcional e acessivel. Use o comando e tente acessar `localhost` no seu navegador.
    ``` bash
    docker run -d -p 80:8000 --name api fastapi
    ```

## 2️⃣ – Criar o GitHub Actions (CI/CD)

## 3️⃣ – Repositório Git com os manifests do ArgoCD

## 4️⃣ – Criar App no ArgoCD

## 5️⃣ – Acessar e testar a aplicação localmente

## 🔚 Conclusão
