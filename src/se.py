from Crypto.Cipher import AES
from hashlib import sha256

import os
import binascii

from sys import argv

def Encrypt(prfk, aesk, index_path, files_path, cipher_path):
	files = os.listdir(files_path)
	
	index = {}
	ie_index = {}
	
	for file in files:
		index[file] = ReadWords(os.path.join(files_path, file), "r")

	# Populate inverted index
	for key in index:
		for word in index[key]:
			hex = sha256(word.encode("utf-8")).hexdigest()		
			
			if hex not in ie_index:
				ie_index[hex] = []
			ie_index[hex].append(key)
			
	# Write the invertex encrypted index to file
	to_write = ""
	for key in ie_index:
		to_write = to_write + key
		to_write = to_write + ' ' + ' '.join(ie_index[key])
		to_write = to_write + '\n'
	
	WriteFile(index_path, "w+", to_write)
	
	


def WriteFile(path, args, content):
	file = open(path, args)
	file.write(content)
	file.close()
# END WriteFile
	
def ReadFile(path, args):
	file = open(path, args)
	content = file.read()
	file.close()
	
	return content
# END ReadFile

def ReadWords(path, args):
	file = open(path, args)
	content = [word for line in file for word in line.split()]
	file.close()
	
	return content
# END ReadFile

def main():	
	LAMBDA = 256

	if argv[1] == "keygen":
		WriteFile(argv[2], "w+", "")
		WriteFile(argv[3], "w+", os.urandom(LAMBDA))
	elif argv[1] == "enc":
		prf_key = ReadFile(argv[2], "r")
		aes_key = ReadFile(argv[3], "r")
		index_path = argv[4]
		files_path = argv[5]
		cipher_path = argv[6]
		
		Encrypt(prf_key, aes_key, index_path, files_path, cipher_path)
		
		
# END main

if __name__ == "__main__":
	main()