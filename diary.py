
#윤년 = True, 아니면 False
def LeapCheck(year): 
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0) 

def lastDay(year, month):#그 달의 마지막날자를 반환
    m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if LeapCheck(year):
        m[1] = 29
    return m[month - 1]

def totalDay(year, month, day): #총 날짜 반환
    total = 365*(year-1)

    for i in range(1, year): #전년도까지 윤년수
        if LeapCheck(i):
            total += 1
    
    for i in range(1, month): #전 달까지 날짜
        total += lastDay(year, i)
    
    return total + day

def weekDay(year, month, day): #월=0 ... 일=6
    return totalDay(year, month, day) % 7

def what_line(year, month, what_day): # 일정을 몇번째줄에 기입할지 반환
    line = 1
    start = 7 - weekDay(year, month, 1)
    while(True):
        if(what_day <= start): # 처음줄도 못지나감
            return line
        else:
            start = start + 7
            line = line + 1

def unicode_check(str): #한글인지 아닌지 확인하고 글자길이 반환
    str_len = 0
    for i in range(0, len(str)):
        check = str[i:i+1]
        if( ord(check)>=0 and ord(check)<=128 ): #아스키코드라면
            str_len = str_len + 1                   # 글자 길이 1
        else:                                   #한글이면
            str_len = str_len + 2                   # 글자 길이 2
    return str_len 

button = 1 
error_code = 0
while(True):
    what_day  = 0
   
    next_line = 0 #몇번째줄인지 알려줌

    if(button == 1): # 다른달력 보기
        year  = (input("\n출력하고 싶은 년도을 입력해주세요(ex:2021): "))
        if year.isdigit() == False:
            error_code = 1
        else:
            year = int(year)
            month = (input("출력하고 싶은 월을 입력해주세요(ex:06): "))
            if month.isdigit() == False:
                error_code = 1
            else:
                month = int(month)
                if(month>0 and month<13):    
                    schedule = [[[0 for col in range(6)] for row in range(7)] for depth in range(5)] #schedule[5][7][6] = 0
                    sp = [0]*31 #날짜 일정갯수 0초기화
                else:
                    error_code = 2        

    elif(button == 2): # 일정추가
        what_day = (input("추가하고 싶은 일정의 날짜를 입력하세요(ex:13): "))
        if what_day.isdigit() == False:
            error_code = 1
        else:
            what_day = int(what_day)    

            if( (what_day < 1) or (what_day > lastDay(year,month)) ): #입력이 불가한 경우
                error_code = 2
            elif(sp[what_day-1] == 5):
                error_code = 3

            else:
                y =  weekDay(year, month, what_day)#요일
                x =  what_line(year, month, what_day)-1 # 몇번째줄

                schedule[sp[what_day-1]][y][x] = input("일정을 입력해주세요(5개까지 가능합니다.): ")
                if(unicode_check(schedule[sp[what_day-1]][y][x]) > 16):
                    error_code = 4
                    schedule[sp[what_day-1]][y][x] = 0 #다시 0으로 초기화
                else:
                    sp[what_day-1] = sp[what_day-1] + 1 

    # 일정을 삭제함과 더불어 원래있던 숫자를 1씩올려주어야함
    elif(button == 3): #일정삭제
        del_day = (input("삭제하고 싶은 일정의 날짜를 알려주세요(ex:19): "))
        if del_day.isdigit() == False:
            error_code = 1
        else:
            del_day = int(del_day)
            if( (del_day < 1) or (del_day > lastDay(year,month)) ):
                error_code = 2
                 
            else:    
                del_weekDay = weekDay(year, month, del_day) #요일
                del_num = (input("몇번째 일정을 삭제하시겠습니까?(ex:3): "))
                if del_num.isdigit() == False:
                    error_code = 1
                else:
                    del_num = int(del_num)

                    if( (del_num < 0) or (del_num > sp[del_day-1]) ):
                        error_code = 5
                
                    else:
                        del_num = del_num -  1
                        for i in range(del_num, 4): #사라진 일정을 빼고 차례대로 올리기
                            schedule[i][del_weekDay][what_line(year, month, del_day)-1]=schedule[i+1][del_weekDay][what_line(year, month, del_day)-1]
                        schedule[4][del_weekDay][what_line(year, month, del_day)-1] = 0
                        sp[del_day-1] = sp[del_day-1] -1

    else:
        error_code = 6

    if(error_code == 0):
        print('=' * 148)
        print(' '*67, year, "년 ", month, "월")
        print('=' * 148)
        print(' '*9, "일", ' '*17, "월", ' '*17, "화", ' '*17, "수", ' '*17, "목", ' '*17, "금", ' '*17, "토")
        print('=' * 148)

        for i in range(weekDay(year, month, 1)): 
            print(' '*21, end = '')

        for i in range(1, lastDay(year, month) + 1): # i가 1부터 해당 달의 마지막 날짜의 수까지 변하는 동안
            print(' '*9,"%2d"%(i),' '*8, end = '')     
            if weekDay(year, month, i) == 6 or i == lastDay(year, month): #다음줄로 넘어감
                
                for i in range(0, 5): #6번 반복
                    print()
                    for j in range(0, 7): #7번 반복
                        if(schedule[i][j][next_line] != 0): #문자열이 들어있다면                        
                            print(i+1,schedule[i][j][next_line],' '*(16-unicode_check(schedule[i][j][next_line])),'|', end='') #문자열의 길이만큼빼서 출력

                        else: #문자열이 안들어있다면
                            print(' '*19,'|', end='')

                next_line = next_line + 1 
                print()
                print('_'*148)   

    #error가 났다면 달력은 출력하지 않고 error코드 출력                  
    else: 
        print("\n￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")
        print("| 　오류 발생!　　　　　　　　　　　　　　　　　　　[－][口][×]|") 
        print("|￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|")
        if(error_code == 1):
            print("|   숫자를 입력 바랍니다.                                      |")
        elif(error_code == 2):
            print("|   날짜가 알맞지 않습니다. 다시 입력바랍니다.                 |")
        elif(error_code == 3):    
            print("|   일정이 가득 찼습니다. 더이상 채울 수 없습니다.             |") 
        elif(error_code == 4):    
            print("|     글자수가 초과되었습니다. 글자수를 줄여주십시오.          |")
        elif(error_code == 5):
            print("|  삭제 할 일정이 없습니다.                                    |")
        else:
            print("|  버튼 숫자가 알맞지 않습니다.                                |")   
        print("|　　　　　　　　　　　　　　　　　　　　　　　　  　          |")
        print("|　　　　　　　　　　　　　　　　　　　　　　　　  　          |")
        print("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣\n")    
        error_code = 0

    button = int(input("1)다른달력보기\n2)일정추가\n3)일정삭제\n4)종료\n1,2,3,4 중 원하는 숫자를 입력후 enter클릭: "))
    if(button == 4):
        break
    
