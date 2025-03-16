from flask import Blueprint, request
from extensions import db
from app.models.berita_acara import BeritaAcaraPemadaman
from app.utils.response_handler import success_response, error_response
from datetime import datetime, time

berita_acara_bp = Blueprint('berita_acara', __name__, url_prefix='/berita-acara')

@berita_acara_bp.route('/', methods=['GET'])
def get_all_berita_acara():
    """Get all berita acara pemadaman"""
    try:
        berita_acara = BeritaAcaraPemadaman.query.all()
        return success_response(
            data=[ba.to_dict() for ba in berita_acara],
            message="Berhasil mengambil semua data berita acara"
        )
    except Exception as e:
        return error_response(
            message="Gagal mengambil data berita acara",
            errors=str(e)
        )

@berita_acara_bp.route('/<int:id>', methods=['GET'])
def get_berita_acara(id):
    """Get berita acara pemadaman by id"""
    try:
        berita_acara = BeritaAcaraPemadaman.query.get_or_404(id)
        return success_response(
            data=berita_acara.to_dict(),
            message="Berhasil mengambil data berita acara"
        )
    except Exception as e:
        return error_response(
            message=f"Berita acara dengan id {id} tidak ditemukan",
            errors=str(e),
            status_code=404
        )

@berita_acara_bp.route('/', methods=['POST'])
def create_berita_acara():
    """Create new berita acara pemadaman"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['judul_laporan', 'informasi_diterima', 'tiba_di_lokasi', 
                         'selesai_pemadaman', 'respon_time', 'hari', 'tanggal']
        
        for field in required_fields:
            if field not in data:
                return error_response(
                    message=f"Field {field} harus diisi",
                    errors=f"Missing required field: {field}",
                    status_code=400
                )

        # Convert time strings to time objects
        time_fields = ['informasi_diterima', 'tiba_di_lokasi', 'selesai_pemadaman', 'respon_time']
        for field in time_fields:
            try:
                if data[field]:
                    time_str = data[field]
                    data[field] = datetime.strptime(time_str, '%H:%M:%S').time()
            except ValueError as e:
                return error_response(
                    message=f"Format waktu tidak valid untuk field {field}",
                    errors=str(e),
                    status_code=400
                )

        # Convert date string to date object
        try:
            if data['tanggal']:
                data['tanggal'] = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
        except ValueError as e:
            return error_response(
                message="Format tanggal tidak valid (gunakan YYYY-MM-DD)",
                errors=str(e),
                status_code=400
            )

        berita_acara = BeritaAcaraPemadaman(**data)
        db.session.add(berita_acara)
        db.session.commit()

        return success_response(
            data=berita_acara.to_dict(),
            message="Berhasil membuat berita acara baru",
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal membuat berita acara",
            errors=str(e)
        )

@berita_acara_bp.route('/<int:id>', methods=['PUT'])
def update_berita_acara(id):
    """Update berita acara pemadaman"""
    try:
        berita_acara = BeritaAcaraPemadaman.query.get_or_404(id)
        data = request.get_json()

        # Convert time strings to time objects if provided
        time_fields = ['informasi_diterima', 'tiba_di_lokasi', 'selesai_pemadaman', 'respon_time']
        for field in time_fields:
            if field in data and data[field]:
                try:
                    time_str = data[field]
                    data[field] = datetime.strptime(time_str, '%H:%M:%S').time()
                except ValueError as e:
                    return error_response(
                        message=f"Format waktu tidak valid untuk field {field}",
                        errors=str(e),
                        status_code=400
                    )

        # Convert date string to date object if provided
        if 'tanggal' in data and data['tanggal']:
            try:
                data['tanggal'] = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
            except ValueError as e:
                return error_response(
                    message="Format tanggal tidak valid (gunakan YYYY-MM-DD)",
                    errors=str(e),
                    status_code=400
                )

        # Update fields
        for key, value in data.items():
            setattr(berita_acara, key, value)

        db.session.commit()
        return success_response(
            data=berita_acara.to_dict(),
            message="Berhasil mengupdate berita acara"
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal mengupdate berita acara",
            errors=str(e)
        )

@berita_acara_bp.route('/<int:id>', methods=['DELETE'])
def delete_berita_acara(id):
    """Delete berita acara pemadaman"""
    try:
        berita_acara = BeritaAcaraPemadaman.query.get_or_404(id)
        db.session.delete(berita_acara)
        db.session.commit()
        
        return success_response(
            message="Berhasil menghapus berita acara"
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal menghapus berita acara",
            errors=str(e)
        ) 