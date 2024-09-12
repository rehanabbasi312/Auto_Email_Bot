import imaplib
import smtplib
import email
import uuid
from datetime import datetime
import pytz
import re
from data import insertDataIntoRiskFraudTable, insertDataIntoRiskOwnershipTable, insertDataIntoEpcRaastTable, insertDataIntoEpcBillComplaintTable, insertDataIntoEpcAccountOpeningComplaintTable, insertDataIntoUnidentified

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                body += part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()
    return body


def extract_Imp_Info(email_body, category):
    # Default values for extraction
    identifiedID = "Unidentified"
    identifiedMsisdn = "Unidentified"
    identifiedLocation = "Unidentified"
    identifiedBlockingReason = "Unidentified"
    identifiedRestorationReason = "Unidentified"
    identifiedComments = "Unidentified"
    identifiedOtherDetails = "Unidentified"
    identifiedChannel = "Unidentified"
    identifiedTransactionAmount = 0.0  # Default to 0.0
    identifiedTransactionID = "Unidentified"
    identifiedReceiverAlias = "Unidentified"
    identifiedIbanNumber = "Unidentified"
    identifiedDateOfTransaction = "Unidentified"
    identifiedBillerName = "Unidentified"
    identifiedConsumerNumber = "Unidentified"
    identifiedReason = "Unidentified"
    identifiedGUID = "Unidentified"
    identifiedCustomerLocation = "Unidentified"
    identifiedErrorMessage = "Unidentified"
    identifiedDuration = "Unidentified"
    identifiedTransactionType = "Unidentified"
    identifiedCustomerCNIC = "Unidentified"
    identifiedCreatedAt = "Unidentified"

    if category == "form1":
        contact_number_pattern = re.compile(r'\b(?:\+?\d{1,3}\s?)?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,9}\b')
        transaction_id_pattern = re.compile(r'\bID#[0-9]+\b', re.IGNORECASE)
        channel_pattern = re.compile(r'\b(app|website|mobile\sapp|portal|web|application|site)\b', re.IGNORECASE)

        contact_matches = contact_number_pattern.findall(email_body)
        transaction_id_matches = transaction_id_pattern.findall(email_body)
        channel_matches = channel_pattern.findall(email_body)

        identifiedID = transaction_id_matches[0] if transaction_id_matches else identifiedID
        identifiedMsisdn = contact_matches[0] if contact_matches else identifiedMsisdn
        identifiedChannel = channel_matches[0] if channel_matches else identifiedChannel
        identifiedBlockingReason = email_body
        identifiedComments = ""

    elif category == "form2":
        restoration_reason_pattern = re.compile(r'reason\s*of\s*restoration:?\s*(.*)', re.IGNORECASE)
        other_details_pattern = re.compile(r'other\s*details:?\s*(.*)', re.IGNORECASE)
        consent_pattern = re.compile(r'customer\s*consent:?\s*(.*)', re.IGNORECASE)
        channel_pattern = re.compile(r'\b(app|website|mobile\sapp|portal|web|application|site)\b', re.IGNORECASE)

        restoration_reason_matches = restoration_reason_pattern.findall(email_body)
        other_details_matches = other_details_pattern.findall(email_body)
        consent_matches = consent_pattern.findall(email_body)
        channel_matches = channel_pattern.findall(email_body)

        identifiedRestorationReason = email_body
        identifiedOtherDetails = other_details_matches[0] if other_details_matches else identifiedOtherDetails
        identifiedChannel = channel_matches[0] if channel_matches else identifiedChannel
        identifiedComments = ""

    elif category == "form3":
        msisdn_pattern = re.compile(r'\b(?:\+?\d{1,3}\s?)?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,9}\b')
        channel_pattern = re.compile(r'\b(app|website|mobile\sapp|portal|web|application|site)\b', re.IGNORECASE)
        transaction_amount_pattern = re.compile(r'transaction\s*amount:?\s*([\d,.]+)', re.IGNORECASE)
        transaction_id_pattern = re.compile(r'transaction\s*id:?\s*(\S+)', re.IGNORECASE)
        receiver_alias_pattern = re.compile(r'receiver\s*alias:?\s*(\S+)', re.IGNORECASE)
        iban_number_pattern = re.compile(r'iban\s*number:?\s*(\S+)', re.IGNORECASE)
        date_of_transaction_pattern = re.compile(r'date\s*of\s*transaction:?\s*([\d/-]+)', re.IGNORECASE)
        comments_pattern = re.compile(r'comments:?\s*(.*)', re.IGNORECASE)

        msisdn_matches = msisdn_pattern.findall(email_body)
        channel_matches = channel_pattern.findall(email_body)
        transaction_amount_matches = transaction_amount_pattern.findall(email_body)
        transaction_id_matches = transaction_id_pattern.findall(email_body)
        receiver_alias_matches = receiver_alias_pattern.findall(email_body)
        iban_number_matches = iban_number_pattern.findall(email_body)
        date_of_transaction_matches = date_of_transaction_pattern.findall(email_body)
        comments_matches = comments_pattern.findall(email_body)

        identifiedMsisdn = msisdn_matches[0] if msisdn_matches else identifiedMsisdn
        identifiedChannel = channel_matches[0] if channel_matches else identifiedChannel
        identifiedTransactionAmount = float(transaction_amount_matches[0].replace(',', '')) if transaction_amount_matches else identifiedTransactionAmount
        identifiedTransactionID = transaction_id_matches[0] if transaction_id_matches else identifiedTransactionID
        identifiedReceiverAlias = receiver_alias_matches[0] if receiver_alias_matches else identifiedReceiverAlias
        identifiedIbanNumber = iban_number_matches[0] if iban_number_matches else identifiedIbanNumber
        identifiedDateOfTransaction = date_of_transaction_matches[0] if date_of_transaction_matches else identifiedDateOfTransaction
        identifiedComments = comments_matches[0] if comments_matches else identifiedComments

    elif category == "form4":
        epc_amount_pattern = re.compile(r'epc\s*bill\s*amount\s*not\s*updated:?\s*([\d,.]+)', re.IGNORECASE)
        msisdn_pattern = re.compile(r'\b(?:\+?\d{1,3}\s?)?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,9}\b')
        channel_pattern = re.compile(r'\b(app|website|mobile\sapp|portal|web|application|site)\b', re.IGNORECASE)
        biller_name_pattern = re.compile(r'biller\s*name:?\s*(\S+)', re.IGNORECASE)
        consumer_number_pattern = re.compile(r'consumer\s*number:?\s*(\S+)', re.IGNORECASE)
        transaction_amount_pattern = re.compile(r'transaction\s*amount:?\s*([\d,.]+)', re.IGNORECASE)
        transaction_id_pattern = re.compile(r'transaction\s*id:?\s*(\S+)', re.IGNORECASE)
        reason_pattern = re.compile(r'reason:?\s*(.*)', re.IGNORECASE)
        comments_pattern = re.compile(r'comments:?\s*(.*)', re.IGNORECASE)

        epc_amount_matches = epc_amount_pattern.findall(email_body)
        msisdn_matches = msisdn_pattern.findall(email_body)
        channel_matches = channel_pattern.findall(email_body)
        biller_name_matches = biller_name_pattern.findall(email_body)
        consumer_number_matches = consumer_number_pattern.findall(email_body)
        transaction_amount_matches = transaction_amount_pattern.findall(email_body)
        transaction_id_matches = transaction_id_pattern.findall(email_body)
        reason_matches = reason_pattern.findall(email_body)
        comments_matches = comments_pattern.findall(email_body)

        identifiedMsisdn = msisdn_matches[0] if msisdn_matches else identifiedMsisdn
        identifiedChannel = channel_matches[0] if channel_matches else identifiedChannel
        identifiedBillerName = biller_name_matches[0] if biller_name_matches else identifiedBillerName
        identifiedConsumerNumber = consumer_number_matches[0] if consumer_number_matches else identifiedConsumerNumber
        identifiedTransactionAmount = float(transaction_amount_matches[0].replace(',', '')) if transaction_amount_matches else identifiedTransactionAmount
        identifiedTransactionID = transaction_id_matches[0] if transaction_id_matches else identifiedTransactionID
        identifiedReason = reason_matches[0] if reason_matches else identifiedReason
        identifiedComments = comments_matches[0] if comments_matches else identifiedComments

    elif category == "form5":
        id_pattern = re.compile(r'\bID:\s*(\S+)', re.IGNORECASE)
        guid_pattern = re.compile(r'\bGUID:\s*(\S+)', re.IGNORECASE)
        msisdn_pattern = re.compile(r'\b(?:\+?\d{1,3}\s?)?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,9}\b')
        channel_pattern = re.compile(r'\b(app|website|mobile\sapp|portal|web|application|site)\b', re.IGNORECASE)
        customer_location_pattern = re.compile(r'customer\s*location:?\s*(.*)', re.IGNORECASE)
        error_message_pattern = re.compile(r'error\s*message:?\s*(.*)', re.IGNORECASE)
        duration_pattern = re.compile(r'duration:?\s*(.*)', re.IGNORECASE)
        transaction_type_pattern = re.compile(r'transaction\s*type:?\s*(.*)', re.IGNORECASE)
        customer_cnic_pattern = re.compile(r'customer\s*cnic:?\s*(\S+)', re.IGNORECASE)
        comments_pattern = re.compile(r'comments:?\s*(.*)', re.IGNORECASE)
        created_at_pattern = re.compile(r'created\s*at:?\s*(.*)', re.IGNORECASE)

        id_matches = id_pattern.findall(email_body)
        guid_matches = guid_pattern.findall(email_body)
        msisdn_matches = msisdn_pattern.findall(email_body)
        channel_matches = channel_pattern.findall(email_body)
        customer_location_matches = customer_location_pattern.findall(email_body)
        error_message_matches = error_message_pattern.findall(email_body)
        duration_matches = duration_pattern.findall(email_body)
        transaction_type_matches = transaction_type_pattern.findall(email_body)
        customer_cnic_matches = customer_cnic_pattern.findall(email_body)
        comments_matches = comments_pattern.findall(email_body)
        created_at_matches = created_at_pattern.findall(email_body)

        identifiedID = id_matches[0] if id_matches else identifiedID
        identifiedGUID = guid_matches[0] if guid_matches else identifiedGUID
        identifiedMsisdn = msisdn_matches[0] if msisdn_matches else identifiedMsisdn
        identifiedChannel = channel_matches[0] if channel_matches else identifiedChannel
        identifiedCustomerLocation = customer_location_matches[0] if customer_location_matches else identifiedCustomerLocation
        identifiedErrorMessage = error_message_matches[0] if error_message_matches else identifiedErrorMessage
        identifiedDuration = duration_matches[0] if duration_matches else identifiedDuration
        identifiedTransactionType = transaction_type_matches[0] if transaction_type_matches else identifiedTransactionType
        identifiedCustomerCNIC = customer_cnic_matches[0] if customer_cnic_matches else identifiedCustomerCNIC
        identifiedComments = comments_matches[0] if comments_matches else identifiedComments
        identifiedCreatedAt = created_at_matches[0] if created_at_matches else identifiedCreatedAt


    elif category == "unidentified":
        msisdn_pattern = re.compile(r'\b(?:\+?\d{1,3}\s?)?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,9}\b')
        channel_pattern = re.compile(r'\b(app|website|mobile\sapp|portal|web|application|site)\b', re.IGNORECASE)
        customer_location_pattern = re.compile(r'customer\s*location:?\s*(.*)', re.IGNORECASE)
        comments_pattern = re.compile(r'comments:?\s*(.*)', re.IGNORECASE)

        msisdn_matches = msisdn_pattern.findall(email_body)
        channel_matches = channel_pattern.findall(email_body)
        customer_location_matches = customer_location_pattern.findall(email_body)
        comments_matches = comments_pattern.findall(email_body)

        identifiedMsisdn = msisdn_matches[0] if msisdn_matches else identifiedMsisdn
        identifiedChannel = channel_matches[0] if channel_matches else identifiedChannel
        identifiedCustomerLocation = customer_location_matches[0] if customer_location_matches else identifiedCustomerLocation
        identifiedComments = comments_matches[0] if comments_matches else identifiedComments

    current_datetime_pkt = datetime.now(pytz.timezone('Asia/Karachi'))

    return (identifiedID, identifiedMsisdn, identifiedLocation, identifiedBlockingReason, identifiedRestorationReason, 
            identifiedComments, identifiedOtherDetails, identifiedChannel, identifiedTransactionAmount, 
            identifiedTransactionID, identifiedReceiverAlias, identifiedIbanNumber, identifiedDateOfTransaction, 
            identifiedBillerName, identifiedConsumerNumber, identifiedReason, identifiedGUID, 
            identifiedCustomerLocation, identifiedErrorMessage, identifiedDuration, identifiedTransactionType, 
            identifiedCustomerCNIC, identifiedCreatedAt, current_datetime_pkt)


