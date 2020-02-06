# a, b= input().split()
# print(a)
# # print(b)


# The first line contains the number of integers.
# The second line contains space separated integers for which you need to find the mean, median, mode, standard deviation and confidence interval boundaries.


# input
print('Enter the num:')
num = int(input())
print('Enter the values:')
values = [int(input())for i in range(num)]
sum = 0
Length = len(values)
# Mean (format:0.0) on the first line
# Median (format: 0.0) on the second line
# Mode(s) (Numerically smallest Integer in case of multiple integers)
# Standard Deviation (format:0.0)
# Lower and Upper Boundary of Confidence Interval (format: 0.0) with a space between them.

print(values)
## Mean
for i in range(len(values)):
    sum += i
print('The mean of the sample is')
print(sum/Length)

## Median
s1 = sorted(values)
print('median is ')
if Length % 2== 0:
    print(values[Length//2-1])
else:
    print(values[Length//2])


## Mode
count = 1
emptyDict1 = {}



# emptyDict = {key = number: values = count(number)} or ed
for i in values:
    if values.count(i) > 1:
       ed[i] = values.count(i)
for k in ed.values():
    m = max(ed.keys())
    print(m)
print('the mode of the sample is')
print(emptyDict1)