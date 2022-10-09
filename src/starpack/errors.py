class DockerNotFoundError(Exception):
    def __init__(self) -> None:
        self.message = "Unable to find Docker running on your system."
        super().__init__(self.message)
