# C:\Users\Peter\Blueprint\app\data_input\routes.py
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from app.data_input import data_input_bp
from app.db_connection.conn import get_connection
from datetime import datetime
from app.auth.decorators import require_valid_staff_initials



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
    if service_name == 'food intake':
        return redirect(url_for('data_input.food_intake', 
                            unit_name=unit_name, 
                            resident_initials=resident_initials))
    else:
        return render_template('under_construction.html')

# Fluid intake     
@data_input_bp.route('/fluid_intake')
def fluid_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT fluid_name FROM fluid_list ORDER BY fluid_name 
        """)
        fluid_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return render_template('fluid_intake.html',
                        fluid_list=fluid_list, 
                        unit_name=unit_name,
                        resident_initials=resident_initials)
    
    
# Submit fluid intake
@require_valid_staff_initials
@data_input_bp.route('/submit_fluid_intake', methods=['POST'])
def submit_fluid_intake():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Get form data
            input_time = request.form.get('input_time')
            #timestamp = datetime.strptime(input_time, '%Y-%m-%d %H:%M').time()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            fluid_name = request.form.get('fluid_name')
            fluid_volume = request.form.get('fluid_volume')
            fluid_note = request.form.get('fluid_note')
            staff_initials = request.form.get('staff_initials')
            resident_initials = request.form.get('resident_initials')

            
            # Insert data
            cursor.execute("""
                INSERT INTO fluid_chart 
                (timestamp, resident_initials, fluid_name, fluid_volume, fluid_note, staff_initials)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (timestamp, resident_initials, fluid_name, fluid_volume, fluid_note, staff_initials))
            
            conn.commit()
            flash('Data updated successfully', 'success')
            return redirect(url_for('data_input.collect_data'))
            
    except Exception as e:
        if conn is not None:
            conn.rollback()
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('data_input.fluid_intake'))
    finally:
        if conn is not None:
            conn.close()
            
@data_input_bp.route('/food_intake')
def food_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT food_name FROM food_list ORDER BY food_name 
        """)
        food_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return render_template('food_intake_form.html', food_list=food_list, unit_name=unit_name, resident_initials=resident_initials)


@data_input_bp.route('/submit_food_intake', methods=['POST'])
@require_valid_staff_initials
def submit_food_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    food_name = request.form.get('food_name')  # Updated variable name
    food_volume = request.form.get('food_volume')
    food_note = request.form.get('food_note')
    input_time = request.form.get('input_time')  # Retrieve input_time from the form data
    staff_initials = request.form.get('staff_initials').upper()  # Convert to uppercase
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time # + ':00'

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO food_chart (timestamp, resident_initials, food_name, food_amount, food_note, staff_initials)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (timestamp, resident_initials,food_name, food_volume, food_note, staff_initials))
        conn.commit()
        conn.close()

    flash('Food intake recorded successfully!', 'success')
    return redirect(url_for('data_input.food_intake', unit_name=unit_name, resident_initials=resident_initials))