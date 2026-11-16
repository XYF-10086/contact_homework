# API Quick Examples

## Create
`POST /api/contacts`

```json
{
  "name": "Li Lei",
  "notes": "Classmate",
  "is_favorite": true,
  "methods": [
    {"type": "phone", "value": "13800000000", "label": "mobile"},
    {"type": "email", "value": "li@example.com", "label": "school"},
    {"type": "social", "value": "@lilei", "label": "Weibo"},
    {"type": "address", "value": "Fuzhou", "label": "home"}
  ]
}
```

## List
`GET /api/contacts?keyword=Li&favorite=true`

## Export
`GET /api/export/excel`

## Import
`POST /api/import/excel`, multipart field name: `file`.
