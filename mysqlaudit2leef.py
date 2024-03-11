# Python script to convert MySQL Audit logs to LEEF format on the fly

import xml.etree.ElementTree as ET

# Sample XML data
xml_data = '''
<root>
    <person>
        <name>John</name>
        <age>30</age>
    </person>
    <person>
        <name>Alice</name>
        <age>25</age>
    </person>
</root>
'''

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

# Parse the XML data
root = ET.fromstring(xml_data)

# Iterate through each 'person' element
for person in root.findall('person'):
    name = person.find('name').text
    age = person.find('age').text
    print(f"Name: {name}, Age: {age}")

# Parse the XML stanza
audit = ET.fromstring(audit_data)
# Iterate through each AUDIT_RECORD element
for audit_record in audit.findall('AUDIT_RECORD'):
    timestamp = audit_record.find('TIMESTAMP').text
    op_name = audit_record.find('NAME').text
    user_info = audit_record.find('USER').text
    hostname = audit_record.find('HOST').text
    IP_address = audit_record.find('IP').text
    command_class = audit_record.find('COMMAND_CLASS').text
    sql_text = audit_record.find('SQL_TEXT').text

