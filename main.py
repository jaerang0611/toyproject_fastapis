
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional

from toyproject_fastapis_02 import crud, schemas

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# API Endpoints
@app.post("/api/notices/", response_model=schemas.Notice, status_code=201)
def create_notice_api(notice: schemas.NoticeCreate):
    return crud.create_notice(notice=notice)

@app.get("/api/notices/", response_model=List[schemas.Notice])
def read_notices_api(skip: int = 0, limit: int = 100):
    notices = crud.get_notices(skip=skip, limit=limit)
    return notices

@app.get("/api/notices/{notice_id}", response_model=schemas.Notice)
def read_notice_api(notice_id: int):
    db_notice = crud.get_notice(notice_id=notice_id)
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return db_notice

@app.put("/api/notices/{notice_id}", response_model=schemas.Notice)
def update_notice_api(notice_id: int, notice_update: schemas.NoticeUpdate):
    updated_notice, message = crud.update_notice(notice_id=notice_id, notice_update=notice_update)
    if not updated_notice:
        if message == "Notice not found":
            raise HTTPException(status_code=404, detail=message)
        else:
            raise HTTPException(status_code=401, detail=message)
    return updated_notice

@app.delete("/api/notices/{notice_id}", status_code=204)
def delete_notice_api(notice_id: int, nickname: str, password: str):
    success, message = crud.delete_notice(notice_id=notice_id, nickname=nickname, password=password)
    if not success:
        if message == "Notice not found":
            raise HTTPException(status_code=404, detail=message)
        else:
            raise HTTPException(status_code=401, detail=message)
    return {}

# Web Interface
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    notices = crud.get_notices()
    return templates.TemplateResponse("index.html", {"request": request, "notices": notices})

@app.get("/notices/{notice_id}", response_class=HTMLResponse)
def read_notice_web(request: Request, notice_id: int):
    notice = crud.get_notice(notice_id=notice_id)
    if notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return templates.TemplateResponse("notice_detail.html", {"request": request, "notice": notice})

@app.get("/new", response_class=HTMLResponse)
def new_notice_form(request: Request):
    return templates.TemplateResponse("new_notice.html", {"request": request})

@app.post("/new", response_class=RedirectResponse)
def create_notice_web(
    title: str = Form(...),
    content: str = Form(...),
    nickname: str = Form(...),
    password: str = Form(...)
):
    notice_data = schemas.NoticeCreate(title=title, content=content, nickname=nickname, password=password)
    crud.create_notice(notice=notice_data)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