def extract_first_email_address(email_string):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_string)
    return match.group(0) if match else None

EMAIL = 'easypaisa@blinkitech.com'
PASSWORD = 'Telenor@123'
IMAP_SERVER = 'mail.blinkitech.com'
IMAP_PORT = 993
SMTP_SERVER = 'mail.blinkitech.com'
SMTP_PORT = 465

def check_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    result, data = mail.search(None, 'UNSEEN')

    if result == 'OK':
        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                sender_email = extract_first_email_address(msg['From'])  # Extract sender email address

                body = get_email_body(msg)  # Extract email body here
                guid = str(uuid.uuid4())
                current_datetime_pkt = datetime.now(pytz.timezone('Asia/Karachi'))

                identifiedIssue = categorize_email(body)

                (identifiedID, identifiedMsisdn, identifiedLocation, 
                 identifiedBlockingReason, identifiedRestorationReason, 
                 identifiedComments, identifiedOtherDetails, 
                 identifiedChannel, identifiedTransactionAmount, 
                 identifiedTransactionID, identifiedReceiverAlias,
                 identifiedIbanNumber, identifiedDateOfTransaction, identifiedBillerName,
                 identifiedConsumerNumber, identifiedReason, identifiedGUID, 
                 identifiedCustomerLocation, identifiedErrorMessage, 
                 identifiedDuration, identifiedTransactionType, 
                 identifiedCustomerCNIC, identifiedCreatedAt, 
                 current_datetime_pkt) = extract_Imp_Info(body, identifiedIssue)

                cnic_scan = ""  # Define variable for scan_cnic
                customer_consent = ""  # Define variable for customer_consent

                if identifiedIssue == "form1":
                    insertDataIntoRiskFraudTable(guid, identifiedMsisdn, identifiedChannel, identifiedLocation,
                                                  identifiedBlockingReason, identifiedComments, current_datetime_pkt, cnic_scan)
                elif identifiedIssue == "form2":
                    insertDataIntoRiskOwnershipTable(guid, identifiedMsisdn, identifiedChannel, identifiedLocation,
                                                      identifiedRestorationReason, identifiedComments, identifiedOtherDetails,
                                                      current_datetime_pkt, customer_consent)
                elif identifiedIssue == "form3":
                    insertDataIntoEpcRaastTable(guid, identifiedMsisdn, identifiedChannel, identifiedLocation,
                                                 identifiedTransactionAmount, identifiedTransactionID, identifiedReceiverAlias,
                                                 identifiedIbanNumber, current_datetime_pkt, identifiedComments)
                elif identifiedIssue == "form4":
                    insertDataIntoEpcBillComplaintTable(guid, identifiedMsisdn, identifiedChannel, identifiedLocation,
                                                         identifiedBillerName, identifiedConsumerNumber, identifiedTransactionAmount,
                                                         identifiedTransactionID, identifiedReason, identifiedComments, current_datetime_pkt)
                elif identifiedIssue == "form5":
                    insertDataIntoEpcAccountOpeningComplaintTable(guid, identifiedMsisdn, identifiedChannel, identifiedLocation,
                                                                 identifiedErrorMessage,identifiedDuration,identifiedTransactionType,
                                                                 identifiedCustomerCNIC,identifiedComments, current_datetime_pkt)
                elif identifiedIssue == "unidentified":
                    insertDataIntoUnidentified(guid, identifiedMsisdn, identifiedChannel, identifiedLocation,
                                            identifiedComments,identifiedRestorationReason, current_datetime_pkt)
                    
                # Send a response email to the sender
                reply_to_sender(sender_email, msg, guid, identifiedIssue)
                
                mail.store(num, '+FLAGS', '\\Seen')  # Mark the email as read

    mail.close()
    mail.logout()



