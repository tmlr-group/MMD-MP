import random
import datasets
import tqdm
import pandas as pd
from MGTBenchold.methods.utils import timeit
import os
# import sys
# import os
# sys.path.append(os.path.abspath('MGTBench/datasets'))
# you can add more datasets here and write your own dataset parsing function
DATASETS = ['meta_HC3', 'HC3', 'TruthfulQA', 'SQuAD1', 'SQuAD2',
			'NarrativeQA', "TruthfulQA_adv1", "TruthfulQA_adv2"]

dataset_path_dit={
	'HC3': '/mnt/cephfs/dataset/zhangshuhai/backup20240107/detect-gpt-gitHub/dataset/H3C'
}

import re
def process_spaces(text):
	text = text.replace(
		' ,', ',').replace(
		' .', '.').replace(
		' ?', '?').replace(
		' !', '!').replace(
		' ;', ';').replace(
		' \'', '\'').replace(
		' ’ ', '\'').replace(
		' :', ':').replace(
		'<newline>', '\n').replace(
		'`` ', '"').replace(
		' \'\'', '"').replace(
		'\'\'', '"').replace(
		'.. ', '... ').replace(
		' )', ')').replace(
		'( ', '(').replace(
		' n\'t', 'n\'t').replace(
		' i ', ' I ').replace(
		' i\'', ' I\'').replace(
		'\\\'', '\'').replace(
		'\n ', '\n').strip()
	text = text.replace('\r\n', '\n').replace('\\n', '').replace('!\n', '') 
	return re.sub('\n+', '\n', text)

def process_text_truthfulqa_adv(text):

	if "I am sorry" in text:
		first_period = text.index('.')
		start_idx = first_period + 2
		text = text[start_idx:]
	if "as an AI language model" in text or "As an AI language model" in text:
		first_period = text.index('.')
		start_idx = first_period + 2
		text = text[start_idx:]
	return text

@timeit#自动计算函数的运行时间
def load_HC3(cache_dir):
	# 设置代理

	d = datasets.load_dataset('Hello-SimpleAI/HC3',
							  name='all', cache_dir=cache_dir)

	d = d['train']
 
	filtered_d = [_ for _ in d if (len(_['human_answers']) > 0 and len(_['chatgpt_answers']) > 0 and len(_['human_answers'][0].split()) > 5 and len(_['chatgpt_answers'][0].split()) > 5)]

	data_new = {
		'train': {
			'text': [],
			'label': [],
		},
		'test': {
			'text': [],
			'label': [],
		}

	}

	# random.seed(0)
	random.shuffle(filtered_d)

	total_num = len(filtered_d)
	# total_num = 100
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.8:
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(filtered_d[i]["human_answers"][0]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(filtered_d[i]["chatgpt_answers"][0]))
		data_new[data_partition]['label'].append(1)
	return data_new

@timeit
def load_meta_HC3(cache_dir):
	d = datasets.load_dataset('Hello-SimpleAI/HC3',
							  name='all', cache_dir=cache_dir)
	d = d['train']
	# filtered_d = [_ for _ in d if (len(_['human_answers']) > 0 and len(_['chatgpt_answers']) > 0 and len(_['human_answers'][0].split()) > 5 and len(
	# 	_['chatgpt_answers'][0].split()) > 5 and len(_['human_answers'][0].split()) < 150 and len(_['chatgpt_answers'][0].split()) < 150)]
	# filtered_d = [_ for _ in d if (len(_['human_answers']) > 0 and len(_['chatgpt_answers']) > 0 and len(_['human_answers'][0].split()) > 100 and len(
	# _['chatgpt_answers'][0].split()) > 100 and len(_['human_answers'][0].split()) < 180 and len(_['chatgpt_answers'][0].split()) < 180)]

	meta_data = {}
	filtered_d = [_ for _ in d if (len(_['human_answers']) > 0 and len(_['chatgpt_answers']) > 0 and len(_['human_answers'][0].split()) > 5 and len(_['chatgpt_answers'][0].split()) > 5)]

	for source in sorted(set([item['source'] for item in filtered_d])):
		meta_data[source] = {
			'train': {
				'text': [],
				'label': [],
			},
			'test': {
				'text': [],
				'label': [],
			}
		}

	# random.seed(0)
	random.shuffle(filtered_d)

	total_num = len(filtered_d)
	# total_num = 100
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.80:
			data_partition = 'train'
		else:
			data_partition = 'test'
		item = filtered_d[i]
		source = item['source']
		meta_data[source][data_partition]['text'].append(
			process_spaces(filtered_d[i]["human_answers"][0]))
		meta_data[source][data_partition]['label'].append(0)
		meta_data[source][data_partition]['text'].append(
			process_spaces(filtered_d[i]["chatgpt_answers"][0]))
		meta_data[source][data_partition]['label'].append(1)
	return meta_data

