"""Geração de PDFs de holerite com ReportLab."""
from datetime import date
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from utils.calculos import calcular_liquido

OUTPUT_DIR = Path("holerites_gerados")

def gerar_holerite(func: dict) -> str:
    depto = func.get("DEPTO","GERAL").replace(" ","_")
    pasta = OUTPUT_DIR / depto
    pasta.mkdir(parents=True, exist_ok=True)
    arq   = str(pasta / f"{func['CODPESSOA']}_{func['NOME'].replace(' ','_')}.pdf")

    calcs = calcular_liquido(float(func["SALARIOBASE"]))
    doc   = SimpleDocTemplate(arq, pagesize=A4,
                               rightMargin=2*cm, leftMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    tit = ParagraphStyle("T", parent=styles["Heading1"], fontSize=13, alignment=1)
    sub = ParagraphStyle("S", parent=styles["Normal"],  fontSize=10, leading=14)

    elementos = [
        Paragraph("HOLERITE DE PAGAMENTO", tit),
        Spacer(1, .4*cm),
        Paragraph(f"<b>Funcionário:</b> {func['NOME']}  |  "
                  f"<b>Cód:</b> {func['CODPESSOA']}  |  "
                  f"<b>Depto:</b> {func['DEPTO']}  |  "
                  f"<b>Competência:</b> {func['COMPETENCIA']}", sub),
        Spacer(1, .6*cm),
    ]

    dados = [
        ["Descrição", "Valor"],
        ["Salário Bruto",   f"R$ {calcs['salario_bruto']:>10,.2f}"],
        ["(-) INSS",        f"R$ {calcs['inss']:>10,.2f}"],
        ["(-) IRRF",        f"R$ {calcs['irrf']:>10,.2f}"],
        ["(=) Salário Líquido", f"R$ {calcs['salario_liquido']:>10,.2f}"],
        ["FGTS (referência)",   f"R$ {calcs['fgts']:>10,.2f}"],
    ]
    t = Table(dados, colWidths=[12*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1D6C4E")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID",       (0,0), (-1,-1), .5, colors.grey),
        ("ALIGN",      (1,0), (1,-1), "RIGHT"),
        ("BACKGROUND", (0,4), (-1,4), colors.HexColor("#E1F5EE")),
        ("FONTNAME",   (0,4), (-1,4), "Helvetica-Bold"),
    ]))
    elementos += [t, Spacer(1,1.5*cm),
                  Paragraph("_"*55, sub),
                  Paragraph(f"Assinatura do Funcionário: {func['NOME']}", sub),
                  Spacer(1,.3*cm),
                  Paragraph(f"Data: ____/____/________", sub)]
    doc.build(elementos)
    return arq

def gerar_holerites_lote(funcionarios: list[dict]) -> dict:
    gerados = []
    for f in funcionarios:
        p = gerar_holerite(f)
        gerados.append(p)
        print(f"  [✓] {p}")
    return {"total": len(gerados), "arquivos": gerados}
