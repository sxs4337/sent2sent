
#Import Flicker 8k data and return the sentences pairs. 

import itertools
import pickle
import pdb
import numpy as np
from random import shuffle

def preProBuildWordVocab(sentence_iterator, word_count_threshold=5): # borrowed this function from NeuralTalk
    print 'preprocessing word counts and creating vocab based on word count threshold %d' % (word_count_threshold, )
    word_counts = {}
    nsents = 0
    for sent in sentence_iterator:
        nsents += 1
        for w in sent.lower().split(' '):
           word_counts[w] = word_counts.get(w, 0) + 1

    vocab = [w for w in word_counts if word_counts[w] >= word_count_threshold]
    print 'filtered words from %d to %d' % (len(word_counts), len(vocab))

    ixtoword = {}
    ixtoword[0] = '.'  # period at the end of the sentence. make first dimension be end token
    wordtoix = {}
    wordtoix['#START#'] = 0 # make first vector be the start token
    ix = 1
    for w in vocab:
        wordtoix[w] = ix
        ixtoword[ix] = w
        ix += 1

    word_counts['.'] = nsents
    bias_init_vector = np.array([1.0*word_counts[ixtoword[i]] for i in ixtoword])
    bias_init_vector /= np.sum(bias_init_vector) # normalize to frequencies
    bias_init_vector = np.log(bias_init_vector)
    bias_init_vector -= np.max(bias_init_vector) # shift to nice numeric range
    return wordtoix, ixtoword, bias_init_vector

captions=open("./data/Flickr8k.token.txt").read()
captions=captions.split("\n")
final_data=[]
for x in range(0,len(captions)-1,5):
    temp_sentences=[]
    for y in range(x,x+5):
        # pdb.set_trace()
        temp_sentences.append(captions[y].split('\t')[1].lower())
    sentence_combinations=itertools.combinations(temp_sentences,2)
    for combinations in sentence_combinations:
        final_data.append(combinations)

# pdb.set_trace()
train_data = final_data[:70000]
shuffle(train_data)
pickle.dump(train_data,open('data/flickr8kPairs_train.pkl','wb'))
test_data = final_data[70000:]
shuffle(test_data)
pickle.dump(test_data,open('data/flickr8kPairs_test.pkl','wb'))

all_sentences=[]
for pair in train_data:
	all_sentences.append(pair[0])
	all_sentences.append(pair[1])

(word2Idx,idx2Word,_)=preProBuildWordVocab(all_sentences,word_count_threshold=5)

np.save('./data/ixtoword-flickr8k', idx2Word)
np.save('./data/wordtoix-flickr8k', word2Idx)

