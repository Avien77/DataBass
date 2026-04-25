from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/rental", response_class=HTMLResponse)
def rental_page(request: Request):

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # Fetch instrument Rentals
    try:
        query = "SELECT * " \
        "FROM Student_Instrument_Rentals r " \
        "join Student s on r.Stud_ID = s.Stud_ID " \
        "join Instrument i on r.Instrument_ID = i.Instrument_ID " \
        "join Instrument_Types t on i.Instrument_Type = t.Instr_Type_ID" 
        cursor.execute(query)
        instrument_rentals = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching instrument rentals: {e}")
        instrument_rentals = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request, 
        "rental.html", 
        {"request": request, "instrument_rentals": instrument_rentals}
    )


@router.post("/rental", response_class=HTMLResponse)
def rental_lookup(request: Request, stud_id: str = Form(...)):

    return templates.TemplateResponse(
        request,
        "rental.html",
        {
            "request": request,
        }
    )
