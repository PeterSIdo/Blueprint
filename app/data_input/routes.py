# C:\Users\Peter\Blueprint\app\data_input\routes.py
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from app.data_input import data_input_bp
from app.db_connection.conn import get_connection



@data_input_bp.route('/collect_data', methods=['GET', 'POST'])
def collect_data():
    conn=get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT DISTINCT unit_name FROM unit_list ORDER BY unit_name")
        units = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT service_name FROM service_list")
        services = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('collect_data.html', units=units, services=services)

# API endpoint to fetch residents dynamically
@data_input_bp.route('/get_residents', methods = ['POST'])
def get_residents():
    unit = request.json.get('unit')
    conn = get_connection()
    with conn.cursor() as cursor:
        # fetch resident initials where resident_unit matches the selected unit
        query = ("SELECT resident_initials FROM resident_list WHERE resident_unit = %s")
        cursor.execute(query, (unit,))
        residents = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(residents=residents)

# Data input logic
@data_input_bp.route('/data_input_logic', methods=['POST'])
def data_input_logic():
    unit_name = request.form.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    service_name = request.form.get('service_name')
    if service_name == 'fluid intake':
        return redirect(url_for('data_input.fluid_intake', 
                            unit_name=unit_name, 
                            resident_initials=resident_initials))
    else:
        return render_template('here.html')
    
@data_input_bp.route('/fluid_intake')
def fluid_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT fluid_name FROM fluid_list ORDER BY fluid_name 
        """)
        fluids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return render_template('fluid_intake.html',
                        fluids=fluids, 
                        unit_name=unit_name,
                        resident_initials=resident_initials)
    
    
@data_input_bp.route('/submit_fluid_intake')
def submit_fluid_intake():
    return render_template('submit_intake.html')