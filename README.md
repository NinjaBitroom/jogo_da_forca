# Jogo_da_Forca

## Grupo

- Gabriel
- Gilberto
- Wagner

## Descrição

Jogo da forca desenvolvido em Python e Django.

## Requisitos

- Python 3.12

## Regras

- Os usuários "professores" deverão se cadastrar na aplicação para poder inserir novas palavras e temas a serem
  utilizadas no jogo.
- A aplicação deverá ter uma área onde um usuário do grupo de professores possa cadastrar um tema e as palavras
  referentes a esse tema, bem como um texto e uma dica(opcionais) referente a cada palavra (somente usuários professores
  poderão fazer isso).
- O aluno, ao entrar na aplicação poderá jogar sem estar logado no sistema, mas também poderá se cadastrar caso o
  professor exiga. O mesmo deve escolher o jogo que quiser, filtrando por tema ou por professor e em seguida por tema.
- O visual do jogo deve ser escolhido e desenvolvido pelo grupo.
- O professor poderá gerar um PDF da atividade para que ele possa imprimir.
- O professor poderá ver relatório de quais alunos 'jogaram', por tema e por período de tempo(data).
- A aplicação deve ser disponibilizada (fazer deploy) no PythonAnywhere ou outro servidor.
- Qualquer outra informação ou dúvida sobre a aplicação perguntar ao professor.

## Instalação

Na raiz do projeto, crie um arquivo `.env` com o seguinte conteúdo:

```dotenv
SECRET_KEY=suachavesecreta
DATABASE_URL=engine://user:password@host:port/name
```

Depois execute os seguintes comandos:

```bash
./pw pdm install
./pw migrate
./pw manage setup_groups
```

## Execução

```bash
./pw start
```

## Ferramentas

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Pyprojectx](https://pyprojectx.github.io/)
- [PDM](https://pdm-project.org)