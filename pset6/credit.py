import cs50 

def main():
    while True:
        cardnumber = int(input("Number: "))
        if cardnumber > 0:
            break
        
    count = 0
    digits = cardnumber
    
    while digits > 0:
        digits = digits // 10
        count = count + 1
    
    array0 = []
    arrayx2 = []
    arraysplit = []
    
    for i in range(count):
        array0.append(cardnumber % 10)
        cardnumber = cardnumber // 10
        
        
    for i in range(1, len(array0), 2):
        arrayx2.append(array0[i] * 2)
    
    
    for i in range(len(arrayx2)):
        if arrayx2[i] > 9:
            arraysplit.append(arrayx2[i] % 10)
            arraysplit.append(1)
        else:
            arraysplit.append(arrayx2[i])
    
    answer = 0
    
    
    for i in range(len(arraysplit)):
        answer = answer + arraysplit[i]
    
    
    for i in range(0, count, 2):
        answer = answer + array0[i]
        
    
    if answer % 10 == 0:
        if count == 15:
            if array0[14] == 3 or (array0[13] == 4 or array0[13] == 7):
                print('AMEX')
        if count == 16:
            if array0[15] == 5 and (array0[14] == 1 or array0[14] == 2 or array0[14] == 3 or array0[14] == 4 or array0[14] == 5):
                print("MASTERCARD")
            
            if array0[15] == 4:
                print("VISA")
        if count == 13:
            if array0[12] == 4:
                print("VISA")
    else:
        print("INVAILD")
        

main()

