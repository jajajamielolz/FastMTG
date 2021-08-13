"""initial_card_tables

Revision ID: 14c5381a5158
Revises:
Create Date: 2021-08-13 00:20:51.721386

"""
import sqlalchemy as sa
import sqlalchemy_utc

from alembic import op


# revision identifiers, used by Alembic.
revision = "14c5381a5158"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "magic_card",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("mana_cost", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("cmc", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
            server_default=sa.text("(DATETIME('NOW'))"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "magic_set",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sub_type",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "card_has_set",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("card_id", sa.String(), nullable=False),
        sa.Column("set_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["card_id"],
            ["magic_card.id"],
        ),
        sa.ForeignKeyConstraint(
            ["set_id"],
            ["magic_set.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "card_has_sub_type",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("card_id", sa.String(), nullable=False),
        sa.Column("sub_type_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["card_id"],
            ["magic_card.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sub_type_id"],
            ["sub_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("card_has_sub_type")
    op.drop_table("card_has_set")
    op.drop_table("sub_type")
    op.drop_table("magic_set")
    op.drop_table("magic_card")
    # ### end Alembic commands ###
