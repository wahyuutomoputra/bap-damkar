"""create rescue table

Revision ID: 9e865270fbba
Revises: f16b1931e658
Create Date: 2025-03-16 11:18:39.896170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e865270fbba'
down_revision = 'f16b1931e658'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rescues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('judul_laporan', sa.String(length=255), nullable=False),
    sa.Column('informasi_diterima', sa.Time(), nullable=False),
    sa.Column('tiba_di_lokasi', sa.Time(), nullable=False),
    sa.Column('selesai_pemadaman', sa.Time(), nullable=False),
    sa.Column('respon_time', sa.Time(), nullable=False),
    sa.Column('hari', sa.String(length=20), nullable=False),
    sa.Column('tanggal', sa.Date(), nullable=False),
    sa.Column('rt', sa.String(length=10), nullable=True),
    sa.Column('rw', sa.String(length=10), nullable=True),
    sa.Column('kampung', sa.String(length=255), nullable=True),
    sa.Column('desa_kelurahan', sa.String(length=255), nullable=True),
    sa.Column('kecamatan', sa.String(length=255), nullable=True),
    sa.Column('kabupaten_kota', sa.String(length=255), nullable=True),
    sa.Column('nama_pemilik', sa.String(length=255), nullable=True),
    sa.Column('jumlah_penghuni', sa.Integer(), nullable=True),
    sa.Column('jenis_evakuasi', sa.String(length=255), nullable=True),
    sa.Column('jenis_penyelamatan', sa.String(length=255), nullable=True),
    sa.Column('korban_luka', sa.Integer(), nullable=True),
    sa.Column('korban_meninggal', sa.Integer(), nullable=True),
    sa.Column('jumlah_mobil', sa.Integer(), nullable=True),
    sa.Column('nomor_polisi', sa.String(length=20), nullable=True),
    sa.Column('jumlah_petugas', sa.Integer(), nullable=True),
    sa.Column('danru_1', sa.String(length=255), nullable=True),
    sa.Column('danru_2', sa.String(length=255), nullable=True),
    sa.Column('danton_1', sa.String(length=255), nullable=True),
    sa.Column('danton_2', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rescues')
    # ### end Alembic commands ###
