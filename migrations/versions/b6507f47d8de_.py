"""empty message

Revision ID: b6507f47d8de
Revises: 
Create Date: 2021-01-23 17:48:35.527539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6507f47d8de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Hospital',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=120), nullable=True),
    sa.Column('lastname', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Patient_phone'), 'Patient', ['phone'], unique=True)
    op.create_table('Department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['Hospital.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Doctors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['Department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('adress', sa.String(length=120), nullable=True),
    sa.Column('room', sa.String(length=120), nullable=True),
    sa.Column('colortape', sa.String(length=120), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['Department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=128), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['Department.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['Patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    op.create_index(op.f('ix_User_username'), 'User', ['username'], unique=True)
    op.create_table('Appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('apdate', sa.String(), nullable=False),
    sa.Column('aptime', sa.String(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['Doctors.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['Patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('DoctorDate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=80), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['Doctors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('TimeSlots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slot', sa.String(length=80), nullable=True),
    sa.Column('doctor_date_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_date_id'], ['DoctorDate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TimeSlots')
    op.drop_table('DoctorDate')
    op.drop_table('Appointment')
    op.drop_index(op.f('ix_User_username'), table_name='User')
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_table('User')
    op.drop_table('Location')
    op.drop_table('Doctors')
    op.drop_table('Department')
    op.drop_index(op.f('ix_Patient_phone'), table_name='Patient')
    op.drop_table('Patient')
    op.drop_table('Hospital')
    # ### end Alembic commands ###
