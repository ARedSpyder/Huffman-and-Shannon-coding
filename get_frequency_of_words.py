# coding:utf-8
import math
import numpy as np
# import scipy.io as scio
# import csv

path = 'C:/Users/guo/Downloads/Fundamentals of Information Theory'
file_name = 'Steve Jobs Speech.txt'

def get_probability_in_descend(frequency):
  """
  convert the frequency to probability in descend
  """
  length = len(frequency)
  probability = np.zeros(length)
  i = 0
  for key in frequency:
  	probability[i] = frequency[key]
  	i += 1

  sum_ = sum(probability)
  probability = probability/sum_

  return -np.sort(-probability)

def information_entropy(frequency):
  """
  compute the information entropy
  """
  length = len(frequency)
  probability = get_probability_in_descend(frequency)
  
  log_probability = [math.log2(x) for x in probability]
  return sum(-probability*log_probability),length
  
def average_code_length(frequency,encode_list):
  """
  get the average code length
  """
  length = len(frequency)
  code_length = 0
  sum_ = 0
  for key in frequency:
  	code_length += frequency[key]*len(encode_list[key])
  	sum_ += frequency[key]
  
  return code_length/sum_


class Node(object):  
  """
  define the node struct of tree
  """
  def __init__(self, symbol='', weight=0):
    self.left = None
    self.right = None
    self.symbol = symbol # symbol
    self.weight = weight # weight or frequency
  
  # judge wether the node is a leaf
  def isLeaf(self):
  	if self.left == None and self.right == None:
  		return 1

def genarate_huffman_tree(frequency):  
  """
  generate the Huffman tree
  """
  SIZE = len(frequency)
  nodes = [Node(char, frequency.get(char)) for char in frequency.keys()]
  for _ in range(SIZE - 1):
    nodes.sort(key=lambda n: n.weight) # sort the symbol on weights
    left = nodes.pop(0)
    right = nodes.pop(0)
    parent = Node('', left.weight + right.weight)
    parent.left = left
    parent.right = right
    nodes.append(parent)
  return nodes.pop()

def encode_with_huffman(symbol, tree):  
  """
  encode symbol with Huffman coding
  """
  bits = None

  def preOrder(tree, path):
    if tree.left:
      preOrder(tree.left, path + "0")
    if tree.right:
      preOrder(tree.right, path + "1")
    if tree.symbol == symbol:
      nonlocal bits
      bits = path

  preOrder(tree, "")
  return bits

def decode_with_huffman(bits, tree):  
  """
  decode bits with Huffman coding
  """
  result = ""
  root = tree
  for bit in bits:
    if bit == "0":
      node = root.left
    elif bit == "1":
      node = root.right
    else:
      return "Code error: {}".format(bit)

    if node.isLeaf():
      result += node.symbol
      root = tree
    else:
      root = node
  return result

def encode_with_shannon(frequency):
  """
  get the encode list with Shannon coding
  """
  SIZE = len(frequency)
  nodes = [Node(char, frequency.get(char)) for char in frequency.keys()]
  probability = get_probability_in_descend(frequency)
  
  F = 0
  encode_list_Shannon = {}
  for i in range(SIZE):
    nodes.sort(key=lambda n: n.weight,reverse= True) # sort the symbol on weights
    node_ = nodes.pop(0)

    F_binary = ""
    L = int(-math.log2(probability[i])) + 1
    for j in range(L): 
      bit = bin(int(F*(2**(j+1))))
      F_binary += str(bit)[-1]

    encode_list_Shannon[node_.symbol] = F_binary

    F += probability[i]
    
  return encode_list_Shannon

def decode_with_shannon(encode_list,encoded_words):
  """
  decode the encoded article with Shannon coding
  """
  result = ""
  coding = ""
  for bit in encoded_words:
    coding += bit
    for word in encode_list:
      if coding == encode_list[word]:
        coding = ""
        result += word 	  

  return result

def txt_save(file_name,string):
  """
  save the string as .txt
  """
  fobj=open(path + '/' + file_name,'w')
  fobj.write(string)
  fobj.close()



#===================load the text file============================
f = open(path + '/' + file_name)
words = f.read()

#===================record the frequency of each symbol=============
frequency = {}
for word in words:
	frequency[word] = frequency[word] + 1 if word in frequency.keys() else 1
print('\nthe words frequency : ')
print(frequency)

## save the dic of frequency 
txt_save('frequency.txt', str(frequency))

# get the information entropy
[entropy, length] = information_entropy(frequency)
print('\n\ninformation entropy : %g ( %d symbols )\n'%(entropy,length))

#///////////////////////////////////////////////////////////////////////////
#///////////////////  Huffman coding  ////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////

#==================encode the words with Huffman coding method===============
# generate the Huffman tree
tree = genarate_huffman_tree(frequency)

# get the encode list with Huffman
encode_list_Huffman = {}
for char in frequency.keys():
	encode_list_Huffman[char] = encode_with_huffman(char, tree)
print('Huffman coding : ')
print(encode_list_Huffman)
txt_save('encode_list_Huffman.txt', str(encode_list_Huffman))

# calculate the avrage code length with Huffman
average_code_length_Huffman = average_code_length(frequency, encode_list_Huffman)
print('\nthe average code length in Huffamn : %g \n'%average_code_length_Huffman)

# encode the article with Huffman coding and save the coded article
print('encoding...')
encoded_with_Huffman = ''
for word in words:
	encoded_with_Huffman += encode_list_Huffman[word]
txt_save('encoded_article_with_Huffman.txt', encoded_with_Huffman)
print('  success')

#==================decode the words with Huffman coding method===============
# decode the words
print('\ndecoding...')
decoded_article_with_Huffman = decode_with_huffman(encoded_with_Huffman, tree)

# save the decoded article in txt
txt_save('decoded_article_with_Huffman.txt', decoded_article_with_Huffman)
print('  success\n')

#///////////////////////////////////////////////////////////////////////////
#///////////////////  Shannon coding  ////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////
# get the encode list with Shannon
encode_list_Shannon = encode_with_shannon(frequency)
print('Shannon coding : ')
print(encode_list_Shannon)
txt_save('encode_list_Shannon.txt', str(encode_list_Shannon))

# calculate the average code length with Shannon
average_code_length_Shannon = average_code_length(frequency, encode_list_Shannon)
print('\nthe average code length in Shannon : %g \n'%average_code_length_Shannon)

# encode the article with Shannon coding and save the coded article
print('encoding...')
encoded_with_Shannon = ''
for word in words:
	encoded_with_Shannon += encode_list_Shannon[word]
txt_save('encoded_article_with_Shannon.txt', encoded_with_Shannon)
print('  success')

# decode the encoded article and save it
print('\ndecoding...')
decoded_article_with_Shannon = decode_with_shannon(encode_list_Shannon, encoded_with_Shannon)
txt_save('decoded_article_with_Shannon.txt', decoded_article_with_Shannon)
print('  success')