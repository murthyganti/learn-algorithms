'''
 Write an efficient function that checks whether any permutation ↴ of an input string is a palindrome. ↴

You can assume the input string only contains lowercase letters.

Examples:

    "civic" should return True
    "ivicc" should return True
    "civil" should return False
    "livci" should return False

'''

'''
Breakdown

The brute force approach would be to check every permutation of the input string to see if it is a palindrome.

What would be the time cost?

    We'd have to generate every permutation of the input string. If the string has nnn characters, then there are nnn choices for the first character, n−1n - 1n−1 choices for the second character, and so on. In total, that's n!n!n! permutations.
    We'd have to check each permutation to see if it's a palindrome. That takes O(n)O(n)O(n) time per permutation, since each permutation is nnn letters.

Together, that's O(n!∗n)O(n! * n)O(n!∗n) time. Yikes! We have to do better.

'''

'''



Let's try rephrasing the problem. How can we tell if any permutation of a string is a palindrome?

Well, how would we check that a string is a palindrome? We could use the somewhat-common "keep two pointers" pattern. We'd start a pointer at the beginning of the string and a pointer at the end of the string, and check that the characters at those pointers are equal as we walk both pointers towards the middle of the string.

  civic
^   ^

civic
 ^ ^

civic
  ^

Can we adapt the idea behind this approach to checking if any permutation of a string is a palindrome?
Notice: we're essentially checking that each character left of the middle has a corresponding copy right of the middle. 



We can simply check that each character appears an even number of times (unless there is a middle character, which can appear once or some other odd number of times). This ensures that the characters can be ordered so that each char on the left side of the string has a matching char on the right side of the string.

But we'll need a data structure to keep track of the number of times each character appears. What should we use?

We could use a dictionary ↴ . (Tip: using a dictionary is the most common way to get from a brute force approach to something more clever. It should always be your first thought.)

So we’ll go through all the characters and track how many times each character appears in the input string. Then we just have to make sure no more than one of the characters appears an odd numbers of times.

That will give us a runtime of O(n)O(n)O(n), which is the best we can do since we have to look at a number of characters dependent on the length of the input string.

Ok, so we’ve reached our best run time. But can we still clean our solution up a little?

We don’t really care how many times a character appears in the string, we just need to know whether the character appears an even or odd number of times.


'''

'''
Solution

Our approach is to check that each character appears an even number of times, allowing for only one character to appear an odd number of times (a middle character).
This is enough to determine if a permutation of the input string is a palindrome.

We iterate through each character in the input string, keeping track of the characters we’ve seen an odd number of times using a set unpaired_characters.

As we iterate through the characters in the input string:

    If the character is not in unpaired_characters, we add it.
    If the character is already in unpaired_characters, we remove it.

Finally, we just need to check if less than two characters don’t have a pair. 


'''
import unittest


def has_palindrome_permutation(the_string):
    # Check if any permutation of the input is a palindrome
    # Track characters we've seen an odd number of times
    unpaired_characters = set()

    for character in the_string:
        if character in unpaired_characters:
            unpaired_characters.remove(character)
        else:
            unpaired_characters.add(character)
    
    # The string has a palindrome permutation if it has one or zero characters without a pair.
    # boolean
    palindrom_result = len(unpaired_characters)<= 1
    return palindrom_result


    

    return False


















# Tests

class Test(unittest.TestCase):

    def test_permutation_with_odd_number_of_chars(self):
        result = has_palindrome_permutation('aabcbcd')
        self.assertTrue(result)

    def test_permutation_with_even_number_of_chars(self):
        result = has_palindrome_permutation('aabccbdd')
        self.assertTrue(result)

    def test_no_permutation_with_odd_number_of_chars(self):
        result = has_palindrome_permutation('aabcd')
        self.assertFalse(result)

    def test_no_permutation_with_even_number_of_chars(self):
        result = has_palindrome_permutation('aabbcd')
        self.assertFalse(result)

    def test_empty_string(self):
        result = has_palindrome_permutation('')
        self.assertTrue(result)

    def test_one_character_string(self):
        result = has_palindrome_permutation('a')
        self.assertTrue(result)


unittest.main(verbosity=2)