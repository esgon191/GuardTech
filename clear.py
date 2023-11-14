def format_api(string):
	garbage_words = [
		'systems',
		'for',
		'and',
		'edition',
		'editions',
		'version',
		'microsoft',
	]

	empty_replace = '(),'

	string = string.lower()

	for i in empty_replace:
		string = string.replace(i, '')

	string = string.split(' ')

	string = ['' if i in garbage_words else i for i in string]

	try: 
		string.remove('')

	except ValueError:
		pass

	string = ' '.join(string).replace('  ', ' ')
	string = string.replace('service pack ', 'sp')
	string = string.replace('/', ' ')
	

	return string

def format_local(string):
	garbage_words = [
		'systems',
		'for',
		'and',
		'edition',
		'editions',
		'version',
		'microsoft',
		'files',
		'professionalworkstation'
	]

	string = string.lower()
	string = string.split(' ')

	if 'microsoft' not in string:
		raise NotImplementedError('Non-microsoft developer')

	for i in range(len(string)):
		if '\\' in string[i]:
			string[i] = ''

	for i in range(len(string)):
		if string[i] in garbage_words:
			string[i] = ''

	try:
		string.remove('')

	except:
		pass

	res = []
	for elem in string:
		if elem not in res:
			res.append(elem)

	string = res
	string = ' '.join(string).replace('  ', ' ')

	empty_replace = '(),-'

	for i in empty_replace:
		string = string.replace(i, '')

	string = string.replace('  ', ' ')

	return string