def categorize_email(body):
    body_lower = body.lower()
    
    fraud_keywords = ['fraud', 'unknown payments', 'refund', 'unauthorized', 'unrecognized', 'blocked account', 'blocked', 'transaction issue']
    if any(keyword in body_lower for keyword in fraud_keywords):
        return "form1"
    
    ownership_keywords = ['account restoration', 'proof provided', 'Account block ho gya','blocking reason', 'ownership', 'customer consent', 'payment details', 'account issues']
    if any(keyword in body_lower for keyword in ownership_keywords):
        return "form2"
    
    raast_keywords = ['amount send kithi receiver ko ni mili', 'money transfer ni hui', 'notrecieved']
    if any(keyword in body_lower for keyword in raast_keywords):
        print("Form3 Identified")  # Debug print
        return "form3"
    
    bill_keywords = ['bill not updated', 'my utility bill issue', 'bill is unpaid', 'pay electricity bill but having issue', 'bill not show and show late', 'main ny bill pay kiya lekin wo ni huwa', 'bill ka masla aa raha hai']
    if any(keyword in body_lower for keyword in bill_keywords):
        print("Form4 Identified")  # Debug print
        return "form4"
    
    account_opening_keywords = ['account opening issue', 'unable to open account', 'problem with account setup', 'error during account registration', 'account opening process', 'error message during registration', 'account opening may issue aa raha hai', 'mera easypaisa account ni ban raha']
    if any(keyword in body_lower for keyword in account_opening_keywords):
        print("Form5 Identified")  # Debug print
        return "form5"
    
    print("Unidentified Category")  # Debug print
    return "unidentified"


def reply_to_sender(sender, msg, guid, identifiedIssue):
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL, PASSWORD)

        subject = "Acknowledgement of Your Query: We're Here to Help!"
        
        url = f"https://emailbotforms-cwemamhmhnh7beaa.eastus-01.azurewebsites.net/{identifiedIssue.replace(' ', '_').lower()}?guid={guid}"
        
        body = f"""
        Dear Customer,

        I hope this email finds you well.

        I wanted to take a moment to acknowledge the query you recently submitted to us. Your feedback and inquiries are invaluable to us as they help us continually improve our services to better meet your needs.

        Additionally, if you ever encounter any issues or have feedback about our services, we encourage you to use our dedicated complaints portal, where you can share your concerns transparently. You can access the portal through the following link:
        {url}

        Thank you for your attention.

        Best Regards,
        Your Support Team
        """
        
        msg = email.message.EmailMessage()
        msg['From'] = EMAIL
        msg['To'] = sender
        msg['Subject'] = subject
        msg.set_content(body)
        
        server.send_message(msg)
        server.quit()
        print(f"Response sent to {sender}")  # Debug print
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


if __name__ == "__main__":
    check_email()
