#!/bin/bash
echo "Start the dump"
mysqldump -h mysql -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} > /backup/db.sql
echo "Database dump completed."
