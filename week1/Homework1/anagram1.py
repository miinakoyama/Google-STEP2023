def sort(word):
	word_list = list(word)
	word_list.sort()
	return ''.join(word_list)

def binary_search(input, dict):
	start = 0
	end = len(dict) - 1
	while start <= end:
		mid = (start + end) //2
		if input == dict[mid][0]:
			return mid
		elif input < dict[mid][0]: #左側
			end = mid - 1
		else:
			start = mid + 1
	#inputがdictに存在しない時
	return -1

def main(input):
	sorted_input = sort(input)

	with open('words.txt', 'r') as fp:
		words = fp.readlines()

	#ソートされた単語と元の単語を辞書に追加する
	dict = []
	for word in words:
		word = word.strip()
		dict.append([sort(word), word])
	sorted_dict = sorted(dict)

	#アナグラムを探してリストに入れる
	anagrams = []
	anagram_location = binary_search(sorted_input, sorted_dict)
	if anagram_location == -1:
		print("No anagram found for '%s'" % input)
	else:
		anagrams.append(sorted_dict[anagram_location][1])
		#アナグラムが1個見つかればその前後もアナグラムの可能性がある
		i = 1
		for i in range(1, len(dict)):
			if sorted_dict[anagram_location + i][0] == sorted_input:
				anagrams.append(sorted_dict[anagram_location + i][1])
			else:
				break
		i = 1
		for i in range(1, len(dict)):
			if sorted_dict[anagram_location - i][0] == sorted_input:
				anagrams.append(sorted_dict[anagram_location - i][1])
			else:
				break
		print("The anagram of %s is %s" % (input, anagrams))

if __name__ == '__main__':
	#test
	main("cat")
	main("moon")
	main("anagram")
	main("turn")
	main("")
	main("nreaikrgrnjkaergbri")
	main("123")
	main("a")
	main("monkey")
	main("アイウエオ")
