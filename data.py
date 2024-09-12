import pyodbc
from datetime import datetime

def insertDataIntoRiskFraudTable(guid, identifiedMsisdn, channel, identifiedLocation, blocking_reason, comments, current_time, cnic_scan):
    print(f"Inserting into Risk Fraud Table:")
    print(f"GUID: {guid}")
    print(f"MSISDN: {identifiedMsisdn}")
    print(f"Channel: {channel}")
    print(f"Location: {identifiedLocation}")
    print(f"Blocking Reason: {blocking_reason}")
    print(f"Comments: {comments}")
    print(f"Date Time: {current_time}")
    print(f"CNIC Scan: {cnic_scan}")
    
    try:
        # Establish connection to the database
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=85.13.199.236,58641;DATABASE=EPC_Email_Bot;UID=EPEmailBot;PWD=EPEmailBot')
        cursor = connection.cursor()
        
        # Define the SQL query
        query = """
        INSERT INTO risk_fraud (
            guid, msisdn, channel, customer_location, blocking_reason, comments, 
            created_at, cnic_scan
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Convert cnic_scan to binary if it's not None
        if isinstance(cnic_scan, str) and cnic_scan.lower() != 'unidentified':
            cnic_scan_value = cnic_scan.encode()  # Convert string to bytes
        else:
            cnic_scan_value = None  # Use None for NULL values
        
        # Execute the query
        cursor.execute(query, (guid, identifiedMsisdn, channel, identifiedLocation, blocking_reason, comments, current_time, cnic_scan_value))
        connection.commit()
        print("Data inserted successfully into risk_fraud.")
        
    except pyodbc.Error as e:
        print(f"Error inserting data into risk_fraud table: {e}")
        
    finally:
        cursor.close()
        connection.close()


def insertDataIntoRiskOwnershipTable(guid, msisdn, channel, customer_location, reason_of_restoration, comments, other_details, created_at, customer_consent):
    
    print(f"Inserting into Risk Ownership Table:")
    print(f"GUID: {guid}")
    print(f"MSISDN: {msisdn}")
    print(f"Channel: {channel}")
    print(f"Location: {customer_location}")
    print(f"Restoration Reason: {reason_of_restoration}")
    print(f"Comments: {comments}")
    print(f"Other Details: {other_details}")
    print(f"Date Time: {created_at}")
    print(f"Customer Consent: {customer_consent}")
    
    try:
        # Connect to the database
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=85.13.199.236,58641;DATABASE=EPC_Email_Bot;UID=EPEmailBot;PWD=EPEmailBot')
        cursor = connection.cursor()
        
        # Define the SQL query
        query = """
        INSERT INTO risk_ownership (
            guid, msisdn, channel, customer_location, reason_of_restoration, comments, other_details, created_at, customer_consent
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

         # Convert customer_consent to binary if it's not None
        if isinstance(customer_consent, str) and customer_consent.lower() != 'unidentified':
            customer_consent_value = customer_consent.encode()  # Convert string to bytes
        else:
            customer_consent_value = None  # Use None for NULL values
        
        # Prepare the data for insertion
        data = (guid, msisdn, channel, customer_location, reason_of_restoration, comments, other_details, created_at, customer_consent_value)
        
        # Execute the query
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully into risk_ownership.")
        
    except pyodbc.Error as e:
        print(f"Error inserting data into risk_ownership table: {e}")
        
    finally:
        cursor.close()
        connection.close()

def insertDataIntoEpcRaastTable(guid, msisdn, channel, customer_location, transaction_amount, transaction_id, receiver_alias, iban_number, date_of_transaction, comments):
    print(f"Inserting into EPC Raast Table:")
    print(f"GUID: {guid}")
    print(f"MSISDN: {msisdn}")
    print(f"Channel: {channel}")
    print(f"Customer Location: {customer_location}")
    print(f"Transaction Amount: {transaction_amount}")
    print(f"Transaction ID: {transaction_id}")
    print(f"Receiver Alias: {receiver_alias}")
    print(f"IBAN Number: {iban_number}")
    print(f"Date of Transaction: {date_of_transaction}")
    print(f"Comments: {comments}")
    
    try:
        # Establish connection to the database
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=85.13.199.236,58641;DATABASE=EPC_Email_Bot;UID=EPEmailBot;PWD=EPEmailBot')
        cursor = connection.cursor()
        
        # Define the SQL query
        query = """
        INSERT INTO epc_raast (
            guid, msisdn, channel, customer_location, transaction_amount, transaction_id, receiver_alias, iban_number, date_of_transaction, comments
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Prepare the data for insertion
        data = (guid, msisdn, channel, customer_location, transaction_amount, transaction_id, receiver_alias, iban_number, date_of_transaction, comments)
        
        # Execute the query
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully into epc_raast.")
        
    except pyodbc.Error as e:
        print(f"Error inserting data into epc_raast table: {e}")
        
    finally:
        cursor.close()
        connection.close()



def insertDataIntoEpcBillComplaintTable(guid, msisdn, channel, customer_location, biller_name, consumer_number, transaction_amount, transaction_id, reason, comments, created_at):
    print(f"Inserting into EPC Bill Complaint Table:")
    print(f"GUID: {guid}")
    print(f"MSISDN: {msisdn}")
    print(f"Channel: {channel}")
    print(f"Customer Location: {customer_location}")
    print(f"Biller Name: {biller_name}")
    print(f"Consumer Number: {consumer_number}")
    print(f"Transaction Amount: {transaction_amount}")
    print(f"Transaction ID: {transaction_id}")
    print(f"Reason: {reason}")
    print(f"Comments: {comments}")
    print(f"Created_At: {created_at}")

    
    try:
        # Establish connection to the database
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=85.13.199.236,58641;DATABASE=EPC_Email_Bot;UID=EPEmailBot;PWD=EPEmailBot')
        cursor = connection.cursor()
        
        # Define the SQL query
        query = """
        INSERT INTO epc_bill_complaint (
            guid, msisdn, channel, customer_location, biller_name, consumer_number, transaction_amount, transaction_id, reason, comments, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Prepare the data for insertion
        data = (guid, msisdn, channel, customer_location, biller_name, consumer_number, transaction_amount, transaction_id, reason, comments, created_at)
        
        # Execute the query
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully into epc_bill_complaint.")
        
    except pyodbc.Error as e:
        print(f"Error inserting data into epc_bill_complaint table: {e}")
        
    finally:
        cursor.close()
        connection.close()


import pyodbc

def insertDataIntoEpcAccountOpeningComplaintTable(guid, msisdn, channel, customer_location, error_message, duration, transaction_type, customer_cnic, comments, created_at):
    print(f"Inserting into EPC Account Opening Complaint Table:")
    print(f"GUID: {guid}")
    print(f"MSISDN: {msisdn}")
    print(f"Channel: {channel}")
    print(f"Customer Location: {customer_location}")
    print(f"Error Message: {error_message}")
    print(f"Duration: {duration}")
    print(f"Transaction Type: {transaction_type}")
    print(f"Customer CNIC: {customer_cnic}")
    print(f"Comments: {comments}")
    print(f"Created At: {created_at}")

    try:
        # Establish connection to the database
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=85.13.199.236,58641;DATABASE=EPC_Email_Bot;UID=EPEmailBot;PWD=EPEmailBot')
        cursor = connection.cursor()
        
        # Define the SQL query
        query = """
        INSERT INTO epc_account_opening_complaint (
            guid, msisdn, channel, customer_location, error_message, duration, transaction_type, customer_cnic, comments, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Convert customer_cnic to binary if it's not None
        if isinstance(customer_cnic, str) and customer_cnic.lower() != 'unidentified':
            customer_cnic_value = customer_cnic.encode()  # Convert string to bytes
        else:
            customer_cnic_value = None  # Use None for NULL values
        
        # Prepare the data for insertion
        data = (guid, msisdn, channel, customer_location, error_message, duration, transaction_type, customer_cnic_value, comments, created_at)
        
        # Execute the query
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully into epc_account_opening_complaint.")
        
    except pyodbc.Error as e:
        print(f"Error inserting data into epc_account_opening_complaint table: {e}")
        
    finally:
        cursor.close()
        connection.close()


def insertDataIntoUnidentified(guid, identifiedMsisdn, channel, identifiedLocation, reason_of_restoration, comments, current_time):
    print(f"Inserting into Unidentified Table:")
    print(f"GUID: {guid}")
    print(f"MSISDN: {identifiedMsisdn}")
    print(f"Channel: {channel}")
    print(f"Location: {identifiedLocation}")
    print(f"Blocking Reason: {reason_of_restoration}")
    print(f"Comments: {comments}")
    print(f"Date Time: {current_time}")
    
    try:
        # Establish connection to the database
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=85.13.199.236,58641;DATABASE=EPC_Email_Bot;UID=EPEmailBot;PWD=EPEmailBot')
        cursor = connection.cursor()
        
        # Define the SQL query
        query = """
        INSERT INTO unidentified (
            guid, msisdn, channel, customer_location, reason_of_restoration, comments, 
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    
        # Execute the query
        cursor.execute(query, (guid, identifiedMsisdn, channel, identifiedLocation, reason_of_restoration, comments, current_time))
        connection.commit()
        print("Data inserted successfully into unidentified.")
        
    except pyodbc.Error as e:
        print(f"Error inserting data into unidentified table: {e}")
        
    finally:
        cursor.close()
        connection.close()

