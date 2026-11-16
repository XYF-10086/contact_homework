from .database import get_connection

def _serialize_contact(conn, row):
    methods = conn.execute(
        "SELECT id, method_type, value, label FROM contact_methods "
        "WHERE contact_id = ? ORDER BY id", (row["id"],)
    ).fetchall()
    return {
        "id": row["id"],
        "name": row["name"],
        "notes": row["notes"],
        "is_favorite": bool(row["is_favorite"]),
        "methods": [
            {"id": m["id"], "type": m["method_type"],
             "value": m["value"], "label": m["label"]}
            for m in methods
        ],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }

def get_contact(conn, contact_id):
    row = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    return _serialize_contact(conn, row) if row else None

def list_contacts(keyword=None, favorite=None):
    with get_connection() as conn:
        sql = "SELECT * FROM contacts WHERE 1=1"
        params = []
        if keyword:
            sql += " AND (name LIKE ? OR notes LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        if favorite is not None:
            sql += " AND is_favorite = ?"
            params.append(1 if favorite else 0)
        sql += " ORDER BY name COLLATE NOCASE, id"
        rows = conn.execute(sql, params).fetchall()
        return [_serialize_contact(conn, row) for row in rows]

def create_contact(data):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO contacts(name, notes, is_favorite) VALUES (?, ?, ?)",
            (data.name.strip(), data.notes, int(data.is_favorite))
        )
        contact_id = cursor.lastrowid
        for method in data.methods:
            conn.execute(
                "INSERT INTO contact_methods(contact_id, method_type, value, label) "
                "VALUES (?, ?, ?, ?)",
                (contact_id, method.type, method.value.strip(), method.label)
            )
        conn.commit()
        return get_contact(conn, contact_id)

def update_contact(contact_id, data):
    with get_connection() as conn:
        existing = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
        if not existing:
            return None
        name = data.name.strip() if data.name is not None else existing["name"]
        notes = data.notes if data.notes is not None else existing["notes"]
        favorite = int(data.is_favorite) if data.is_favorite is not None else existing["is_favorite"]
        conn.execute(
            "UPDATE contacts SET name=?, notes=?, is_favorite=?, updated_at=CURRENT_TIMESTAMP "
            "WHERE id=?", (name, notes, favorite, contact_id)
        )
        if data.methods is not None:
            conn.execute("DELETE FROM contact_methods WHERE contact_id=?", (contact_id,))
            for method in data.methods:
                conn.execute(
                    "INSERT INTO contact_methods(contact_id, method_type, value, label) "
                    "VALUES (?, ?, ?, ?)",
                    (contact_id, method.type, method.value.strip(), method.label)
                )
        conn.commit()
        return get_contact(conn, contact_id)

def delete_contact(contact_id):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        return cursor.rowcount > 0

def set_favorite(contact_id, favorite):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE contacts SET is_favorite=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (int(favorite), contact_id)
        )
        conn.commit()
        return get_contact(conn, contact_id) if cursor.rowcount else None
