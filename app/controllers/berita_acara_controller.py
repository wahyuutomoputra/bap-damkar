from flask import Blueprint, request
from extensions import db
from app.models.berita_acara import BeritaAcaraPemadaman
from app.utils.response_handler import success_response, error_response
from datetime import datetime, time
from sqlalchemy import and_

berita_acara_bp = Blueprint('berita_acara', __name__, url_prefix='/berita-acara')

@berita_acara_bp.route('', methods=['GET'], strict_slashes=False)
def get_all_berita_acara():
    """Get all berita acara pemadaman with pagination, date range filter, and title search"""
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get filter parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        search = request.args.get('search', '').strip()
        
        # Validate pagination parameters
        if page < 1:
            return error_response(
                message="Nomor halaman harus lebih dari 0",
                errors="Invalid page number",
                status_code=400
            )
        if per_page < 1 or per_page > 100:
            return error_response(
                message="Jumlah item per halaman harus antara 1 dan 100",
                errors="Invalid per_page value",
                status_code=400
            )

        # Build query
        query = BeritaAcaraPemadaman.query

        # Apply date range filter
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(BeritaAcaraPemadaman.tanggal >= start_date)
            except ValueError:
                return error_response(
                    message="Format tanggal awal tidak valid (gunakan YYYY-MM-DD)",
                    errors="Invalid start_date format",
                    status_code=400
                )

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(BeritaAcaraPemadaman.tanggal <= end_date)
            except ValueError:
                return error_response(
                    message="Format tanggal akhir tidak valid (gunakan YYYY-MM-DD)",
                    errors="Invalid end_date format",
                    status_code=400
                )

        # Apply search filter
        if search:
            query = query.filter(BeritaAcaraPemadaman.judul_laporan.ilike(f'%{search}%'))

        # Apply ordering and pagination
        pagination = query.order_by(BeritaAcaraPemadaman.tanggal.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Check if page exists
        if not pagination.items and page > 1:
            return error_response(
                message="Halaman tidak ditemukan",
                errors="Page not found",
                status_code=404
            )

        return success_response(
            data={
                'items': [ba.to_dict() for ba in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
                'next_page': pagination.next_num if pagination.has_next else None,
                'prev_page': pagination.prev_num if pagination.has_prev else None,
                'filters': {
                    'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
                    'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
                    'search': search if search else None
                }
            },
            message="Berhasil mengambil data berita acara"
        )
    except Exception as e:
        return error_response(
            message="Gagal mengambil data berita acara",
            errors=str(e)
        )

@berita_acara_bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
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

@berita_acara_bp.route('', methods=['POST'], strict_slashes=False)
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

@berita_acara_bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
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

@berita_acara_bp.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
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