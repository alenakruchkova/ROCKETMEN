lst = [12,19,21," ",24,22," ",3,15,26," ",3,24,1,26," ",6,19,4," ",
        16,2,2, " ",25,19,19,7," ",21,19,1,26,12," ",
        3,19, " ", 10,19,1,26, " ", 3,19, " ",3,15,26," ",
        16,24,7," ",19,6, " ", 3,15,26,24,4, " ", 10,19,15,19,4,3]

# 3,19
# 19,6

# if 19 is E the 19,6 does not work
# if 19 is T then 3,19 is either IT or AT and 19,6 is TO
t_list = ["T" if x == 19 else x for x in lst]
o_list = ["O" if x == 6 else x for x in t_list]
i_list = ["I" if x == 3 else x for x in o_list]

print i_list
