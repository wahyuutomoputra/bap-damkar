from extensions import db
from datetime import datetime

class Rescue(db.Model):
    __tablename__ = 'rescues'
    
    id = db.Column(db.Integer, primary_key=True)
    judul_laporan = db.Column(db.String(255), nullable=False)
    informasi_diterima = db.Column(db.Time, nullable=False)
    tiba_di_lokasi = db.Column(db.Time, nullable=False)
    selesai_pemadaman = db.Column(db.Time, nullable=False)
    respon_time = db.Column(db.Time, nullable=False)
    hari = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    rt = db.Column(db.String(10))
    rw = db.Column(db.String(10))
    kampung = db.Column(db.String(255))
    desa_kelurahan = db.Column(db.String(255))
    kecamatan = db.Column(db.String(255))
    kabupaten_kota = db.Column(db.String(255))
    nama_pemilik = db.Column(db.String(255))
    jumlah_penghuni = db.Column(db.Integer)
    jenis_evakuasi = db.Column(db.String(255))
    jenis_penyelamatan = db.Column(db.String(255))
    korban_luka = db.Column(db.Integer)
    korban_meninggal = db.Column(db.Integer)
    jumlah_mobil = db.Column(db.Integer)
    nomor_polisi = db.Column(db.String(20))
    jumlah_petugas = db.Column(db.Integer)
    danru_1 = db.Column(db.String(255))
    danru_2 = db.Column(db.String(255))
    danton_1 = db.Column(db.String(255))
    danton_2 = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Rescue {self.judul_laporan}>'

    def to_dict(self):
        """Convert the model instance to a dictionary"""
        return {
            'id': self.id,
            'judul_laporan': self.judul_laporan,
            'informasi_diterima': self.informasi_diterima.strftime('%H:%M:%S') if self.informasi_diterima else None,
            'tiba_di_lokasi': self.tiba_di_lokasi.strftime('%H:%M:%S') if self.tiba_di_lokasi else None,
            'selesai_pemadaman': self.selesai_pemadaman.strftime('%H:%M:%S') if self.selesai_pemadaman else None,
            'respon_time': self.respon_time.strftime('%H:%M:%S') if self.respon_time else None,
            'hari': self.hari,
            'tanggal': self.tanggal.strftime('%Y-%m-%d') if self.tanggal else None,
            'rt': self.rt,
            'rw': self.rw,
            'kampung': self.kampung,
            'desa_kelurahan': self.desa_kelurahan,
            'kecamatan': self.kecamatan,
            'kabupaten_kota': self.kabupaten_kota,
            'nama_pemilik': self.nama_pemilik,
            'jumlah_penghuni': self.jumlah_penghuni,
            'jenis_evakuasi': self.jenis_evakuasi,
            'jenis_penyelamatan': self.jenis_penyelamatan,
            'korban_luka': self.korban_luka,
            'korban_meninggal': self.korban_meninggal,
            'jumlah_mobil': self.jumlah_mobil,
            'nomor_polisi': self.nomor_polisi,
            'jumlah_petugas': self.jumlah_petugas,
            'danru_1': self.danru_1,
            'danru_2': self.danru_2,
            'danton_1': self.danton_1,
            'danton_2': self.danton_2,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 