from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import database as db

app = FastAPI(title="Ventas BCP API")

# Permitir peticiones desde cualquier origen (el HTML del banco)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    db.inicializar_db()


# ── MODELOS ──────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    matricula: str

class VentaRequest(BaseModel):
    matricula: str
    campana: str
    monto: float = 0

class AnularRequest(BaseModel):
    venta_id: int

class EditarRequest(BaseModel):
    venta_id: int
    nueva_campana: str
    nuevo_monto: float
    nuevos_puntos: float

class MarcarLeidasRequest(BaseModel):
    matricula_sup: str


# ── ENDPOINTS ────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "app": "Ventas BCP API"}


@app.post("/login")
def login(req: LoginRequest):
    usuario = db.login(req.matricula.strip().upper())
    if not usuario:
        raise HTTPException(status_code=404, detail="Matricula no encontrada")
    return usuario


@app.post("/ventas/registrar")
def registrar_venta(req: VentaRequest):
    puntos = db.registrar_venta(req.matricula, req.campana, req.monto)
    return {"ok": True, "puntos": puntos}


@app.post("/ventas/anular")
def anular_venta(req: AnularRequest):
    db.anular_venta(req.venta_id)
    return {"ok": True}


@app.post("/ventas/editar")
def editar_venta(req: EditarRequest):
    db.editar_venta(req.venta_id, req.nueva_campana, req.nuevo_monto, req.nuevos_puntos)
    return {"ok": True}


@app.get("/ventas/asesor/{matricula}")
def ventas_asesor(matricula: str, fecha: Optional[str] = None):
    return db.get_ventas_asesor_con_anuladas(matricula, fecha)


@app.get("/resumen/asesor/{matricula}")
def resumen_asesor(matricula: str, fecha: Optional[str] = None):
    return db.get_resumen_asesor(matricula, fecha)


@app.get("/resumen/equipo/{matricula_sup}")
def resumen_equipo(matricula_sup: str, fecha: Optional[str] = None):
    return db.get_resumen_equipo(matricula_sup, fecha)


@app.get("/resumen/gerencia")
def resumen_gerencia(fecha: Optional[str] = None):
    return db.get_resumen_gerencia(fecha)


@app.get("/notificaciones/{matricula_sup}")
def notificaciones(matricula_sup: str, solo_hoy: bool = True):
    return db.get_notificaciones(matricula_sup, solo_hoy)


@app.get("/notificaciones/nuevas/{matricula_sup}/{ultimo_id}")
def notificaciones_nuevas(matricula_sup: str, ultimo_id: int):
    return db.get_notificaciones_nuevas(matricula_sup, ultimo_id)


@app.post("/notificaciones/marcar-leidas")
def marcar_leidas(req: MarcarLeidasRequest):
    db.marcar_leidas(req.matricula_sup)
    return {"ok": True}


@app.get("/moderador/usuarios")
def todos_usuarios():
    return db.get_todos_usuarios()


@app.get("/moderador/ventas")
def todas_ventas(fecha: Optional[str] = None):
    return db.get_todas_ventas(fecha)


@app.get("/historial/equipo/{matricula_sup}")
def historial_equipo(matricula_sup: str, fecha_ini: str, fecha_fin: str):
    return db.get_historial_equipo(matricula_sup, fecha_ini, fecha_fin)
