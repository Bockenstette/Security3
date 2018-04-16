from Crypto.Cipher import AES
from hashlib import sha256
from sys import argv
import os

IV = "abc123ABC456XYZ0"

def Enc(prfk, aesk, index_path, files_path, cipher_path):
	files = os.listdir(files_path)
	
	index = {}
	ie_index = {}
	
	for file in files:
		filepath = os.path.join(files_path, file)
		index[file] = ReadWords(filepath, "r")
		
		# Encrypt the files as we build the index
		to_encrypt = ReadFile(filepath, "r")
		while len(to_encrypt) % 16 != 0:
			to_encrypt = to_encrypt + ' '
		
		cipher = Encrypt(aesk, to_encrypt)
		cipher_file = file.replace('f', 'c')
		
		WriteFile(os.path.join(cipher_path, cipher_file), "w+", cipher)

	# Populate inverted index
	for key in index:
		for word in index[key]:
			token = Tokenize(word)	
			
			key = key.replace('f', 'c')
			
			if token not in ie_index:
				ie_index[token] = []
			ie_index[token].append(key)
			
	# Write the invertex encrypted index to file
	to_write = ""
	for key in ie_index:
		to_write = to_write + key
		to_write = to_write + ' ' + ' '.join(ie_index[key])
		to_write = to_write + '\n'
	
	WriteFile(index_path, "w+", to_write)
	
def Search(index, token, cipher_path, aesk):
	result_filepath = "../data/result.txt"
	
	# Build Index
	ie_index = {}
	
	lines = index.splitlines()
	for line in lines:
		words = line.split(' ')
		ie_index[words[0]] = words[1:]
		
	# Error out if provided token isnt a searchable word
	if token not in ie_index:
		WriteFile(result_filepath, "w+", "")
		return

	files_to_decrypt = ie_index[token]
	files_string = ' '.join(files_to_decrypt)
	print(files_string)
	
	to_write = ""
	for file in files_to_decrypt:
		cipher = ReadFile(os.path.join(cipher_path, file))
		plaintext = Decrypt(aesk, cipher)

		to_write = to_write + file + ' ' + plaintext + '\n'
		
	print(to_write)
	WriteFile(result_filepath, "w+", files_string + '\n' + to_write)
	
def Encrypt(aesk, plaintext):
	aes = AES.new(aesk, AES.MODE_CBC, IV)
	return aes.encrypt(plaintext)
	
def Decrypt(aesk, cipher):
	aes = AES.new(aesk, AES.MODE_CBC, IV)	
	return aes.decrypt(cipher)
	
def Tokenize(word):
	return sha256(word.encode("utf-8")).hexdigest()


def WriteFile(path, args, content):
	file = open(path, args)
	file.write(content)
	file.close()
# END WriteFile
	
def ReadFile(path, args = "r"):
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
	LAMBDA = 32 # * 8 = 256 | Random generator returns bytes not bits

	if argv[1] == "keygen":
		WriteFile(argv[2], "w+", "")
		WriteFile(argv[3], "w+", os.urandom(LAMBDA))
		
	elif argv[1] == "enc":
		prfk = ReadFile(argv[2], "r")
		aesk = ReadFile(argv[3], "r")
		
		Enc(prfk, aesk, argv[4], argv[5], argv[6])
		
	elif argv[1] == "token":
		prf_key = argv[3]
		WriteFile(argv[4], "w+", Tokenize(argv[2]))
		
	elif argv[1] == "search":
		index = ReadFile(argv[2], "r")
		token = ReadFile(argv[3], "r")
		aesk = ReadFile(argv[5], "r")
		
		Search(index, token, argv[4], aesk)
		
		
# END main

if __name__ == "__main__":
	main()