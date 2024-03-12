# Python script to convert MySQL Audit logs to LEEF format on the fly

import xml.etree.ElementTree as ET


def printLEEFentry(audit_record_data):
    # Parse the XML stanza
    audit_record = ET.fromstring(audit_record_data)

    # Parse AUDIT_RECORD element
    timestamp = audit_record.find('TIMESTAMP').text

    try:
        record_id = audit_record.find('RECORD_ID').text
    except AttributeError:
        record_id = 'N/A'

    op_name = audit_record.find('NAME').text
    try:
        user_info = audit_record.find('USER').text
    except AttributeError:
        user_info = 'N/A'

    try:
        hostname = audit_record.find('HOST').text
    except AttributeError:
        hostname = 'N/A'

    try:
        IP_address = audit_record.find('IP').text
    except AttributeError:
        IP_address = 'N/A'

    try:
        command_class = audit_record.find('COMMAND_CLASS').text
    except AttributeError:
        command_class = 'N/A'

    try:
        sqltext = audit_record.find('SQLTEXT').text
    except AttributeError:
        sqltext = 'N/A'

    # Print syslog header
    # Need to convert timestamp into RFC 5424
    # TODO replace/convert timezone appropriately (need sample data to decide how)
    # examples:
    #    2019-01-18T11:07:53.520+07:00 
    #    2019-01-18T11:07:53.520Z
    formatted_timestamp = timestamp.replace(" UTC","Z")
    print(f"<13>1 {formatted_timestamp} {hostname}",end=' ')
    
    # Print LEEF 2.0 header
    print(f"2.0|BiSoft|mysqlaudit2leef.py|1.0|{record_id}|^|",end='')

    # Print Event attributes
    print(f"usrName={user_info}^sev=1^src={IP_address}^auditName={op_name}^commClass={command_class}^sqlText={sqltext}^")


# Main mysqlaudit2leef.py 

while True:
    # Read from input until matching "<AUDIT_RECORD>"
    inputline = ''
    while "<AUDIT_RECORD>" not in inputline:
        inputline = input()

    # Start initializing AUDIT_RECORD multiline text variable
    audit_record_text = inputline

    # Until matching "</AUDIT_RECORD>"
    while "</AUDIT_RECORD>" not in inputline:
        inputline = input()
        # Append every new line 
        audit_record_text = audit_record_text + inputline

    printLEEFentry(audit_record_text)
