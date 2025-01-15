"""blank migration

Revision ID: 30fe5bccd4b0
Revises: 7e834723ff32
Create Date: 2025-01-15 12:26:46.838210

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "30fe5bccd4b0"
down_revision: Union[str, None] = "7e834723ff32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO users (email, password)
        VALUES ('test@test.com', '$2b$12$EmwlGZjQAxZLkXee.6YK3uMceliCY2yukxoS2aNQ5Hr7KHylaN80K');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM users
        WHERE email = 'test@test.com'
        """
    )
