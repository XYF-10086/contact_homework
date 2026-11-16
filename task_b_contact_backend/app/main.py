from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .database import init_db
from .schemas import ContactCreate, ContactUpdate
from .contact_service import (
    list_contacts, create_contact, get_contact, update_contact,
    delete_contact, set_favorite
)
from .excel_service import export_contacts_xlsx, import_contacts_xlsx

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Contact Manager API",
    description="Backend API for contacts, multiple contact methods, favorites and Excel import/export.",
    version="1.0.0",
    lifespan=lifespan,
)

# For local development. In production, replace "*" with the deployed frontend origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Contact Manager API"}

@app.get("/api/contacts")
def api_list_contacts(
    keyword: str | None = Query(default=None),
    favorite: bool | None = Query(default=None),
):
    return list_contacts(keyword=keyword, favorite=favorite)

@app.post("/api/contacts", status_code=201)
def api_create_contact(data: ContactCreate):
    if not data.name.strip():
        raise HTTPException(status_code=422, detail="联系人姓名不能为空")
    return create_contact(data)

@app.get("/api/contacts/{contact_id}")
def api_get_contact(contact_id: int):
    contact = get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return contact

def get_contact_by_id(contact_id):
    from .database import get_connection
    with get_connection() as conn:
        return get_contact(conn, contact_id)

@app.put("/api/contacts/{contact_id}")
def api_update_contact(contact_id: int, data: ContactUpdate):
    contact = update_contact(contact_id, data)
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return contact

@app.delete("/api/contacts/{contact_id}")
def api_delete_contact(contact_id: int):
    if not delete_contact(contact_id):
        raise HTTPException(status_code=404, detail="联系人不存在")
    return {"message": "联系人已删除"}

@app.patch("/api/contacts/{contact_id}/favorite")
def api_set_favorite(contact_id: int, favorite: bool = Query(...)):
    contact = set_favorite(contact_id, favorite)
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return contact

@app.get("/api/export/excel")
def api_export_excel():
    output = export_contacts_xlsx()
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="contacts.xlsx"'},
    )

@app.post("/api/import/excel")
async def api_import_excel(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="请上传 .xlsx 格式文件")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="上传文件为空")
    try:
        return import_contacts_xlsx(content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Excel 文件解析失败：{exc}")

@app.get("/api/import/template")
def api_excel_template():
    from openpyxl import Workbook
    from io import BytesIO
    from .excel_service import HEADERS
    wb = Workbook()
    ws = wb.active
    ws.title = "Contacts"
    ws.append(HEADERS)
    ws.append(["张三", "13800000000; 13900000000", "zhangsan@example.com", "微信: zhangsan", "福州市", "示例联系人", "否"])
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="contacts_template.xlsx"'},
    )
