from collections import Counter
import math
# The basic idea behind this code is that we will first generate all w-permutations of "S" and "F" to a list that fit the criteria of the problem
# w = time periods
# n = number of successes required before experiment end not allowed
# p = probability of success
# s = number of successes in a general permutation
# f = w - s, number of failures in a general permutation

# change these as you like
w = 15
n = 6
p = 3/8

#Generate substrings that we should not see in the permutation ('F' followed by less than n successes)
forbidden_substrings = []
for i in range(0, n):
    forbidden_substring = 'F'
    for j in range(0, i):
        forbidden_substring += 'S'
    forbidden_substring += 'F'
    forbidden_substrings.append(forbidden_substring)

#Convert list to string in order to use .endswith
def convert(li):
    return ''.join(li)

#Create an example permutation with s Ss and f Fs
def create_permutation(s):
    elements = []
    for i in range(0, s):
        elements.append('S')
    for i in range(0, w - s):
        elements.append('F')
    return elements

#Count now many times each element of an iterable is in a string
def count_for_iterables(string, iterable):
    count = 0
    for element in iterable:
        count += string.count(element)
    return count

#Return the max index of a character in a string up to index w-n-1
def max_index_of_character(string, character):
    if character not in string:
        return -1
    else:
        for i in range(0, len(string)):
            if string[i] == character:
                max_index = i
                if max_index > w-n-1:
                    break
        return max_index

#Code adapted from more_itertools' distinct_permuation function
def distinct_success_permutations(iterable):
    def perm_unique_helper(item_counts, perm, i):
        if i < 0:
            yield tuple(perm)
        else:
            for item in item_counts:
                if item_counts[item] <= 0:
                    continue
                perm[i] = item
                item_counts[item] -= 1
                for x in perm_unique_helper(item_counts, perm, i - 1):
                    permutation = convert(x)
                    #Make sure it's a success
                    if permutation.endswith('S'):
                         # make sure there are zero instances of a forbidden substring in a success permutaton and that there is no failure afte w-m-1 trails
                        if not count_for_iterables(permutation, forbidden_substrings) > 0 and not max_index_of_character(permutation, 'F') > w-n-1:
                            yield permutation
                item_counts[item] += 1

    item_counts = Counter(iterable)
    length = sum(item_counts.values())

    return perm_unique_helper(item_counts, [None] * length, length - 1)

def main():
    success_permutations = []
    # theoretically impossible for there to be more than floor(w/2) failures in a success permutation
    for s in range(math.floor(w/2), w+1):
        success_permutations += list(distinct_success_permutations(create_permutation(s)))
    success_permutations = list(set(success_permutations))
    probability_of_success = 0
    for success_permutation in success_permutations:
        s = success_permutation.count('S')
        probability_of_success += ((p)**s)*((1-p)**(w-s))
    probability_of_failure = 1 - probability_of_success
    print('The probability of failure is: ', probability_of_failure)

main()
