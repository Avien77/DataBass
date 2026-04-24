from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")


@router.get("/uniforms", response_class=HTMLResponse)
def uniforms_page(request: Request, query: str = ""):

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("SELECT * FROM Uniform")
        rows = cursor.fetchall()

        uniforms = []
        for row in rows:
            uniform = {
                "uniform_id": row["Uniform_ID"],
                "uniform_type": "Standard",  # placeholder
                "role": str(row["Role_ID"]) if row["Role_ID"] else "N/A",
                "size": f"W{row['Uniform_Waist']}/I{row['Uniform_Inseam']}",
                "status": "Available"  # placeholder
            }
            uniforms.append(uniform)

        if query:
            q = query.lower()
            uniforms = [
                u for u in uniforms
                if q in str(u["uniform_id"]).lower()
                or q in u["uniform_type"].lower()
                or q in u["role"].lower()
                or q in u["size"].lower()
                or q in u["status"].lower()
            ]

        success = True

    except Exception as e:
        error_message = str(e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

    if success:
        return templates.TemplateResponse(
            request=request,
            name="uniforms.html",
            context={"request": request, "uniforms": uniforms},
            status_code=200
        )

    return templates.TemplateResponse(
        request=request,
        name="uniforms.html",
        context={"request": request, "uniforms": [], "error": error_message},
        status_code=500
    )