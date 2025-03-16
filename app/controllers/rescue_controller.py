from flask import Blueprint, request
from app.models.rescue import Rescue
from extensions import db
from app.utils.response_handler import success_response, error_response
from flask_jwt_extended import jwt_required

rescue_bp = Blueprint('rescue', __name__, url_prefix='/rescue')

@rescue_bp.route('', methods=['GET'])
@jwt_required()
def get_all_rescues():
    """Get all rescue records"""
    try:
        rescues = Rescue.query.all()
        rescue_list = [rescue.to_dict() for rescue in rescues]
        return success_response(
            message="Berhasil mengambil semua data rescue",
            data=rescue_list
        )
    except Exception as e:
        return error_response(
            message="Gagal mengambil data rescue",
            errors=str(e)
        )

@rescue_bp.route('', methods=['POST'])
@jwt_required()
def create_rescue():
    """Create a new rescue record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'judul_laporan', 'informasi_diterima', 'tiba_di_lokasi',
            'selesai_pemadaman', 'respon_time', 'hari', 'tanggal'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return error_response(
                    message=f"Field {field} harus diisi",
                    errors=f"Missing required field: {field}",
                    status_code=400
                )
        
        new_rescue = Rescue(
            judul_laporan=data.get('judul_laporan'),
            informasi_diterima=data.get('informasi_diterima'),
            tiba_di_lokasi=data.get('tiba_di_lokasi'),
            selesai_pemadaman=data.get('selesai_pemadaman'),
            respon_time=data.get('respon_time'),
            hari=data.get('hari'),
            tanggal=data.get('tanggal'),
            rt=data.get('rt'),
            rw=data.get('rw'),
            kampung=data.get('kampung'),
            desa_kelurahan=data.get('desa_kelurahan'),
            kecamatan=data.get('kecamatan'),
            kabupaten_kota=data.get('kabupaten_kota'),
            nama_pemilik=data.get('nama_pemilik'),
            jumlah_penghuni=data.get('jumlah_penghuni'),
            jenis_evakuasi=data.get('jenis_evakuasi'),
            jenis_penyelamatan=data.get('jenis_penyelamatan'),
            korban_luka=data.get('korban_luka'),
            korban_meninggal=data.get('korban_meninggal'),
            jumlah_mobil=data.get('jumlah_mobil'),
            nomor_polisi=data.get('nomor_polisi'),
            jumlah_petugas=data.get('jumlah_petugas'),
            danru_1=data.get('danru_1'),
            danru_2=data.get('danru_2'),
            danton_1=data.get('danton_1'),
            danton_2=data.get('danton_2')
        )
        
        db.session.add(new_rescue)
        db.session.commit()
        
        return success_response(
            message="Berhasil membuat rescue baru",
            data=new_rescue.to_dict(),
            status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal membuat rescue baru",
            errors=str(e)
        )

@rescue_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_rescue(id):
    """Get a rescue record by ID"""
    try:
        rescue = Rescue.query.get(id)
        if not rescue:
            return error_response(
                message="Data rescue tidak ditemukan",
                errors="Not found",
                status_code=404
            )
        
        return success_response(
            message="Berhasil mengambil data rescue",
            data=rescue.to_dict()
        )
    except Exception as e:
        return error_response(
            message="Gagal mengambil data rescue",
            errors=str(e)
        )

@rescue_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_rescue(id):
    """Update a rescue record"""
    try:
        rescue = Rescue.query.get(id)
        if not rescue:
            return error_response(
                message="Data rescue tidak ditemukan",
                errors="Not found",
                status_code=404
            )
        
        data = request.get_json()
        
        # Update fields if they exist in the request
        for field in rescue.__table__.columns.keys():
            if field in data and field != 'id':
                setattr(rescue, field, data[field])
        
        db.session.commit()
        
        return success_response(
            message="Berhasil mengupdate rescue",
            data=rescue.to_dict()
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal mengupdate rescue",
            errors=str(e)
        )

@rescue_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_rescue(id):
    """Delete a rescue record"""
    try:
        rescue = Rescue.query.get(id)
        if not rescue:
            return error_response(
                message="Data rescue tidak ditemukan",
                errors="Not found",
                status_code=404
            )
        
        db.session.delete(rescue)
        db.session.commit()
        
        return success_response(
            message="Berhasil menghapus rescue"
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Gagal menghapus rescue",
            errors=str(e)
        ) 