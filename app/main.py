import sys


def main():
    builtins = {"echo", "exit", "type"}
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        if command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            arg = command[5:]  
            if arg in builtins:
                print(f"{arg} is a shell builtin")   
            else:
                print(f"{arg}: not found")                 
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
