import re
import operator
import csv


per_user = {}
error_dict = {}

def check_cat(line):
    global error_dict
    global per_user
    pattern = r"ticky: ([\w]+):( [\w\ \#\[\]]+) \((\w+)\)"
    result = re.search(pattern, line)
    if result!=None:
        category = result.group(1)
        error = result.group(2)
        username = result.group(3)
        if category == "ERROR":
            error_dict[error] = error_dict.get(error, 0)
            error_dict[error] += 1
            if username in per_user:
                user_dict = per_user.get(username)
                user_dict["ERROR"] = user_dict.get("ERROR",0)
                user_dict["ERROR"] += 1
                per_user[username]["ERROR"] = user_dict["ERROR"]
            else:
                per_user[username] = {"ERROR":1}

        elif category == "INFO":
            if username in per_user:
                user_dict = per_user.get(username)
                user_dict["INFO"] = user_dict.get("INFO",0)
                user_dict["INFO"] += 1
                per_user[username]["INFO"] = user_dict["INFO"]
            else:
                per_user[username] = {"INFO":1}

def sort_error():
    return sorted(error_dict.items(),key=operator.itemgetter(1),reverse=True)

def sort_user():
    return sorted(per_user.items(),key=operator.itemgetter(0))

def err_csv(err_sorted):
    file_name = "error_message.csv"
    columns = ["ERROR","Count"]
    try:
        with open(file_name,"w") as file:
            file.write("%s,%s\n"%(columns[0], columns[1]))
            for item in err_sorted:
                file.write("%s,%s\n"%(item[0], item[1]))
    except:
        print("failed to write file")

def user_csv(user_sorted):
    file_name = "user_info.csv"
    columns = ["Username", "INFO","ERROR"]

    #try:
    with open(file_name,"w") as file:
        file.write("%s,%s,%s\n"%(columns[0], columns[1], columns[2]))
        for item in user_sorted:
            file.write("%s,%d,%d\n"%(item[0], item[1]["INFO"],item[1]["ERROR"]))




err_sorted = sort_error()
user_sorted = sort_user()
print(user_sorted)
print(err_sorted)
err_csv(err_sorted)
user_csv(user_sorted)
