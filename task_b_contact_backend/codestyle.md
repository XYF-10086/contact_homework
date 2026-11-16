# Code Style

- Use Python 3.10+ type hints where practical.
- Use `snake_case` for variables and functions.
- Use `PascalCase` for Pydantic models.
- Keep HTTP routing in `app/main.py`, database setup in `app/database.py`, business logic in `app/contact_service.py`, and spreadsheet logic in `app/excel_service.py`.
- Validate external input with Pydantic.
- Use parameterized SQL statements; never concatenate user input into SQL.
- Keep database writes inside transaction contexts.
- Use clear HTTP status codes and error messages.
