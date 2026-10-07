For the first working version, SQLAlchemy create_all() creates the tables.

For production:
1. install alembic
2. alembic init migrations
3. create revisions
4. run alembic upgrade head
5. remove Base.metadata.create_all() from app/main.py