def load_TruthfulQA(cache_dir):
	f = pd.read_csv("/mnt/cephfs/home/zhangshuhai/detect-gpt/MGTBench/datasets/TruthfulQA_chatgpt.csv")
	q = f['Question'].tolist()
	a_human = f['Best Answer'].tolist()
	a_chat = f['chatgpt_answer'].tolist()
	c = f['Category'].tolist()

	res = []
	for i in range(len(q)):
		if len(a_human[i].split()) > 10 and len(a_chat[i].split()) > 10: # 原来是大于1，太短没有意义，改成大于4
			res.append([q[i], a_human[i], a_chat[i], c[i]])

	data_new = {
		'train': {
			'text': [],
			'label': [],
			'category': [],
		},
		'test': {
			'text': [],
			'label': [],
			'category': [],
		}

	}

	total_num = len(res)
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.1: #原来是0.8，由于不训练，改成0.01	
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(res[i][1]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(res[i][2]))
		data_new[data_partition]['label'].append(1)

		data_new[data_partition]['category'].append(res[i][3])
		data_new[data_partition]['category'].append(res[i][3])

	return data_new


def load_TruthfulQA_adv1(cache_dir):
	f = pd.read_csv("/mnt/cephfs/home/zhangshuhai/detect-gpt/MGTBench/datasets/TruthfulQA_chatgpt_adv1.csv")
	q = f['complete_question'].tolist()
	a_human = f['Best Answer'].tolist()
	a_chat = f['chatgpt_answer'].tolist()
	c = f['Category'].tolist()
	res = []
	for i in range(len(q)):
		if len(a_human[i].split()) > 1 and len(a_chat[i].split()) > 1:
			res.append([q[i], a_human[i], a_chat[i], c[i]])

	data_new = {
		'train': {
			'text': [],
			'label': [],
			'category': [],
		},
		'test': {
			'text': [],
			'label': [],
			'category': [],
		}

	}

	total_num = len(res)
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.8:
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(res[i][1]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(res[i][2]))
		data_new[data_partition]['label'].append(1)

		data_new[data_partition]['category'].append(res[i][3])
		data_new[data_partition]['category'].append(res[i][3])

	return data_new


def load_TruthfulQA_adv2(cache_dir):
	f = pd.read_csv("/mnt/cephfs/home/zhangshuhai/detect-gpt/MGTBench/datasets/TruthfulQA_chatgpt_adv2.csv")
	q = f['complete_question'].tolist()
	a_human = f['Best Answer'].tolist()
	a_chat = f['chatgpt_answer'].tolist()
	a_chat = [process_text_truthfulqa_adv(_) for _ in a_chat]
	c = f['Category'].tolist()

	res = []
	for i in range(len(q)):
		if len(a_human[i].split()) > 1 and len(a_chat[i].split()) > 1:
			res.append([q[i], a_human[i], a_chat[i], c[i]])

	data_new = {
		'train': {
			'text': [],
			'label': [],
			'category': [],
		},
		'test': {
			'text': [],
			'label': [],
			'category': [],
		}

	}

	total_num = len(res)
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.8:
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(res[i][1]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(res[i][2]))
		data_new[data_partition]['label'].append(1)

		data_new[data_partition]['category'].append(res[i][3])
		data_new[data_partition]['category'].append(res[i][3])

	return data_new


