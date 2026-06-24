from app.database import SessionLocal
from app.models.user import User
from app.security.auth import hash_password
db = SessionLocal()


users = [
    {
        "full_name": "Admin",
        "email": "admin@sysguardian.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "full_name": "Technician",
        "email": "tech@sysguardian.com",
        "password": "tech123",
        "role": "technician"
    },
    {
        "full_name": "Viewer",
        "email": "viewer@sysguardian.com",
        "password": "viewer123",
        "role": "viewer"
    }
]

for user_data in users:

    existing_user = (
        db.query(User)
        .filter(User.email == user_data["email"])
        .first()
    )

    if existing_user:
        print(f'{user_data["email"]} already exists')
        continue

    user = User(
        full_name=user_data["full_name"],
        email=user_data["email"],
        hashed_password=hash_password(user_data["password"]),
        role=user_data["role"],
        is_active=True
    )

    db.add(user)

db.commit()
db.close()

print("Seed completed successfully")