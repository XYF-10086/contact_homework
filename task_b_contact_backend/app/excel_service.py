from io import BytesIO
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from .database import get_connection
from .contact_service import create_contact
from .schemas import ContactCreate, ContactMethodIn

HEADERS = ["姓名", "电话", "邮箱", "社交账号", "地址", "备注", "是否收藏"]
METHOD_COLUMNS = {
    "phone": "电话",
    "email": "邮箱",
    "social": "社交账号",
    "address": "地址",
}

def _split_values(value):
    if value is None:
        return []
    # Excel 模板中多个同类联系方式使用英文分号或换行分隔
    return [part.strip() for part in str(value).replace("\n", ";").split(";") if part.strip()]

def export_contacts_xlsx():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM contacts ORDER BY id").fetchall()
        wb = Workbook()
        ws = wb.active
        ws.title = "Contacts"
        ws.append(HEADERS)
        for row in rows:
            methods = conn.execute(
                "SELECT method_type, value FROM contact_methods WHERE contact_id=? ORDER BY id",
                (row["id"],)
            ).fetchall()
            grouped = {kind: [] for kind in METHOD_COLUMNS}
            for method in methods:
                grouped[method["method_type"]].append(method["value"])
            ws.append([
                row["name"],
                "; ".join(grouped["phone"]),
                "; ".join(grouped["email"]),
                "; ".join(grouped["social"]),
                "; ".join(grouped["address"]),
                row["notes"],
                "是" if row["is_favorite"] else "否",
            ])
        _style_sheet(ws)
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

def _style_sheet(ws):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="315B83")
        cell.alignment = Alignment(horizontal="center")
    widths = [20, 28, 28, 28, 35, 35, 14]
    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

def import_contacts_xlsx(file_bytes):
    wb = load_workbook(BytesIO(file_bytes), read_only=True, data_only=True)
    ws = wb["Contacts"] if "Contacts" in wb.sheetnames else wb.active
    headers = [str(c).strip() if c is not None else "" for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    required = {"姓名", "电话", "邮箱", "社交账号", "地址", "备注", "是否收藏"}
    if not required.issubset(set(headers)):
        missing = sorted(required - set(headers))
        raise ValueError("Excel 缺少必要列：" + "、".join(missing))
    index = {name: headers.index(name) for name in required}
    imported = 0
    skipped = 0
    for values in ws.iter_rows(min_row=2, values_only=True):
        def cell(column):
            i = index[column]
            return values[i] if i < len(values) else None
        name = str(cell("姓名") or "").strip()
        if not name:
            skipped += 1
            continue
        methods = []
        for kind, column in METHOD_COLUMNS.items():
            for value in _split_values(cell(column)):
                methods.append(ContactMethodIn(type=kind, value=value))
        favorite_value = str(cell("是否收藏") or "").strip().lower()
        favorite = favorite_value in {"是", "yes", "true", "1", "y"}
        data = ContactCreate(
            name=name,
            notes=str(cell("备注") or ""),
            is_favorite=favorite,
            methods=methods,
        )
        create_contact(data)
        imported += 1
    wb.close()
    return {"imported": imported, "skipped": skipped}
