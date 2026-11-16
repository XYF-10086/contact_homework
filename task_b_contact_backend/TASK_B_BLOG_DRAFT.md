# Extreme Programming 通讯录项目——Task B 后端与数据管理实现

## 作业基本信息

| 项目 | 内容 |
|---|---|
| 课程 | Software Engineering (FZU–MU) |
| 作业要求 | https://bbs.csdn.net/topics/620593436 |
| 本人分工 | Task B：后端、数据结构、数据存取、Excel 导入导出、多联系方式存储 |
| 作业目标 | 为通讯录前端提供可持久化的数据服务，并支持一个联系人维护多条联系方式及 Excel 数据交换 |

## 一、任务范围

根据团队分工，Task A 负责前端、UI 和收藏交互；Task B 负责后端、数据、Excel 导入导出和多联系方式存储。本部分聚焦 Task B，并提供收藏状态的后端存储和查询接口，供前端调用。

## 二、技术选型

- Python：后端开发语言。
- FastAPI：构建 REST API，并自动生成 Swagger 文档。
- SQLite：保存联系人和联系方式。
- OpenPyXL：读取和生成 Excel `.xlsx` 文件。
- Pydantic：校验前端传入的数据结构。

## 三、数据库设计

采用一对多关系，将联系人基本信息和联系方式分开保存。

### 3.1 contacts 联系人表

| 字段 | 含义 |
|---|---|
| id | 联系人主键 |
| name | 姓名 |
| notes | 备注 |
| is_favorite | 收藏状态 |
| created_at / updated_at | 创建及更新时间 |

### 3.2 contact_methods 联系方式表

| 字段 | 含义 |
|---|---|
| id | 联系方式主键 |
| contact_id | 联系人外键 |
| method_type | 类型：phone、email、social、address |
| value | 联系方式内容 |
| label | 标签，例如工作、私人 |

一个联系人可以关联多条联系方式，包括多个电话、邮箱、社交账号和地址。联系人删除时，数据库通过外键级联删除其联系方式，避免产生孤立记录。

## 四、后端接口

| HTTP 方法 | API | 功能 |
|---|---|---|
| GET | `/api/contacts` | 获取联系人列表，支持关键词和收藏状态筛选 |
| POST | `/api/contacts` | 新增联系人及多条联系方式 |
| GET | `/api/contacts/{id}` | 获取联系人详情 |
| PUT | `/api/contacts/{id}` | 更新联系人信息及联系方式 |
| DELETE | `/api/contacts/{id}` | 删除联系人 |
| PATCH | `/api/contacts/{id}/favorite?favorite=true` | 更新收藏状态 |
| GET | `/api/export/excel` | 导出联系人 Excel |
| POST | `/api/import/excel` | 导入 `.xlsx` 联系人 |
| GET | `/api/import/template` | 下载 Excel 模板 |

新增联系人时，前端传入 `methods` 数组。每一项包含 `type`、`value` 和 `label`，因此同一联系人可以保存多条相同类型的联系方式。

## 五、Excel 导入导出设计

Excel 使用 `Contacts` 工作表，列为：姓名、电话、邮箱、社交账号、地址、备注、是否收藏。每个联系人占一行；同一类别有多个值时，使用英文分号分隔。导出时将数据库中的多条联系方式按类型聚合到对应单元格；导入时再按分隔符拆分并写入联系方式表。

导入采用新增策略，不会自动覆盖已有联系人；姓名为空的行会跳过。导入前可通过 `/api/import/template` 下载标准模板。

## 六、运行与测试

在项目目录执行：

```bash
python -m venv .venv
.venv\\Scripts\\activate        # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

浏览器访问 `http://127.0.0.1:8000/docs` 可查看和调试接口。

当前开发环境已完成以下验证：

- Python 文件编译检查通过。
- 自动化测试：`pytest -q`，1 项测试通过。
- API 冒烟测试：联系人新增、Excel 导出、模板下载、Excel 导入均返回成功。

> 发布博客前，请替换为你自己运行时的截图和录屏，并保留真实测试结果。不要将本地测试截图描述为云端部署结果。

## 七、与队友 A 的接口约定

前端新增/更新联系人时，联系方式统一放入 `methods` 数组；列表页可调用 `GET /api/contacts`；收藏页可调用 `GET /api/contacts?favorite=true`。Excel 导入通过 `multipart/form-data` 上传字段 `file`，导出直接访问 `/api/export/excel` 下载文件。

开发阶段 CORS 允许跨域请求。正式部署时应将后端 `allow_origins` 改为前端实际域名，并统一双方约定的 API 基础地址。

## 八、个人 PSP 表

| 阶段 | 计划用时 | 实际用时 | 备注 |
|---|---:|---:|---|
| 需求分析与接口设计 | 待本人填写 | 待本人填写 | 明确 Task B 范围 |
| 数据库设计与实现 | 待本人填写 | 待本人填写 | 联系人及联系方式一对多 |
| REST API 开发 | 待本人填写 | 待本人填写 | CRUD 与收藏状态 |
| Excel 导入导出 | 待本人填写 | 待本人填写 | 模板、导入、导出 |
| 测试与调试 | 待本人填写 | 待本人填写 | 自动化测试及接口测试 |
| 文档与提交 | 待本人填写 | 待本人填写 | README、博客、Git 提交 |

## 九、提交前需要补充的真实材料

1. GitHub 仓库地址及至少 3 次真实 commit 记录截图。
2. Swagger 页面截图、联系人多联系方式请求/响应截图。
3. Excel 导入前后数据截图和导出文件截图。
4. 完整运行视频。
5. 团队成员贡献比例（总计 100%）及协作问题记录。
6. 本人的实际 PSP 用时。

## 十、总结

Task B 已实现联系人及多联系方式的数据模型、联系人数据 API、收藏状态存储、Excel 模板下载、导入和导出。该后端可独立启动，并通过 Swagger 页面供前端联调。最终集成时仍需与 Task A 确认前端 API 地址、字段命名和部署域名。
