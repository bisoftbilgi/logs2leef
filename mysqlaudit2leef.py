# Python script to convert MySQL Audit logs to LEEF format on the fly

import xml.etree.ElementTree as ET

audit_data = '''
<AUDIT>
 <AUDIT_RECORD>
  <TIMESTAMP>2019-10-03T14:09:38 UTC</TIMESTAMP>
  <RECORD_ID>6_2019-10-03T14:06:33</RECORD_ID>
  <NAME>Query</NAME>
  <CONNECTION_ID>5</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER>root[root] @ localhost [127.0.0.1]</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>drop_table</COMMAND_CLASS>
  <SQLTEXT>DROP TABLE IF EXISTS t</SQLTEXT>
 </AUDIT_RECORD>
</AUDIT>
'''

# Parse the XML stanza
audit = ET.fromstring(audit_data)

# Iterate through each AUDIT_RECORD element
for audit_record in audit.findall('AUDIT_RECORD'):
    timestamp = audit_record.find('TIMESTAMP').text
    record_id = audit_record.find('RECORD_ID').text
    op_name = audit_record.find('NAME').text
    user_info = audit_record.find('USER').text
    hostname = audit_record.find('HOST').text
    IP_address = audit_record.find('IP').text
    command_class = audit_record.find('COMMAND_CLASS').text
    sqltext = audit_record.find('SQLTEXT').text
    # print(f"Timestamp: {timestamp}, Op: {op_name}, User: {user_info}, Host: {hostname}, IP: {IP_address}, Class: {command_class}, SQL: {sqltext}")

    # Print syslog header
    # Need to convert timestamp into RFC 5424
    # TODO replace/convert timezone appropriately (need sample data to decide how)
    # examples:
    #    2019-01-18T11:07:53.520+07:00 
    #    2019-01-18T11:07:53.520Z
    print(f"<13>1 {timestamp} {hostname}",end=' ')
    
    # Print LEEF 2.0 header
    print(f"2.0|BiSoft|mysqlaudit2leef|1.0|{record_id}|^|",end=' ')

    # Print Event attributes
    print(f"usrName={user_info}^sev=1^src={IP_address}^commClass={command_class}^sqlText={sqltext}")
