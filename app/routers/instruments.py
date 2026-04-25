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
def instruments_page(request: Request, query: str = ""):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary = True)

    cursor.execute("select * " \
    "from Instrument i " \
    "inner join Instrument_Types t on i.Instrument_Type = t.Instr_Type_ID ")
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

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("select * from Instrument_Types")
        instrument_types = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    
    return templates.TemplateResponse(request, "add_instrument.html", {"request": request, "instrument": None, "instrument_types": instrument_types})

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
            cursor.execute("select * from " \
            "Instrument i inner join Instrument_Types t on i.Instrument_Type = t.Instr_Type_ID")
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
            cursor.execute("SELECT * FROM " \
            "Instrument i inner join Instrument_Types t on i.Instrument_Type = t.Instr_Type_ID " \
            "WHERE i.Instrument_ID LIKE %s OR t.Instr_Type_Name LIKE %s OR i.Instrument_Brand LIKE %s",
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

@router.get("/edit-instrument/{instrument_id}", response_class=HTMLResponse)
def edit_instrument_page(request: Request, instrument_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Instrument WHERE Instrument_ID = %s", (instrument_id,))
        instrument = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    
    if not instrument:
        return RedirectResponse(url="/instruments", status_code=303)

    return templates.TemplateResponse(request, "add_instrument.html", {"request": request, "instrument": instrument})

@router.post("/edit-instrument", response_class=HTMLResponse)
def edit_instrument_submit(
    request: Request,
    instrument_id: str = Form(...),
    instrument_type: str = Form(...),
    instrument_brand: str = Form(...)
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute(
            "UPDATE Instrument SET Instrument_Type = %s, Instrument_Brand = %s WHERE Instrument_ID = %s",
            (instrument_type, instrument_brand, instrument_id)
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
        "edit_instrument.html",
        {
            "request": request,
            "instrument": {"Instrument_ID": instrument_id, "Instrument_Type": instrument_type, "Instrument_Brand": instrument_brand},
            "message": f"Error updating instrument: {error_message}"
        }
    , status_code=200
    )

@router.get("/delete-instrument/{instrument_id}")
def delete_instrument(instrument_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("DELETE FROM Instrument WHERE Instrument_ID = %s", (instrument_id,))
        conn.commit()
        success = True
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/instruments", status_code=303)


@router.get("/assign-instrument/{instrument_id}", response_class=HTMLResponse)
def assign_instrument_page(request: Request, instrument_id: str):

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("select * from Student")
        students = cursor.fetchall()
        success = True
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
            "students": students if success else [], #type: ignore
            "instrument_id": instrument_id,
            "message": f"Error loading students: {error_message}" if not success else None,
        }
    )


@router.post("/assign-instrument/{instrument_id}/{stud_id}", response_class=HTMLResponse)
def assign_instrument_submit(
    request: Request,
    instrument_id: str,
    stud_id: str,
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None

    try:
        cursor.execute(
            "insert into Student_Instrument_Rentals (Stud_ID, Instrument_ID, Instr_Rental_Start_Date) " \
            "values (%s, %s, CURDATE())",
            (stud_id, instrument_id)
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
        return RedirectResponse(url="/rental", status_code=303)

    return templates.TemplateResponse(
        request,
        "assign_instrument.html",
        {
            "request": request,
            "message": f"Error assigning instrument: {error_message}"
        }
    )