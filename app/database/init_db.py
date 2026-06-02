from app.database.base import Base
from app.database.session import engine

from app.models.event import Event

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")