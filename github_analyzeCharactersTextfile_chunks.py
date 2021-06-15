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
#The above copyright notice and this permission notice shall be included in all
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
author: eitieatgithub

Count type of characters in line-arranged textfiles and visualize results. Using Python.
Note: Some characters may not be interpreted and / or misinterpreted and / or miscounted (e.g. due to file encoding)
"""

## ## Use Parallel Threaads
## WORKAROUND: Ensure Program can count characters in parallel threads

## ## Definitions

import matplotlib.pyplot as plt


def check_freq(x):
    freq = {}
    for c in set(x):
        freq[c] = x.count(c)
    return freq

## ## ERRORS:

## A-Error:
## # Counted characters: result is depending on chunk size, assumption: only last chunk is analyzed or added to results
 
## B-Error: 
## Chunk-Size is not caring about line ending / word ending. Therefore characters may be "cut" and counted wrong.
## Stastically this effect should be less with bigger chunk sizes: the bigger chunk size, the less characters "cut"
## WORKAROUND: write function to read linewise / wordwise -> no charachters "cut".
## number of words is no longer depending on newline character \n.  Allows better estimation of number of words and wordlength, too.
def read_in_chunks(chunk, chunk_size):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = chunk.read(chunk_size)
        if not data:
            break
        yield data



## ## Data-input file to be used. Note file needs.
name_of_datafile = "testfile.txt"
name_of_datafile = "testfile2.txt"

## ## Set chunk size, must smaller than available system memory with some threshold
## 1000000000 equals 1 Gigabyte
#size_of_chunk = 1000

## ## how big is file / how big are chunks
## how many chunks will be needed
## chunk counter: print out number of chunk processed currently

chunk_size = 6
chunk_counter = 0
number_of_characters_total = 0
print("number_of_characters_total", number_of_characters_total)
number_of_chunks_processed = 0
number_of_type_char = {} ## ## initialize empty dictionary
with open(name_of_datafile) as f:
    for piece in read_in_chunks(f, chunk_size):
        chunk_counter = chunk_counter + 1
        print("chunk {} is in progress".format(chunk_counter))
        ## ## get information about length of data
        number_of_characters_chunk = len(piece)
        number_of_characters_total = number_of_characters_total + number_of_characters_chunk
        print("number_of_characters_chunk", number_of_characters_chunk)
        number_of_chunks_processed = number_of_chunks_processed + 1
        ## ## Count character types in certain chunk
        check_freq_count = check_freq(piece)
        ## Update dictionary with results of last piece
        #number_of_type_char = number_of_type_char + check_freq_count
        number_of_type_char.update(check_freq_count)
        print("\n", )
        

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

## print out sorted dictionary
#print("check_freq_count_sorted:\n", check_freq_count_sorted)

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
plt.savefig("occurance_of_characters.pdf")
plt.show()

print("\n", )