import os
import glob
import operator

# Find .mrc files
mrc_files = glob.glob('*.mrc')

# Extract the base names of these files
base_names = [os.path.splitext(file)[0] for file in mrc_files]

# Find .txt files with the same base name
txt_files = [f"{base}.txt" for base in base_names if os.path.isfile(f"{base}.txt")]

# Write these file names to txtname.filelist
with open('txtname.filelist', 'w') as f:
    for file in txt_files:
        f.write(f"{file}\n")

# Read the file names from txtname.filelist and extract the sixth column of text and all the text
data = []
with open('txtname.filelist', 'r') as f:
    for line in f:
        parts = line.split('_')
        if len(parts) >= 6:
            data.append((parts[5], line.strip()))

# Write this data to txtname.filelist2
with open('txtname.filelist2', 'w') as f:
    for item in data:
        f.write(f"{item[0]} {item[1]}\n")

# Sort the lines in txtname.filelist2
data.sort(key=lambda item: float(item[0]))

# Write the sorted data to txtname.filelist2
with open('txtname.filelist2', 'w') as f:
    for item in data:
        f.write(f"{item[0]} {item[1]}\n")

# Extract the second column of text from the sorted txtname.filelist2 and write it to txtname.filelist3
with open('txtname.filelist3', 'w') as f:
    for item in data:
        f.write(f"{item[1]}\n")


# Get the current folder name
current_folder = os.path.basename(os.getcwd())


# Create a .txt file with the same name as the current folder
with open(f'{current_folder}.txt', 'w') as folder_txt:
    # Read the file names from txtname.filelist3
    with open('txtname.filelist3', 'r') as f:
        lines = f.readlines()

    # Write the text from the .txt files that does not start with # into "current folder.txt"
    serial_number = 1
    for line in lines[:-1]:  # Exclude the last line
        with open(line.strip(), 'r') as txt_file:
            for txt_line in txt_file:
                if not txt_line.startswith('#'):
                    parts = txt_line.split(' ', 1)
                    folder_txt.write(f"{serial_number} {parts[1]}")
                    serial_number += 1


    # Write all the text starting with # from the .txt file in the last line of txtname.filelist3
    # and insert it at the front of the "current folder.txt" text
    with open(lines[-1].strip(), 'r') as last_txt_file:
        hash_lines = [txt_line for txt_line in last_txt_file if txt_line.startswith('#')]

# Reopen "current folder.txt" and prepend the lines starting with #
with open(f'{current_folder}.txt', 'r+') as folder_txt:
    content = folder_txt.read()
    folder_txt.seek(0, 0)
    folder_txt.write(''.join(hash_lines) + '\n' + content)

os.remove('txtname.filelist2')
os.remove('txtname.filelist')


