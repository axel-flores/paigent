from functions.get_files_info import get_files_info
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file
from functions.run_python import run_python_file


if __name__ == "__main__":

    # print("Result for current directory:")
    # result = get_file_content("calculator", "lorem.txt")
    # print(result)
    
    print("Result for current directory:")
    
    result = run_python_file("calculator", "main.py") 
    print(result)
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    result = run_python_file("calculator", "tests.py")
    print(result)
    result = run_python_file("calculator", "../main.py")
    print(result)
    result = run_python_file("calculator", "nonexistent.py")
    print(result)


    # result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print(result)
    # result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print(result)
    # result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print(result)
    
    # result = get_file_content("calculator", "main.py")
    # print(result)
    # result = get_file_content("calculator", "pkg/calculator.py")
    # print(result)
    # result = get_file_content("calculator", "/bin/cat")
    # print(result)
    # result = get_file_content("calculator", "pkg/does_not_exist.py")
    # print(result)

    # print("Result for current directory:")
    # result = get_files_info("calculator", ".")
    # print(result)
   
    # print("Result for 'pkg' directory:")
    # result = get_files_info("calculator", "pkg")
    # print(result)
   
    # print("Result for '/bin' directory:")
    # result = get_files_info("calculator", "/bin")
    # print(result)
   
    # print("Result for '../' directory:")
    # result = get_files_info("calculator", "../")
    # print(result)