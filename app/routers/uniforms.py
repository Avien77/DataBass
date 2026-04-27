from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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
        cursor.execute(
            "SELECT u.*, r.*, IF(sur.Uniform_ID IS NOT NULL, 1, 0) AS Uniform_Status "
            "FROM Uniform u "
            "INNER JOIN Role r ON u.Role_ID = r.Role_ID "
            "LEFT JOIN Student_Uniform_Rentals sur "
            "ON u.Uniform_ID = sur.Uniform_ID AND sur.Unif_Rental_End_Date IS NULL"
        )
        uniforms = cursor.fetchall()

        cursor.execute("SELECT * FROM Role")
        roles = cursor.fetchall()

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
            context={"request": request, "uniforms": uniforms, "roles": roles}, #type: ignore
            status_code=200
        )

    return templates.TemplateResponse(
        request=request,
        name="uniforms.html",
        context={"request": request, "uniforms": [], "error": error_message},
        status_code=500
    )

@router.post("/uniforms", response_class=HTMLResponse)
def search_uniforms(
    request: Request, 
    role_id: int = Form(...),
    chest: float = Form(...),
    arms: float = Form(...),
    hips: float = Form(...),
    waist: float = Form(...),
    inseam: float = Form(...),
    gloves: str = Form(...)
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False

    try:
        query = """
            SELECT u.*, r.*,
              IF(sur.Uniform_ID IS NOT NULL, 1, 0) AS Uniform_Status,
              ABS(Uniform_Chest - %s) +
              ABS(Uniform_Arms - %s) +
              ABS(Uniform_Hips - %s) +
              ABS(Uniform_Waist - %s) +
              ABS(Uniform_Inseam - %s) as difference
            FROM Uniform u
            INNER JOIN Role r ON u.Role_ID = r.Role_ID
            LEFT JOIN Student_Uniform_Rentals sur
              ON u.Uniform_ID = sur.Uniform_ID AND sur.Unif_Rental_End_Date IS NULL
            WHERE u.Role_ID = %s
            ORDER BY difference ASC
        """
        cursor.execute(query, (chest, arms, hips, waist, inseam, role_id))
        uniforms = cursor.fetchall()

        cursor.execute("SELECT * FROM Role")
        roles = cursor.fetchall()

        success = True
    except Exception as e:
        uniforms = []
        roles = []
    finally:
        cursor.close()
        conn.close()
    
    if success:
        return templates.TemplateResponse(
            request=request,
            name="uniforms.html",
            status_code=200,
            context={"request": request, "uniforms": uniforms, "roles": roles, "message": "Successfully queried uniforms."}
        )
    return templates.TemplateResponse(
        request=request,
        name="uniforms.html",
        status_code=500,
        context={"request": request, "uniforms": [], "roles": roles, "message": "An error occurred while searching for uniforms."}
    )

@router.get("/add-uniform", response_class=HTMLResponse)
def add_uniform_page(request: Request):

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Role")
        roles = cursor.fetchall()
    except Exception as e:
        roles = []
    finally:
        cursor.close()
        conn.close()

    return templates.TemplateResponse(
        request=request,
        name="add_uniform.html",
        context={"request": request, "roles": roles}
    )

@router.post("/add-uniform", response_class=HTMLResponse)
def add_uniform(request: Request,
    role_id: int = Form(...),
    chest: float = Form(...),
    arms: float = Form(...),
    hips: float = Form(...),
    waist: float = Form(...),
    inseam: float = Form(...),
    gloves: str = Form(...)
 ):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("""
            insert into Uniform (Role_ID, Uniform_Chest, Uniform_Arms, Uniform_Hips, Uniform_Waist, Uniform_Inseam, Uniform_Gloves)
            values (%s, %s, %s, %s, %s, %s, %s)
        """, (role_id, chest, arms, hips, waist, inseam, gloves))

        conn.commit()
        success = True

    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    if success:
        return RedirectResponse(url="/uniforms", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="add_uniform.html",
        context={"request": request, "error": error_message}
    )

@router.get("/assign-uniform/{uniform_id}", response_class=HTMLResponse)
def assign_uniform_page(request: Request, uniform_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()

        success = True
    except Exception as e:
        error_message = str(e)
        students = []
    finally:
        cursor.close()
        conn.close()
    
    if success:
        return templates.TemplateResponse(
            request=request,
            name="assign_uniform.html",
            context={"request": request, "students": students, "uniform_id": uniform_id}, #type: ignore
            status_code=200
        )
    return templates.TemplateResponse(
            request=request,
            name="assign_uniform.html",
            context={"request": request, "students": [], "uniform_id": uniform_id, "error": error_message},
            status_code=500
    )

@router.post("/assign-uniform/{uniform_id}/{stud_id}", response_class=HTMLResponse)
def assign_uniform(request: Request, uniform_id: str, stud_id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute(
            "SELECT Uniform_ID FROM Student_Uniform_Rentals "
            "WHERE Uniform_ID = %s AND Unif_Rental_End_Date IS NULL",
            (uniform_id,)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return templates.TemplateResponse(
                request=request,
                name="assign_uniform.html",
                context={
                    "request": request,
                    "uniform_id": uniform_id,
                    "students": [],
                    "message": "This uniform is already assigned to a student."
                },
                status_code=409
            )

        cursor.execute("""
            insert into Student_Uniform_Rentals (Uniform_ID, Stud_ID, Unif_Rental_Start_Date)
            values (%s, %s, CURDATE())
        """, (uniform_id, stud_id))

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
        request= request,
        name="assign_uniform.html",
        context={
            "request": request,
            "uniform_id": uniform_id,
            "message": f"Error assigning uniform: {error_message}"
        }
    , status_code=500
    )
