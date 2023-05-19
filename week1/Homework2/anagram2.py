import sys

#1つの単語のスコアを算出する
def calc_score(word):
	score = 0
	for letter in word:
		if letter in 'aehinorst':
			score += 1
		elif letter in 'cdlmu':
			score += 2
		elif letter in 'bfgpvwy':
			score += 3
		elif letter in 'jkqxz':
			score += 4
	return score

#辞書をスコア順に並べ替える
def sort_by_score(words):
	word_scores = {}
	for word in words:
		score = calc_score(word)
		word_scores[word] = score
	sorted_words = sorted(word_scores, key = word_scores.get, reverse = True)
	return sorted_words

#一つの単語の中にそれぞれのアルファベットがいくつ入っているかを辞書にまとめる
def count_word(word):
	counted_word = {chr(counted_word): 0 for counted_word in range(ord('a'), ord('z') + 1)}
	for letter in word:
		if letter in counted_word.keys():
			counted_word[letter] += 1
	return counted_word

#wordがinputのsubsetかどうかを判断
def is_subset(counted_word ,counted_input):
	for letter, count in counted_word[1].items():
		if count > counted_input[1][letter]: #一つでも辞書の方が多いとだめ
			return False
	return True

def main(input_file, output_file):
	counted_words = []
	counted_inputs = []
	with open('words.txt', 'r') as fp:
		words = fp.readlines()
	sorted_words = sort_by_score(words)

	for word in sorted_words:
		counted_words.append([word, count_word(word)])

	with open(input_file, 'r') as fp:
		inputs = fp.readlines()

	for input in inputs:
		counted_inputs.append([input, count_word(input)])

	f = open(output_file, 'w')
	for counted_input in counted_inputs:
		for counted_word in counted_words:
			found = False
			if is_subset(counted_word, counted_input) == True:
				f.write(counted_word[0])
				found = True
				break
		if found == False:
			f.write("Not Found\n")
	f.close()

if __name__ == '__main__':
	input_file = input("input file: ")
	output_file = input("output file: ")
	main(input_file, output_file)