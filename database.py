import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "ventas.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            matricula   TEXT PRIMARY KEY,
            nombre      TEXT NOT NULL,
            rol         TEXT NOT NULL,
            supervisor  TEXT,
            equipo      TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula   TEXT NOT NULL,
            campana     TEXT NOT NULL,
            monto       REAL DEFAULT 0,
            puntos      REAL DEFAULT 0,
            fecha       TEXT NOT NULL,
            hora        TEXT NOT NULL,
            estado      TEXT DEFAULT 'activo'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS notificaciones (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula_sup   TEXT NOT NULL,
            matricula_as    TEXT NOT NULL,
            nombre_as       TEXT NOT NULL,
            campana         TEXT NOT NULL,
            puntos          REAL DEFAULT 0,
            fecha           TEXT NOT NULL,
            hora            TEXT NOT NULL,
            leida           INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula_sup   TEXT NOT NULL,
            tipo            TEXT NOT NULL,
            valor           REAL NOT NULL,
            fecha           TEXT NOT NULL,
            dias_comerciales INTEGER DEFAULT 26,
            UNIQUE(matricula_sup, tipo, fecha)
        )
    """)

    conn.commit()

    c.execute("SELECT COUNT(*) FROM usuarios")
    if c.fetchone()[0] == 0:
        usuarios = [
            ("T49493", "Esteban Poma Calderon",                "moderador", None,    None),
            ("S11243", "Gabriela Hutchins",                    "gerente",   None,    "Gerencia"),
            ("T15797", "Lourdes Pierina Vertiz Leyva",         "supervisor", None,   "CD 03"),
            ("S93534", "Angela Valencia Bravo",                "supervisor", None,   "INB 07"),
            ("E18886", "Adela Peceros",                        "supervisor", None,   "INB 09"),
            ("T44499", "Katherine Ramos",                      "supervisor", None,   "INB 38"),
            ("S74723", "Claudia Echevarria",                   "supervisor", None,   "SWAT 03"),
            # ASESORES CD 03
            ("S96551", "Carrasco Torres Salome",               "asesor", "T15797", "CD 03"),
            ("T43756", "Llaque Asurza Valeria Andrea",         "asesor", "T15797", "CD 03"),
            ("T65103", "Huayta Quispe Katherine Mariffer",     "asesor", "T15797", "CD 03"),
            ("T65116", "Polo Zapata Nayeli Ximena",            "asesor", "T15797", "CD 03"),
            ("T65146", "Camacho Castello Eland Eduardo",       "asesor", "T15797", "CD 03"),
            ("T65182", "De La Cruz Enriquez Lucero",           "asesor", "T15797", "CD 03"),
            ("T65255", "Curo Vega Ivon Yulissa",               "asesor", "T15797", "CD 03"),
            ("T66228", "Enciso Mauli Kevin Santiago",          "asesor", "T15797", "CD 03"),
            ("T69463", "Egas Ramirez Miriam Alexandra",        "asesor", "T15797", "CD 03"),
            ("T69607", "Velasquez Caballero Nathaly Anthuane", "asesor", "T15797", "CD 03"),
            ("T69650", "Cobenas Fernandez Andrea Esperanza",   "asesor", "T15797", "CD 03"),
            ("T69652", "Vega Ascoy Victor Jesus",              "asesor", "T15797", "CD 03"),
            # ASESORES INB 07
            ("T30105", "Melgarejo Justiniano Yessyca Karin",   "asesor", "S93534", "INB 07"),
            ("T41349", "Castilla Dulanto Jesus Aaron",         "asesor", "S93534", "INB 07"),
            ("T69408", "Vega Figueroa Cindy Stephanie",        "asesor", "S93534", "INB 07"),
            ("T65147", "Carranza Menor Katherin Xiomara",      "asesor", "S93534", "INB 07"),
            ("T46553", "Ortega Ingaruca Luis Daniel",          "asesor", "S93534", "INB 07"),
            ("S99413", "Saldana Llanos Cynthia Alejandra",     "asesor", "S93534", "INB 07"),
            ("T65104", "Aquino Llantay Aldair Jholinho",       "asesor", "S93534", "INB 07"),
            ("T67678", "Sullon Chiroque Rosmery Katterine",    "asesor", "S93534", "INB 07"),
            ("T45577", "Yaro Felix Sebastian Mateo",           "asesor", "S93534", "INB 07"),
            ("T35348", "Araujo Garcia Michael Sklibert",       "asesor", "S93534", "INB 07"),
            ("T63508", "Acosta Suarez Brallan Manuel",         "asesor", "S93534", "INB 07"),
            ("T70946", "Alfaro Paredes Evelyn Rosita",         "asesor", "S93534", "INB 07"),
            ("T70951", "Toledo Zapata Betsabe Sarai",          "asesor", "S93534", "INB 07"),
            # ASESORES INB 09
            ("T65063", "Villanueva Julon Mirella Del Rocio",   "asesor", "E18886", "INB 09"),
            ("T65194", "Burgos Garcia Johnathan Ricardo",      "asesor", "E18886", "INB 09"),
            ("T30218", "Fajardo Ccahuana Elizabeth Jessica",   "asesor", "E18886", "INB 09"),
            ("T59052", "Calagua Apcho Jean Fernando",          "asesor", "E18886", "INB 09"),
            ("T56538", "Pacori Mayanga Edward Guillermo",      "asesor", "E18886", "INB 09"),
            ("T36336", "Huamali Solis Antonio Arturo",         "asesor", "E18886", "INB 09"),
            ("T59056", "Ingaruca Pardo Kevin Rafael",          "asesor", "E18886", "INB 09"),
            ("T59328", "Delgado Alvarado Ana Gabriel",         "asesor", "E18886", "INB 09"),
            ("T15892", "Tello Castillo Anderson Julio",        "asesor", "E18886", "INB 09"),
            ("T66329", "Cango Garcia Manuel Antonio",          "asesor", "E18886", "INB 09"),
            ("T67644", "Surco Nunez Mathias Samher",           "asesor", "E18886", "INB 09"),
            ("S98192", "Quiroga Mamani Jose Luis",             "asesor", "E18886", "INB 09"),
            ("T45432", "Aldana Alarcon Jean Marko",            "asesor", "E18886", "INB 09"),
            ("T31158", "Pena Mendoza Keyla Darlene",           "asesor", "E18886", "INB 09"),
            ("T67789", "Astete Ynga Mery Key",                 "asesor", "E18886", "INB 09"),
            ("S99423", "Yucra Fabian Cristhoper Jose",         "asesor", "E18886", "INB 09"),
            # ASESORES INB 38
            ("T75404", "Apestegui Huaman Ruth Sofia",          "asesor", "T44499", "INB 38"),
            ("T75448", "Figueroa Olaya Nayeli Angelina",       "asesor", "T44499", "INB 38"),
            ("T75453", "Huaman Milla Francessco Skyabi",       "asesor", "T44499", "INB 38"),
            ("T75454", "Lossio Tapia Marcelo",                 "asesor", "T44499", "INB 38"),
            ("T75484", "Zapata Garcia Nallely Rubi",           "asesor", "T44499", "INB 38"),
            ("T75511", "Aquino Alvarez Sara Adriana",          "asesor", "T44499", "INB 38"),
            ("T75514", "Rojas Condo Marysabel",                "asesor", "T44499", "INB 38"),
            ("T75529", "Huane Valentin Jennifer Nahomy",       "asesor", "T44499", "INB 38"),
            ("T75557", "Hernandez Mendoza Luis Fernando",      "asesor", "T44499", "INB 38"),
            ("T75571", "Sandoval Zapata Daniel Junior",        "asesor", "T44499", "INB 38"),
            ("T75572", "Zegarra Mantilla Marisol Grecia",      "asesor", "T44499", "INB 38"),
        ]
        c.executemany("INSERT INTO usuarios VALUES (?,?,?,?,?)", usuarios)
        conn.commit()
    conn.close()


# ── CALCULOS ─────────────────────────────────────────────────────────────────

PUNTOS_FIJOS = {
    "AMP": 7.0, "UPG": 0.0, "UPG_ACT": 11.0, "TA": 7.0, "SPT": 2.0,
}

def calcular_puntos(campana, monto=0):
    if campana in PUNTOS_FIJOS:
        return PUNTOS_FIJOS[campana]
    if campana == "PTC":
        return round(monto * 0.0021, 2)
    if campana == "BT":
        return round(monto * 0.0013, 2)
    return 0.0


def login(matricula):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE matricula=?", (matricula,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def registrar_venta(matricula, campana, monto=0):
    puntos = calcular_puntos(campana, monto)
    hoy  = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M")
    conn = get_conn()
    conn.execute(
        "INSERT INTO ventas (matricula,campana,monto,puntos,fecha,hora) VALUES (?,?,?,?,?,?)",
        (matricula, campana, monto, puntos, hoy, hora)
    )
    c = conn.cursor()
    c.execute("SELECT nombre, supervisor FROM usuarios WHERE matricula=?", (matricula,))
    row = c.fetchone()
    if row and row["supervisor"]:
        conn.execute(
            "INSERT INTO notificaciones (matricula_sup,matricula_as,nombre_as,campana,puntos,fecha,hora) VALUES (?,?,?,?,?,?,?)",
            (row["supervisor"], matricula, row["nombre"], campana, puntos, hoy, hora)
        )
    conn.commit()
    conn.close()
    return puntos


def anular_venta(venta_id):
    conn = get_conn()
    conn.execute("UPDATE ventas SET estado='anulado' WHERE id=?", (venta_id,))
    conn.commit()
    conn.close()


def editar_venta(venta_id, nueva_campana, nuevo_monto, nuevos_puntos):
    conn = get_conn()
    conn.execute(
        "UPDATE ventas SET campana=?, monto=?, puntos=?, estado='activo' WHERE id=?",
        (nueva_campana, nuevo_monto, nuevos_puntos, venta_id)
    )
    conn.commit()
    conn.close()


def get_notificaciones(matricula_sup, solo_hoy=True):
    conn = get_conn()
    c = conn.cursor()
    if solo_hoy:
        hoy = datetime.now().strftime("%Y-%m-%d")
        c.execute("SELECT * FROM notificaciones WHERE matricula_sup=? AND fecha=? ORDER BY id DESC",
                  (matricula_sup, hoy))
    else:
        c.execute("SELECT * FROM notificaciones WHERE matricula_sup=? ORDER BY id DESC LIMIT 50",
                  (matricula_sup,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_notificaciones_nuevas(matricula_sup, ultimo_id):
    conn = get_conn()
    c = conn.cursor()
    hoy = datetime.now().strftime("%Y-%m-%d")
    c.execute(
        "SELECT * FROM notificaciones WHERE matricula_sup=? AND fecha=? AND id > ? ORDER BY id ASC",
        (matricula_sup, hoy, ultimo_id)
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def marcar_leidas(matricula_sup):
    conn = get_conn()
    conn.execute("UPDATE notificaciones SET leida=1 WHERE matricula_sup=?", (matricula_sup,))
    conn.commit()
    conn.close()


def get_ventas_asesor(matricula, fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id,campana,monto,puntos,hora FROM ventas WHERE matricula=? AND fecha=? AND estado='activo' ORDER BY hora",
        (matricula, fecha)
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_ventas_asesor_con_anuladas(matricula, fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id,campana,monto,puntos,hora,estado FROM ventas WHERE matricula=? AND fecha=? ORDER BY hora",
        (matricula, fecha)
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_resumen_asesor(matricula, fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    ventas = get_ventas_asesor(matricula, fecha)
    resumen = {"AMP":0,"UPG":0,"PTC":0,"BT":0,"UPG_ACT":0,"TA":0,"SPT":0,"total_puntos":0.0}
    for v in ventas:
        camp = v["campana"]
        if camp in resumen:
            resumen[camp] += 1
        resumen["total_puntos"] = round(resumen["total_puntos"] + v["puntos"], 2)
    return resumen


def get_equipo_de_supervisor(matricula_sup):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE supervisor=?", (matricula_sup,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_resumen_equipo(matricula_sup, fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    equipo = get_equipo_de_supervisor(matricula_sup)
    resultado = []
    for asesor in equipo:
        resumen = get_resumen_asesor(asesor["matricula"], fecha)
        resumen["nombre"] = asesor["nombre"]
        resumen["matricula"] = asesor["matricula"]
        resultado.append(resumen)
    return resultado


def get_todos_supervisores():
    conn = get_conn()
    c = conn.cursor()
    # CD 03 y SWAT 03 son equipos no comerciales — se excluyen del ranking
    c.execute("SELECT * FROM usuarios WHERE rol='supervisor' AND equipo NOT IN ('CD 03', 'SWAT 03')")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_resumen_gerencia(fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    supervisores = get_todos_supervisores()
    resultado = []
    for sup in supervisores:
        equipo = get_resumen_equipo(sup["matricula"], fecha)
        total_puntos = round(sum(a["total_puntos"] for a in equipo), 2)
        resultado.append({
            "supervisor": sup["nombre"], "equipo": sup["equipo"],
            "matricula":  sup["matricula"], "asesores": equipo,
            "total_puntos": total_puntos,
            "total_ventas": sum(
                a["AMP"]+a["UPG"]+a["PTC"]+a["BT"]+a["UPG_ACT"] for a in equipo
            )
        })
    return resultado


def get_historial_equipo(matricula_sup, fecha_ini, fecha_fin):
    equipo  = get_equipo_de_supervisor(matricula_sup)
    matriculas = [a["matricula"] for a in equipo]
    nombres    = {a["matricula"]: a["nombre"] for a in equipo}
    if not matriculas:
        return []
    placeholders = ",".join("?" * len(matriculas))
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        f"SELECT id,matricula,campana,monto,puntos,fecha,hora,estado FROM ventas "
        f"WHERE matricula IN ({placeholders}) AND fecha BETWEEN ? AND ? AND estado='activo' "
        f"ORDER BY fecha,hora,matricula",
        matriculas + [fecha_ini, fecha_fin]
    )
    rows = []
    for r in c.fetchall():
        d = dict(r)
        d["nombre"] = nombres.get(d["matricula"], d["matricula"])
        rows.append(d)
    conn.close()
    return rows


def get_todos_usuarios():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios ORDER BY rol, equipo, nombre")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_todas_
