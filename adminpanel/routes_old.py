# C:\Users\Peter\Blueprint\adminpanel\routes.py
from flask import render_template, redirect, url_for, request
#from app.admin import admin_bp
from app.db_connection.conn import get_connection
from psycopg2 import sql
from adminpanel import adminpanel_bp

@adminpanel_bp.route('/admin_menu')
def admin_menu():
    return render_template('admin_menu.html')

@adminpanel_bp.route('/admin/residents')
def admin_residents():
    connection = get_connection()
    if connection is None:
        return "Error connecting to the database."

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM resident_list")
    residents = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('admin_residents.html', residents=residents)

@adminpanel_bp.route('/admin/residents/add', methods=['GET', 'POST'])
def add_resident():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        unit = request.form['unit']
        room = request.form['room']
        initials = request.form['initials']
        unique_id = request.form['unique_id']
        notes = request.form['notes']

        connection = get_connection()
        if connection is None:
            return "Error connecting to the database."

        cursor = connection.cursor()
        insert_query = sql.SQL("""
            INSERT INTO resident_list (resident_firstname, resident_surname, resident_unit, resident_room, resident_initials, resident_unique_id, resident_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (firstname, surname, unit, room, initials, unique_id, notes))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('adminpanel.admin_residents'))

    return render_template('add_resident.html')