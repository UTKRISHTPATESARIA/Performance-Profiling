import os
from shutil import move
for file_name in os.listdir('.'):
    if file_name.endswith('.c'):
        os.system(f'gcc -o {file_name.split(".")[0]} {file_name}')

# new_path = '../Programs/'
# for file_name in os.listdir('.'):
#     if file_name.endswith('.c'):
#         move(f'./{file_name}', f'{new_path}{file_name}')