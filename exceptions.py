from fastapi import HTTPException, status


usuarioYaExisteException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="El usuario ya existe",
)
 
usuarioNoEncontradoException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Usuario no encontrado",
)

contrasenaIncorrectaException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Contraseña incorrecta",
)

credentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales inválidas",
    headers={"WWW-Authenticate": "Bearer"},
)

noAutorizadoException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No autorizado",
)

proveedorYaExisteException = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="El proveedor ya existe",
)

contactoYaExisteException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="El contacto ya existe",
)

proveedorNoEncontradoException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Proveedor no encontrado",
)

materialYaExisteException = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="El material ya existe",
)

materialNoEncontradoException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Material no encontrado",
)

clienteNoEncontradoException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Cliente no encontrado",
)

clienteYaExisteException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="El cliente ya existe con ese contacto",
)

transaccionNoEncontradaException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Transaccion no encontrada",
)

transaccionYaExisteException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="La transaccion ya existe",
)

proveedorNoEncontradoCompraException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Proveedor no encontrado",
)

constantePacaException = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="La constante paca es la misma que la actual",
)