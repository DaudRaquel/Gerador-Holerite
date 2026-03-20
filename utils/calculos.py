"""Cálculos de descontos e proventos para holerite."""

TABELA_INSS = [
    (1412.00,  0.075),
    (2666.68,  0.09),
    (4000.03,  0.12),
    (7786.02,  0.14),
]

def calcular_inss(salario: float) -> float:
    """Cálculo progressivo do INSS."""
    total, anterior = 0.0, 0.0
    for teto, aliq in TABELA_INSS:
        if salario <= 0: break
        base = min(salario, teto) - anterior
        total += base * aliq
        anterior = teto
        if salario <= teto: break
    return round(total, 2)

def calcular_irrf(salario: float, inss: float) -> float:
    """Cálculo simplificado do IRRF."""
    base = salario - inss
    if   base <= 2259.20: return 0.0
    elif base <= 2826.65: return round(base * 0.075 - 169.44, 2)
    elif base <= 3751.05: return round(base * 0.15  - 381.44, 2)
    elif base <= 4664.68: return round(base * 0.225 - 662.77, 2)
    else:                  return round(base * 0.275 - 896.00, 2)

def calcular_liquido(salario: float) -> dict:
    inss  = calcular_inss(salario)
    irrf  = calcular_irrf(salario, inss)
    fgts  = round(salario * 0.08, 2)
    liquido = round(salario - inss - irrf, 2)
    return {"salario_bruto": salario, "inss": inss,
            "irrf": irrf, "fgts": fgts, "salario_liquido": liquido}
