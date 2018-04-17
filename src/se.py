from Crypto.Cipher import AES
from hashlib import sha256
from sys import argv
import os

IV = "abc123ABC456XYZ0"

# @Param
# 	prfk		-	string
#	aesk		-	string
#	index_path	-	string
#	files_path	-	string
#	cipher_path	-	string
# @Returns
#	Nothing
# @Desc
#	Takes in a file directory to read into an inverted
#	encrypted index. Saves the build ie_index at passed
#	index path and encrypts all files with the passed
#	AES key. Encrypted files then saved into passed
#	cipher directory
def Enc(prfk, aesk, index_path, files_path, cipher_path):
	# Get list of all files in passed directory
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
		# Rename the files from f# to c#
		cipher_file = file.replace('f', 'c')
		
		WriteFile(os.path.join(cipher_path, cipher_file), "w+", cipher)

	# Populate inverted index
	for key in index:
		for word in index[key]:
			token = Tokenize(word)	
			
			# Rename key from f# to c#
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
	
	
# @Param
#	index		-	string
#	token		-	string
#	cipher_path	-	string
#	aesk		-	string
# @Returns
#	Nothing
# @Desc
#	Loads in inverted encrypted index for searching.
#	Searches for the passed token in the index, and 
#	if found, decrypts the relevant ciphertext files
#	with the passed AES key and displays them while
#	also writing the result to a file.
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

	# Get the files that need to be decrypted and print them out
	files_to_decrypt = ie_index[token]
	files_string = ' '.join(files_to_decrypt)
	print(files_string)
	
	# Decrypt the files and build up a string of their contents
	# for printing and writing
	to_write = ""
	for file in files_to_decrypt:
		cipher = ReadFile(os.path.join(cipher_path, file))
		
		plaintext = Decrypt(aesk, cipher.decode('string_escape'))

		to_write = to_write + file + ' ' + plaintext + '\n'
		
	print(to_write)
	WriteFile(result_filepath, "w+", files_string + '\n' + to_write)
# END Search
	
	
# @Param
#	aesk		-	string
#	plaintext	-	string
# @Returns
#	Ciphertext result of encryption
# @Desc
#	Takes in an AES key and a plaintext to encrypt,
#	then ecrypts the plaintext and returns the result
def Encrypt(aesk, plaintext):
	aes = AES.new(aesk, AES.MODE_CBC, IV)
	return aes.encrypt(plaintext)
# END Encrypt
	
	
# @Param
#	aesk	-	string
#	cipher	-	string
# @Returns
#	Decrypted plaintext
# @Desc
#	Takes in an AES key and a ciphertext to decrypt,
#	then decrypts the ciphertext and returns the result
def Decrypt(aesk, cipher):
	aes = AES.new(aesk, AES.MODE_CBC, IV)	
	return aes.decrypt(cipher)
# END Decrypt
	
	
# @Param
#	word	-	string
# @Returns
#	Tokenized word
# @Desc
#	Takes in a word then performs sha256 to simulate a prf.
#	Requires no key
def Tokenize(word):
	return sha256(word.encode("utf-8")).hexdigest()
# END Tokenize
	
	
def WriteFile(path, args, content):
	file = open(path, args)
	file.write(content)
	file.close()
# END WriteFile
	
	
def ReadFile(path, args = "rb"):
	file = open(path, args)
	content = file.read()
	file.close()
	
	return content
# END ReadFile


# @Param
#	path	-	string
#	args	-	string
# @Returns
#	List of all words in the file found at path
# @Desc
#	Reads in a file found at path then splits every word found
#	within into a list, which is then returned.
def ReadWords(path, args):
	file = open(path, args)
	content = [word for line in file for word in line.split()]
	file.close()
	
	return content
# END ReadWords


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