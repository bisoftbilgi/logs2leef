#!/bin/bash
# Script to convert MySQL Audit logs to LEEF format on the fly

cat samplemysqlaudit.log | python3 mysqlaudit2leef.py

