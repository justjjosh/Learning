#Leetcode twosum
class Solution(object):
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        found_numbers = {}
        for index, current_number in enumerate(nums):
            compliment = target - current_number
            if compliment in found_numbers:
                return [found_numbers[compliment], index]
            found_numbers[current_number] = index

"""test = Solution()
nums = [3,2,4]
target = 6
print(test.twoSum(nums, target))"""

#contains duplicate
class Solutions(object):
    def containsDuplicate(self, nums: list[int]) -> bool:
        found_numbers = set()
        for value in nums:
            if value in found_numbers:
                return True
            found_numbers.add(value)
        return False
    
"""test = Solutions()
nums = [3,2,4,3]
print(test.containsDuplicate(nums))"""

#valid anagram
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        counts = {}
        for letter in s:
            if letter in counts:
                counts[letter] += 1
            else:
                counts[letter] = 1

        search = {}
        for letter in t:
            if letter in search:
                search[letter] += 1
            else:
                search[letter] = 1

        if counts == search:
            return True
        else:
            return False

#Replace element with greatest element on the right hand side
#make the last element in the array -1 since there are no elements to its right
class Solution:
    def replaceElements(self, arr: list[int]) -> list[int]:
        #input example arr = [17, 18, 5, 4 6, 1], output: [18, 6, 6, 6, 1, -1]
        #reverse
        #get the initial max for the last index = -1
        #compare with the current index
        initial_max = -1
        for i in range(len(arr)-1, -1, -1):
            #i becomes 5-4-3-2-1
            current_value = arr[i] #current value becomes 1
            arr[i] = initial_max #the index of the current value becomes -1
            #comparing
            new_max = max(current_value, initial_max) #comparing -1 to 1
            initial_max = new_max #setting our initial max to the new max
        return arr #returns the arr after the loop finishes
    
#is Subsequence leetcode problem
#provided you have a string s = "abc" and t = "abcde", return true if s is subsequence of t without changing the order in t, i.e i.e., "ace" is a subsequence of "abcde" while "aec" is not.
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0
        j = 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1

        return i == len(s)#checks if i got to the last index, if yes it means we have found all the letters in the order that is required.

#solved leetcode majority element
#return the number that appears most frequently in an array of integer
class Solution:
    def majElement(self, nums: list) -> int:
        found_numbers = {} #create an empty hashmaps to store found values and counts
        for value in nums: #loop through the values in nums
            if value in found_numbers: #if the value alredy exist
                found_numbers[value] += 1 #add one to its count
            else:
                found_numbers[value] = 1 #if not initialize the value to count 0
        return max(found_numbers, found_numbers.get) #return the key with the maximum count.
    
#leetcode majority element second solution reducing space coplexity to O(1)
class Solution:
    def majElement(self, nums: list) -> int:
        candidate = None
        count = 0
        for num in nums:
            if count == 0:
                candidate = num
            if candidate == num:
                count += 1
            else:
                count -= 1
        if count != 0:
            return candidate
        
#solved leetcode longestcommonprefix
class Solution:
    def longestcommonprefix(self, strs: list) -> str:
        ref = ""
        for i in range(len(strs[0])):
            for w in strs:
                if i == len(w) or w[i] != strs[0][i]:
                    return ref
            ref += strs[0][i]
        return ref