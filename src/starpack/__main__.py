import typer
from typing import Optional
from starpack.resources import Resource

app = typer.Typer()

@app.command(name="list")
def list_resources(resource: Resource):
    if not resource:
        print("Nada")
    print(resource)

@app.command(name="delete")
def delete_resource(resource: Resource):
    if not resource:
        print("Deleted nothing")
    print(f"Deleted {resource}")


if __name__ == "__main__":
    app()