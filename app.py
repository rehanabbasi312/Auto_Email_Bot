import pyodbc
from flask import Flask, request, render_template, abort

app = Flask(__name__)

# Database connection parameters
db_host = '85.13.199.236,58641'
db_user = 'EPEmailBot'
db_password = 'EPEmailBot'
db_database = 'EPC_Email_Bot'

def get_db_connection():
    """Establish a database connection."""
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_database};UID={db_user};PWD={db_password}'
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        abort(500, description="Database connection error.")

@app.route('/<form_type>', methods=['GET', 'POST'])
def form(form_type):
    """Handle form submissions and display forms based on the type."""
    guid = request.args.get('guid')
    clear_form = request.args.get('clear_form', 'false') == 'true'

    if form_type not in ['form1', 'form2', 'form3', 'form4', 'form5', 'unidentified']:
        return "Invalid form type", 400

    if request.method == 'POST':
        guid = request.form.get('guid')
        if not guid:
            return "GUID is missing", 400

        conn = get_db_connection()
        cursor = conn.cursor()

        table_name = {
            'form1': 'risk_fraud',
            'form2': 'risk_ownership',
            'form3': 'epc_raast',
            'form4': 'epc_bill_complaint',
            'form5': 'epc_account_opening_complaint',
            'unidentified': 'unidentified'
        }.get(form_type)

        file_field_name = 'cnic_scan' if form_type == 'form1' else 'customer_consent' if form_type == 'form2' else 'customer_cnic' if  form_type == 'form5' else None

        file_data = None
        if file_field_name != 'none':
            file = request.files.get(file_field_name)
            if file and file.filename:
                file_data = file.read()

        try:
            if form_type == 'form1':
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET msisdn = ?, channel = ?, customer_location = ?, blocking_reason = ?, comments = ?, cnic_scan = ?
                    WHERE guid = ?
                """, (request.form.get('msisdn'), request.form.get('channel'), request.form.get('customer_location'),
                      request.form.get('blocking_reason'), request.form.get('comments'), file_data, guid))

            elif form_type == 'form2':
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET msisdn = ?, channel = ?, customer_location = ?, reason_of_restoration = ?, other_details = ?, comments = ?, customer_consent = ?
                    WHERE guid = ?
                """, (request.form.get('msisdn'), request.form.get('channel'), request.form.get('customer_location'),
                      request.form.get('reason_of_restoration'), request.form.get('other_details'), request.form.get('comments'), file_data, guid))

            elif form_type == 'form3':
                transaction_amount = request.form.get('transaction_amount', '').strip()
                transaction_id = request.form.get('transaction_id', '').strip()

                if not transaction_amount:
                    return "Transaction amount cannot be empty.", 400

                try:
                    transaction_amount = float(transaction_amount)
                except ValueError:
                    return "Invalid transaction amount. It must be a valid number.", 400

                if len(transaction_id) == 0:
                    return "Invalid transaction ID. It must not be empty.", 400

                cursor.execute(f"""
                    UPDATE {table_name}
                    SET msisdn = ?, channel = ?, customer_location = ?, transaction_amount = ?, transaction_id = ?, receiver_alias = ?, iban_number = ?, comments = ?
                    WHERE guid = ?
                """, (request.form.get('msisdn'), request.form.get('channel'), request.form.get('customer_location'),
                      transaction_amount, transaction_id, request.form.get('receiver_alias'), request.form.get('iban_number')
                      , request.form.get('comments'), guid))

            elif form_type == 'form4':
                transaction_amount = request.form.get('transaction_amount', '').strip()
                transaction_id = request.form.get('transaction_id', '').strip()

                if not transaction_amount:
                    return "Transaction amount cannot be empty.", 400

                try:
                    transaction_amount = float(transaction_amount)
                except ValueError:
                    return "Invalid transaction amount. It must be a valid number.", 400

                if len(transaction_id) == 0:
                    return "Transaction ID cannot be empty.", 400

                cursor.execute(f"""
                    UPDATE {table_name}
                    SET msisdn = ?, channel = ?, customer_location = ?, biller_name = ?, consumer_number = ?, transaction_amount = ?, transaction_id = ?, reason = ?, comments = ?
                    WHERE guid = ?
                """, (request.form.get('msisdn'), request.form.get('channel'), request.form.get('customer_location'),
                      request.form.get('biller_name'), request.form.get('consumer_number'), transaction_amount,
                      transaction_id, request.form.get('reason'), request.form.get('comments'), guid))

            elif form_type == 'form5':
                error_message = request.form.get('error_message', '').strip()
                duration = request.form.get('duration', '').strip()
                transaction_type = request.form.get('transaction_type', '').strip()
                customer_cnic = request.form.get('customer_cnic', '').strip()

                cursor.execute(f"""
                    UPDATE {table_name}
                    SET msisdn = ?, channel = ?, customer_location = ?, error_message = ?, duration = ?, transaction_type = ?, customer_cnic = ?, comments = ?
                    WHERE guid = ?
                """, (request.form.get('msisdn'), request.form.get('channel'), request.form.get('customer_location'),
                      request.form.get('error_message'), request.form.get('duration'), request.form.get('transaction_type'), 
                      file_data, request.form.get('comments'), guid))
                

            elif form_type == 'unidentified':
               
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET msisdn = ?, channel = ?, customer_location = ?, comments = ?, reason_of_restoration=?
                    WHERE guid = ?
                """, (request.form.get('msisdn'), request.form.get('channel'), request.form.get('customer_location'),
                      request.form.get('comments'),
                      request.form.get('reason_of_restoration'), guid))
                      
            conn.commit()

            cursor.execute(f"SELECT id FROM {table_name} WHERE guid = ?", (guid,))
            ticket_id = cursor.fetchone()[0]

            return render_template('confirmation.html', ticket_id=ticket_id, form_type=form_type)

        except Exception as e:
            conn.rollback()
            print(f"Error updating {form_type} data: {e}")
            return "An error occurred while updating the data", 500

        finally:
            conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()

    table_name = {
        'form1': 'risk_fraud',
        'form2': 'risk_ownership',
        'form3': 'epc_raast',
        'form4': 'epc_bill_complaint',
        'form5': 'epc_account_opening_complaint',
        'unidentified': 'unidentified'
    }.get(form_type)

    if not clear_form and guid:
        cursor.execute(f"SELECT * FROM {table_name} WHERE guid = ?", (guid,))
        data = cursor.fetchone()

        if not data:
            conn.close()
            #return "No data found", 404
            return render_template('no_data.html')  # Render the no data found page

        form_data = {
            'msisdn': data.msisdn,
            'channel': data.channel,
            'customer_location': data.customer_location,
            'comments': data.comments,
            'blocking_reason': data.blocking_reason if form_type == 'form1' else '',
            'reason_of_restoration': data.reason_of_restoration if form_type == 'form2' else '',
            'other_details': data.other_details if form_type == 'form2' else '',
            'transaction_amount': data.transaction_amount if form_type in ['form3', 'form4'] else '',
            'transaction_id': data.transaction_id if form_type in ['form3', 'form4'] else '',
            'receiver_alias': data.receiver_alias if form_type == 'form3' else '',
            'iban_number': data.iban_number if form_type == 'form3' else '',
            'date_of_transaction': data.date_of_transaction if form_type == 'form3' else '',
            'biller_name': data.biller_name if form_type == 'form4' else '',
            'consumer_number': data.consumer_number if form_type == 'form4' else '',
            'reason': data.reason if form_type == 'form4' else '',
            'error_message': data.error_message if form_type == 'form5' else '',
            'duration': data.duration if form_type == 'form5' else '',
            'transaction_type': data.transaction_type if form_type == 'form5' else '',
            'customer_cnic': data.customer_cnic if form_type == 'form5' else ''
        }
    else:
        form_data = {key: '' for key in (
            'msisdn', 'channel', 'customer_location', 'comments', 
            'blocking_reason', 'reason_of_restoration', 'other_details', 
            'transaction_amount', 'transaction_id', 'receiver_alias', 
            'iban_number', 'date_of_transaction', 'biller_name', 
            'consumer_number', 'reason', 'error_message', 'duration', 
            'transaction_type', 'customer_cnic'
        )}
        
    conn.close()
    return render_template(f'{form_type}.html', form_data=form_data, guid=guid)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
