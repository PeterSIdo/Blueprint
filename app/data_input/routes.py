# C:\Users\Peter\Blueprint\app\templates\collect_data.html
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



                    