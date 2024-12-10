# C:\Users\Peter\Blueprint\app\data_input\input_modules.py
from flask import render_template, session, request, redirect, url_for, flash, jsonify
from app.data_input import data_input_bp
from app.db_connection.conn import get_connection

@data_input_bp.route('/fluid_intake')
def fluid_intake():
    session['unit_name'] = request.form.get('unit_name')
    session['resident_initials'] = request.form.get('resident_initials')
    return redirect(url_for('fluid_intake'))
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute
        ("""
            SELECT DISTINCT fluid_name FROM fluid_intake ORDER BY fluid_name 
        """)
        fluids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template ('fluid_intake.html',
        fluids=fluids, init_name=unit_name, resident_initials=resident_initials)