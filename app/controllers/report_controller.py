from flask import Blueprint, jsonify, request
from app.models.rescue import Rescue
from app.models.berita_acara import BeritaAcaraPemadaman
from app.utils.response_handler import success_response, error_response
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from calendar import monthrange
from extensions import db

report_bp = Blueprint('report', __name__, url_prefix='/api/report')

@report_bp.route('/rescue/summary', methods=['GET'])
def get_rescue_summary():
    try:
        # Total rescue berdasarkan jenis evakuasi
        jenis_summary = Rescue.query.with_entities(
            Rescue.jenis_evakuasi,
            func.count(Rescue.id).label('total')
        ).group_by(Rescue.jenis_evakuasi).all()
        
        # Total rescue berdasarkan lokasi
        location_summary = Rescue.query.with_entities(
            Rescue.kabupaten_kota,
            func.count(Rescue.id).label('total')
        ).group_by(Rescue.kabupaten_kota).all()
        
        # Total rescue per bulan
        monthly_summary = Rescue.query.with_entities(
            func.date_format(Rescue.tanggal, '%Y-%m').label('month'),
            func.count(Rescue.id).label('total')
        ).group_by('month').order_by('month').all()
        
        return success_response({
            'jenis_summary': [{'jenis': s[0], 'total': s[1]} for s in jenis_summary],
            'location_summary': [{'lokasi': l[0], 'total': l[1]} for l in location_summary],
            'monthly_summary': [{'month': m[0], 'total': m[1]} for m in monthly_summary]
        })
    except Exception as e:
        return error_response(str(e))

@report_bp.route('/berita-acara/summary', methods=['GET'])
def get_berita_acara_summary():
    try:
        # Total berita acara berdasarkan jenis bangunan
        jenis_summary = BeritaAcaraPemadaman.query.with_entities(
            BeritaAcaraPemadaman.jenis_bangunan,
            func.count(BeritaAcaraPemadaman.id).label('total')
        ).group_by(BeritaAcaraPemadaman.jenis_bangunan).all()
        
        # Total berita acara per bulan
        monthly_summary = BeritaAcaraPemadaman.query.with_entities(
            func.date_format(BeritaAcaraPemadaman.tanggal, '%Y-%m').label('month'),
            func.count(BeritaAcaraPemadaman.id).label('total')
        ).group_by('month').order_by('month').all()
        
        return success_response({
            'jenis_summary': [{'jenis': j[0], 'total': j[1]} for j in jenis_summary],
            'monthly_summary': [{'month': m[0], 'total': m[1]} for m in monthly_summary]
        })
    except Exception as e:
        return error_response(str(e))

