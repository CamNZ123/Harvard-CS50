import cs50 

def main():
    Height = -1
    while True:
            print("Height: ", end = "")
            Height = cs50.get_int()
            if Height >= 0 and Height <= 23:
                break
    
    for i in range(Height):
        for j in range(Height - i - 1):
            print(' ', end = "")
        for j in range(i + 1):
            print("#", end = "")
        print('  ', end = "")
        for j in range(i + 1):
            print('#', end = "")
        print('')
        
main()