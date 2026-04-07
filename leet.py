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
