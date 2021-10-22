"""
# MIT License

# Copyright (c) 2021 eitieatgithub

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
"""
## PROGRAM ##
name:         COUNT_CHARS 2.0
description:  Count type of characters in line-arranged textfiles and visualize results. Using Python.
version:      2.0 - Program is able to handle files bigger than system memory (random access memory). Therefore chunk size has to been set properly.
author:       eitieatgithub

note:         Some characters may not be interpreted and / or misinterpreted and / or miscounted (e.g. due to file encoding)
"""

"""
MILESTONE: Make program parallel
Find a way to analyze chunks parallel on many threads / cores. Program work is almost only count characters, until it comes to adding 
the counted characters of the different chunks - until then no result is needed from the previous operation. In general the result of 
operation "before" (count chunk n-1) is not needed to work on current operation (count chunk n), and to work on chunk n+1 results of 
chunk n are not needed and so on ...
Assumption: Parallelized program should perform almost linear with core count. At first glance, only input bandwidth from mass storage 
(HDD, SSD) may limit the performance gain from parallelization.
"""

import matplotlib.pyplot as plt
import collections
import time
import json

## ## Definitions

def check_freq(x):
    freq = {}
    for c in set(x):
        freq[c] = x.count(c)
    return freq

def read_in_chunks(chunk, chunk_size):  ## ## ##https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.""" ##https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    while True:
        data = chunk.read(chunk_size)
        if not data:
            break
        yield data


## ## Data-input file to be used. Note file needs.
name_of_datafile = "testfile.txt"
## ## Set chunk size in byte, must smaller than available system memory with some threshold
## 1000 equals roughly one Kilobyte, 1000000 equals roughly one Megabyte, 1000000000 equals roughly one Gigabyte
#size_of_chunk = 1000000000
#size_of_chunk = 5000000
#size_of_chunk = 1000000
#size_of_chunk = 1000
size_of_chunk = 10
#size_of_chunk = 1

## ## get timestamp start
start_time = time.time()

chunk_size = size_of_chunk
chunk_counter = 0
number_of_characters_total = 0
number_of_chunks_processed = 0
number_of_type_char = collections.Counter()
number_of_type_char_temp = collections.Counter()
collection_so_far = collections.Counter()
with open(name_of_datafile) as f:
    for piece in read_in_chunks(f, chunk_size):
        chunk_counter = chunk_counter + 1
        ## ## get information about length of data
        ## may becomes obsolete with knowledge of chunk size, except for the last chunk: can be smaller than chunk size (file end no more data).
        ## still here for checking purposes:
        ## datafile size should be equal to chunk_size * (number of chunks -1) + number of characters of last chunk 
        ## may causes some performance drawback
        number_of_characters_chunk = len(piece)
        number_of_characters_total = number_of_characters_total + number_of_characters_chunk
        print("chunk {} is in progress, chunk_size set: {}, number of characters counted in chunk: {}".format(chunk_counter, chunk_size, number_of_characters_chunk))
        number_of_chunks_processed = number_of_chunks_processed + 1
        ## ## Count character types in certain chunk
        collection_new = check_freq(piece)
        ## convert to collections.Counter
        collection_new = collections.Counter(collection_new)
        ## add new values already existing values
        collection_so_far = collection_so_far + collection_new
        print("\n", )

## ## convert collections.Counter into dicitonary 
number_of_type_char = dict(collection_so_far) 

print("\n", )
print("number_of_chunks_processed", number_of_chunks_processed)
print("number_of_characters_total", number_of_characters_total)
print("number_of_type_char", number_of_type_char)
print("\n", )

## ## get the number of words
## Line-arranged textfile: number of words must equal number of lines in input file
## Not counting every line on purpose (would be expensive for big files), 
## instead using count of newline character "\n" to count number of words / lines
number_of_words = number_of_type_char.get("\n")
print("number of newline characters / number of words:",  number_of_words )


## ## manipulate data
## delete newline characters "\n" from dictionary
## otherwise bar without character signifier will appear in plot
del number_of_type_char["\n"]
## ## sort dictionary
number_of_type_char_sorted = sorted(number_of_type_char.items(), key=lambda x: x[1], reverse=True)
for i in number_of_type_char_sorted:
	print(i[0], i[1])
print("\n", )

print("number_of_type_char_sorted \n", number_of_type_char_sorted)

## Convert data from pairs to lists by using zip function (for plotting)
x, y = zip(*number_of_type_char_sorted)
print("\n", )

## ## plot graph
plt.figure(dpi=600)
plt.figure(figsize=(35,10))
plt.title(label="datafile used: {}; {} characters out of {} words, chunk_size: {}".format(name_of_datafile, number_of_characters_total, number_of_words, chunk_size))
plt.bar(x, y, label="ocurrance", color="orange")
plt.legend(loc='best')
plt.ylabel("number of characters occured")
plt.xlabel("character")
plt.annotate(" Copyright (c) 2021 eitieatgithub,\n https://github.com/eitieatgithub/wordlistStatisticsPython, \n note license", xy=(0.42, 0.9), xycoords='axes fraction')
plt.savefig("occurance_of_characters_chunks10.pdf")
plt.show()

## ## write results to file
## write raw results as dictionary object
## some characters might be written / appear as unicode; e.g. "\u00d6" for O (upper case o) with two dots above it
results_origin = name_of_datafile[:-4] ## get rid of ".txt" ending of input datafile
with open("raw_result_"+ results_origin, "w") as converted_rawresult:
    converted_rawresult.write(json.dumps(number_of_type_char))
## get runtime
runtime =  (time.time() - start_time)
print("runtime in seconds ", runtime)
## write runtime
with open("runtime_"+ results_origin, "w") as runtimefile:
    runtimefile.write(str(runtime)+"\n")

print("\n", )
