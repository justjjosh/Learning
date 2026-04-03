#Leetcode twosum
class Solution(object):
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        found_numbers = {}
        for index, current_number in enumerate(nums):
            compliment = target - current_number
            if compliment in found_numbers:
                return [found_numbers[compliment], index]
            found_numbers[current_number] = index

test = Solution()
nums = [3,2,4]
target = 6
print(test.twoSum(nums, target))
        