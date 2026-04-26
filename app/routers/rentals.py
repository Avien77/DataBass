from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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

    try:
        # Fetch instrument Rentals
        query = "SELECT * " \
        "FROM Student_Instrument_Rentals r " \
        "join Student s on r.Stud_ID = s.Stud_ID " \
        "join Instrument i on r.Instrument_ID = i.Instrument_ID " \
        "join Instrument_Types t on i.Instrument_Type = t.Instr_Type_ID" 
        cursor.execute(query)
        instrument_rentals = cursor.fetchall()

        #Fetch uniform rentals
        query = "SELECT * " \
        "FROM Student_Uniform_Rentals r " \
        "join Student s on r.Stud_ID = s.Stud_ID " \
        "join Uniform u on r.Uniform_ID = u.Uniform_ID " \
        "join Role ro on u.Role_ID = ro.Role_ID"
        cursor.execute(query)
        uniform_rentals = cursor.fetchall()

    except Exception as e:
        print(f"Error fetching instrument rentals: {e}")
        instrument_rentals = []
        uniform_rentals = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request, 
        "rental.html", 
        {"request": request, "instrument_rentals": instrument_rentals, "uniform_rentals": uniform_rentals}
    )


@router.post("/rental", response_class=HTMLResponse)
def rental_lookup(request: Request, stud_id: str = Form(...)):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM Student_Instrument_Rentals r "
            "JOIN Student s ON r.Stud_ID = s.Stud_ID "
            "JOIN Instrument i ON r.Instrument_ID = i.Instrument_ID "
            "JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID "
            "WHERE r.Stud_ID = %s",
            (stud_id,)
        )
        instrument_rentals = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching rentals: {e}")
        instrument_rentals = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request,
        "rental.html",
        {"request": request, "instrument_rentals": instrument_rentals}
    )


@router.get("/return-instrument/{instrument_id}")
def return_instrument(instrument_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE Student_Instrument_Rentals "
            "SET Instr_Rental_End_Date = CURDATE() "
            "WHERE Instrument_ID = %s AND Instr_Rental_End_Date IS NULL",
            (instrument_id,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error returning instrument: {e}")
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/rental", status_code=303)