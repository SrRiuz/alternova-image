# Python
from typing import Optional

# Libs
from sqlalchemy.orm.query import Query
from pydantic._internal._model_construction import ModelMetaclass

# Settings
from core.settings import PAGINATION


class Pagination:

    def __init__(
        self,
        queryset: Query,
        schema: ModelMetaclass,
        page: int,
        page_limit: int = PAGINATION.get("PAGE_LIMIT", 10),
    ) -> None:
        self.current_page: int = page
        self.schema: ModelMetaclass = schema
        self.page_limit: int = page_limit
        self.offset: int = page_limit * page
        self.queryset: Query = queryset
        self.total_count = queryset.count()
        self.paginated_queryset: Query = self.get_queryset().limit(page_limit).offset(self.offset)

    def get_data(self) -> list:
        return [self.schema.parse_obj(item.to_dict()).to_representation() for item in self.get_paginated_results()]

    def get_paginated_queryset(self) -> Query:
        return self.paginated_queryset

    def get_paginated_results(self) -> Query:
        return self.get_paginated_queryset().all()

    def get_queryset(self) -> Query:
        return self.queryset

    def get_count(self) -> int:
        return self.get_paginated_queryset().count()

    def get_previews(self) -> Optional[int]:
        previews = self.current_page - 1
        return previews if previews >= 0 and self.get_count() else None

    def get_next_page(self) -> Optional[int]:
        return (self.current_page + 1) if self.get_count() == self.page_limit and self.get_queryset().count() != self.get_count() else None

    def get_paginated_response(self) -> dict:
        return {
            "total_count": self.total_count,
            "count": self.get_count(),
            "next": self.get_next_page(),
            "previews": self.get_previews(),
            "data": self.get_data(),
        }
