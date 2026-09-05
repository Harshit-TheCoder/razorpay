import os

target_files = [
    "app/analytics/controller.py",
    "app/subscriptions/controller.py",
    "app/recovery/controller.py",
    "app/payments/controller.py",
    "app/checkout/controller.py",
    "app/recovery/models.py",
    "app/checkout/models.py",
    "app/payments/models.py",
    "app/subscriptions/models.py",
    "app/events/models.py",
    "app/core/db/postgres/base_models.py"
]

for file_path in target_files:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
        
        # Replace get_db_session
        content = content.replace("from app.core.db.postgres.engine import get_db_session", "from app.core.db.session import get_db_session")
        # Replace Base
        content = content.replace("from app.core.db.postgres.engine import Base", "from app.core.db.session import Base")
        
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Refactored {file_path}")
    else:
        print(f"File not found: {file_path}")
