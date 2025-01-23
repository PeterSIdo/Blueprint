# C:\Users\Peter\Blueprint\app\data_output\routes.py
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from app.data_output import data_output_bp
from app.db_connection.conn import get_connection
from datetime import datetime
from app.auth.decorators import require_valid_staff_initials


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
            cursor.execute("SELECT report_name FROM report_list")
            services = cursor.fetchall()
    except Exception as e:
        flash('An error occurred while fetching data.')
        return redirect(url_for('error_page'))
    finally:
        conn.close()
        
            # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')    
        
    # Initialize resident_initials with None for GET requests
    resident_initials = None
        
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
    return render_template('report_selection.html', 
                        units=units, services=services, 
                        resident=resident_initials,
                        current_date=current_date)

@data_output_bp.route('/report_selection_logic', methods=['GET', 'POST'])
def report_selection_logic():
    if request.method == 'POST':
        unit_name = request.form.get('unit_name')
        resident_initials = request.form.get('resident_initials')
        service_name = request.form.get('service_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    else:  # Handle GET request
        unit_name = request.args.get('unit_name')
        resident_initials = request.args.get('resident_initials')
        service_name = request.args.get('service_name')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    if service_name == 'fluid chart':
        return redirect(url_for('data_output.report_fluid', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    if service_name == 'food chart':
        return redirect(url_for('data_output.report_food', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    if service_name == 'personal care chart':
        return redirect(url_for('data_output.report_personal_care', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    if service_name == 'cardex chart':
        return redirect(url_for('data_output.report_cardex', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    if service_name == 'care frequency chart':
        return redirect(url_for('data_output.report_care_frequency', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    if service_name == 'bowels observation':
        return redirect(url_for('data_output.report_bowels', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    elif service_name == 'all daily records': 
        return redirect(url_for('data_output.report_all_daily_records', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    else:
        return redirect(url_for('data_output.report_selection'))

@data_output_bp.route('/get_residents', methods=['GET'])
def get_residents():
    unit = request.args.get('unit_name')
    conn = get_connection()
    with conn.cursor() as cursor:
        query = ("SELECT resident_initials FROM resident_list WHERE resident_unit = %s")
        cursor.execute(query, (unit,))
        residents = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(residents=residents)


@data_output_bp.route('/report_fluid')
def report_fluid():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, fluid_name, fluid_volume, fluid_note, staff_initials 
        FROM fluid_chart 
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Format without seconds 
    formatted_data = []
    for row in data:
        row = list(row)
        row[1] = row[1].strftime('%d-%m-%y %H:%M')  
        formatted_data.append(row)
    return render_template('report_fluid.html', 
                        resident_initials=resident_initials,
                        start_date=start_date,
                        end_date=end_date, 
                        data=formatted_data)

def fetch_and_summarize_fluid_volume(resident_initials, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fluid_volume FROM fluid_chart 
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()
    
    total_fluid_volume = sum(row[0] for row in data)
    return total_fluid_volume

# Report food
@data_output_bp.route('/report_food')
def report_food():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, food_name, food_amount, food_note, staff_initials 
        FROM food_chart 
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Format without seconds
    formatted_data = []
    for row in data:
        row = list(row)
        row[1] = row[1].strftime('%d-%m-%y %H:%M')  # Format without seconds
        formatted_data.append(row)

    return render_template('report_food.html',
                        resident_initials=resident_initials, 
                        start_date=start_date,
                        end_date=end_date,
                        data=formatted_data)
# Report personal care    
@data_output_bp.route('/report_personal_care')
def report_personal_care():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, personal_care_type, personal_care_note, personal_care_duration, staff_initials
        FROM personal_care_chart
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    personal_care_records = cursor.fetchall()
    conn.close()
    
    # Format without seconds
    formatted_data = []
    for row in personal_care_records:
        row = list(row)
        row[1] = row[1].strftime('%d-%m-%y %H:%M')  
        formatted_data.append(row)
    
    return render_template('report_personal_care.html',
                        personal_care_records=formatted_data, 
                        unit_name=unit_name,
                        start_date=start_date,
                        end_date=end_date, 
                        resident_initials=resident_initials)
    
# Report cardex
@data_output_bp.route('/report_cardex')
def report_cardex():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, cardex_text, staff_initials 
        FROM cardex_chart 
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Format without seconds
    formatted_data = []
    for row in data:
        row = list(row)
        row[1] = row[1].strftime('%d-%m-%y %H:%M')
        formatted_data.append(row)

    return render_template('report_cardex.html', 
                        start_date=start_date,
                        end_date=end_date, 
                        resident_initials=resident_initials,
                        data=formatted_data)
    
@data_output_bp.route('/report_care_frequency')
def report_care_frequency():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, mattress_appropriate, cushion_appropriate, functionality_check, 
            pressure_areas_checked, redness_present, position, incontinence_urine, 
            incontinence_bowels, diet_intake, fluid_intake, supplement_intake, 
            staff_initials, notes
        FROM care_frequency_chart
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Format without seconds
    formatted_data = []
    for row in data:
        row = list(row)
        row[0] = row[0].strftime('%d-%m-%y %H:%M')
        formatted_data.append(row)

    return render_template('report_care_frequency.html', 
                        resident_initials=resident_initials,
                        start_date=start_date,
                        end_date=end_date, 
                        data=formatted_data)
    
@data_output_bp.route('/report_bowels')
def report_bowels():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, resident_initials, bowel_type, bowel_size, bowel_mode, bowel_note, staff_initials 
        FROM bowel_chart 
        WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Convert timestamp strings to datetime objects
    formatted_data = []
    for row in data:
        row = list(row)
        # Format the timestamp (first column)
        row[0] = row[0].strftime('%d-%m-%y %H:%M') if row[0] else ''
        formatted_data.append(row)

    return render_template('report_bowels.html', 
                    resident_initials=resident_initials,
                    start_date=start_date,
                    end_date=end_date, 
                    data=formatted_data)
    
@data_output_bp.route('/report_all_daily_records')
def report_all_daily_records():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_connection()
    cursor = conn.cursor()

    # Helper function to fetch and format records
    def fetch_and_format_records(query, params):
        cursor.execute(query, params)
        records = cursor.fetchall()
        formatted_records = []
        for record in records:
            record = list(record)
            # Format the timestamp (first column)
            record[0] = record[0].strftime('%d-%m-%y %H:%M') if record[0] else ''
            formatted_records.append(record)
        return formatted_records

    # Define queries for each chart
    queries = {
        'fluid': '''
            SELECT timestamp, fluid_name, fluid_volume, fluid_note, staff_initials 
            FROM fluid_chart 
            WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        ''',
        'food': '''
            SELECT timestamp, food_name, food_amount, food_note, staff_initials 
            FROM food_chart 
            WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        ''',
        'personal_care': '''
            SELECT timestamp, personal_care_type, personal_care_duration, personal_care_note, staff_initials 
            FROM personal_care_chart 
            WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        ''',
        'cardex': '''
            SELECT timestamp, cardex_text, staff_initials 
            FROM cardex_chart 
            WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        ''',
        'care_frequency': '''
            SELECT timestamp, mattress_appropriate, cushion_appropriate, functionality_check, 
                pressure_areas_checked, redness_present, position, incontinence_urine, 
                incontinence_bowels, diet_intake, fluid_intake, supplement_intake, 
                staff_initials, notes
            FROM care_frequency_chart
            WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        ''',
        'bowel': '''
            SELECT timestamp, bowel_type, bowel_size, bowel_mode, bowel_note, staff_initials 
            FROM bowel_chart 
            WHERE resident_initials = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        '''
    }

    # Fetch and format records for each chart
    fluid_records = fetch_and_format_records(queries['fluid'], (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    food_records = fetch_and_format_records(queries['food'], (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    personal_care_records = fetch_and_format_records(queries['personal_care'], (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    cardex_records = fetch_and_format_records(queries['cardex'], (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    care_frequency_records = fetch_and_format_records(queries['care_frequency'], (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    bowel_records = fetch_and_format_records(queries['bowel'], (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))

    conn.close()

    return render_template(
        'report_all_daily_records.html',
        resident_initials=resident_initials,
        start_date=start_date,
        end_date=end_date,
        fluid_records=fluid_records,
        food_records=food_records,
        personal_care_records=personal_care_records,
        cardex_records=cardex_records,
        care_frequency_records=care_frequency_records,
        bowel_records=bowel_records
    )