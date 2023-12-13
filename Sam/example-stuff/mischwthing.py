def sequence_value(n):
    return 5 * (-2)**(n - 1)

target_value = 100**100
n = 1

while sequence_value(n) <= target_value:
    n += 1
# print(sequence_value(n))
print(sequence_value(661)-target_value)

print("The smallest value of n where u_n > 100^100 is:", n)
