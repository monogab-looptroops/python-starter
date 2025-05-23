# Example MES Microservice
The goal of this repository is guidance/guidelines for creating a microservice.
Advantages:
- Faster development
- Polished/Up-to-date tech stack
- Same style used by everybody
- can be used as a starter
- can be used as a cheatsheet


## Layers
- api: definitions, documentation, authentication and dependency injection. It should stay purely declaretive.
- service: the business logic of the microservice comes here. For unit testing it contains classes for the adapters. Domain models are here.
- adapters: connecting to databases, working queues, devices, other apis, etc. Every adapter can be tested separately.

## Packages
- <b>[FastAPI](https://fastapi.tiangolo.com/)</b>: web framework for building APIs
- <b>[Uvicorn](https://www.uvicorn.org/)</b>: ASGI web server implementation
- <b>[Pydantic](https://docs.pydantic.dev/)</b>: data validation
- <b>[SQLModel](https://sqlmodel.tiangolo.com/)</b>: interacting with SQL databases, with or without python objects (e.g. pydantic models)
- <b>[pytest](https://docs.pytest.org/)</b>: framework for creating python tests
- <b>[dynaconf](https://www.dynaconf.com/)/[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)</b>: Loading settings and/or config from environment variables or secrets
- <b>[NiceGUI](https://nicegui.io/)/[FastUI](https://github.com/pydantic/FastUI)</b>: frontend development


## Documentation
See [here](/docs/README.md)

## API Client
See [here](/client/README.md)

## Test
See [here](/test/README.md)

## Deploy
See [here](/kubernetes/README.md)

## Misc

Client code generation??
Deployment using invoke e.g. invoke deploy <site> ??

## Main branch protection

Settings > Branches > Add branch ruleset

Ruleset Name: protect-main

Enforcement Status: Active

Target branches: main

Check: Require a pull request before merging


# Quick start

### Create virtual environment and activate 
```
python3.12 -m venv venv
source venv/bin/activate 
```

### Install dependencies
You need to have credentials to the Clarebout Azure artifact repository.

For that install Azure cli from here:
```
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
```
You might need .Net Core package, install that as well.

Login in interactively throught the browser.
```
az login
```

Install keyring to be able to use your azure login with pip. 
```
python -m pip install --upgrade pip
pip install keyring artifacts-keyring
```

Install the packages:
```
pip install -r requirements.txt
```
