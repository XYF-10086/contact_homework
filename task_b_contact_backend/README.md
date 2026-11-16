# Contact Manager Backend — Task B

本仓库实现通讯录项目的后端、数据存取、多联系方式管理及 Excel 导入导出。

## 1. 技术栈

- Python 3.10+
- FastAPI：REST API
- SQLite：本地持久化数据库
- OpenPyXL：Excel `.xlsx` 导入导出
- Pydantic：请求数据校验

## 2. 启动方式

```bash
# 进入项目目录
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

服务默认地址：`http://127.0.0.1:8000`

交互式接口文档：`http://127.0.0.1:8000/docs`

数据库默认生成在项目根目录 `contacts.db`。可通过环境变量 `DATABASE_PATH` 指定数据库位置。

## 3. 数据结构

### contacts 联系人主表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INTEGER | 主键 |
| name | TEXT | 姓名，必填 |
| notes | TEXT | 备注 |
| is_favorite | INTEGER | 是否收藏，0/1 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### contact_methods 联系方式表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INTEGER | 主键 |
| contact_id | INTEGER | 外键，关联 contacts.id |
| method_type | TEXT | phone/email/social/address |
| value | TEXT | 联系方式内容 |
| label | TEXT | 标签，例如工作、私人 |

一个联系人可以对应多条 contact_methods 记录。删除联系人时，外键级联删除其联系方式，避免孤立数据。

## 4. API 接口

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/contacts` | 联系人列表；支持 `keyword`、`favorite` 筛选 |
| POST | `/api/contacts` | 新增联系人及多条联系方式 |
| GET | `/api/contacts/{id}` | 联系人详情 |
| PUT | `/api/contacts/{id}` | 更新联系人；传入 methods 时整体替换联系方式 |
| DELETE | `/api/contacts/{id}` | 删除联系人 |
| PATCH | `/api/contacts/{id}/favorite?favorite=true` | 设置收藏状态 |
| GET | `/api/export/excel` | 导出全部联系人为 Excel |
| POST | `/api/import/excel` | 上传 `.xlsx` 并导入联系人 |
| GET | `/api/import/template` | 下载 Excel 模板 |

### 新增联系人示例

```json
{
  "name": "张三",
  "notes": "项目合作伙伴",
  "is_favorite": false,
  "methods": [
    {"type": "phone", "value": "13800000000", "label": "工作"},
    {"type": "phone", "value": "13900000000", "label": "私人"},
    {"type": "email", "value": "zhangsan@example.com", "label": "工作"},
    {"type": "social", "value": "微信: zhangsan", "label": "微信"},
    {"type": "address", "value": "福州市", "label": "公司"}
  ]
}
```

联系方式类型仅允许 `phone`、`email`、`social`、`address`。同一类型可以添加多条记录。

## 5. Excel 格式约定

工作表名称为 `Contacts`，首行为表头：

`姓名 | 电话 | 邮箱 | 社交账号 | 地址 | 备注 | 是否收藏`

- 每个联系人占一行。
- 同一类型有多条联系方式时，在单元格中用英文分号 `;` 分隔。
- 收藏状态使用“是/否”，也兼容 `yes/no`、`true/false`、`1/0`。
- 导入时姓名为空的行会跳过。
- 导入接口采用新增策略，不自动覆盖已有联系人。
- 请先下载 `/api/import/template` 获取标准模板。

## 6. 与前端对接

前端通过 JSON 请求 `/api/contacts`。新增/更新联系人时，联系方式放在 `methods` 数组中。收藏筛选可调用：

`GET /api/contacts?favorite=true`

Excel 导入使用 `multipart/form-data`，字段名为 `file`；导出接口返回 `.xlsx` 文件流。

开发阶段 CORS 暂时允许所有来源。正式部署时应将 `allow_origins` 改为前端实际域名。

## 7. 测试

安装依赖后运行：

```bash
pytest -q
```

## 8. Task B 完成范围

- [x] 联系人和联系方式分表存储
- [x] 一个人支持多电话、多邮箱、多社交账号、多地址
- [x] 联系人增删改查
- [x] 收藏状态存储和筛选接口
- [x] Excel 导入
- [x] Excel 导出
- [x] Excel 模板下载
- [x] 自动生成 Swagger API 文档
