from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# 1. 모듈 및 환경 설정
app = FastAPI()

# `toyproject_fastapis_01` 디렉토리를 템플릿 폴더로 설정합니다.
templates = Jinja2Templates(directory="toyproject_fastapis_01")

# CSS나 Images 같은 정적 파일 마운트 코드는 제외합니다.


# 2. 라우트(Route) 구현
@app.get("/")
async def get_main_page(request: Request):
    """
    루트 URL (/)에 대한 요청을 처리하고 main.html 템플릿을 렌더링합니다.
    """
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/style/no")
async def get_stylesheet_no(request: Request):
    """
    URL (/style/no)에 대한 요청을 처리하고 stylesheetNo.html 템플릿을 렌더링합니다.
    """
    return templates.TemplateResponse("stylesheetNo.html", {"request": request})


@app.get("/style/{num}")
async def get_stylesheet_by_num(request: Request, num: int):
    """
    동적 URL (/style/{num})에 대한 요청을 처리하고
    숫자에 해당하는 stylesheet{num}.html 템플릿을 렌더링합니다.
    num은 1, 2, 3, 4 중 하나여야 합니다.
    """
    # 파일명이 stylesheet01.html 형식이므로 숫자를 두 자리로 포맷팅합니다.
    template_name = f"stylesheet{num:02d}.html"
    return templates.TemplateResponse(template_name, {"request": request, "num": num})

