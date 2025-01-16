def setUp():
    """It is responsible for initializing the database."""
    from core.db.connection import engine
    from core.db.models import Model

    if engine:
        Model.metadata.create_all(bind=engine)
        return engine
