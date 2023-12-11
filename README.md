# puc-rio-machine-learning

Este é o repositório do projeto **puc-rio-machine-learning**, uma aplicação web para análise de ranking e avaliação de jogos. A aplicação permite que os usuários se cadastrem, realizem o login, visualizem um mural de jogos fornecidos pela api da RAWG **(https://api.rawg.io/docs/)**, vejam avaliações de jogos específicos e contribuam com suas próprias avaliações.

## Pré-requisitos

- Python 3.x
- Flask
- MySQL (ou outro banco de dados de sua escolha)
- Outras dependências listadas no arquivo `requirements.txt`

## Instalação

1. Clone o repositório: `git clone https://github.com/joaofeliperl/puc-rio-machine-learning.git`
2. Navegue até o diretório do projeto: `cd machine-learning`
3. Instale as dependências: `pip install -r requirements.txt`

## Configuração

1. Configure as credenciais do banco de dados no arquivo `config.py`.
2. Execute o script SQL (`database.sql`) para criar o banco de dados e as tabelas necessárias.

## Uso

1. Execute o aplicativo Flask: `python src/backend/app.py`
2. Abra o navegador e acesse `http://localhost:5000`

## Funcionalidades

- **Cadastro de Usuário:** Os usuários podem se cadastrar fornecendo seu nome, e-mail e senha.
- **Login:** Os usuários podem fazer login para acessar as funcionalidades restritas.
- **Mural de Jogos:** Visualize uma lista de jogos disponíveis.
- **Detalhes do Jogo:** Veja informações detalhadas sobre um jogo específico, incluindo avaliações e comentários.
- **Avaliação de Jogos:** Os usuários podem contribuir com suas próprias avaliações e comentários para jogos.
- **Ranking de Jogos:** Os usuários podem verificar ranking de avaliações de jogos.

## Estrutura do Projeto

```
src
├── backend
│   ├── app.py
│   ├── models
│   ├── templates
│   └── static
├── frontend
│   ├── css
│   ├── img
│   ├── js
│   └── templates
├── database.sql
├── README.md
└── requirements.txt
```

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature: `git checkout -b feature-nova`
3. Faça commit das suas mudanças: `git commit -m 'Adicione nova feature'`
4. Envie para o branch: `git push origin feature-nova`
5. Abra um Pull Request

