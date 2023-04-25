import pandas as pd

candidates = pd.read_csv("Z_stack_inclusion_planning/candidates.csv")
candidates0 = pd.read_csv("Z_stack_inclusion_planning/candidates_Z0_only.csv")
candidates1 = pd.read_csv("Z_stack_inclusion_planning/candidates_Z1_only.csv")
candidates2 = pd.read_csv("Z_stack_inclusion_planning/candidates_Z2_only.csv")

cand = candidates.head(10)["TF"].to_list()
cand0 = candidates0.head(10)["TF"].to_list()
cand1 = candidates1.head(10)["TF"].to_list()
cand2 = candidates2.head(10)["TF"].to_list()

union_size_0 = len(set(cand).intersection(set(cand0)))
union_size_1 = len(set(cand).intersection(set(cand1)))
union_size_2 = len(set(cand).intersection(set(cand2)))


def num_same_postions(list1, list2):
    count = 0
    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            count += 1
    return count


num0 = num_same_postions(cand, cand0)
num1 = num_same_postions(cand, cand1)
num2 = num_same_postions(cand, cand2)

print(union_size_0, union_size_1, union_size_2)
print(num0, num1, num2)
