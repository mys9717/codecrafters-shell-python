import os
import subprocess
import sys
import shlex


def main():
    builtins = {"echo", "exit", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        command = input()
        if not command.strip():
            continue
        args = shlex.split(command)
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
