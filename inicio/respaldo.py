from django.db import connection
sql = 'mysqldump orquesta > orquesta.sql'
a = connection.cursor()
a.execute(sql)
