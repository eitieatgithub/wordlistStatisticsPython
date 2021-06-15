"""
# MIT License

# Copyright (c) 2021 chrisX220

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
author: chrisX220

Count type of characters in line-arranged textfiles and visualize results. Using Python.
Note: Some characters may not be interpreted and / or misinterpreted and / or miscounted (e.g. due to file encoding)
"""

## ## Definitions

import matplotlib.pyplot as plt


def check_freq(x):
    freq = {}
    for c in set(x):
        freq[c] = x.count(c)
    return freq


## ## Data-input file to be used. Note file needs.
name_of_datafile="testfile.txt"

## ## get data out of input file and count some characters 
## open file in read mode
file = open(name_of_datafile, "r")
## read the content of file
data = file.read()
print("\n", )

## get the total number of characters
number_of_characters = len(data)
print("number_of_characters: \n", number_of_characters)
print("\n", )

## call function check_freq to count type of characters       
check_freq_count = check_freq(data)

##  get the number of words
## Line-arranged textfile: number of words must equal number of lines in input file
## Not counting every line on purpose (would be expensive for big files), 
## instead using count of newline character "\n" to count number of words / lines
number_of_words = check_freq_count.get("\n")
print("number of newline characters / number of words:",  number_of_words )


## ## manipulate data
## delete newline characters "\n" from dictionary
## otherwise bar without character signifier will appear in plot
del check_freq_count["\n"]
## ## sort dictionary
check_freq_count_sorted = sorted(check_freq_count.items(), key=lambda x: x[1], reverse=True)
for i in check_freq_count_sorted:
	print(i[0], i[1])
print("\n", )

## print out sorted dictionary
#print("check_freq_count_sorted:\n", check_freq_count_sorted)

## Convert data from pairs to lists by using zip function (for plotting)
x, y = zip(*check_freq_count_sorted)
print("\n", )


## ## plot graph
plt.figure(dpi=600)
plt.figure(figsize=(35,10))
plt.title(label="datafile used: {}; {} characters out of {} words".format(name_of_datafile, number_of_characters, number_of_words))
plt.bar(x, y, label="ocurrance", color="orange")
plt.legend(loc='best')
plt.ylabel("number of characters occured")
plt.xlabel("character")
plt.savefig("occurance_of_characters.pdf")
plt.show()

print("\n", )