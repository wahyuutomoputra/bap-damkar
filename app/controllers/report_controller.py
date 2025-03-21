from flask import Blueprint, jsonify
from app.models.rescue import Rescue
from app.models.berita_acara import BeritaAcaraPemadaman
from app.utils.response_handler import success_response, error_response
from sqlalchemy import func, extract
from datetime import datetime, timedelta

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