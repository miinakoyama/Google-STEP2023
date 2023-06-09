import sys
import collections
import copy

class Wikipedia:

	# Initialize the graph of pages.
	def __init__(self, pages_file, links_file):

		# A mapping from a page ID (integer) to the page title.
		# For example, self.titles[1234] returns the title of the page whose
		# ID is 1234.
		self.titles = {}

		# A set of page links.
		# For example, self.links[1234] returns an array of page IDs linked
		# from the page whose ID is 1234.
		self.links = {}

		# Read the pages file into self.titles.
		with open(pages_file) as file:
			for line in file:
				(id, title) = line.rstrip().split(" ")
				id = int(id)
				assert not id in self.titles, id
				self.titles[id] = title
				self.links[id] = []
		print("Finished reading %s" % pages_file)

		# Read the links file into self.links.
		with open(links_file) as file:
			for line in file:
				(src, dst) = line.rstrip().split(" ")
				(src, dst) = (int(src), int(dst))
				assert src in self.titles, src
				assert dst in self.titles, dst
				self.links[src].append(dst)
		print("Finished reading %s" % links_file)

		# A set of page links just for shiritori.
		self.links_for_shiritori = {}
		self.links_for_shiritori = self.make_graph_for_shiritori()
		print("Finished making graph for shiritori")
		print()


	# Find the longest titles. This is not related to a graph algorithm at all
	# though :)
	def find_longest_titles(self):
		titles = sorted(self.titles.values(), key=len, reverse=True)
		print("The longest titles are:")
		count = 0
		index = 0
		while count < 15 and index < len(titles):
			if titles[index].find("_") == -1:
				print(titles[index])
				count += 1
			index += 1
		print()


	# Find the most linked pages.
	def find_most_linked_pages(self):
		link_count = {}
		for id in self.titles.keys():
			link_count[id] = 0

		for id in self.titles.keys():
			for dst in self.links[id]:
				link_count[dst] += 1

		print("The most linked pages are:")
		link_count_max = max(link_count.values())
		for dst in link_count.keys():
			if link_count[dst] == link_count_max:
				print(self.titles[dst], link_count_max)
		print()


	# Find the shortest path.
	# |start|: The title of the start page.
	# |goal|: The title of the goal page.
	def find_shortest_path(self, start, goal, shiritori = False):
		if shiritori:
			links = self.links_for_shiritori
		else:
			links = self.links
		start_id = list(self.titles.keys())[list(self.titles.values()).index(start)]
		goal_id = list(self.titles.keys())[list(self.titles.values()).index(goal)]
		queue_id = collections.deque([start_id])
		visited_id = {start_id: 0}
		found = False
		while len(queue_id) != 0:
			node_id = queue_id.popleft() #dequeue
			if node_id == goal_id:
				found = True
				break
			for child_id in links[node_id]:
				if not child_id in visited_id:
					queue_id.append(child_id) #enqueue
					visited_id[child_id] = node_id #どこからきたかの情報とともにvisitedに追加
		if found == False:
			print("path not found")
		else:
			trace_back_id = goal_id
			path_title = collections.deque()
			while trace_back_id in visited_id:
				path_title.appendleft(self.titles[trace_back_id])
				trace_back_id = visited_id[trace_back_id]
			if shiritori:
				print("The shortest shiritori path is:")
			else:
				print("The shortest path is:")
			for path in path_title:
				print(path, end = ' ')
			print()


	def calculate_page_ranks(self):
		pass

	# Calculate the page ranks and print the most popular pages.
	def find_most_popular_pages(self):
		self.calculate_page_ranks()
		pass

	# Make graph for shiritori by deleting the links that are not shiritori.
	def make_graph_for_shiritori(self):
		links_for_shiritori = copy.deepcopy(self.links)
		for key, values in links_for_shiritori.items():
			front_title = self.titles[key]
			remove_indices = []
			for i, back_id in enumerate(values):
				back_title = self.titles[back_id]
				if front_title[-1] != back_title[0]:
					remove_indices.append(i) #削除する要素のindexを記録
			for index in reversed(remove_indices):
				del links_for_shiritori[key][index]
		return links_for_shiritori

	# Do something more interesting!!
	# Find the shortest shiritori path.
	def find_shortest_shiritori(self, start, goal):
		self.find_shortest_path(start, goal, shiritori = True)

	def find_shiritori(self, start):
		shiritori = set()
		start_id = list(self.titles.keys())[list(self.titles.values()).index(start)]
		shiritori.add(start_id)
		visited_ids = set()
		prev_id = start_id
		while prev_id in self.links_for_shiritori and self.links_for_shiritori[prev_id] and prev_id not in visited_ids:
			shiritori.add(self.links_for_shiritori[prev_id][0])
			visited_ids.add(prev_id)
			prev_id = self.links_for_shiritori[prev_id][0]
		for id in shiritori:
			print(self.titles[id], end = ' ')
		print()


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("usage: %s pages_file links_file" % sys.argv[0])
		exit(1)

	wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
	wikipedia.find_longest_titles()
	wikipedia.find_most_linked_pages()
	wikipedia.find_shortest_path("渋谷", "パレートの法則")
	wikipedia.find_shortest_shiritori("渋谷", "法学")
	wikipedia.find_shortest_shiritori("彗星", "コンパイラ")
	wikipedia.find_shortest_shiritori("シアピッチーア", "モンスターハンター")
	wikipedia.find_shortest_shiritori("ザ・クークス", "スケートパーク")
	wikipedia.find_shiritori("渋谷")
	wikipedia.find_shiritori("ISBN")
	wikipedia.find_shiritori("安倍政権")
	wikipedia.find_shiritori("日本語")
	wikipedia.find_shiritori("エジプト")
	wikipedia.find_shiritori("オーストリア")
	wikipedia.find_shiritori("イタリア語")
	wikipedia.find_shiritori("音楽")
	
	# wikipedia.find_shortest_path("A", "F")
	wikipedia.find_most_popular_pages()
