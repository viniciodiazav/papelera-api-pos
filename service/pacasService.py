from models import Material, Paca
import uuid

def registrarProduccionPacas(cantidad: int, material: Material):
    pesoTotalDescontar = cantidad * material.constante_paca
    
    if material.kgs_en_inventario < pesoTotalDescontar:
        return []

    material.kgs_en_inventario -= pesoTotalDescontar
    
    nuevasPacas = []
    for i in range(0, cantidad):
        paca = Paca(
            id_material = material.id,
            peso_estimado = material.constante_paca,
            codigo = generarCodigoPaca()
        )
        nuevasPacas.append(paca)

    return nuevasPacas

def generarCodigoPaca():
    return f"PAC-{uuid.uuid4().hex[:8].upper()}"