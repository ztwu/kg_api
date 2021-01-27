# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 9:11
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : algo_test.py
# @Software: PyCharm

#冒泡排序
data = [2,1,6,3,2,1]
for i in range(len(data)-1):
    print(i)
    for j in range(len(data)-1-i):
        if data[j] > data[j+1]:
            temp = data[j]
            data[j] = data[j+1]
            data[j+1] = temp
print(data)

# 递归
def test(n):
    global sum
    if n == 1:
        print("1==", sum+1)
        return sum + 1
    else:
        sum = sum + n
        print(sum, n)
        test(n-1)
sum = 0
n = 10
print(sum,n)
rs = test(n)
print(sum,n)

# 最大子序和
# 给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
#
# 示例:
#
# 输入: [-2,1,-3,4,-1,2,1,-5,4],
# 输出: 6
# 解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

# 状态转移方程
# dp[i] = max(nums[i], nums[i] + dp[i - 1])
#
# 解释
# i代表数组中的第i个元素的位置
# dp[i]
# 代表从0到i闭区间内，所有包含第i个元素的连续子数组中，总和最大的值
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
dp = [-2, 1, -2, 4, 3, 5, 6, 1, 5]
def maxSubArray(nums):
    """
    :type nums: List[int]
    :rtype: int
    """

    #        判断边界
    if len(nums) == 0:
        return 0
    # 定义一个表格进行存储上一个子问题的最优解
    d = []
    data = []
    data_json = {}
    d.append(nums[0])  # 第一个最优解为第一个元素
    data.append(nums[0])
    max_ = nums[0]  # 返回的最大值
    for i in range(1, len(nums)):
        print("上一个问题的最优解", data)
        data_json.setdefault(i-1, data.copy())

        # 不需要上一个问题的最优解
        if nums[i] > nums[i] + d[i - 1]:
            d.append(nums[i])
            if i > 1:
                data.clear()
            data.append(nums[i])
        else:
            d.append(nums[i] + d[i - 1])
            # 符合条件
            data.append(nums[i])
        if max_ < d[i]:
            max_ = d[i]
    return max_, d, nums, data_json

print(maxSubArray(nums))

s = [12,-4,32,-36,12,6,-6]
print("定义的数组为：",s)
s_max, s_sum = 0, 0
for i in range(len(s)):
    s_sum += s[i]
    if s_sum >= s_max:
        s_max = s_sum # 不断更新迭代s_max的值，尽可能的令其最大
    elif s_sum < 0:
        s_sum = 0
print("最大子数组和为：",s_max)

def beibao(s,m,b):
    bb = 0  # 现在的背包容量
    beibaoA = [] #放入背包的东西
    #循环的i的范围不能超过传过来的数量，并且背包的容量也不能超过预定的数量（例如：50，则只能小于等于50）
    i = 0
    while i < len(s) and bb<=b:
        #判断是否已经放入背包了
        if len(beibaoA)  != 0:
            #背包里现在没装，并且数量也不够
            if beibaoA.__contains__(s[i]) == False  and bb<b and (bb + s[i]) <= b:
                beibaoA.append(s[i])  # 暂存
                bb = bb + s[i]
            elif beibaoA.__contains__(s[i]) == False  and bb<b and (bb + s[i]) >= b:
                num = b - bb
                bb = bb + num
                beibaoA.append(num)
        else:
            beibaoA.append(s[i])  # 暂存
            bb = bb + s[i]
        i += 1
    return beibaoA,bb


if __name__ == '__main__':
    # 价值 / 重量    价值比从高低排序，，没超过往里装，超过了就不装了。  分数背包
    s = [ 10, 20, 30]  # 重量
    m = [60, 100, 120]  # 价值
    b = 50  # 背包总容量
    k = 0
    beibao  = beibao(s,m,b)
    print("背包中存入的:", beibao[0])
    print("背包的容量:", beibao[1])

    for i in range(len(s)):
        print("从：商品",i,"取：",beibao[0][i])