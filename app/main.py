import os
import subprocess
import sys

def parse_input(command):
    args = []
    current_word = ""
    in_single_quotes = False
    for char in command:
        if char == "'":
            in_single_quotes = not in_single_quotes
        elif char == " ":
            if in_single_quotes: # equivalente a == True
                current_word += char
            else:
                if current_word: # Solo agregamos si hay texto (evita guardar espacios dobles)
                    args.append(current_word)
                    current_word = ""
        else:
            current_word += char
            
    if current_word: # Si quedó una palabra al terminar el texto, la guardamos
        args.append(current_word)
        
    return args


def main():
    builtins = {"echo", "exit", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        command = input()
        if not command.strip():
            continue
        args = parse_input(command)
        cmd = args[0]
        if cmd == "exit":
            break
        elif cmd == "pwd":
            cwd = os.getcwd()
            print(cwd)
        elif cmd == "echo":   
            print(" ".join(args[1:]))
        elif cmd == "cd":
            direc = args[1]
            direc = os.path.expanduser(direc)
            if os.path.isdir(direc):
                os.chdir(direc)   
            else:
                print(f"cd: {direc}: No such file or directory")                         
        elif cmd == "type":
            arg = args[1]  
            if arg in builtins:
                print(f"{arg} is a shell builtin")   
            else:
                path = os.environ.get("PATH", "")
                found = False
                for dir in path.split(os.pathsep):
                    full_path = os.path.join(dir, arg)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        print(f"{arg} is {full_path}")
                        found = True
                        break
                if not found:
                    print(f"{arg}: not found")                 
        else:
            path = os.environ.get("PATH", "")
            found = False
            for dir in path.split(os.pathsep):
                full_path = os.path.join(dir, cmd)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    found = True
                    break
            if found:
                subprocess.run(args)
            else:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
