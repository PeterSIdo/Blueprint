# Blueprint/app/staff_board/routes.py
from flask import render_template, request, redirect, url_for, flash
from app.staff_board import staff_board_bp
from app.db_connection.conn import get_connection
from datetime import datetime, timezone
from app.auth.decorators import require_valid_staff_initials
from datetime import datetime, timedelta
import uuid

from app.main.utils import get_current_uk_date


@staff_board_bp.route('/staff_board')
def staff_board():
    return render_template('staff_board.html')





@staff_board_bp.route('/create_staff_log', methods=['GET', 'POST'])
def create_staff_log():
    if request.method == 'POST':
        entry_category = request.form['entry_category']
        description = request.form['description']
        suggested_completion_time = request.form['suggested_completion_time']      
        initiator = request.form['initiator']
        completer = request.form.get('completer', '')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO staff_log (id, timestamp, entry_category, description, suggested_completion_time, initiator, completer)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (str(uuid.uuid4()), datetime.now().strftime('%Y-%m-%d %H:%M'), entry_category, description, suggested_completion_time, initiator, completer))
        conn.commit()
        conn.close()

        flash('New staff log entry created successfully!', 'success')
        return redirect(url_for('staff_board.view_staff_log'))

    return render_template('create_staff_log.html')

# VIEW staff-log
@staff_board_bp.route('/view_staff_log', methods=['GET'])
def view_staff_log():
    # Get filter parameters from request arguments
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    task_completed = request.args.get('task_completed')  # 'all', 'completed', 'not_completed'
    current_date = get_current_uk_date()

    # Connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # Build the base query
    query = 'SELECT * FROM staff_log WHERE 1=1'
    params = []


    # Add date filtering
    if start_date and end_date:
        query += ' AND timestamp BETWEEN %s AND %s'
        params.extend([start_date, end_date])

    # Debugging: Print the query and params
    print("Executing query Start date:", query)
    print("With parameters:", params)

    # Add task completion filtering
    if task_completed == 'completed':
        query += ' AND task_completed = %s'
        params.append(True)
    elif task_completed == 'not_completed':
        query += ' AND task_completed = %s'
        params.append(False)

    # Execute the query
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()
    
    # Debugging: Print the number of logs found
    print(f"Number of logs found: {len(logs)}")

    # Format the suggested_completion_time
    formatted_logs = []
    for log in logs:
        log = list(log)
        log[4] = datetime.strptime(log[4], '%Y-%m-%dT%H:%M').strftime('%d-%m-%Y %H:%M') 
        formatted_logs.append(log)
        
    print(formatted_logs)

    return render_template('report_staff_log.html', logs=formatted_logs, current_date=current_date)

# Submit staff_log
@staff_board_bp.route('/submit_staff_log', methods=['POST'])
def submit_staff_log():
    # Extract data from the form
    entry_category = request.form['entry_category']
    description = request.form['description']
    suggested_completion_time = request.form['suggested_completion_time']
    initiator = request.form['initiator']
    completer = request.form.get('completer', '')

    # Generate a timestamp for the current date and time
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Database insertion logic
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO staff_log (timestamp, entry_category, description, suggested_completion_time, initiator, completer)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (current_timestamp, entry_category, description, suggested_completion_time, initiator, completer))
    conn.commit()
    conn.close()

    flash('New staff log entry created successfully!', 'success')
    return redirect(url_for('staff_board.view_staff_log'))

# UPDATE Staff_log
@staff_board_bp.route('/update_staff_log/<log_id>', methods=['GET', 'POST'])
def update_staff_log(log_id):
    current_date=get_current_uk_date()
    if request.method == 'POST':
        completer = request.form['completer']
        task_completed = request.form.get('task_completed', 'off') == 'on'

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE staff_log
            SET completer = %s, task_completed = %s
            WHERE id = %s
        ''', (completer, task_completed, log_id))
        conn.commit()
        conn.close()

        flash('Staff log entry updated successfully!', 'success')
        return redirect(url_for('staff_board.view_staff_log'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM staff_log WHERE id = %s', (log_id,))
    log = cursor.fetchone()
    conn.close()

    return render_template('update_staff_log.html', log=log, current_date=current_date)