# C:\Users\Peter\Blueprint\app\data_output\routes.py
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from app.data_output import data_output_bp
from app.db_connection.conn import get_connection
from datetime import datetime
# jlkkwwe wewew
@data_output_bp.route('/test')
def test():
    return "Test Route Works!"

@data_output_bp.route('/report_selection', methods=['GET', 'POST'])
def report_selection():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT unit_name FROM unit_list ORDER BY unit_name")
            units = cursor.fetchall()
            cursor.execute("SELECT service_name FROM service_list")
            services = cursor.fetchall()
            #cursor.execute("SELECT resident_initials FROM resident_list")
            #residents = cursor.fetchall()
    except Exception as e:
        flash('An error occurred while fetching data.')
        return redirect(url_for('error_page'))
    finally:
        conn.close()

    if request.method == 'POST':
        unit_name = request.form.get('unit_name')
        resident_initials = request.form.get('resident_initials')
        service_name = request.form.get('service_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not all([unit_name, resident_initials, service_name, start_date, end_date]):
            flash('Please enter all required fields.')
            return redirect(url_for('data_output.report_selection'))

        return redirect(url_for('data_output.report_selection_logic',
            unit_name=unit_name,
            resident_initials=resident_initials,
            service_name=service_name,
            start_date=start_date,
            end_date=end_date
        ))
    #return render_template('under_construction.html')
    return render_template('report_selection.html', units=units, services=services, residents=residents)


@data_output_bp.route('/report_selection_logic', methods=['GET'])
def report_selection_logic():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    service_name = request.args.get('service_name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    service_routes = {
        'fluid chart': 'reports.report_fluid',
        'food chart': 'reports.report_food',
        'personal care chart': 'reports.report_personal_care',
        'cardex chart': 'reports.report_cardex',
        'care frequency chart': 'reports.report_care_frequency',
        'bowels observation': 'reports.report_bowels',
        'all daily records': 'reports.report_all_daily_records',
    }

    if service_name in service_routes:
        return redirect(url_for(service_routes[service_name], 
                                unit_name=unit_name, 
                                resident_initials=resident_initials, 
                                start_date=start_date, 
                                end_date=end_date))
    else:
        flash('Invalid report selection.')
        return redirect(url_for('data_output.report_selection'))

@data_output_bp.route('/get_residents', methods=['GET'])
def get_residents():
    unit_name = request.args.get('unit_name')
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT resident_initials 
                FROM resident_list 
                WHERE unit_name = %s
            """, (unit_name,))
            residents = cursor.fetchall()
            resident_initials = [resident[0] for resident in residents]
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching residents.'}), 500
    finally:
        conn.close()
    
    return jsonify({'residents': resident_initials})