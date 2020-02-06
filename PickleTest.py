import pickle

newDict = {1:'efg', 2:'pqr', 3:'jkl', 4:'rst', 5:'abc'}
#
# # open and write the bytes file
# pickle_out = open('dict.pickle', 'wb')
#
# # now dump the file
# pickle.dump(newDict, pickle_out)
#
# # now close the file
# pickle_out.close()
#

# now load the dict.pickle

# read the pickle file
pickle_in = open('dict.pickle','r')

# now load the pickle
#pickle.load(pickle_in, encoding = '-8')
#print(newDict[5])
#help(pickle)

pickle_in = pickle.dumps(pickle_in).encode('base64', 'strict')
color = pickle.loads(pickle_in.decode('base64', 'strict'))