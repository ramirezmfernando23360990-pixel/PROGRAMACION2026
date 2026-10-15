from datetime import date, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI()

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

# Tipo de cambio USD -> MXN (pesos mexicanos por 1 dólar estadounidense).
# Fuente: Frankfurter API (tasas de referencia del Banco Central Europeo).
# Son valores de días hábiles; no hay dato en fines de semana ni días festivos.
TIPO_DE_CAMBIO = {
    "2026-01-02": 17.9396, "2026-01-05": 18.0101, "2026-01-06": 17.9576,
    "2026-01-07": 17.9810, "2026-01-08": 17.9640, "2026-01-09": 18.0278,
    "2026-01-12": 17.9028, "2026-01-13": 17.8986, "2026-01-14": 17.8113,
    "2026-01-15": 17.7891, "2026-01-16": 17.6750, "2026-01-19": 17.6296,
    "2026-01-20": 17.6236, "2026-01-21": 17.4785, "2026-01-22": 17.4851,
    "2026-01-23": 17.4434, "2026-01-26": 17.3902, "2026-01-27": 17.2982,
    "2026-01-28": 17.1547, "2026-01-29": 17.1507, "2026-01-30": 17.2817,
    "2026-02-02": 17.4096, "2026-02-03": 17.3070, "2026-02-04": 17.2428,
    "2026-02-05": 17.3852, "2026-02-06": 17.3639, "2026-02-09": 17.2118,
    "2026-02-10": 17.2356, "2026-02-11": 17.2034, "2026-02-12": 17.1745,
    "2026-02-13": 17.2205, "2026-02-16": 17.1556, "2026-02-17": 17.2138,
    "2026-02-18": 17.1136, "2026-02-19": 17.2798, "2026-02-20": 17.2006,
    "2026-02-23": 17.1970, "2026-02-24": 17.2828, "2026-02-25": 17.1487,
    "2026-02-26": 17.1771, "2026-02-27": 17.2122,
    "2026-03-02": 17.3491, "2026-03-03": 17.5151, "2026-03-04": 17.5483,
    "2026-03-05": 17.6338, "2026-03-06": 17.7857, "2026-03-09": 17.8477,
    "2026-03-10": 17.5595, "2026-03-11": 17.6496, "2026-03-12": 17.7128,
    "2026-03-13": 17.8215, "2026-03-16": 17.8001, "2026-03-17": 17.6620,
    "2026-03-18": 17.7339, "2026-03-19": 17.9180, "2026-03-20": 17.8174,
    "2026-03-23": 17.7665, "2026-03-24": 17.8854, "2026-03-25": 17.7657,
    "2026-03-26": 17.8178, "2026-03-27": 18.0577, "2026-03-30": 18.0930,
    "2026-03-31": 18.0118,
    "2026-04-01": 17.8535, "2026-04-02": 17.9393, "2026-04-07": 17.7529,
    "2026-04-08": 17.4013, "2026-04-09": 17.4360, "2026-04-10": 17.3495,
    "2026-04-13": 17.3913, "2026-04-14": 17.2280, "2026-04-15": 17.3056,
    "2026-04-16": 17.2696, "2026-04-17": 17.2196, "2026-04-20": 17.3503,
    "2026-04-21": 17.3086, "2026-04-22": 17.3195, "2026-04-23": 17.3516,
    "2026-04-24": 17.3881, "2026-04-27": 17.3547, "2026-04-28": 17.4563,
    "2026-04-29": 17.3988, "2026-04-30": 17.5158,
    "2026-05-04": 17.4906, "2026-05-05": 17.4414, "2026-05-06": 17.2607,
    "2026-05-07": 17.2022, "2026-05-08": 17.2366, "2026-05-11": 17.2197,
    "2026-05-12": 17.2474, "2026-05-13": 17.2232, "2026-05-14": 17.1988,
    "2026-05-15": 17.3736, "2026-05-18": 17.2922, "2026-05-19": 17.3425,
    "2026-05-20": 17.3681, "2026-05-21": 17.3515, "2026-05-22": 17.3385,
    "2026-05-25": 17.2679, "2026-05-26": 17.2881, "2026-05-27": 17.3189,
    "2026-05-28": 17.3883, "2026-05-29": 17.3394,
    "2026-06-01": 17.3270, "2026-06-02": 17.2830, "2026-06-03": 17.2912,
    "2026-06-04": 17.2826, "2026-06-05": 17.2706, "2026-06-08": 17.4125,
    "2026-06-09": 17.3818, "2026-06-10": 17.4790, "2026-06-11": 17.3919,
    "2026-06-12": 17.2243, "2026-06-15": 17.2113, "2026-06-16": 17.2027,
    "2026-06-17": 17.2105, "2026-06-18": 17.3914, "2026-06-19": 17.3364,
    "2026-06-22": 17.3311, "2026-06-23": 17.4860, "2026-06-24": 17.6197,
    "2026-06-25": 17.6389, "2026-06-26": 17.5156, "2026-06-29": 17.4754,
    "2026-06-30": 17.4680,
    "2026-07-01": 17.5341, "2026-07-02": 17.5586, "2026-07-03": 17.4472,
    "2026-07-06": 17.4845, "2026-07-07": 17.4238, "2026-07-08": 17.5754,
    "2026-07-09": 17.5505, "2026-07-10": 17.5276, "2026-07-13": 17.4908,
    "2026-07-14": 17.5000, "2026-07-15": 17.4303, "2026-07-16": 17.4264,
    "2026-07-17": 17.4837, "2026-07-20": 17.4899, "2026-07-21": 17.3943,
    "2026-07-22": 17.4235, "2026-07-23": 17.4601, "2026-07-24": 17.4803,
    "2026-07-27": 17.4569, "2026-07-28": 17.4742, "2026-07-29": 17.4755,
    "2026-07-30": 17.4001, "2026-07-31": 17.3715,
    "2026-08-03": 17.3207, "2026-08-04": 17.2881, "2026-08-05": 17.2120,
    "2026-08-06": 17.2515, "2026-08-07": 17.1551, "2026-08-10": 17.1512,
    "2026-08-11": 17.1223, "2026-08-12": 17.0614, "2026-08-13": 17.0534,
    "2026-08-14": 16.9959, "2026-08-17": 17.0091, "2026-08-18": 17.0535,
    "2026-08-19": 17.0365, "2026-08-20": 16.9906, "2026-08-21": 16.8980,
    "2026-08-24": 16.9282, "2026-08-25": 16.9467, "2026-08-26": 16.9309,
    "2026-08-27": 16.9732, "2026-08-28": 16.9481, "2026-08-31": 17.0083,
    "2026-09-01": 17.0009, "2026-09-02": 17.0008, "2026-09-03": 17.0119,
    "2026-09-04": 16.8991, "2026-09-07": 16.9121, "2026-09-08": 16.9510,
    "2026-09-09": 16.9025, "2026-09-10": 16.9435, "2026-09-11": 16.9771,
    "2026-09-14": 17.0721, "2026-09-15": 17.1568, "2026-09-16": 17.1382,
    "2026-09-17": 17.1881, "2026-09-18": 17.1776, "2026-09-21": 17.1917,
    "2026-09-22": 17.2491, "2026-09-23": 17.4392, "2026-09-24": 17.5841,
    "2026-09-25": 17.6989, "2026-09-28": 17.7650, "2026-09-29": 17.8970,
    "2026-09-30": 18.1259,
    "2026-10-01": 18.1669, "2026-10-02": 18.3350, "2026-10-05": 18.1498,
    "2026-10-06": 17.9448, "2026-10-07": 18.0943, "2026-10-08": 18.0127,
    "2026-10-09": 18.2001, "2026-10-12": 18.3418, "2026-10-13": 18.3348,
    "2026-10-14": 18.3653,
}


