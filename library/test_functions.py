import os

def functions_operations():
    print(f" echo from functions_operations in test_functions.py")
    print(f"1 {os.path.basename(__file__)}")
    print(f"2 {__file__}")
    print(f"3 {os.path.dirname(__file__)}")
    print(f"4 {os.path.basename(__file__)}")
    print(f"5 {__file__}")
    print(f"6 {os.path.basename(__file__)}")
    print(f"7 {os.path.basename(os.path.realpath(__file__))}")
    print(f"8 {os.path.basename(os.path.realpath(__file__))}")
    print(f"9 {os.path.realpath(__file__)}")
    print(f"10 {os.path.basename(os.path.realpath(__file__))}")
    print(f"11 {__file__}")
    print(f"12 {os.path.abspath(os.path.dirname(__file__))}")
    print(f"13 {os.path.dirname(__file__)}") 