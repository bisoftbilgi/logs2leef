# logs2leef
Set of scripts that converts different log formats to LEEF 2.0 on the fly

Using reference

   https://www.ibm.com/docs/en/SS42VS_DSM/pdf/b_Leef_format_guide.pdf
## mysqlaudit2leef
Requirements:
- python3 installed
- MySQL audit log format is XML "NEW"

Usage:
`$ mysqlaudit2leef.sh <MySQL Audit Logfile> { <Remote syslog address> | local } { start | stop }`
