from models import Material
import uuid

def verificacionDeMateriaPrima(cantidad: int, material: Material):
    materialDisponible = material.kgs_en_inventario - material.estimado_kg_pacas
    if materialDisponible < 0:
        return False
    maximaCantidadPacas = materialDisponible // (material.constante_paca - material.tolerancia_paca)
    if cantidad > maximaCantidadPacas:
        return False
    material.estimado_kg_pacas += cantidad * material.constante_paca
    return True    

def generarCodigoPaca() -> str:
    return f"PAC-{uuid.uuid4().hex[:8].upper()}"