from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/assign-instrument", response_class=HTMLResponse)
def assign_instrument_page(request: Request):
    return templates.TemplateResponse(request, "assign_instrument.html")


@router.post("/assign-instrument", response_class=HTMLResponse)
def assign_instrument_submit(
    request: Request,
    stud_id: str = Form(...),
    staff_id: str = Form(...),
    instrument_id: str = Form(...),
    start_condition: str = Form(...),
    rental_start_date: str = Form(...)
):
    return templates.TemplateResponse(
        request,
        "assign_instrument.html",
        {
            "request": request,
            "message": f"Instrument {instrument_id} assigned to student {stud_id}"
        }
    )

@router.get("/instruments", response_class=HTMLResponse)
def instruments_page(request: Request, query: str = ""):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary = True)

    cursor.execute("select * from Instrument")
    instruments = cursor.fetchall()

    return templates.TemplateResponse(
        request,
        "instruments.html",
        {
            "request": request,
            "instruments": instruments
        }
    )

@router.get("/add-instrument", response_class=HTMLResponse)
def add_instrument_page(request: Request):
    return templates.TemplateResponse(request, "add_instrument.html", {"request": request, "instrument": None})

@router.post("/add-instrument", response_class=HTMLResponse)
def add_instrument_submit(
    request: Request,
    instrument_id: str = Form(...),
    instrument_type: str = Form(...),
    instrument_brand: str = Form(...)
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None

    try:
        cursor.execute(
            "INSERT INTO Instrument (Instrument_ID, Instrument_Type, Instrument_Brand) VALUES (%s, %s, %s)",
            (instrument_id, instrument_type, instrument_brand)
        )
        conn.commit()
        success = True
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    if success:
        return RedirectResponse(url="/instruments", status_code=303)
    
    return templates.TemplateResponse(
        request,
        "add_instrument.html",
        {
            "request": request,
            "message": f"Error adding instrument: {error_message}"
        }
    )

@router.post("/search-instruments", response_class=HTMLResponse)
def search_instruments(
    request: Request, 
    query: str | None = Form(None)
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    if not query:
        try:
            cursor.execute("SELECT * FROM Instrument")
            instruments = cursor.fetchall()
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()
        finally:    
            cursor.close()
            conn.close()
    else:
        try:
            cursor.execute("SELECT * FROM Instrument WHERE Instrument_ID LIKE %s OR Instrument_Type LIKE %s OR Instrument_Brand LIKE %s",
            (f"%{query}%", f"%{query}%", f"%{query}%"))
            instruments = cursor.fetchall()
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        
    if success:
        return templates.TemplateResponse(
            request,
            "instruments.html",
            {"request": request, "instruments": instruments}, #type: ignore
            status_code=200
        )
    return templates.TemplateResponse(
            request,
            "instruments.html",
            status_code=500
    )
    
