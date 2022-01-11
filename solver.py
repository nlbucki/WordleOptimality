import multiprocessing as mp
import csv

from wordleWords import wordleWords
from filter import Filter

num_words = len(wordleWords)

# List in form of (first_guess, average over all answers of number of words remaining after guess)
avg_words_remaining = []
def printBestWords():
    # Sort by avg number words remaining
    avg_words_remaining.sort(key= lambda x : x[1])
    for word, avg_remaining in avg_words_remaining[:5]:
        print(f'First guess = {word}, Average words remaining = {avg_remaining}')

def averageWordsRemaining(first_guess):
    sum_of_words_remaining = 0.0
    for answer in wordleWords:
        filter = Filter(first_guess, answer)
        sum_of_words_remaining += len(filter.applyFilter(wordleWords))
    return sum_of_words_remaining / num_words

pool = mp.Pool(mp.cpu_count())

num_batches = 100
batch_size = num_words // num_batches
for i in range(num_batches - 1):
    print('Progress = {}%'.format(100 * i / float(num_batches)))
    printBestWords()
    start_inx = i * batch_size
    end_inx = (i+1) * batch_size
    first_guess_batch = wordleWords[start_inx:end_inx]
    batch_averages = pool.map(averageWordsRemaining, first_guess_batch)
    avg_words_remaining += zip(first_guess_batch, batch_averages)

# Last batch contains the rest in case num_words isn't perfectly divisible by num_batches
print('Progress = {}%'.format(100 * (num_batches - 1) / float(num_batches)))
printBestWords()
first_guess_batch = wordleWords[end_inx:]
batch_averages = pool.map(averageWordsRemaining, first_guess_batch)
avg_words_remaining += zip(first_guess_batch, batch_averages)

pool.close()


print('Final results = ')
printBestWords()

with open('results.csv', 'w') as file:
    csvwriter = csv.writer(file) 
    csvwriter.writerows(avg_words_remaining)