def load_SQuAD1(cache_dir):
	f = pd.read_csv("/mnt/cephfs/home/zhangshuhai/detect-gpt/MGTBench/datasets/SQuAD1_chatgpt.csv")
	q = f['Question'].tolist()
	a_human = [eval(_)['text'][0] for _ in f['answers'].tolist()]
	a_chat = f['chatgpt_answer'].tolist()

	res = []
	for i in range(len(q)):
		if len(a_human[i].split()) > 1 and len(a_chat[i].split()) > 1:
			res.append([q[i], a_human[i], a_chat[i]])

	data_new = {
		'train': {
			'text': [],
			'label': [],
		},
		'test': {
			'text': [],
			'label': [],
		}

	}

	total_num = len(res)
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.8:
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(res[i][1]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(res[i][2]))
		data_new[data_partition]['label'].append(1)
	return data_new


def load_SQuAD2(cache_dir):
	f = pd.read_csv("/mnt/cephfs/home/zhangshuhai/detect-gpt/MGTBench/datasets/SQuAD2_chatgpt.csv")

	anwsers = f['answers'].tolist()
	a_chat = f['chatgpt_answer'].tolist()
	selected_index = [i for i in range(len(anwsers)) if (
		len(eval(anwsers[i])['text']) > 0 and len(a_chat[i]) > 0)]
	q = f['Question'].tolist()
	q = [q[i] for i in selected_index]

	a_human = [eval(anwsers[i])['text'][0] for i in selected_index]

	a_chat = [a_chat[i] for i in selected_index]

	res = []
	for i in range(len(q)):
		if len(a_human[i].split()) > 1 and len(a_chat[i].split()) > 1:
			res.append([q[i], a_human[i], a_chat[i]])

	data_new = {
		'train': {
			'text': [],
			'label': [],
		},
		'test': {
			'text': [],
			'label': [],
		}

	}

	total_num = len(res)
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.8:
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(res[i][1]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(res[i][2]))
		data_new[data_partition]['label'].append(1)
	return data_new


def load_NarrativeQA(cache_dir):
	f = pd.read_csv("/mnt/cephfs/home/zhangshuhai/detect-gpt/MGTBench/datasets/NarrativeQA_chatgpt.csv")
	q = f['Question'].tolist()
	a_human = f['answers'].tolist()
	a_human = [_.split(";")[0] for _ in a_human]
	a_chat = f['chatgpt_answer'].tolist()

	res = []
	for i in range(len(q)):
		if len(a_human[i].split()) > 1 and len(a_chat[i].split()) > 1 and len(a_chat[i].split()) < 150 and len(a_chat[i].split()) < 150:

			res.append([q[i], a_human[i], a_chat[i]])

	data_new = {
		'train': {
			'text': [],
			'label': [],
		},
		'test': {
			'text': [],
			'label': [],
		}

	}

	total_num = len(res)
	for i in tqdm.tqdm(range(total_num), desc="parsing data"):
		if i < total_num * 0.8:
			data_partition = 'train'
		else:
			data_partition = 'test'
		data_new[data_partition]['text'].append(
			process_spaces(res[i][1]))
		data_new[data_partition]['label'].append(0)
		data_new[data_partition]['text'].append(
			process_spaces(res[i][2]))
		data_new[data_partition]['label'].append(1)
	return data_new


def load(name, cache_dir, **kwargs):
	if name in DATASETS:
		load_fn = globals()[f'load_{name}']
		return load_fn(cache_dir=cache_dir, **kwargs)
	else:
		raise ValueError(f'Unknown dataset {name}')
