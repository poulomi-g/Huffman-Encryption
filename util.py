#-----------------------------------------------------
# Name: Poulomi Ganguly
# ID: 1598887
# CMPUT 274, Fall 2019
# 
# Assignment 1: Huffman decompressor and compressor
#-----------------------------------------------------

import bitio
import huffman
import pickle


def read_tree(tree_stream):
	'''Read a description of a Huffman tree from the given compressed
	tree stream, and use the pickle module to construct the tree object.
	Then, return the root node of the tree itself.

	Args:
	  tree_stream: The compressed stream to read the tree from.

	Returns:
	  A Huffman tree root constructed according to the given description.
	'''

	unpickled = pickle.load(tree_stream)

	return unpickled

def decode_byte(tree, bitreader):
	"""
	Reads bits from the bit reader and traverses the tree from
	the root to a leaf. Once a leaf is reached, bits are no longer read
	and the value of that leaf is returned.

	Args:
	  bitreader: An instance of bitio.BitReader to read the tree from.
	  tree: A Huffman tree.

	Returns:
	  Next byte of the compressed bit stream.
	"""

	currentNode = tree

	# Stops when either a leaf node is encountered OR its EOF
	while isinstance(currentNode, huffman.TreeBranch):
		
		currentBit = bitreader.readbit()

		if currentBit == 0:
			currentNode = currentNode.getLeft()
		elif currentBit == 1:
			currentNode = currentNode.getRight()

	eof = False 

	while not eof:
		try: 
			leafValue = currentNode.getValue() #Can either be a letter or may throw an EOF error
			return leafValue
		except EOFError:
			eof = True
			return None



def decompress(compressed, uncompressed):
	'''First, read a Huffman tree from the 'compressed' stream using your
	read_tree function. Then use that tree to decode the rest of the
	stream and write the resulting symbols to the 'uncompressed'
	stream.

	Args:
	  compressed: A file stream from which compressed input is read.
	  uncompressed: A writable file stream to which the uncompressed
		  output is written.
	'''
	tree = read_tree(compressed)

	bitreader = bitio.BitReader(compressed)
	bitwriter = bitio.BitWriter(uncompressed)


	returnValue = decode_byte(tree, bitreader)

	# Loop runs as long as EOF has not been encountered.
	while returnValue != None:
		
		bitwriter.writebits(returnValue, 8)

		returnValue = decode_byte(tree, bitreader)

	bitwriter.flush()

	pass




def write_tree(tree, tree_stream):
	'''Write the specified Huffman tree to the given tree_stream
	using pickle.

	Args:
	  tree: A Huffman tree.
	  tree_stream: The binary file to write the tree to.
	'''

	pickle.dump(tree, tree_stream)
	
	pass


def compress(tree, uncompressed, compressed):
	'''First write the given tree to the stream 'compressed' using the
	write_tree function. Then use the same tree to encode the data
	from the input stream 'uncompressed' and write it to 'compressed'.
	If there are any partially-written bytes remaining at the end,
	write 0 bits to form a complete byte.

	Flush the bitwriter after writing the entire compressed file.

	Args:
	  tree: A Huffman tree.
	  uncompressed: A file stream from which you can read the input.
	  compressed: A file stream that will receive the tree description
		  and the coded input data.
	'''

	write_tree(tree, compressed)

	encodingTable = huffman.make_encoding_table(tree)

	bitreader = bitio.BitReader(uncompressed)
	bitwriter = bitio.BitWriter(compressed)


	flag = 1

	# Loop runs as long as EOF has not been encountered
	while flag != 0:

		try:

			returnValue = bitreader.readbits(8)

			if returnValue in encodingTable:
				# Means the byte that has been read exists in the huffman tree

				for i in range(len(encodingTable[returnValue])):

					if encodingTable[returnValue][i] is True:
						bitwriter.writebit(True)
					elif encodingTable[returnValue][i] is False:
						bitwriter.writebit(False)

		except EOFError:

			# Searches for EOF symbol, None's sequence:
			for key in encodingTable[None]:
				bitwriter.writebit(key)
			flag = 0


	bitwriter.flush()

	pass