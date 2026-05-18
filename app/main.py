import os
import subprocess
import sys


def main():
    builtins = {"echo", "exit", "type", "pwd"}
    while True:
        sys.stdout.write("$ ")
        command = input()
        if not command.strip():
            continue
        if command == "exit":
            break
        elif command == "pwd":
            cwd = os.getcwd()
            print(cwd)
        elif command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            arg = command[5:]  
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
            args = command.split()
            cmd = args[0]
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
