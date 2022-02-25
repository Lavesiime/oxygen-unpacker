import sys
import os

if __name__ == '__main__':
	path = sys.argv[1]
	path = path.replace(os.getcwd(), "") # hacky fix for drag-and-drop, somewhat breaks command line use if there's a trailing slash
	path = path.replace("\\", "") + "/"
	
	# Could probably combine them all into 1 table but idk what i'm doing anyways
	fileNames   = []
	fileSizes   = []
	fileOffsets = []
	fileCount = 0
	
	for (root, dirs, file) in os.walk(path):
		for f in file:
			temp = root.replace("\\", "/") + "/" + f # Full relative path + name
			fileNames.append(temp)
			fileSizes.append(os.path.getsize(temp))
			fileCount = fileCount + 1

	outFile = open("data.bin", "wb")
	outFile.write(bytes("OPCK", "utf-8")) # signature
	outFile.write(b'\x02\x00\x00\x00') # version?
	outFile.write(b'\x00\x24\x02\x22') # version b? seems to align with the game version normally, may as well make it today's date
	outFile.write(b'\x00\x00\x00\x00') # seems to be content offset minus header size?
	outFile.write(fileCount.to_bytes(4, "little")) # file count
	
	print("Inputs: ")
	
	# first enter header data, using filler zeros for offsets right now
	for i in range(fileCount):
		temp = fileNames[i]
		temp = len(temp)
		temp = temp.to_bytes(4, "little")
		outFile.write(temp)
		
		temp = fileNames[i]
		temp = bytes(temp, "utf-16")
		temp = bytearray(temp)
		del temp[0] # dumb, but it works
		del temp[0]
		outFile.write(temp)
		
		outFile.write(b'\x00\x00\x00\x00')
		
		temp = fileSizes[i]
		temp = temp.to_bytes(4, "little")
		outFile.write(temp)
	
	for i in range(fileCount):
		fileOffsets.append(outFile.tell())
		
		incFile = open(fileNames[i], "rb")
		outFile.write(incFile.read())

		print(fileNames[i], "...")
	
	# and now do that again, but with the newly-gained info
	outFile.seek(20)
	for i in range(fileCount):
		temp = fileNames[i]
		temp = len(temp)
		temp = temp.to_bytes(4, "little")
		outFile.write(temp)
		
		temp = fileNames[i]
		temp = bytes(temp, "utf-16")
		temp = bytearray(temp)
		del temp[0] # again somewhat dumb, but at least it works
		del temp[0]
		outFile.write(temp)
		
		# now in place of the offset placeholde we can put actual length instead
		outFile.write(fileOffsets[i].to_bytes(4, "little"))
		
		temp = fileSizes[i]
		temp = temp.to_bytes(4, "little")
		outFile.write(temp)
	
	outFile.seek(12)
	temp = fileOffsets[0]
	temp = temp - 20
	temp = temp.to_bytes(4, "little")
	outFile.write(temp)
