# pyrefly: ignore [missing-import]
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from typing import Optional
# pyrefly: ignore [missing-import]
from datetime import datetime


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    username: str
    admin: bool

    model_config = {
        "from_attributes": True
    }