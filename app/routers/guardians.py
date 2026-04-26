from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/guardians", response_class=HTMLResponse)
def guardian_page(request: Request):

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("SELECT * FROM Guardian")
        guardians = cursor.fetchall()
        success = True
        print(guardians)
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    if success:
        return templates.TemplateResponse(
            request=request,
            name="guardians.html",
            context={"guardians": guardians}, #type: ignore
            status_code=200
        )
    return templates.TemplateResponse(
        request=request,
        name="guardians.html",
        status_code=500
    )

@router.post("/search-guardians")
def search_guardian(
    request: Request,
    guard_fname: str | None = Form(None)
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    # default, fetch all
    if not guard_fname:
        try:
            cursor.execute("SELECT * FROM Guardian")
            guardians = cursor.fetchall()
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        try:
            cursor.execute("SELECT * FROM Guardian WHERE Guardian_FName LIKE %s", (f"%{guard_fname}%",))
            guardians = cursor.fetchall()
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
            "guardians.html",
            {"guardians": guardians}, # type: ignore
            status_code=200
        )
    return templates.TemplateResponse(
            request,
            "guardians.html",
            status_code=500
    )

@router.get("/add-guardian", response_class=HTMLResponse)
def add_guardian_page(request: Request):
    return templates.TemplateResponse(request, "add_guardian.html")

@router.post("/add-guardian", response_class=HTMLResponse)
def add_guardian_submit(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
):
    
    conn = db.get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None

    try:
        cursor.execute("INSERT INTO Guardian (Guardian_FName, Guardian_LName, Guardian_Phone) VALUES" \
        "(%s, %s, %s)",
        (first_name, last_name, phone))
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        error_message = str(e)
        print(f"Transaction Failed: {e}")
    finally:
        cursor.close()
        conn.close()

    if success:
        return RedirectResponse(url="/guardians", status_code=303)
    return templates.TemplateResponse(
        request,
        "add_guardian.html",
        status_code=500
    )

@router.get("/edit-guardian/{id}", response_class=HTMLResponse)
def edit_student_page(request: Request, id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Guardian WHERE Guardian_ID = %s", (id,))
        guardian = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not guardian:
        return RedirectResponse(url="/guardians", status_code=303)

    return templates.TemplateResponse(request, "add_guardian.html", {"guardian": guardian})


@router.post("/edit-guardian/{guard_id}")
def edit_guardian_submit(
    request: Request,
    guard_id: str,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None

    try:
        cursor.execute(
            "UPDATE Guardian SET Guardian_FName=%s, Guardian_LName=%s, Guardian_Phone=%s WHERE Guardian_ID=%s",
            (first_name, last_name, phone, guard_id)
        )
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        error_message = str(e)
        print(f"Transaction Failed: {e}")
    finally:
        cursor.close()
        conn.close()

    if success:
        return RedirectResponse(url="/guardians", status_code=303)
    return templates.TemplateResponse(
        request,
        "guardian.html",
        {"guardian": {"Guardian_ID": guard_id}, "message": f"Failed to update guardian: {error_message}"},
        status_code=500
    )


@router.get("/delete-guardian/{id}")
def delete_guardian(request: Request, id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = ""

    try:
        cursor.execute("DELETE from Guardian WHERE Guardian_ID = %s", (id,))
        conn.commit()
        success = True
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/guardians", status_code=303)

@router.get("/link-guardian", response_class=HTMLResponse)
def link_guardian_page(request: Request, message: str | None = None):

    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()

        cursor.execute("SELECT * FROM Guardian")
        guardians = cursor.fetchall()

        return templates.TemplateResponse(
            request=request,
            name="link_guardian.html",
            context={"guardians": guardians, "students": students, "message": message},
            status_code=200
        )
    except Exception as e:
        conn.rollback()
        return templates.TemplateResponse(
            request=request,
            name="link_guardian.html",
            status_code=500
        )
    finally:
        cursor.close()
        conn.close()

@router.post("/link-guardian", response_class=HTMLResponse)
def link_guardian_submit(
    request: Request,
    stud_id: str = Form(...),
    guard_id: str = Form(...)
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("insert into Student_Guardian (Stud_ID, Guardian_ID) VALUES " \
        "(%s, %s)",
        (stud_id, guard_id))   
        conn.commit()
        success=True
    except Exception as e:
        error_message = str(e)
    finally:
        cursor.close()
        conn.close()
    
    if success:
        return link_guardian_page(request, message=f"Guardian {guard_id} linked to student {stud_id}")
    return link_guardian_page(request, message="Failed to link Guardian to Student")
        

