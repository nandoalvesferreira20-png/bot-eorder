import os
from dotenv import load_dotenv

load_dotenv()

EORDER_URL = os.getenv("EORDER_URL")
EXCEL_PATH = os.getenv("EXCEL_PATH", "planilhas/notas.xlsx")