import json
import csv

with open("hats_info.json", "r", encoding='utf-8') as f:
    hat_dicts = json.load(f)


# with open('hat_data.csv', 'w', encoding='utf-8', newline='') as csvfile:
#     # Get the fieldnames from the first dictionary (keys)
#     fieldnames = hat_dicts[0].keys()
    
#     # Create a csv.DictWriter object
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    
#     # Write the header
#     writer.writeheader()
    
#     # Write each dictionary to the CSV file
#     for hat_dict in hat_dicts:
#         hat_dict['g'] = f"'{hat_dict['g']}'"
#         writer.writerow(hat_dict)

new_hat_dict = {}

for hat_dict in hat_dicts:
    name = hat_dict.pop("n").lower()
    if name not in new_hat_dict:
        new_hat_dict[name] = hat_dict
    elif new_hat_dict[name]['u'] == "11" and hat_dict['u'] != "11":
        new_hat_dict[name] = hat_dict

with open('hat_data.json', 'w', encoding='utf-8') as f:
    json.dump(new_hat_dict, f, ensure_ascii=False, indent=4)