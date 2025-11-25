## ✨ Vibe 코딩 프롬프트 (Markdown 형식)

### **요청 내용**

다음 요구 사항을 모두 만족하는 **전체 FastAPI Python 코드**를 작성해 주세요.

### **1. 모듈 및 환경 설정**

* `FastAPI`, `Request`, `Jinja2Templates` 모듈을 import해야 합니다.
* `Jinja2Templates`의 템플릿 디렉토리는 **`toyproject_fastapis_01`** 폴더로 설정해야 합니다.
* **CSS나 Images 같은 정적 파일 마운트 코드는 모두 제외**해야 합니다.

### **2. 라우트(Route) 구현**

모든 라우트 함수는 **`request: Request`** 객체를 받아 템플릿 렌더링 시 전달해야 합니다.

| URL 경로 | 렌더링할 HTML 파일 | 비고 |
| :--- | :--- | :--- |
| **`/`** | `main.html` | 기본 페이지 |
| **`/style/{num}`** | `stylesheet{num}.html` | `num`은 **1, 2, 3, 4** 중 하나여야 합니다. |
| **`/style/no`** | `stylesheetNo.html` | 'No' 스타일시트 페이지 |

### **3. 최종 출력 형식**

* 위의 모든 요구 사항을 반영한 **완성된 하나의 Python 파일 코드**를 제시해 주십시오.