"""Conexão Oracle (TOTVS RM) via variáveis de ambiente."""
import os
import cx_Oracle
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    dsn = cx_Oracle.makedsn(os.getenv("ORACLE_HOST"), int(os.getenv("ORACLE_PORT",1521)),
                            service_name=os.getenv("ORACLE_SERVICE"))
    return cx_Oracle.connect(user=os.getenv("ORACLE_USER"),
                             password=os.getenv("ORACLE_PASSWORD"), dsn=dsn)

def buscar_funcionarios() -> list[dict]:
    """Busca funcionários e seus dados de pagamento do TOTVS RM."""
    query = """
        SELECT F.CODPESSOA, P.NOME, F.DATAADMISSAO,
               S.NOMEDEPARTAMENTO AS DEPTO,
               FP.SALARIOBASE, FP.COMPETENCIA
        FROM PRFUNCIONARIO F
        JOIN PPESSOA P         ON P.CODPESSOA  = F.CODPESSOA
        JOIN PDEPTO S          ON S.CODDEPTO   = F.CODDEPTO
        JOIN PRFOLHAPAGTO FP   ON FP.CODPESSOA = F.CODPESSOA
        WHERE F.CODSITUACAO = 'A'
          AND FP.COMPETENCIA = TO_CHAR(ADD_MONTHS(SYSDATE,-1),'MM/YYYY')
        ORDER BY S.NOMEDEPARTAMENTO, P.NOME
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query)
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        conn.close()
