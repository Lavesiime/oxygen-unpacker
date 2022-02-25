import sys
import os

if __name__ == '__main__':
	# Open the file and also load its contents to an array
	# Yes I know this is essentially loading two instances of the same large file, but I'm lazy so this'll have to do
	f = open(sys.argv[1], "rb")
	package = f.read()

	# Header check
	if package[0:4] != b'OPCK':
		sys.exit("Invalid package file")

	# Make the directories

	entryCount = int.from_bytes(package[16:20], 'little')

	# Bytes between header and 0x10 are unknown, they probably do nothing anyways I hope
	f.seek(20)

	for i in range(entryCount):
		strlength = f.read(4)
		strlength = int.from_bytes(strlength, 'little')
		filename = f.read(strlength * 2)
		filename = filename.decode("utf-16")
		offset = int.from_bytes(f.read(4), 'little')
		size = int.from_bytes(f.read(4), 'little')
		start = offset
		end = start + size
		dump = package[start:end]

		filepaths = filename.split('/')[0:-1]
		filename = os.path.basename(filename)

		for i in filepaths:
			if not os.path.isdir(i):
				os.mkdir(i)
			os.chdir(i)

		out = open(filename, "wb")
		
		try:
			out.write(dump)
		finally:
			out.close()

		for i in filepaths:
			os.chdir("..")
		
		print("File: " + filename)