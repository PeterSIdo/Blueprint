import psycopg2
from flask import Flask
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import SubmitField

# Define a standalone RegistrationForm using WTForms.
class RegistrationForm(FlaskForm):
    staff_firstname = StringField('First Name', validators=[DataRequired()])
    staff_surname = StringField('Surname', validators=[DataRequired()])
    staff_initials = StringField('Initials', validators=[DataRequired(), Length(max=5)])
    staff_unique_id = StringField('Unique ID', validators=[DataRequired()])
    staff_access = StringField('Access Level', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Register')

def get_connection_nb():
    try:
        connection = psycopg2.connect(
            dbname='care6',
            user='postgres',
            password='jelszo',
            host='34.105.189.70',
            port='5432'
        )
        return connection
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None

# Mapping WTForms field types to PostgreSQL data types
FIELD_TYPE_MAPPING = {
    StringField: "VARCHAR(255)",
    PasswordField: "VARCHAR(255)"
}

def generate_create_table_query():
    # Instantiate the RegistrationForm
    form = RegistrationForm()
    # Starting with a primary key column
    column_definitions = ["id SERIAL PRIMARY KEY"]
    # Build column definitions based on form fields.
    # WTForms stores fields in the _fields attribute.
    for field_name, field in form._fields.items():
        field_type = type(field)
        sql_type = FIELD_TYPE_MAPPING.get(field_type, "TEXT")  # Default to TEXT if unknown type
        # Add NOT NULL constraint; modify as needed.
        column_definitions.append(f"{field_name} {sql_type} NOT NULL")
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS staff_list (\n  " +
        ",\n  ".join(column_definitions) +
        "\n);"
    )
    return create_table_query

def create_tables():
    connection = get_connection_nb()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        # Generate the dynamic table creation query.
        create_table_query = generate_create_table_query()
        print(f"Executing query:\n{create_table_query}")
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully.")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key"  # Required by Flask-WTF
    # Option 1: Disable CSRF if you do not need it
    # app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        # Option 2: Activate a test request context to satisfy FlaskForm requirements
        with app.test_request_context():
            create_tables()