#! /usr/bin/python3

def read_number(line, index):
	number = 0
	while index < len(line) and line[index].isdigit():
		number = number * 10 + int(line[index])
		index += 1
	if index < len(line) and line[index] == '.':
		index += 1
		decimal = 0.1
		while index < len(line) and line[index].isdigit():
			number += int(line[index]) * decimal
			decimal /= 10
			index += 1
	token = {'type': 'NUMBER', 'number': number}
	return token, index


def read_operator(line, index):
	if line[index] == '+':
		token = {'type': 'PLUS'}
	elif line[index] == '-':
		token = {'type': 'MINUS'}
	elif line[index] == '*':
		token = {'type': 'MULTIPLY'}
	elif line[index] == '/':
		token = {'type': 'DIVIDE'}
	elif line[index] == '(':
		token = {'type': 'LEFT_P'}
	elif line[index] == ')':
		token = {'type': 'RIGHT_P'}
	return token, index + 1


def read_function(line, index):
	if line[index:index+3] == 'abs':
		token = {'type': 'FUNCTION', 'function': 'abs'}
		index += 3
	elif line[index:index+3] == 'int':
		token = {'type': 'FUNCTION', 'function': 'int'}
		index += 3
	elif line[index:index+5] == 'round':
		token = {'type': 'FUNCTION', 'function': 'round'}
		index += 5
	else:
		print('Invalid function found')
		exit(1)
	return token, index


# トークン化する
def tokenize(line):
	tokens = []
	index = 0
	if len(line) == 0:
		print("Empty string")
		exit(1)
	while index < len(line):
		if line[index].isdigit():
			(token, index) = read_number(line, index)
		elif line[index] in ['+', '-', '*', '/', '(', ')']:
			(token, index) = read_operator(line, index)
		elif line[index].isalpha():
			(token, index) = read_function(line, index)
		else:
			print('Invalid character found: ' + line[index])
			exit(1)
		tokens.append(token)
	return tokens


# *か/がある部分を計算する
def evaluate_mul_div(tokens):
	index = 0
	while index < len(tokens):
		if tokens[index]['type'] == 'MULTIPLY':
			new_number = tokens[index - 1]['number'] * tokens[index + 1]['number']
			tokens[index] = {'type': 'NUMBER', 'number': new_number}
			del tokens[index + 1]
			del tokens[index - 1]
			index -= 1
		elif tokens[index]['type'] == 'DIVIDE':
			new_number = tokens[index - 1]['number'] / tokens[index + 1]['number']
			tokens[index] = {'type': 'NUMBER', 'number': new_number}
			del tokens[index + 1]
			del tokens[index - 1]
			index -= 1
		index += 1
	return tokens


#プラスマイナスのみの式を計算する
def evaluate_plus_minus(tokens):
	index = 1
	answer = 0
	while index < len(tokens):
		if tokens[index]['type'] == 'NUMBER':
			if tokens[index - 1]['type'] == 'PLUS':
				answer += tokens[index]['number']
			elif tokens[index - 1]['type'] == 'MINUS':
				answer -= tokens[index]['number']
			else:
				print('Invalid syntax')
				exit(1)
		index += 1
	return answer


#()の中身を計算する
def evaluate_parenthesis(tokens):
	while True:
		right_p_index = None
		for i, token in enumerate(tokens):
			if token['type'] == 'RIGHT_P':
				right_p_index = i
				break
		if right_p_index is None:
			break

		left_p_index = None
		for i in range(right_p_index - 1, -1, -1):
			if tokens[i]['type'] == 'LEFT_P':
				left_p_index = i
				break

		if left_p_index is None:
			print('Invalid syntax: No matching left parenthesis')
			exit(1)

		sub_tokens = tokens[left_p_index + 1:right_p_index]
		if len(sub_tokens) == 0:
			print('Invalid syntax: Empty parenthesis')
			exit(1)

		sub_result = evaluate(sub_tokens)
		del tokens[left_p_index:right_p_index + 1] # 括弧を削除
		tokens.insert(left_p_index, {'type': 'NUMBER', 'number': sub_result})
	return tokens

#関数を計算する
def evaluate_functions(tokens):
	index = 1
	while index < len(tokens):
		if tokens[index]['type'] == 'FUNCTION':
			if tokens[index]['function'] == 'abs':
				tokens[index + 1]['number'] = abs(tokens[index + 1]['number'])
				del tokens[index]
			elif tokens[index]['function'] == 'int':
				tokens[index + 1]['number'] = int(tokens[index + 1]['number'])
				del tokens[index]
			elif tokens[index]['function'] == 'round':
				tokens[index + 1]['number'] = round(tokens[index + 1]['number'])
				del tokens[index]
		index += 1
	return tokens


def evaluate(tokens):
	if tokens[0] != {'type': 'MINUS'}:
		tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token

	tokens = evaluate_parenthesis(tokens)
	tokens = evaluate_functions(tokens)
	tokens = evaluate_mul_div(tokens)
	answer = evaluate_plus_minus(tokens)

	return answer


def test(line):
	tokens = tokenize(line)
	actual_answer = evaluate(tokens)
	expected_answer = eval(line)
	if abs(actual_answer - expected_answer) < 1e-8:
		print("PASS! (%s = %f)" % (line, expected_answer))
	else:
		print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
	print("==== Test started! ====")
	print("-----------plus and minus-------------")
	test("1")
	test("1+2")
	test("1.0+2.1-3")
	test("0.1+9.3-100.8")
	test("-1+9*5") #最初がマイナス
	print("----------multiply and divide---------")
	test("2+3*5")
	test("1+2+4*5*1")
	test("3/4+9.1")
	test("1/2.3/2-5")
	print("------------parenthesis------------")
	test("1*(2+2)+3")
	test("1*(2*(5+3))+3") #()の中に()
	test("8.8/(45.2+2*(9-4.4/(10)))")
	# test("()")
	print("------------functions------------")
	test("abs(-4)")
	test("2+abs(-99)-int(0.88)")
	test("int(2.66)*round(6.61)")
	test("int(abs(-5)+2.2)-round(int(abs(-6.66)-1.2))")
	print("==== Test finished! ====\n")

run_test()

while True:
	print('> ', end="")
	line = input()
	tokens = tokenize(line)
	answer = evaluate(tokens)
	expected_answer = eval(line)
	print("answer = %f" % answer)
	print("expected answer = %f\n" % expected_answer)
