from typing import ClassVar, TypeVar

from pydantic import BaseModel, ConfigDict


T = TypeVar("T", bound="BaseSchemaModel")


class BaseSchemaModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True,)

    @classmethod
    def get_config(cls) -> ConfigDict:
        return cls.model_config


