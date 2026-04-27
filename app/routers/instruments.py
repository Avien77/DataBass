from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/instruments", response_class=HTMLResponse)
def instruments_page(request: Request):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT i.*, t.*, IF(sir.Instrument_ID IS NOT NULL, 1, 0) AS Instrument_Status "
            "FROM Instrument i "
            "INNER JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID "
            "LEFT JOIN Student_Instrument_Rentals sir "
            "ON i.Instrument_ID = sir.Instrument_ID AND sir.Instr_Rental_End_Date IS NULL"
        )
        instruments = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "instruments.html",
        {"request": request, "instruments": instruments}
    )

@router.get("/add-instrument", response_class=HTMLResponse)
def add_instrument_page(request: Request):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Instrument_Types")
        instrument_types = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(request, "add_instrument.html", {
        "request": request,
        "instrument": None,
        "instrument_types": instrument_types
    })

@router.post("/add-instrument", response_class=HTMLResponse)
def add_instrument_submit(
    request: Request,
    instrument_type: str = Form(...),
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    error_message = None

    try:
        cursor.execute(
            "INSERT INTO Instrument (Instrument_Type) VALUES (%s)",
            (instrument_type,)
        )
        conn.commit()
        return RedirectResponse(url="/instruments", status_code=303)
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    # re-fetch instrument types for the form on error
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Instrument_Types")
        instrument_types = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "add_instrument.html",
        {
            "request": request,
            "instrument": None,
            "instrument_types": instrument_types,
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

    error_message = None

    try:
        base = (
            "SELECT i.*, t.*, IF(sir.Instrument_ID IS NOT NULL, 1, 0) AS Instrument_Status "
            "FROM Instrument i "
            "INNER JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID "
            "LEFT JOIN Student_Instrument_Rentals sir "
            "ON i.Instrument_ID = sir.Instrument_ID AND sir.Instr_Rental_End_Date IS NULL"
        )
        if not query:
            cursor.execute(base)
        else:
            cursor.execute(
                base + " WHERE CAST(i.Instrument_ID AS CHAR) LIKE %s OR t.Instr_Type_Name LIKE %s",
                (f"%{query}%", f"%{query}%")
            )
        instruments = cursor.fetchall()
    except Exception as e:
        error_message = str(e)
        instruments = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "instruments.html",
        {
            "request": request,
            "instruments": instruments,
            "message": f"Search error: {error_message}" if error_message else None
        },
        status_code=500 if error_message else 200
    )

@router.get("/edit-instrument/{instrument_id}", response_class=HTMLResponse)
def edit_instrument_page(request: Request, instrument_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Instrument WHERE Instrument_ID = %s", (instrument_id,))
        instrument = cursor.fetchone()

        cursor.execute("SELECT * FROM Instrument_Types")
        instrument_types = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    if not instrument:
        return RedirectResponse(url="/instruments", status_code=303)

    return templates.TemplateResponse(request, "add_instrument.html", {
        "request": request,
        "instrument": instrument,
        "instrument_types": instrument_types
    })

@router.post("/edit-instrument", response_class=HTMLResponse)
def edit_instrument_submit(
    request: Request,
    instrument_id: str = Form(...),
    instrument_type: str = Form(...),
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    error_message = None

    try:
        cursor.execute(
            "UPDATE Instrument SET Instrument_Type = %s WHERE Instrument_ID = %s",
            (instrument_type, instrument_id)
        )
        conn.commit()
        return RedirectResponse(url="/instruments", status_code=303)
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    # re-fetch instrument types for the form on error
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Instrument_Types")
        instrument_types = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "add_instrument.html",
        {
            "request": request,
            "instrument": {"Instrument_ID": instrument_id, "Instrument_Type": instrument_type},
            "instrument_types": instrument_types,
            "message": f"Error updating instrument: {error_message}"
        }
    )

@router.get("/delete-instrument/{instrument_id}")
def delete_instrument(instrument_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Instrument WHERE Instrument_ID = %s", (instrument_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/instruments", status_code=303)

@router.get("/assign-instrument/{instrument_id}", response_class=HTMLResponse)
def assign_instrument_page(request: Request, instrument_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    error_message = None

    try:
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()
    except Exception as e:
        error_message = str(e)
        students = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "assign_instrument.html",
        {
            "request": request,
            "students": students,
            "instrument_id": instrument_id,
            "message": f"Error loading students: {error_message}" if error_message else None,
        }
    )

@router.post("/assign-instrument/{instrument_id}/{stud_id}", response_class=HTMLResponse)
def assign_instrument_submit(
    request: Request,
    instrument_id: str,
    stud_id: str,
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    error_message = None

    try:

        cursor.execute(
            "SELECT * FROM Student_Instrument_Rentals "
            "WHERE Instrument_ID = %s AND Instr_Rental_End_Date IS NULL",
            (instrument_id,)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            conn.close()
            conn = db.get_db_conn()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Student")
            students = cursor.fetchall()
            return templates.TemplateResponse(
                request,
                "assign_instrument.html",
                {
                    "request": request,
                    "students": students,
                    "instrument_id": instrument_id,
                    "message": "This instrument is already assigned to a student."
                }
            )

        cursor.execute(
            "INSERT INTO Student_Instrument_Rentals "
            "(Stud_ID, Instrument_ID, Instr_Rental_Start_Date) "
            "VALUES (%s, %s, CURDATE())",
            (stud_id, instrument_id)
        )
        conn.commit()
        return RedirectResponse(url="/rental", status_code=303)

    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "assign_instrument.html",
        {
            "request": request,
            "students": [],
            "instrument_id": instrument_id,
            "message": f"Error assigning instrument: {error_message}"
        }
    )

@router.get("/create-instrument", response_class=HTMLResponse)
def create_instrument_page(request: Request):
    
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Instrument_Types")
        instrument_types = cursor.fetchall()
    except Exception as e:
        instrument_types = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "create_instrument.html",
        {
            "request": request,
            "instrument_types": instrument_types
        }
    )

@router.post("/create-instrument", response_class=HTMLResponse)
def create_instrument_submit(
    request: Request, 
    instrument_name: str = Form(...)
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Instrument_Types (Instr_Type_Name) VALUES (%s)", (instrument_name,))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/create-instrument", status_code=303)
