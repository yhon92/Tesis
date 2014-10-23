import time

def vps():
	env.hosts = ['localhost']
	env.user = ''
	env.dbname = 'orquesta'
	env.dbuser = 'root'
	env.dbpass = ''

def backup():
	require('hosts', provided_by=[vps])
	require('dbname')
	require('dbuser')
	require('dbpass')

	date = time.strftime('%d%m%Y%H%M%S')
	fname = '/home/oscar/%(database)s-backup-%(date)s.xml.gz' % {
		'database': env.dbname,
		'date': date,
	}

	if exists(fname):
		run('rm "%s"' % fname)

	run('mysqldump -u %(username)s -p%(password)s %(database)s --xml | '
		'gzip > %(fname)s' % {'username': env.dbuser, 'password': env.dbpass, 'database': env.dbname, 'fname': fname})

	get(fname, os.path.basename(fname))
	run('rm "%s"' % fname)