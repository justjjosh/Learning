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


s = "car"
t = "crr"
test = Solution()
print(test.isAnagram(s, t))