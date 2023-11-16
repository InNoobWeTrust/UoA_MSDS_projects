# Ad Recommender System

## Prerequisite
Install Poetry

- With pipx
```sh
pip install pipx
pipx install poetry
```
- With official installer
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Install task runner `poethepoet`
```sh
pipx install poethepoet
```

Install dependencies with poetry
```sh
poetry install
```

## Run locally

Start flask server
```sh
poe dev
```
Then go to [http://localhost:5000](http://localhost:5000) to interact with the app

Or view a fancy UI using streamlit
```sh
poe streamlit-run
```

## Run with docker

```sh
poe docker-dev
```

Stop docker container with

```sh
poe docker-stop
```

## Run test

__Note:__ Only test case is the test to check if the pickled input processor is working to ensure the deployment matches the environment in Colab's noteboook when building the models.

To run test:
```sh
poe test
```

## Format code with Ruff

```sh
poe ruff-fix
```
