class Solution(object):
    def longestCommonPrefix(self, strs: list[str]):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ""

        strs.sort()
        first_word = strs[0]
        last_word = strs[-1]

        idx = 0
        #comparing character by character
        while idx < len(first_word) and idx < len(last_word):
            if first_word[idx] == last_word[idx]:
                idx += 1
            else:
                break

        return first_word[:idx]
    def longestCommonPrefixVertical(self, strs: list[str]):
        if not strs:
            return ""
        ref = strs[0]
        others = strs[1:]
        for i in range(len(ref)):
            char_position = i
            other_index = [w[i] for w in others]
            if ref[char_position] == others[char_position]:


    
strs = ["flower","flow","flight"]
call = Solution()
print(call.longestCommonPrefix(strs))