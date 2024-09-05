# Jogo_da_Forca

## Grupo

- Gabriel
- Gilberto
- Wagner

## Descrição

Jogo da forca desenvolvido em Python e Django.

## Requisitos

- Python 3.12

## Instalação

Na raiz do projeto, crie um arquivo `.env` com o seguinte conteúdo:

```dotenv
SECRET_KEY=suachavesecreta
DATABASE_URL=engine://user:password@host:port/name
```

```bash
./pw pdm install
./pw migrate
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