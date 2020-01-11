#!/usr/bin/env python

#########################################################################
# Author    : Sagar Surendran
# Brief     : Program to download the file given in the URL. 
#             It will be downloaded in "parts" given in the number 
#             provided while executing the same in the command line.
# Date      : 1/10/2020
# Usage     : ./downloader <URL> -c nThreads
##########################################################################

import os
import requests
import sys
import threading
import urllib.request
#import time

#Function to divide the content of the URL data to the number of small parts given in the command line(num_of_splits)
def split_content(value, num_of_splits):
    lst = []
    for i in range(num_of_splits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(num_of_splits*1.0) + value/(num_of_splits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(num_of_splits*1.0),0)), int(round(1 + i * value/(num_of_splits*1.0) + value/(num_of_splits*1.0)-1, 0))))
    return lst

# Main function
def main():

    #set the starting time
    #start_time = time.time()

    # Check the arguments and set them.
    arguments = len(sys.argv) -1
    if arguments < 3:
        print("Insufficient arguments. Total provided is ", arguments)
        print("Usage : ./downloader <URL> -c nThreads")
        return

    print(sys.argv[1])

    url = sys.argv[1]
    num_of_threads = int(sys.argv[3])

    file_name: object = url.split('/')[-1]
    data_length = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    print("%s bytes will be downloaded" % data_length)
    if not data_length:
        print("Invalid data length has been received for the requested url.")
        return

    dataDict = {}

    ranges = split_content(int(data_length), num_of_threads)

    #This function downloads the content. There is only one retry when the first try for the download is failed.
    def download_chunk(idx, irange):
        try:
            req = urllib.request.Request(url)
            req.headers['Range'] = 'bytes={}'.format(irange)
        except:
            print("Unable to establish connection using the given URL!!!")
        try:
            dataDict[idx] = urllib.request.urlopen(req, timeout=1.0).read()
            fir=irange.split('-')[0]
            sec=irange.split('-')[1]
            diff=int(sec) - int(fir) + 1
            #print("dict data len : ", dataDict[idx].__len__(), "and diff : ", diff)
        except:
            if (int(diff) < int(dataDict[idx].__len__())):
                try:
                    print("Download failed. Trying once again..")
                    dataDict[idx] = urllib.request.urlopen(req, timeout=1.0).read()
                except:
                    print("Error in downloading the file.")
                    pass

    # create one downloading thread per chunk
    downloaders = [
        threading.Thread(target=download_chunk, args=(idx, irange),)
        for idx,irange in enumerate(ranges)
        ]

    # start threads and run all in parallel
    for th in downloaders:
        th.start()
    for th in downloaders:
        th.join()

    print ('In {} parts/threads, total {} bytes will be downloaded'.format(
        len(dataDict), sum( (
            len(chunk) for chunk in dataDict.values()
        ) )
    ))

    # print ("Total time taken: %s seconds" % str(time.time() - start_time))

    if os.path.exists(file_name):
        print("Same file name already exists in the directory. This file will be replaced with the one given in the URL")
        os.remove(file_name)

    # aggregate the content to form the file
    with open(file_name, 'wb') as fh:
        if num_of_threads == dataDict.__len__():
            for _idx,chunk in sorted(dataDict.items()):
                fh.write(chunk)
        else:
            print("Error: URL content could not be downloaded")
            if os.path.exists(file_name):
                os.remove(file_name)

    print ("Download successful. \nFile name: ", str(file_name) )
    print ('File size:  {} bytes'.format(os.path.getsize(file_name)))

if __name__ == '__main__':
    main()
