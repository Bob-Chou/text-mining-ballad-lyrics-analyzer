from collections import Counter

def get_most_common_words(filename, topn=None, stopword=[]):
	with open(filename, 'r', encoding='utf-8') as f:
		words = [w.strip() for w in f.readlines() if bool(w.strip()) and w.strip() not in stopword]
	total = len(words)
	cnt = Counter(words)
	coms, nums = zip(*[pair for pair in cnt.most_common(topn)])
	freq = [n/total for n in nums]
	return coms, nums, freq

def get_city_list(filename, split=','):
	city = []
	with open(filename, 'r', encoding='utf-8') as f:
		for line in f.readlines():
			city.append(line.strip().split(split))
	return tuple(zip(*city))

if __name__ == '__main__':
	print(get_most_common_words('../songs/宋冬野/statistic/words.txt', 50))