# Último valor del 2025 (31 dic), necesario para el 1 de enero.
VALOR_PREVIO = 17.9728

FECHA_INICIO = date(2026, 1, 1)
FECHA_FIN = date(2026, 10, 14)
ANIO_DATOS = 2026


# ---------------------------------------------------------------------------
# Formato de fechas en español (día-mes-año)
# ---------------------------------------------------------------------------
def fecha_corta(d: date) -> str:
    """ID de cada registro: DD-MM-AA, por ejemplo 02-10-26."""
    return d.strftime("%d-%m-%y")


def fecha_numerica(d: date) -> str:
    """Fecha completa: DD-MM-AAAA, por ejemplo 02-10-2026."""
    return d.strftime("%d-%m-%Y")


def fecha_texto(d: date) -> str:
    """Fecha en texto: 'viernes 2 de octubre de 2026'."""
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]} de {d.year}"


def parsear_fecha(texto: str) -> date:
    """Convierte texto en español a date.

    Acepta:  DD-MM-AA (02-10-26), DD-MM-AAAA (02-10-2026),
             DD-MM (02-10, asume 2026) y también AAAA-MM-DD.
    Los separadores pueden ser "-" o "/".
    """
    partes = texto.strip().replace("/", "-").split("-")
    try:
        if len(partes) == 2:
            dia, mes = (int(p) for p in partes)
            anio = ANIO_DATOS
        elif len(partes) == 3:
            if len(partes[0]) == 4:  # formato AAAA-MM-DD
                anio, mes, dia = (int(p) for p in partes)
            else:
                dia, mes, anio = (int(p) for p in partes)
                if anio < 100:
                    anio += 2000
        else:
            raise ValueError
        return date(anio, mes, dia)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido. Usa DD-MM-AA, por ejemplo 02-10-26.",
        )


