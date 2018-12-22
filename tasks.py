from invoke import task


@task
def install(c):
    c.run("pip install -r requirements.txt")
