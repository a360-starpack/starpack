from enum import Enum


class Resource(str, Enum):
    """ENUM class for CRUD resources"""
    def __str__(self):
        return self.value

    MODEL = "model"
    PACKAGE = "package"
    DEPLOYMENT = "deployment"
