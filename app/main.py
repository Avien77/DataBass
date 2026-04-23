import os
from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from mysql.connector import pooling
from dotenv import load_dotenv
from app import db
from .routers import guardians, student_portal, instruments, inventory, measurements, rentals, search, students, uniforms
from fastapi import Form

# Load environment variables
load_dotenv()

app = FastAPI(title="DataBass")
router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

app.include_router(guardians.router)
app.include_router(instruments.router)
app.include_router(inventory.router)
app.include_router(measurements.router)
app.include_router(rentals.router)
app.include_router(search.router)
app.include_router(students.router)
app.include_router(uniforms.router)
app.include_router(student_portal.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:

        return templates.TemplateResponse(request, "login.html")
    finally:
        cursor.close()
        conn.close() # Returns connection to pool

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/DataBASS_Logo.ico")
