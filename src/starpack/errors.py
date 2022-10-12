from typer import Exit

from rich import print


class DockerNotFoundError(Exit):
    def __init__(self) -> None:
        print("Unable to find Docker running on your system.")
        super().__init__(1)


class LocalOnlyError(Exit):
    def __init__(self) -> None:
        print("Currently Unable to tear down non-local Engines.")
        super().__init__(1)


class EngineInitializationError(Exit):
    def __init__(self) -> None:
        print("The Starpack Engine was unable to start up. Please try again.")
        super().__init__(1)
