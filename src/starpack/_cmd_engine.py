import typer

from starpack import initialize_engine, terminate

engine_app = typer.Typer(pretty_exceptions_show_locals=False)


@engine_app.command(name="start")
def cmd_start_engine(
    force: bool = typer.Option(
        False,
        "--force",
        "-F",
        help="Force a removal of all older starpack-engine containers",
    )
):
    """
    Starts the Starpack Engine. If given a custom Docker image name, will attempt to run it instead.
    If `force` is passed, will remove any existing containers and ensure that the latest version is pulled.
    """

    initialize_engine(force=force)


@engine_app.command(name="terminate")
def cmd_engine_terminate(
    all_resources: bool = typer.Option(
        False, "--all", "-A", help="Remove associated volumes and saved data as well."
    )
) -> None:
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data.
    """

    terminate(all_resources=all_resources)
