# By Steve Hanov, 2011. Released to the public domain
# More or less
class TrieNode:
	def __init__(self):
		self.word = None
		self.children = {}

	def Insert(self, word):
		node = self
		for letter in word:
			if letter not in node.children:
				node.children[letter] = TrieNode()
			node = node.children[letter]
		node.word = word


class LevenshteinSearch:
	def __init__(self, insertionWeight=1, deletionWeight=1, replaceWeight=1):
		self.trie = TrieNode()
		self.deletionWeight = deletionWeight
		self.insertionWeight = insertionWeight
		self.replaceWeight = replaceWeight

	def loadList(self, list):
		for word in list:
			self.trie.Insert(word)

	def search(self, word, maxCost=4):
		currentRow = range(len(word) + 1)

		results = []
		minDist = 1e9

		for letter in self.trie.children:
			self.__SearchRecursive(self.trie.children[letter], letter, word,
			                       currentRow, results, maxCost, minDist)

		results.sort(key=lambda x: x[1])
		return results

	def __SearchRecursive(self, node, letter, word, previousRow, results,
	                      maxCost, minDist):
		if minDist == 0:
			return

		columns = len(word) + 1
		currentRow = [previousRow[0] + 1]

		for column in range(1, columns):
			insertCost = currentRow[column - 1] + self.insertionWeight
			deleteCost = previousRow[column] + self.deletionWeight

			if word[column - 1] != letter:
				replaceCost = previousRow[column - 1] + self.replaceWeight
			else:
				replaceCost = previousRow[column - 1]

			currentRow.append(min(insertCost, deleteCost, replaceCost))

		if currentRow[-1] < minDist:
			minDist = currentRow[-1]
		if currentRow[-1] <= maxCost and node.word != None:
			# print(node.word, currentRow[-1])
			results.append((node.word, currentRow[-1]))

		if min(currentRow) <= maxCost:
			for letter in node.children:
				self.__SearchRecursive(node.children[letter], letter, word,
				                       currentRow, results, maxCost, minDist)
