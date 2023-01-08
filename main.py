import json


def mask_cart_info(cart_info):
	# account
	if cart_info.find('Счет') != -1:
		result = ' '.join(cart_info.split()[:-1]) + ' ' + cart_info.split()[-1][:4] + ' ' + \
			cart_info.split()[-1][4:6] + '** **** ' + cart_info.split()[-1][-4:]
		return result
	# no card or account
	elif cart_info.find('Отсутствует') != -1:
		return cart_info
	# card
	else:
		result = ' '.join(cart_info.split()[:-1]) + ' **' + cart_info.split()[-1][-4:]
		return result


def main():
	# read json
	f = open('operations.json', encoding="utf8")
	operations_json = json.load(f)
	# delete CANCELED operations and operations without date
	filtred_operations = []
	for operation in operations_json:
		if operation.get('date') and operation.get('state') == 'EXECUTED':
			filtred_operations.append(operation)
	# sort operations by date
	filtred_operations = sorted(filtred_operations, key=lambda d: str(d.get('date')))
	# print results
	operations_for_print = filtred_operations[-5:]
	for operation in operations_for_print:
		# prepare values
		_date = operation.get("date").split('T')[0]
		_description = operation.get("description")
		_from = mask_cart_info(operation.get("from", "Отсутствует"))
		_to = mask_cart_info(operation.get("to"))
		_sum = operation.get("operationAmount").get("amount")
		_currency = operation.get("operationAmount").get("currency").get("name")
		# print in format
		print(f'{_date} {_description}\n{_from} -> {_to}\n{_sum} {_currency}\n')


if __name__ == '__main__':
	main()
