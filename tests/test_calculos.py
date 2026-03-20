"""Testes para cálculos de INSS, IRRF e FGTS."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from utils.calculos import calcular_inss, calcular_irrf, calcular_liquido


# ── INSS ──────────────────────────────────────────────────────────────
def test_inss_isento():
    """Salário abaixo da primeira faixa → alíquota mínima (7,5%)."""
    inss = calcular_inss(1000.0)
    assert inss == round(1000.0 * 0.075, 2)

def test_inss_faixa_maxima():
    """Salário acima do teto deve ser limitado ao teto."""
    inss_alto = calcular_inss(20000.0)
    inss_teto = calcular_inss(7786.02)
    assert inss_alto == inss_teto

def test_inss_progressivo():
    """Salário maior deve gerar INSS maior."""
    assert calcular_inss(3000.0) > calcular_inss(2000.0)

def test_inss_nunca_negativo():
    assert calcular_inss(0.0) == 0.0

# ── IRRF ──────────────────────────────────────────────────────────────
def test_irrf_isento():
    """Base de cálculo abaixo do limite → IRRF zero."""
    inss = calcular_inss(2000.0)
    irrf = calcular_irrf(2000.0, inss)
    assert irrf == 0.0

def test_irrf_positivo_em_salario_alto():
    inss = calcular_inss(8000.0)
    irrf = calcular_irrf(8000.0, inss)
    assert irrf > 0.0

def test_irrf_nunca_negativo():
    for sal in [1000, 2000, 3000, 5000, 10000]:
        inss = calcular_inss(float(sal))
        assert calcular_irrf(float(sal), inss) >= 0.0

# ── Liquido ───────────────────────────────────────────────────────────
def test_liquido_menor_que_bruto():
    resultado = calcular_liquido(5000.0)
    assert resultado["salario_liquido"] < resultado["salario_bruto"]

def test_liquido_campos_presentes():
    resultado = calcular_liquido(3000.0)
    assert {"salario_bruto","inss","irrf","fgts","salario_liquido"}.issubset(resultado.keys())

def test_fgts_e_8_porcento():
    resultado = calcular_liquido(2000.0)
    assert resultado["fgts"] == round(2000.0 * 0.08, 2)

def test_liquido_consistente():
    """liquido = bruto - inss - irrf."""
    r = calcular_liquido(4000.0)
    esperado = round(r["salario_bruto"] - r["inss"] - r["irrf"], 2)
    assert r["salario_liquido"] == esperado
