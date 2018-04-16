from Crypto.Cipher import AES
from sys import argv

# "Constant" lamda since Python has no constants
LAMBDA = lambda :256

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

def main():	
	if argv[1] == "keygen":
		prf_key = ReadFile(argv[2], "r")
		aes_key = ReadFile(argv[3], "r")
# END main

if __name__ == "__main__":
	main()