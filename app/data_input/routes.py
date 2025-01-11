# C:\Users\Peter\Blueprint\app\data_input\routes.py
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from app.data_input import data_input_bp
from app.db_connection.conn import get_connection
from datetime import datetime
from app.auth.decorators import require_valid_staff_initials

import speech_recognition as sr


@data_input_bp.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files['audio']
    # Assuming voice_to_text.py has a function `transcribe_audio` to process the audio file
    from SpeechRecog.voice_to_text import transcribe_audio
    recognized_text = transcribe_audio(audio_file)
    return jsonify({'recognized_text': recognized_text})



# Collect data for Unit and Service
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
    if service_name == 'personal care':
        return redirect(url_for('data_input.personal_care_input', 
                            unit_name=unit_name, 
                            resident_initials=resident_initials))
    if service_name == 'cardex':
        return redirect(url_for('data_input.cardex_input', 
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

# Food intake            
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

# Submit food intake
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

# Personal care input
@data_input_bp.route('/personal_care_input')
def personal_care_input():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT DISTINCT personal_care_name FROM personal_care_list ORDER BY personal_care_name')

        personal_care_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('personal_care_form.html', personal_care_list= personal_care_list, unit_name=unit_name, resident_initials=resident_initials)

# Personal care submit
@data_input_bp.route('/submit_personal_care', methods=['POST'])
@require_valid_staff_initials
def submit_personal_care():
    unit_name = request.form.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    personal_care_type = request.form.get('personal_care_type')
    personal_care_note = request.form.get('personal_care_note')
    personal_care_duration = request.form.get('personal_care_duration')
    input_time = request.form.get('input_time')
    staff_initials = request.form.get('staff_initials').upper()
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time # + ':00'

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
        INSERT INTO personal_care_chart (resident_initials, timestamp, personal_care_type, personal_care_note, personal_care_duration, staff_initials)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (resident_initials, timestamp, personal_care_type, personal_care_note, personal_care_duration,staff_initials))
    conn.commit()
    conn.close()

    flash('Personal care entry recorded successfully!', 'success')
    return redirect(url_for('data_input.personal_care_input', unit_name=unit_name, resident_initials=resident_initials))

# Kardex input
@data_input_bp.route('/cardex_input')
def cardex_input():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, cardex_text FROM cardex_chart')
    cardex_text = cursor.fetchall()
    conn.close()
    return render_template('cardex_form.html', cardex_text=cardex_text, unit_name=unit_name, resident_initials=resident_initials)


# Kardex submit
@data_input_bp.route('/submit_cardex', methods=['POST'])
@require_valid_staff_initials
def submit_cardex():
    resident_initials = request.form.get('resident_initials')
    cardex_text = request.form.get('cardex_text')
    input_time = request.form.get('input_time')  # Retrieve input_time from the form data
    staff_initials = request.form.get('staff_initials').upper()  # Retrieve staff_initials from the form data
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time + ':00'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cardex_chart (resident_initials, timestamp, cardex_text, staff_initials)
        VALUES (%s, %s, %s, %s)
    ''', (resident_initials, timestamp, cardex_text, staff_initials))
    conn.commit()
    conn.close()

    flash('Cardex entry recorded successfully!', 'success')
    return redirect(url_for('data_input.cardex_input', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))
