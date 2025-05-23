from invoke import task
from datetime import datetime
import os
import sys
import pytest


repository = "europe-west1-docker.pkg.dev/upheld-coast-328110/realtimestack"
version = datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
module_path = os.path.join(os.getcwd(), 'src')
container_title = "microservice-example"

if module_path not in sys.path:
    sys.path.append(module_path)


@task()
def testdata(c):
    """
    Add here the scripts which initialize the database with some test data

    """
    os.environ["PYTHONPATH"] = f"{os.getcwd()}/src"
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    # c.run("python init_db.py")


@task()
def test(c):
    """
    Run tests for the microservice both in the src folder(unit test as close to the source as possible)
    and in the tests folder (integration tests). Settings are in pyproject.toml under [tool.pytest]
    """
    os.getcwd()
    os.environ['PYTHONPATH'] = f"{os.getcwd()}/src"

    retcode = pytest.main([])

    # this is needed to block the CI/CD pipeline in case of test failure
    if retcode != 0:
        raise Exception("Tests failed")

    return None


@task(help={'build_type': "Type of the build, possible value 'development', 'production'"})
def build(c, build_type: str = "production"):
    """
    Build docker

    """

    c.run("cp $HOME/.config/gcloud/application_default_credentials.json .")
    c.run(f"docker build --target {build_type} -t {container_title}:latest .")  # --platform linux/amd64

    c.run(f"docker tag {container_title}:latest {container_title}-{build_type}:latest")
    c.run(f"docker tag {container_title}:latest {repository}/{container_title}:latest")
    c.run(f"docker tag {container_title}:latest {repository}/{container_title}:{version}")
    c.run("rm application_default_credentials.json")


@task()
def push(c):
    """
    Push docker
    """
    c.run(f"docker push {repository}/{container_title}:latest")
    c.run(f"docker push {repository}/{container_title}:{version}")
