from hashlib import sha256
from sys import argv

# @Param
#	difficulty	-	integer
# @Returns
#	Generated target binary string
# @Desc
# 	Generate target 2^255 binary string with the first 
# 		difficulty-bits set to 0 and the rest set to 1
def TargetGen(difficulty):
	binaryTarget = ""
	for index in range(0, difficulty):
		binaryTarget += '1'
	for index in range(difficulty, 255):
		binaryTarget += '0'
		
	return binaryTarget
# END TargetGen
	
	
# @Param
#	target		-	binary string
#	input		- 	string
#	solution	-	string
#	maxSolution	-	integer
# @Returns
#	Discovered solution
# @Desc
# Find a solution that when hashed (by SHA256) with
# 	input is less than target
def FindSolution(target, input, solution, maxSolution):	
	if Verify(input, solution, target) == 1:
		return solution
	elif solution == ('Z' * maxSolution):
		return "Solution not found"
	
	if len(solution) == maxSolution:
		return FindSolution(target, input, IncSolution(solution, -1), maxSolution)
	else:
		return FindSolution(target, input, IncSolution(solution), maxSolution)
# END FindSolution
		
		
# @Param
#	solution	- string
#	index		- integer
# @Returns
#	Solution after incrementing the letters
# @Desc
#	Takes a string and increments the characters according to their ascii value
#	i.e. aAbZ => aAca
def IncSolution(solution, index = None):
	# When size of string isn't an issue and can be easily incremented
	# Need special cases for string of size 1
	
	if (index is None):
		if solution[-1] == 'Z':
			return "aa" if (len(solution) == 1) else solution[:-2] + "aa"
		if solution[-1] == 'z':
			return 'A' if (len(solution) == 1) else solution[:-2] + 'A'
		else:
			return chr(ord(solution[-1]) + 1) if (len(solution) == 1) else solution[:-2] + chr(ord(solution[-1]) + 1)

	# When string is max size and incrementing is a bit more involved
	# Need special cases for incrementing final character
	
	# If Z is found, replace Z with a and recurse to previous letter
	if solution[index] == 'Z':
		# if string is ZZZZ, cannot increment any more, return error
		if solution[1] == 'Z':
			return "Solution not found"
		
		# Recurse to previous letter, decrement index
		IncSolution(solution[:index-1] + 'a', index - 1)
		
	# If z is found, change to A for capital letters and return
	elif solution[index] == 'z':
		return solution[:index-1] + 'A' + ("" if (index == -1) else solution[index+1:])
	
	# If current letter isn't z or Z, then simply increment the ascii value
	else:
		return solution[:index-1] + chr(ord(solution[index]) + 1) + ("" if (index == -1) else solution[index+1:])
# END IncSolution
	
	
# @Param
#	input	-	string
#	solution-	string
#	target	-	binary string
# @Returns
#	1 if the solution is valid, 0 otherwise
# @Desc
#	Hashes the input and solution with sha256 and determines
#		if the resultant hash is less than the target value
def Verify(input, solution, target, output = False):
	toHash = (input + solution).encode("utf-8")
	hashResult = sha256(toHash).hexdigest()

	ret = 0
	
	if int(hashResult,16) <= int(target,2):
		ret = 1
	
	if output:
		print(ret)
		
	return ret
# END Verify

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
	if argv[1] == "target":
		target = TargetGen(int(argv[2]))
		
		WriteFile(argv[3], "w+", target);
	elif argv[1] == "sol":
		target = ReadFile(argv[3], "r")
		input = ReadFile(argv[2], "r")
		
		solution = FindSolution(target, input, "a", 4)
		WriteFile(argv[4], "w+", solution)
	elif argv[1] == "verify":
		input = ReadFile(argv[2], "r")
		target = ReadFile(argv[3], "r")
		solution = ReadFile(argv[4], "r")
		
		Verify(input, solution, target, True)
# END main
		
if __name__ == "__main__":
	main()