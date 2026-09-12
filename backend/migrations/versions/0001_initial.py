from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuarios",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "nombre",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "activo",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_usuarios_email",
        "usuarios",
        ["email"],
        unique=True,
    )

    op.create_table(
        "proyectos",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "nombre",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "descripcion",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey(
                "usuarios.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_proyectos_usuario_id",
        "proyectos",
        ["usuario_id"],
    )

    op.create_table(
        "tareas",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),
        sa.Column(
            "titulo",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "descripcion",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "prioridad",
            sa.String(length=20),
            nullable=False,
            server_default="Media",
        ),
        sa.Column(
            "estado",
            sa.String(length=30),
            nullable=False,
            server_default="Pendiente",
        ),
        sa.Column(
            "categoria",
            sa.String(length=100),
            nullable=False,
            server_default="General",
        ),
        sa.Column(
            "fecha_limite",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey(
                "usuarios.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "proyecto_id",
            sa.Integer(),
            sa.ForeignKey(
                "proyectos.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        ),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_tareas_usuario_id",
        "tareas",
        ["usuario_id"],
    )

    op.create_index(
        "ix_tareas_proyecto_id",
        "tareas",
        ["proyecto_id"],
    )


def downgrade():
    op.drop_table("tareas")
    op.drop_table("proyectos")
    op.drop_table("usuarios")