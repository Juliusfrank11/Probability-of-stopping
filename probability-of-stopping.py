import more_itertools
# The basic idea behind this code is that we will first generate all w-permutations of "S" and "F" to a list, then remove ones which do not make sence in the context of the problem
# w = time periods
# n = number of successes required before experiment end not allowed
# p = probability of failure
# s = number of successes in a general permutation
# f = w - s, number of failures in a general permutation

# Change these to suit your needs
w = 12
n = 6
p = 3/8

# Generate substrings that we should not see in valid permutations
forbidden_substrings = []
for i in range(0, n):
    forbidden_substring = 'F'
    for j in range(0, i):
        forbidden_substring += 'S'
    forbidden_substring += 'F'
    forbidden_substrings.append(forbidden_substring)
forbidden_substrings.append('FFF')

def convert(li):
    return ''.join(li)

def create_permutation(s):
    elements = []
    for i in range(0, s):
        elements.append('S')
    for i in range(0, w - s):
        elements.append('F')
    return elements

def count_for_iterables(string, iterable):
    count = 0
    for element in iterable:
        count += string.count(element)
    return count

def element_in_string(string, iterable):
    if count_for_iterables(string, iterable) > 1 or count_for_iterables(string, iterable) == 0:
        return None
    else:
        for element in iterable:
            if element in string:
                return element

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

def find_valid_permutations(permutations):
    valid_permutations = []
    for permutation in permutations:
        # make sure there is only one instance of a forbidden substring in a stopping permutaton
        while count_for_iterables(permutation, forbidden_substrings) > 1:
            for forbidden_substring in forbidden_substrings:
                if forbidden_substring in permutation:
                    permutation = permutation[0:permutation.index(forbidden_substring)+len(forbidden_substring)]
        valid_permutations.append(permutation)
        if element_in_string(permutation, forbidden_substrings) != None:
            el = element_in_string(permutation, forbidden_substrings)
            #The forbidden string should be at the end of the permuation and we should remove things like FSSFSSF when n > 2 even though count_for_iterables will return one with such a string
            if not permutation.endswith(el) or (permutation.index(el) < len(permutation) - len(el)):
                valid_permutations.remove(permutation)
    valid_permutations_temp = valid_permutations
    for valid_permutation in valid_permutations_temp:
        # Processes should stop if there is a failure at least on period w-n
        if max_index_of_character(valid_permutation, 'F') > w-n-1 and max_index_of_character(valid_permutation, 'F') != w-1:
            valid_permutations[valid_permutations.index(valid_permutation)] = valid_permutation[:max_index_of_character(valid_permutation, 'F') + 1]
        #All successes should be of lenght w
        elif not valid_permutation.endswith('F') and len(valid_permutation) < w:
            valid_permutation[valid_permutations.index(valid_permutation)] = valid_permutation+ 'F'
    #remove duplicates
    valid_permutations = list(set(valid_permutations))
    return valid_permutations

def find_probability(permutation):
    s = permutation.count('S')
    f = permutation.count('F')
    probability = ((1-p)**s)*(p**f)
    return probability

def probability_of_stopping(permutations):
    stopping_probability = 0
    for permutation in permutations:
        if permutation.endswith('F'):
            stopping_probability += find_probability(permutation)
    return stopping_probability

def main():
    valid_permutations = []
    for i in range(0, w+1):
        permutation = create_permutation(i)
        permutations = list(map(convert, more_itertools.distinct_permutations(permutation)))
        valid_permutations += find_valid_permutations(permutations)
    valid_permutations = list(set(valid_permutations))
    print('The probability of stopping: ', probability_of_stopping(valid_permutations))
    
main()
