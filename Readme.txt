##########################################
Readme file for the script downloader.py
##########################################


Installation of the script.
---------------------------

This script is created using Python 3.7. Below packages need to be installed to run the script.
	os
	requests
	sys
	threading
	urllib.request

To install, use the below command
	sudo pip install <Package>

1. Copy the script to the desired directory
2. If the file has extension, type below
	mv downloader.py downloader
3. Execute below, so that the tool can be run without the extension
	chmod 777 downloader
4. Execute the script in the format given in the question
	./downloader <URL> -c nThreads
	Eg: ./downloader http://crystal.uta.edu/~gopikrishnav/classes/common/4308_5360/slides/Informed_Search.pdf -c 5


About downloader.py
-------------------
This tool downloads the file given by the URL provided to the script during the execution.

The "nThreads" value decides as to how many threads needs to be parallelly run inorder to download the whole file. When the value given is 5, the whole file is divided into 5 chunks and using 5 threads, each chunks will be downloaded.

Each chunk will be retried only once when the first try is failed.

When all the chunks are downloaded, they are aggragated to form a complete file.

Note: When the number of threads increases, the performance decreases since it has to process all the threads and calculate the chunks. When the number of chunks are small, the downloading time increases since using less threads, the whole file is downloaded. Hence, it is advised to give an average number of threads.