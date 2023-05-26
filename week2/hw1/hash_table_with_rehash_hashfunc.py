import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value
# 各asciiコードの和がハッシュ値になる
# def calculate_hash(key):
# 	assert type(key) == str
# 	# Note: This is not a good hash function. Do you see why?
# 	hash = 0
# 	for i in key:
# 		hash += ord(i)
# 	return hash

# new hash function1
# (文字のasciiコード) * 128^(右から何文字目か)
def calculate_hash(key):
	assert type(key) == str
	hash = 0
	i = 0
	for char in key:
		hash += ord(char) * pow(128, i)
		i += 1
	return hash

# An item object that represents one key - value pair in the hash table.
class Item:
	# |key|: The key of the item. The key must be a string.
	# |value|: The value of the item.
	# |next|: The next item in the linked list. If this is the last item in the
	#         linked list, |next| is None.
	def __init__(self, key, value, next):
		assert type(key) == str
		self.key = key
		self.value = value
		self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

	# Initialize the hash table.
	def __init__(self):
		# Set the initial bucket size to 97. A prime number is chosen to reduce
		# hash conflicts.
		self.bucket_size = 97
		self.buckets = [None] * self.bucket_size
		self.item_count = 0

	# Put an item to the hash table. If the key already exists, the
	# corresponding value is updated to a new value.
	#
	# |key|: The key of the item.
	# |value|: The value of the item.
	# Return value: True if a new item is added. False if the key already exists
	#               and the value is updated.
	def put(self, key, value):
		assert type(key) == str #keyが文字列であることを確認
		self.check_size() # Note: Don't remove this code.
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if item.key == key:
				item.value = value
				return False
			item = item.next
		new_item = Item(key, value, self.buckets[bucket_index])
		self.buckets[bucket_index] = new_item
		self.item_count += 1
		self.rehash()
		return True

	# Get an item from the hash table.
	#
	# |key|: The key.
	# Return value: If the item is found, (the value of the item, True) is
	#               returned. Otherwise, (None, False) is returned.
	def get(self, key):
		assert type(key) == str
		self.check_size() # Note: Don't remove this code.
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if item.key == key:
				return (item.value, True)
			item = item.next
		return (None, False)

	# Delete an item from the hash table.
	#
	# |key|: The key.
	# Return value: True if the item is found and deleted successfully. False
	#               otherwise.
	def delete(self, key):
		assert type(key) == str
		bucket_index = calculate_hash(key) % self.bucket_size #keyからhash値を計算->bucketのindexを計算
		item = self.buckets[bucket_index] #計算したindexのbucketの先頭アイテム
		previous_item = None

		while item:
			if item.key == key:
				if previous_item: #削除するitemがlinked listの先頭でない時
					previous_item.next = item.next
				else: #削除するitemがlinked listの先頭の時
					self.buckets[bucket_index] = item.next
				self.item_count -= 1
				self.rehash() #再ハッシュ
				return True
			previous_item = item
			item = item.next
		return False


	# Return the total number of items in the hash table.
	def size(self):
		return self.item_count	
	# Check that the hash table has a "reasonable" bucket size.
	# The bucket size is judged "reasonable" if it is smaller than 100 or
	# the buckets are 30% or more used.

	#numが素数かどうかを判定する関数
	def is_prime(self, num):
		if num <= 1:
			return False
		
		if num == 2:
			return True
		
		if num % 2 == 0: #先に2の倍数をはじく
			return False
		
		i = 3
		while i * i < num:
			if num % i == 0:
				return False
			i += 2
		return True

	#入力された数字に最も近い素数を探す関数
	def find_nearest_prime(self, num):
		if num < 2:
			return 2
		
		if self.is_prime(num):
			return num
		
		lower_prime = None
		upper_prime = None

		i = num - 1
		while lower_prime is None and i >= 2:
			if self.is_prime(i):
				lower_prime = i
			i -= 1

		i = num + 1
		while upper_prime is None:
			if self.is_prime(i):
				upper_prime = i
			i += 1

		if lower_prime is None:
			return upper_prime
		
		if num - lower_prime < upper_prime - num:
			return lower_prime
		else:
			return upper_prime


	# 再ハッシュ関数
	def rehash(self):
		#bucketの30%以下しか使われていない -> bucket_sizeを半分にした数に1番近い素数にする
		if self.item_count / self.bucket_size <= 0.3:
			bucket_size_new = self.find_nearest_prime(self.bucket_size // 2)
		# bucketの70%以上使われている -> bucket_sizeを2倍にした数に1番近い素数にする
		elif self.item_count / self.bucket_size >= 0.7:
			bucket_size_new = self.find_nearest_prime(self.bucket_size * 2)
		else:
			return
		
		buckets_new = [None] * bucket_size_new #backetを新たに作成
		#元のbacketからitemを取り出して新たなbacketに入れる
		for i in range(self.bucket_size):
			item = self.buckets[i]
			while item:
				key = item.key
				value = item.value
				# 新たなハッシュ値から新たなインデックスを計算
				bucket_index_new = calculate_hash(key) % bucket_size_new
				#新たなbacketにitemを入れる
				item_new = Item(key, value, buckets_new[bucket_index_new])
				buckets_new[bucket_index_new] = item_new
				item = item.next
		self.buckets = buckets_new
		self.bucket_size = bucket_size_new


	# Note: Don't change this function.
	def check_size(self):
		assert (self.bucket_size < 100 or self.item_count >= self.bucket_size * 0.3)

	def print_hash_table_items(self):
		for i in range(self.bucket_size):
			item = self.buckets[i]
			while item:
				print(f"Key: {item.key}, Value: {item.value}")



# Test the functional behavior of the hash table.
def functional_test():
	hash_table = HashTable()

	assert hash_table.put("aaa", 1) == True
	assert hash_table.get("aaa") == (1, True)
	assert hash_table.size() == 1

	assert hash_table.put("bbb", 2) == True
	assert hash_table.put("ccc", 3) == True
	assert hash_table.put("ddd", 4) == True
	assert hash_table.get("aaa") == (1, True)
	assert hash_table.get("bbb") == (2, True)
	assert hash_table.get("ccc") == (3, True)
	assert hash_table.get("ddd") == (4, True)
	assert hash_table.get("a") == (None, False)
	assert hash_table.get("aa") == (None, False)
	assert hash_table.get("aaaa") == (None, False)
	assert hash_table.size() == 4

	assert hash_table.put("aaa", 11) == False
	assert hash_table.get("aaa") == (11, True)
	assert hash_table.size() == 4

	assert hash_table.delete("aaa") == True
	assert hash_table.get("aaa") == (None, False)
	assert hash_table.size() == 3

	assert hash_table.delete("a") == False
	assert hash_table.delete("aa") == False
	assert hash_table.delete("aaa") == False
	assert hash_table.delete("aaaa") == False


	assert hash_table.delete("ddd") == True
	assert hash_table.delete("ccc") == True
	assert hash_table.delete("bbb") == True
	assert hash_table.get("aaa") == (None, False)
	assert hash_table.get("bbb") == (None, False)
	assert hash_table.get("ccc") == (None, False)
	assert hash_table.get("ddd") == (None, False)
	assert hash_table.size() == 0

	assert hash_table.put("abc", 1) == True
	assert hash_table.put("acb", 2) == True
	assert hash_table.put("bac", 3) == True
	assert hash_table.put("bca", 4) == True
	assert hash_table.put("cab", 5) == True
	assert hash_table.put("cba", 6) == True
	assert hash_table.get("abc") == (1, True)
	assert hash_table.get("acb") == (2, True)
	assert hash_table.get("bac") == (3, True)
	assert hash_table.get("bca") == (4, True)
	assert hash_table.get("cab") == (5, True)
	assert hash_table.get("cba") == (6, True)
	assert hash_table.size() == 6

	assert hash_table.delete("abc") == True
	assert hash_table.delete("cba") == True
	assert hash_table.delete("bac") == True
	assert hash_table.delete("bca") == True
	assert hash_table.delete("acb") == True
	assert hash_table.delete("cab") == True
	assert hash_table.size() == 0
	print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
	hash_table = HashTable()

	for iteration in range(100):
		begin = time.time()
		random.seed(iteration)
		for i in range(10000):
			rand = random.randint(0, 100000000)
			hash_table.put(str(rand), str(rand))
		random.seed(iteration)
		for i in range(10000):
			rand = random.randint(0, 100000000)
			hash_table.get(str(rand))
		end = time.time()
		print("%d %.6f" % (iteration, end - begin))
		with open("output_rehash_hashfunc.txt", "a") as f:
			f.write("%d %.6f\n" % (hash_table.item_count, end - begin))

	for iteration in range(100):
		random.seed(iteration)
		for i in range(10000):
			rand = random.randint(0, 100000000)
			hash_table.delete(str(rand))

	assert hash_table.size() == 0
	print("Performance tests passed!")


if __name__ == "__main__":
	functional_test()
	performance_test()
