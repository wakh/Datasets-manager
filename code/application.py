from code.map_operator import MapOperator
from code.database import SqlOperator

def main():
    while True:
        print("Input a command:")
        cmd = input()

        # Exit Command
        if cmd == "\\q":
            break
        elif cmd == "\\range coordinates":
            print("")
        elif cmd == "\\range date":
            print("")
        elif cmd == "\\location coordinates":
            print("")
        else:
            print("ERROR: Input not Valid.")


if __name__ == "__main__":
    main()