# ---------------------------------------------------------------------------
# Construcción de los registros (uno por cada día natural)
# ---------------------------------------------------------------------------
def construir_registros():
    """Genera un registro por CADA día natural (incluye fines de semana y festivos).

    El id de cada registro es su fecha en formato español DD-MM-AA.
    El mercado no opera sábados, domingos ni festivos, así que en esos días
    se arrastra el último valor publicado (el del día hábil anterior) y se
    marca con "es_dia_habil": False.
    """
    registros = {}
    anterior = VALOR_PREVIO
    dia = FECHA_INICIO
    while dia <= FECHA_FIN:
        clave = dia.isoformat()
        es_habil = clave in TIPO_DE_CAMBIO
        valor = TIPO_DE_CAMBIO[clave] if es_habil else anterior
        registros[dia] = {
            "id": fecha_corta(dia),
            "fecha": fecha_numerica(dia),
            "fecha_texto": fecha_texto(dia),
            "dia_semana": DIAS[dia.weekday()],
            "moneda_base": "USD",
            "moneda_destino": "MXN",
            "valor": valor,
            "variacion_vs_dia_anterior": round(valor - anterior, 4),
            "es_dia_habil": es_habil,
        }
        anterior = valor
        dia += timedelta(days=1)
    return registros


REGISTROS = construir_registros()  # {date: registro}


def simplificar(registro: dict) -> dict:
    """Lo que se muestra al consultar: solo id (fecha), moneda base y valor."""
    return {
        "id": registro["id"],
        "moneda_base": registro["moneda_base"],
        "valor": registro["valor"],
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def data_info():
    return {
        "message": "Bienvenidos a la API del valor del dólar (USD a MXN) en 2026",
        "author": "cristofer fernando ramirez medrano",
        "version": "1.0.0",
        "fuente": "Frankfurter API (tasas de referencia del Banco Central Europeo)",
        "nota": "Fines de semana y festivos repiten el último valor hábil (es_dia_habil: false).",
        "como_consultar": {
            "id": "La fecha en formato español DD-MM-AA (día-mes-año).",
            "ejemplo": "/dolar/02-10-26",
            "tambien_acepta": ["02-10-2026", "02-10 (asume 2026)"],
            "rango_disponible": f"{fecha_numerica(FECHA_INICIO)} al {fecha_numerica(FECHA_FIN)}",
        },
    }


@app.get("/dolar")
def data_dolar(inicio: Optional[str] = None, fin: Optional[str] = None):
    """Lista de registros. Filtros opcionales en español: ?inicio=01-10-26&fin=14-10-26"""
    d_inicio = parsear_fecha(inicio) if inicio else FECHA_INICIO
    d_fin = parsear_fecha(fin) if fin else FECHA_FIN

    datos = [simplificar(r) for d, r in REGISTROS.items() if d_inicio <= d <= d_fin]

    return {
        "api_version": "v1",
        "total_records": len(datos),
        "filters_applied": {
            "desde": fecha_numerica(d_inicio),
            "hasta": fecha_numerica(d_fin),
        },
        "data": datos,
    }


@app.get("/dolar/resumen")
def resumen_dolar():
    lista = list(REGISTROS.values())
    valores = [r["valor"] for r in lista]
    maximo = max(lista, key=lambda r: r["valor"])
    minimo = min(lista, key=lambda r: r["valor"])
    return {
        "periodo": {"desde": lista[0]["fecha"], "hasta": lista[-1]["fecha"]},
        "valor_inicial": lista[0]["valor"],
        "valor_actual": lista[-1]["valor"],
        "promedio": round(sum(valores) / len(valores), 4),
        "maximo": {"id": maximo["id"], "fecha": maximo["fecha"], "valor": maximo["valor"]},

    }


@app.get("/dolar/{id_fecha}")
def data_dolar_fecha(id_fecha: str):
    """Busca por id (la fecha en español). Ejemplo: /dolar/02-10-26"""
    fecha = parsear_fecha(id_fecha)
    registro = REGISTROS.get(fecha)
    if registro is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No hay dato para el {fecha_numerica(fecha)}. "
                f"El rango disponible es del {fecha_numerica(FECHA_INICIO)} "
                f"al {fecha_numerica(FECHA_FIN)}."
            ),
        )
    return simplificar(registro)
