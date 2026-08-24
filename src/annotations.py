import datetime
import uuid
from typing import Annotated
from sqlalchemy import DateTime, func, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, sort_order=-10)
]

int_pk = Annotated[
    int,
    mapped_column(primary_key=True, autoincrement=True, sort_order=-10)
]

bigint_pk = Annotated[
    int,
    mapped_column(BigInteger, primary_key=True, autoincrement=True, sort_order=-10)
]

tz_timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
    )
]
