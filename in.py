# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 09:37:50 2023

@author: Sai Teja Sanku
"""

import os
import json
import re  # Import the regular expression module for grep

class InMemoryFileSystem:
    def __init__(self):
        self.current_directory = '/'
        self.file_system = {}
    # the mkdir command use to make directories
    def mkdir(self, directory_name):
        new_directory_path = os.path.join(self.current_directory, directory_name)
        self.file_system[new_directory_path] = {}
        print(f"Directory '{directory_name}' created.")
    #the cd command use to naviagte the path root and parent directories
    def cd(self, path):
        if path == '/':
            self.current_directory = '/'
        elif path.startswith('/'):
            self.current_directory = os.path.normpath(path)
        elif path == '..':
            # Move to the parent directory
            self.current_directory = os.path.normpath(os.path.dirname(self.current_directory.rstrip('/')))
        else:
            self.current_directory = os.path.normpath(os.path.join(self.current_directory, path))
            print(f"Current directory changed to '{self.current_directory}'.")

    #the touch command use to import files in specified 
    def touch(self, file_name, path='.'):
        file_path = os.path.normpath(os.path.join(self.current_directory, path.lstrip('/'), file_name))
        self.file_system[file_path] = {'content': ''}
        print(f"File '{file_path}' created.")
    
    #ls command use to list out the contents of specified directories
    def ls(self, path='.'):
        target_path = os.path.normpath(os.path.join(self.current_directory, path.lstrip('/')))
        if target_path not in self.file_system or not self.file_system[target_path]:
            print(f"Error: Directory '{target_path}' not found or is empty.")
        else:
            contents = list(self.file_system[target_path].keys())
            print(f"Contents of {target_path}: {contents}")


    def grep(self, pattern, path='.'):
        target_path = os.path.join(self.current_directory, path)
        if target_path not in self.file_system:
            print(f"Error: Directory '{target_path}' not found.")
        else:
            matching_files = [file for file in self.file_system[target_path] if re.search(pattern, self.file_system[file].get('content', ''))]
            print(f"Files matching pattern '{pattern}' in {target_path}: {matching_files}")

    def cat(self, file_name, path='.'):
        file_path = os.path.join(self.current_directory, path, file_name)
        if file_path not in self.file_system:
            print(f"Error: File '{file_path}' not found.")
        else:
            print(f"Contents of {file_path}: {self.file_system[file_path].get('content', '')}")
            
    #echo is used to write the text into the file
    def echo(self, content, file_name, path='.'):
        file_path = os.path.join(self.current_directory, path, file_name)
        if file_path not in self.file_system:
            print(f"Error: File '{file_path}' not found.")
        else:
            self.file_system[file_path]['content'] = content
            print(f"Content '{content}' written to {file_path}.")
    #mv command used to move from one location to another location
    def mv(self, source, destination):
        source_path = os.path.join(self.current_directory, source)
        destination_path = os.path.join(self.current_directory, destination)
        if source_path not in self.file_system:
            print(f"Error: Source '{source_path}' not found.")
        elif destination_path in self.file_system:
            print(f"Error: Destination '{destination_path}' already exists.")
        else:
            self.file_system[destination_path] = self.file_system.pop(source_path)
            print(f"Moved '{source_path}' to '{destination_path}'.")
    
    #copy the content
    def cp(self, source, destination):
        source_path = os.path.join(self.current_directory, source)
        destination_path = os.path.join(self.current_directory, destination)
        if source_path not in self.file_system:
            print(f"Error: Source '{source_path}' not found.")
        elif destination_path in self.file_system:
            print(f"Error: Destination '{destination_path}' already exists.")
        else:
            self.file_system[destination_path] = json.loads(json.dumps(self.file_system[source_path]))  # Deep copy
            print(f"Copied '{source_path}' to '{destination_path}'.")
            
    #remove the file
    def rm(self, target, path='.'):
        target_path = os.path.join(self.current_directory, path, target)
        if target_path not in self.file_system:
            print(f"Error: Target '{target_path}' not found.")
        else:
            del self.file_system[target_path]
            print(f"Removed '{target_path}'.")

    def save_state(self, path):
        with open(path, 'w') as file:
            json.dump(self.file_system, file)
        print(f"File system state saved to {path}.")

    def load_state(self, path):
        with open(path, 'r') as file:
            self.file_system = json.load(file)
        print(f"File system state loaded from {path}.")
        
        
#the mainfunction runs utill-unlse we use command "exit"
def main():
    file_system = InMemoryFileSystem()

    while True:
        command = input("Enter command: ")
        if command.lower() == 'exit':
            break
        elif command.startswith('save_state'):
            _, path = command.split(' ')
            file_system.save_state(path)
        elif command.startswith('load_state'):
            _, path = command.split(' ')
            file_system.load_state(path)
        else:
        
            parts = command.split(' ')
            operation = parts[0]
            args = parts[1:]
            if hasattr(file_system, operation):
                getattr(file_system, operation)(*args)
            else:
                print(f"Error: Unknown command '{command}'.")
                
                
# it is the function where we can call main function
if __name__ == "__main__":
    main()
    
    
    
    
    

