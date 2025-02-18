"""prueba

Revision ID: 35aa43375323
Revises: 
Create Date: 2021-01-09 22:02:46.306166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35aa43375323'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workflows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tableros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('asignaciones',
    sa.Column('usuario_id', sa.String(length=100), nullable=False),
    sa.Column('tablero_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tablero_id'], ['tableros.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('usuario_id', 'tablero_id')
    )
    op.create_table('estados',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('tablero_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tablero_id'], ['tableros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('tablero_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tablero_id'], ['tableros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tareas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tablero_id', sa.Integer(), nullable=False),
    sa.Column('estado_id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=50), nullable=True),
    sa.Column('descripcion', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['estado_id'], ['estados.id'], ),
    sa.ForeignKeyConstraint(['tablero_id'], ['tableros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transiciones_posibles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workflow_id', sa.Integer(), nullable=False),
    sa.Column('estado_inicial_id', sa.Integer(), nullable=False),
    sa.Column('estado_final_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['estado_final_id'], ['estados.id'], ),
    sa.ForeignKeyConstraint(['estado_inicial_id'], ['estados.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscripciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('evento', sa.Enum('CREACION_TARJETA', 'BORRACION_TARJETA', 'MOVICION_TARJETA', 'AGREGACION_USUARIO', 'INGRESO_TARJETA', 'EGRESO_TARJETA', 'CAMBIO_DE_ESTADO', 'BORRADO_TARJETA', name='evento'), nullable=True),
    sa.Column('estado_id', sa.Integer(), nullable=True),
    sa.Column('tablero_id', sa.Integer(), nullable=True),
    sa.Column('tarea_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['estado_id'], ['estados.id'], ),
    sa.ForeignKeyConstraint(['tablero_id'], ['tableros.id'], ),
    sa.ForeignKeyConstraint(['tarea_id'], ['tareas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tareaXrol',
    sa.Column('tarea_id', sa.Integer(), nullable=False),
    sa.Column('rol_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rol_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tarea_id'], ['tareas.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tarea_id', 'rol_id')
    )
    op.create_table('transiciones_realizadas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tablero_id', sa.Integer(), nullable=False),
    sa.Column('tarea_id', sa.Integer(), nullable=False),
    sa.Column('estado_inicial_id', sa.Integer(), nullable=False),
    sa.Column('estado_final_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['estado_final_id'], ['estados.id'], ),
    sa.ForeignKeyConstraint(['estado_inicial_id'], ['estados.id'], ),
    sa.ForeignKeyConstraint(['tablero_id'], ['tableros.id'], ),
    sa.ForeignKeyConstraint(['tarea_id'], ['tareas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transicion_id', sa.Integer(), nullable=True),
    sa.Column('subscripcion_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('payload', sa.Text(), nullable=True),
    sa.Column('contador', sa.Integer(), nullable=True),
    sa.Column('contador_2', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=50), nullable=True),
    sa.Column('method', sa.String(length=1024), nullable=True),
    sa.Column('headers', sa.String(length=1024), nullable=True),
    sa.Column('body', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['subscripcion_id'], ['subscripciones.id'], ),
    sa.ForeignKeyConstraint(['transicion_id'], ['transiciones_posibles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resultados_acciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transicion_realizada_id', sa.Integer(), nullable=True),
    sa.Column('respuesta', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['transicion_realizada_id'], ['transiciones_realizadas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resultados_acciones')
    op.drop_table('acciones')
    op.drop_table('transiciones_realizadas')
    op.drop_table('tareaXrol')
    op.drop_table('subscripciones')
    op.drop_table('transiciones_posibles')
    op.drop_table('tareas')
    op.drop_table('roles')
    op.drop_table('estados')
    op.drop_table('asignaciones')
    op.drop_table('tableros')
    op.drop_table('workflows')
    op.drop_table('usuarios')
    # ### end Alembic commands ###