@report_bp.route('/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    try:
        # Total rescue hari ini
        today_rescue = Rescue.query.filter(
            func.date(Rescue.tanggal) == datetime.now().date()
        ).count()
        
        # Total berita acara hari ini
        today_berita_acara = BeritaAcaraPemadaman.query.filter(
            func.date(BeritaAcaraPemadaman.tanggal) == datetime.now().date()
        ).count()
        
        # Rescue dalam 7 hari terakhir
        last_week = datetime.now() - timedelta(days=7)
        weekly_rescue = Rescue.query.filter(
            Rescue.tanggal >= last_week
        ).count()
        
        # Total korban dalam 7 hari terakhir
        weekly_casualties = Rescue.query.with_entities(
            func.sum(Rescue.korban_luka).label('total_luka'),
            func.sum(Rescue.korban_meninggal).label('total_meninggal')
        ).filter(
            Rescue.tanggal >= last_week
        ).first()
        
        return success_response({
            'today_rescue': today_rescue,
            'today_berita_acara': today_berita_acara,
            'weekly_rescue': weekly_rescue,
            'weekly_casualties': {
                'total_luka': weekly_casualties[0] or 0,
                'total_meninggal': weekly_casualties[1] or 0
            }
        })
    except Exception as e:
        return error_response(str(e))

@report_bp.route('/rescue/trend', methods=['GET'])
def get_rescue_trend():
    try:
        # Coba ambil data 30 hari terakhir
        last_30_days = datetime.now() - timedelta(days=30)
        daily_trend = Rescue.query.with_entities(
            func.date(Rescue.tanggal).label('date'),
            func.count(Rescue.id).label('total')
        ).filter(
            Rescue.tanggal >= last_30_days
        ).group_by('date').order_by('date').all()
        
        # Jika tidak ada data dalam 30 hari, coba ambil data 3 bulan terakhir
        if not daily_trend:
            last_3_months = datetime.now() - timedelta(days=90)
            daily_trend = Rescue.query.with_entities(
                func.date(Rescue.tanggal).label('date'),
                func.count(Rescue.id).label('total')
            ).filter(
                Rescue.tanggal >= last_3_months
            ).group_by('date').order_by('date').all()
            
            # Jika masih tidak ada data, ambil semua data yang ada
            if not daily_trend:
                daily_trend = Rescue.query.with_entities(
                    func.date(Rescue.tanggal).label('date'),
                    func.count(Rescue.id).label('total')
                ).group_by('date').order_by('date').all()
        
        # Tambahkan informasi total keseluruhan dan korban
        total_rescue = sum(d[1] for d in daily_trend)
        
        # Hitung total korban dalam periode yang sama
        casualties = Rescue.query.with_entities(
            func.sum(Rescue.korban_luka).label('total_luka'),
            func.sum(Rescue.korban_meninggal).label('total_meninggal')
        ).filter(
            Rescue.tanggal >= (daily_trend[0][0] if daily_trend else last_30_days.date())
        ).first()
        
        return success_response({
            'daily_trend': [{'date': d[0].strftime('%Y-%m-%d'), 'total': d[1]} for d in daily_trend],
            'total_rescue': total_rescue,
            'total_casualties': {
                'total_luka': casualties[0] or 0,
                'total_meninggal': casualties[1] or 0
            },
            'period': '30 hari terakhir' if len(daily_trend) > 0 and daily_trend[0][0] >= last_30_days.date() else 
                     '3 bulan terakhir' if len(daily_trend) > 0 and daily_trend[0][0] >= last_3_months.date() else 
                     'seluruh periode'
        })
    except Exception as e:
        return error_response(str(e))

@report_bp.route('/berita-acara/trend', methods=['GET'])
def get_berita_acara_trend():
    try:
        # Coba ambil data 30 hari terakhir
        last_30_days = datetime.now() - timedelta(days=30)
        daily_trend = BeritaAcaraPemadaman.query.with_entities(
            func.date(BeritaAcaraPemadaman.tanggal).label('date'),
            func.count(BeritaAcaraPemadaman.id).label('total')
        ).filter(
            BeritaAcaraPemadaman.tanggal >= last_30_days
        ).group_by('date').order_by('date').all()
        
        # Jika tidak ada data dalam 30 hari, coba ambil data 3 bulan terakhir
        if not daily_trend:
            last_3_months = datetime.now() - timedelta(days=90)
            daily_trend = BeritaAcaraPemadaman.query.with_entities(
                func.date(BeritaAcaraPemadaman.tanggal).label('date'),
                func.count(BeritaAcaraPemadaman.id).label('total')
            ).filter(
                BeritaAcaraPemadaman.tanggal >= last_3_months
            ).group_by('date').order_by('date').all()
            
            # Jika masih tidak ada data, ambil semua data yang ada
            if not daily_trend:
                daily_trend = BeritaAcaraPemadaman.query.with_entities(
                    func.date(BeritaAcaraPemadaman.tanggal).label('date'),
                    func.count(BeritaAcaraPemadaman.id).label('total')
                ).group_by('date').order_by('date').all()
        
        # Tambahkan informasi total keseluruhan
        total_berita_acara = sum(d[1] for d in daily_trend)
        
        return success_response({
            'daily_trend': [{'date': d[0].strftime('%Y-%m-%d'), 'total': d[1]} for d in daily_trend],
            'total_berita_acara': total_berita_acara,
            'period': '30 hari terakhir' if len(daily_trend) > 0 and daily_trend[0][0] >= last_30_days.date() else 
                     '3 bulan terakhir' if len(daily_trend) > 0 and daily_trend[0][0] >= last_3_months.date() else 
                     'seluruh periode'
        })
    except Exception as e:
        return error_response(str(e))

@report_bp.route('/dashboard/monthly', methods=['GET'])
def get_monthly_dashboard():
    """Get monthly dashboard summary combining rescue and berita acara data"""
    try:
        # Get year and month from query parameters
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)

        # If year and month not provided, use current date
        if not year or not month:
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month

        # Validate year and month
        if not (1 <= month <= 12):
            return error_response(
                message="Bulan harus antara 1 dan 12",
                errors="Invalid month value",
                status_code=400
            )

        # Get first and last day of the month
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, monthrange(year, month)[1])

        # Rescue Summary
        rescue_summary = db.session.query(
            func.count(Rescue.id).label('total_rescue'),
            func.sum(Rescue.korban_luka).label('total_luka'),
            func.sum(Rescue.korban_meninggal).label('total_meninggal')
        ).filter(
            Rescue.tanggal.between(first_day.date(), last_day.date())
        ).first()

        # Rescue by jenis evakuasi
        rescue_by_type = db.session.query(
            Rescue.jenis_evakuasi,
            func.count(Rescue.id).label('total')
        ).filter(
            Rescue.tanggal.between(first_day.date(), last_day.date())
        ).group_by(Rescue.jenis_evakuasi).all()

        # Rescue by location
        rescue_by_location = db.session.query(
            Rescue.kabupaten_kota,
            func.count(Rescue.id).label('total')
        ).filter(
            Rescue.tanggal.between(first_day.date(), last_day.date())
        ).group_by(Rescue.kabupaten_kota).all()

        # Berita Acara Summary
        berita_acara_summary = db.session.query(
            func.count(BeritaAcaraPemadaman.id).label('total_kejadian'),
            func.avg(BeritaAcaraPemadaman.respon_time).label('rata_rata_respon'),
            func.min(BeritaAcaraPemadaman.respon_time).label('respon_tercepat'),
            func.max(BeritaAcaraPemadaman.respon_time).label('respon_terlambat')
        ).filter(
            BeritaAcaraPemadaman.tanggal.between(first_day.date(), last_day.date())
        ).first()

        # Berita Acara by jenis bangunan
        berita_acara_by_type = db.session.query(
            BeritaAcaraPemadaman.jenis_bangunan,
            func.count(BeritaAcaraPemadaman.id).label('total')
        ).filter(
            BeritaAcaraPemadaman.tanggal.between(first_day.date(), last_day.date())
        ).group_by(BeritaAcaraPemadaman.jenis_bangunan).all()

        # Daily breakdown for both
        daily_rescue = db.session.query(
            extract('day', Rescue.tanggal).label('day'),
            func.count(Rescue.id).label('total')
        ).filter(
            Rescue.tanggal.between(first_day.date(), last_day.date())
        ).group_by(extract('day', Rescue.tanggal)).all()

        daily_berita_acara = db.session.query(
            extract('day', BeritaAcaraPemadaman.tanggal).label('day'),
            func.count(BeritaAcaraPemadaman.id).label('total')
        ).filter(
            BeritaAcaraPemadaman.tanggal.between(first_day.date(), last_day.date())
        ).group_by(extract('day', BeritaAcaraPemadaman.tanggal)).all()

        # Format response data
        response_data = {
            'period': {
                'year': year,
                'month': month,
                'start_date': first_day.strftime('%Y-%m-%d'),
                'end_date': last_day.strftime('%Y-%m-%d')
            },
            'rescue': {
                'summary': {
                    'total_rescue': rescue_summary.total_rescue or 0,
                    'total_luka': rescue_summary.total_luka or 0,
                    'total_meninggal': rescue_summary.total_meninggal or 0
                },
                'by_type': [{'jenis': t[0], 'total': t[1]} for t in rescue_by_type],
                'by_location': [{'lokasi': l[0], 'total': l[1]} for l in rescue_by_location],
                'daily_breakdown': [{'day': int(d[0]), 'total': d[1]} for d in daily_rescue]
            },
            'berita_acara': {
                'summary': {
                    'total_kejadian': berita_acara_summary.total_kejadian or 0,
                    'rata_rata_respon': str(berita_acara_summary.rata_rata_respon) if berita_acara_summary.rata_rata_respon else None,
                    'respon_tercepat': str(berita_acara_summary.respon_tercepat) if berita_acara_summary.respon_tercepat else None,
                    'respon_terlambat': str(berita_acara_summary.respon_terlambat) if berita_acara_summary.respon_terlambat else None
                },
                'by_type': [{'jenis': t[0], 'total': t[1]} for t in berita_acara_by_type],
                'daily_breakdown': [{'day': int(d[0]), 'total': d[1]} for d in daily_berita_acara]
            }
        }

        return success_response(
            data=response_data,
            message="Berhasil mengambil ringkasan dashboard bulanan"
        )

    except Exception as e:
        return error_response(
            message="Gagal mengambil ringkasan dashboard bulanan",
            errors=str(e)
        ) 