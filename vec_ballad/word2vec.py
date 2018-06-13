import jieba as jb
import os
import numpy as np
from gensim.models import word2vec

def get_mean_embed(model, sequences, stopword=[]):
	mean_vec = np.zeros(model.vector_size)
	cnt = 0
	for sequence in sequences:
		for s in sequence:
			if bool(s) and s in model.wv and (s not in stopword):
				mean_vec += model.wv[s]
				cnt += 1
	return mean_vec / cnt

def get_mean_word(model, vec, topn=1, stopword=[]):
	alike = 0
	words = []
	alike = []
	for k in model.wv.vocab.keys():
		if k not in stopword:
			words.append(k)
			alike.append(cos_dis(vec, model.wv[k]))
	words = np.asarray(words)
	alike = np.asarray(alike)
	idx = np.argsort(-alike)
	words = words[idx]
	alike = alike[idx]
	return words[:topn], alike[:topn]

def discripe(model, file, topn=1, stopword=[]):
	with open(file, 'r', encoding='utf-8') as f:
		sequences = [line.strip().split(' ') for line in f.readlines() if bool(line.strip())]
	vec = get_mean_embed(model, sequences, stopword=stopword)
	return get_mean_word(model, vec, topn=topn, stopword=stopword)

def cos_dis(vec1, vec2):
	return np.sum(vec1*vec2)/np.sqrt(np.sum(vec1*vec1))/np.sqrt(np.sum(vec2*vec2))

def train_word2vec(root='./', workers=4):
	with open(os.path.join(root, 'config/stopwords.txt'), 'r', encoding='utf-8') as f:
		stopword = [w.strip() for w in f]

	if not os.path.isdir(os.path.join(root, 'statistic/'))  \
	or not os.path.isfile(os.path.join(root, 'statistic/sequences.txt')) \
	or not os.path.isfile(os.path.join(root, 'statistic/sentences.txt')) \
	or not os.path.isfile(os.path.join(root, 'statistic/words.txt')):
		root_dir = os.path.join(root, 'songs/')
		if not os.path.isdir(os.path.join(root, 'statistic')):
			os.mkdir(os.path.join(root, 'statistic'))
		sentences = []
		sequences = []
		words = []
		singers = os.listdir(root_dir)
		song_cnt = 0
		for singer in singers:
			song_dir = os.path.join(root_dir, singer)
			if singer[0] == '.' or os.path.isfile(song_dir):
				continue
			single_sen = []
			single_seq = []
			single_word = []
			songs = os.listdir(song_dir)

			for song in songs:
				file = os.path.join(song_dir, song)
				if song[0]!='.' and os.path.isfile(file):
					with open(file, 'r', encoding='utf-8') as f:
						song_cnt += 1
						single_seq.append([])
						for line in f.readlines():
							line = line.strip()
							if not bool(line):
								continue
							single_sen.append(line)
							seq = [w.strip() for w in jb.cut(line) if bool(w.strip())]

							if seq != []:
								single_word.extend(seq)
								single_seq[-1].extend(seq)

			stat_path = os.path.join(os.path.join(root, 'statistic/'), singer)
			if not os.path.isdir(stat_path):
				os.mkdir(stat_path)
			with open(os.path.join(stat_path, 'sentences.txt'), 'w', encoding='utf-8') as f:
				for s in single_sen:
					f.write(s + '\n')

			with open(os.path.join(stat_path, 'sequences.txt'), 'w', encoding='utf-8') as f:
				for s in single_seq:
					for w in s:
						f.write(w + ' ')
					f.write('\n')

			with open(os.path.join(stat_path, 'words.txt'), 'w', encoding='utf-8') as f:
				for w in single_word:
					f.write(w + '\n')

			sentences.extend(single_sen)
			sequences.extend(single_seq)
			words.extend(single_word)


		print('Total songs: {}'.format(song_cnt))
		print('Total sentences: {}'.format(len(sentences)))
		print('Total words: {}'.format(len(words)))

		with open(os.path.join(root, 'statistic/sentences.txt'), 'w', encoding='utf-8') as f:
			for s in sentences:
				f.write(s + '\n')

		with open(os.path.join(root, 'statistic/sequences.txt'), 'w', encoding='utf-8') as f:
			for s in sequences:
				for w in s:
					f.write(w + ' ')
				f.write('\n')

		with open(os.path.join(root, 'statistic/words.txt'), 'w', encoding='utf-8') as f:
			for w in words:
				f.write(w + '\n')

	# word 2 vec
	sentences = word2vec.Text8Corpus(os.path.join(root, "statistic/sequences.txt"))  # 加载语料
	
	model = word2vec.Word2Vec(sentences, size=256, window=10, iter=200, workers=workers) 
	model.wv.save_word2vec_format(os.path.join(root, 'checkpoint/ballad.vec'))


if __name__ == '__main__':
	train_word2vec('../')
				
