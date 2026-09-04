"""unique no nome_login das unidades de saude

Revision ID: ac5ddf5fa7f5
Revises: 369ddd5e57b4
Create Date: 2026-09-04 08:38:35.427542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac5ddf5fa7f5'
down_revision: Union[str, Sequence[str], None] = '369ddd5e57b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("unidade_saude") as batch_op:
        batch_op.create_unique_constraint(
            "uq_unidade_saude_nome_login",
            ["nome_login"]
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("unidade_saude") as batch_op:
        batch_op.drop_constraint(
            "uq_unidade_saude_nome_login",
            type_="unique"
        )
    # ### end Alembic commands ###
