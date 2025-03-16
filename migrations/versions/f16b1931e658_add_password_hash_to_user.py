"""add password_hash to user

Revision ID: f16b1931e658
Revises: dd33d5af0b86
Create Date: 2025-03-16 11:06:53.942952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f16b1931e658'
down_revision = 'dd33d5af0b86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('berita_acara_pemadaman',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('judul_laporan', sa.String(length=255), nullable=False),
    sa.Column('informasi_diterima', sa.Time(), nullable=False),
    sa.Column('tiba_di_lokasi', sa.Time(), nullable=False),
    sa.Column('selesai_pemadaman', sa.Time(), nullable=False),
    sa.Column('respon_time', sa.Time(), nullable=False),
    sa.Column('hari', sa.String(length=20), nullable=False),
    sa.Column('tanggal', sa.Date(), nullable=False),
    sa.Column('rt', sa.String(length=10), nullable=True),
    sa.Column('rw', sa.String(length=10), nullable=True),
    sa.Column('kampung', sa.String(length=100), nullable=True),
    sa.Column('desa_kelurahan', sa.String(length=100), nullable=True),
    sa.Column('kecamatan', sa.String(length=100), nullable=True),
    sa.Column('kabupaten_kota', sa.String(length=100), nullable=True),
    sa.Column('nama_pemilik', sa.String(length=100), nullable=True),
    sa.Column('jumlah_penghuni', sa.Integer(), nullable=True),
    sa.Column('jenis_bangunan', sa.String(length=100), nullable=True),
    sa.Column('area_terbakar', sa.String(length=255), nullable=True),
    sa.Column('luas_area', sa.Integer(), nullable=True),
    sa.Column('penyebab_kebakaran', sa.String(length=255), nullable=True),
    sa.Column('aset_keseluruhan', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('nilai_kerugian', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('aset_terselamatkan', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('korban_luka', sa.Integer(), nullable=True),
    sa.Column('korban_meninggal', sa.Integer(), nullable=True),
    sa.Column('jumlah_mobil', sa.Integer(), nullable=True),
    sa.Column('nomor_polisi', sa.String(length=50), nullable=True),
    sa.Column('jumlah_petugas', sa.Integer(), nullable=True),
    sa.Column('danru_1', sa.String(length=100), nullable=True),
    sa.Column('danru_2', sa.String(length=100), nullable=True),
    sa.Column('danton_1', sa.String(length=100), nullable=True),
    sa.Column('danton_2', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    op.drop_table('berita_acara_pemadaman')
    # ### end Alembic commands ###
