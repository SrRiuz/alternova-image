# Python
from http import HTTPStatus

# Fasiapi
from fastapi import HTTPException

# Libs
from core.settings import SHORT_ID_SIZE


def get_object_or_404(model, id):
    """Attempts to retrieve the model by its ID or returns None."""
    if len(id) == SHORT_ID_SIZE:
        obj = model.query().filter((model.is_active == True), model.id.startswith(id)).first()
    else:
        obj = model.query().filter((model.is_active == True), (model.id == id)).first()

    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Object not found")

    return obj
