from functions.get_file_content import get_file_content
from config import MAX_CHARS

def test():
    result = get_file_content("calculator", "lorem.txt")
    print("Result for 'lorem.txt':")
    print(f"  Length of output: {len(result)}")
    print(result[MAX_CHARS:])

    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py'")
    print(f"  Length of output: {len(result)}")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py':")
    print(f"  Length of output: {len(result)}")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat':")
    print(f"  Length of output: {len(result)}")
    print(result)

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'pkg/does_not_exist.py':")
    print(f"  Length of output: {len(result)}")
    print(result)


if __name__ == "__main__":
    test()