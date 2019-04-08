#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import os
import json

base_path = r"C:\DocumentsAndStuff\Documents\Research\CollapsedWithAOI"


# In[ ]:


def count_num_tasks(df):
    prev_task = ""
    count = 0
    row_count = 0
    total_row_count = len(df.index)

    for index, row in df.iterrows():
        cur_task = row["Current_task"]
        if cur_task.upper() != "PRETASK".upper():
            if prev_task.upper() != cur_task.upper():
                count += 1

            prev_task = cur_task

        row_count += 1
        s = "Row: {}/{}".format(row_count, total_row_count)
        print(s, end="\r")

    print("")
    print(count)
    return count


# In[ ]:


non_50_list = []

for file in os.listdir(base_path):
    if file.endswith("csv"):
        filepath = os.path.join(base_path, file)
        print("File: {}".format(filepath))
        df2 = pd.read_csv(filepath, index_col=False)
        count = count_num_tasks(df2)
        
        if (count != 50):
            # raise ValueError("This file does not have 50 tasks!")
            print("This file does not have 50 tasks")
            non_50_list.append([file, count])


# In[ ]:


non_50_list
with open("non50tasks.txt", "w") as file:
    for list1 in non_50_list:
        list1 = [str(x) for x in list1]
        file.write(",".join(list1))
        file.write("\n")


# In[ ]:


df_temp = pd.read_csv("13_output.csv", index_col=False)
count_num_tasks(df_temp)


# # Count repeated tasks

# In[7]:


list_of_repeated = []
list_of_counts = []

for file in os.listdir(base_path):
    if file.endswith("csv"):
        total_count = 0
        
        set1 = set()
        # Have another set to check if the task is already added
        already_added_set = set()

        list1 = []
        
        filepath = os.path.join(base_path, file)
        print("File: {}".format(filepath))
        df2 = pd.read_csv(filepath, index_col=False)
        
        row_count = 0
        total_row_count = len(df2.index)
        prev_task = ""
        
        # Iterate over each row
        for index, row in df2.iterrows():
            cur_task = row["Current_task"]
            if cur_task.upper() != "PRETASK".upper():
                # Add it to the set ONLY if the contiguous block "ends"
                if prev_task != cur_task:
                    prev_task = cur_task
                    # Check for repeats
                    if cur_task in set1 and cur_task not in already_added_set:
                        # add to the list
                        list1.append(cur_task)
                        already_added_set.add(cur_task)
                    
                    # Only increment count on non-repeated sets
                    if cur_task not in set1:
                        total_count += 1
                    
                    set1.add(cur_task)
            row_count += 1
            s = "Row: {}/{}".format(row_count, total_row_count)
            print(s, end="\r")
            
        list_of_repeated.append([file, list1])
        list_of_counts.append([file, total_count])


# In[12]:


print(list_of_counts)
print(list_of_repeated)

total_deficit = 0
for row in list_of_counts:
    deficit = 50 - row[1]
    print(deficit, end=", ")
    total_deficit += deficit

print("")
print(total_deficit)


# In[14]:


# Total Deficit Output
total_deficit = 0
with open("TasksDeficit.csv", "w") as file:
    headers = ["File Name", "Number of Unique Tasks", "Deficit (From 50)"]
    file.write(",".join(headers))
    file.write("\n")
    for row in list_of_counts:
        deficit = 50 - row[1]
        total_deficit += deficit
        s = [row[0], row[1], deficit]
        s = [str(x) for x in s]
        file.write(",".join(s))
        file.write("\n")

    # "Total" row
    s = ["TOTAL", "", str(total_deficit)]
    file.write(",".join(s))
    file.write("\n")

print("Finished exporting")


# In[20]:


# RepeatedTask output
with open("RepeatedTasks.csv", "w") as file:
    for row in list_of_repeated:
        s = [row[0]]
        s.append(",".join(row[1]))
        file.write(",".join(s))
        file.write("\n")
    print("finished writing!")


# In[ ]:




