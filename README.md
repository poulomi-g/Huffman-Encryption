# Huffman-Encryption

### Description
Programs that compress and decompress ﬁles using Huffman codes. The compressor will be a command-line utility that encodes any ﬁle into a compressed version with a .huf extension. The decompressor will be a web server that will let you directly browse compressed ﬁles, decoding them on-the-ﬂy as they are being sent to your web browser. 

### Included Files as part of assignment:
- bitio.py: Contains the classs BitWriter and BitReader
- compress.py: Runs the code to compress a file.
- huffman.py: Used to create huffman trees as well as encode and decode messages. To be written in class.
- webserver.py: The file that allows viewing of the compressed files as they are being sent to the web browser
- wwwroot directory: contains compressed versions of the webpage (index.html.huf) and the image of Huffman (huffman.bmp.huf)

### Modified Files:
- util.py: Contains the five functions read_tree(), decode_byte(), write_tree(), compress(), and decompress().
	* read_tree(): Takes in a tree stream and returns it unpickled.
	* decode_byte(): Traverses given tree from root to leaf and returns the leaf node it ends at.
	* decompress(): Takes in a compressed file stream and unpickles it using read_tree(). Then uses decode_byte() and tree to decode compressed stream and writes it to uncompressed stream.
	* write_tree(): Takes in a tree and pickles it to be written into given tree_stream
	* compress(): Uses write_tree() to pass in pickled tree to compressed stream. With the use of an huffman.make_encoding_table() and instances of class BitReader and BitWriter, writes encodied bits into compressed stream taking into account EOF error.

### Running the code:
Go to the wwwroot directory. Open a bash terminal and open the web server using "python3 ../webserver.py". You can then go to the url "http://localhost:8000" to view the webpage and image of Huffman that will appear if the decompressor is functioning properly. Note that the port can be changed by modifying the variable port in webserver.py.

To compress a file, first copy that file over to the wwwroot directory and then move to that directory and type "python3 ../compress.py somefile.ext" where somefile is the name of the file you wish to compress and ext is the extension. Then go to the url "http://localhost:8000/somefile.ext" to view and/or download the decompressed file.


### Assumptions:
	* Streams are opened in proper modes.
	* Files entered in command line exists and in correct directory
	* util.py exists in correct directory
