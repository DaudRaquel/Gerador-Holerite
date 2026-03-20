"""
Gerador de Holerites — Script principal.

Extrai dados de funcionários do TOTVS RM (Oracle) e gera
holerites em PDF organizados por departamento.

Uso:
    python main.py           # produção (Oracle)
    python main.py --mock    # testes (dados fictícios)
"""
import argparse
from database.conexao import buscar_funcionarios
from database.mock_data import FUNCIONARIOS_MOCK
from pdf.gerador_holerite import gerar_holerites_lote


def main(mock: bool = False):
    print("=" * 50)
    print("  GERADOR DE HOLERITES")
    print("=" * 50)
    print("\n[1/3] Buscando funcionários...")
    funcionarios = FUNCIONARIOS_MOCK if mock else buscar_funcionarios()
    print(f"      {len(funcionarios)} funcionário(s) encontrado(s).")
    print("\n[2/3] Gerando PDFs...")
    resultado = gerar_holerites_lote(funcionarios)
    print(f"\n✅  {resultado['total']} holerites gerados em ./holerites_gerados/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mock", action="store_true")
    main(mock=ap.parse_args().mock)
