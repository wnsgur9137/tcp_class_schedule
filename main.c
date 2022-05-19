#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define STRING_SIZE 256

void help(char select[STRING_SIZE]);
char main_menu();

void root_main();
bool root_login();
char root_menu();
char root_user();
char root_subject();

char select_class();
char select_sub();
char select_pro();



char main_menu() {
    
    char result = 'q';
    char select[STRING_SIZE] = "";

    printf("\n\n");
    printf("시간표 검색 프로그램\n");
    printf("-------------------\n");
    printf("1. 학년/반 별 시간표\n");
    printf("2. 과목 검색\n");
    printf("3. 교수님 검색\n");
    printf("-------------------\n");
    printf("H. 프로그램 도움말\n");
    printf("R. 관리자 메뉴\n");
    printf("Q. 프로그램 종료\n\n");
    printf(" > ");

    scanf("%s", select);

    if (!strcmp(select, "q") || !strcmp(select, "Q")) { result = 'q'; }
    else if (!strcmp(select, "h") || !strcmp(select, "H")) { result = 'h'; }
    else if (!strcmp(select, "r") || !strcmp(select, "R")) { result = 'r'; }
    else if (!strcmp(select, "1")) { result = '1'; }
    else if (!strcmp(select, "2")) { result = '2'; }
    else if (!strcmp(select, "3")) { result = '3'; }
    else { result = 'e'; }

    return result;
}


void help(char select[STRING_SIZE]) {
    printf("\n\n도움말\n");
    printf("------------------------\n");
    printf("1. 학년/반 별 시간표: \n\t학년과 반을 선택하여 해당 반의 시간표를 출력합니다.\n");
    printf("2. 과목 검색: \n\t과목을 검색하여 해당 과목에 대한 시간표를 출력합니다.\n");
    printf("3. 교수님 검색: \n\t교수님을 검색하여 그 교수님의 시간표를 출력합니다.\n");
    printf("H. 프로그램 도움말: \n\t프로그램에 대한 도움말을 출력합니다.\n");
    printf("Q. 종료: \n\t프로그램을 종료합니다.\n");
    printf("R. 관리자 메뉴: \n\t관리자 메뉴로, 지정된 관리자만 사용할 수 있습니다.(로그인 필요)\n");
    printf("\n\n");
}


bool root_login() {
    
    bool result = false;

    char id[30] = "";
    char pw[100] = "";

    printf("ID: ");
    scanf("%s", id);
    printf("PW: ");
    scanf("%s", pw); 
    
    if(!strcmp(id, "root") && !strcmp(pw, "wns2044")) {
        printf("\n\n로그인 성공\n\n");
        result = true;
    } else {
        printf("\n\n로그인 실패\n\n");
    }
    return result;
}

char root_menu() {
    char result = 'e';
    while (1) {
        char select[10] = "";
        printf("root_menu()\n");
        printf("----------------------\n");
        printf("1. USER\n");
        printf("2. SUBJECT\n\n");
        printf(" > ");
        scanf("%s", select);
        if(!strcmp(select, "1")) {
            result = 'u';
        } else if(!strcmp(select, "2")) {
            result = 's';
        } else {
            printf("\n\n [경고] \n1, 2를 입력해 주십시오.\n\n");
            continue;
        }
        break;
    }
    return result;
}


char root_user() {
    char result = 'e';
    while (1) {
        char select[10] = "";
        printf("유저 관리\n");
        printf("--------------------\n");
        printf("1. 유저 조회\n");
        printf("2. 유저 등록\n");
        printf("3. 유저 수정\n");
        printf("4. 유저 삭제\n");
        printf("Q. 나가기\n\n");
        printf(" > ");
        scanf("%s", select);
        if(!strcmp(select, "1")) {
            result = 's';
        } else if(!strcmp(select, "2")) {
            result = 'c';
        } else if(!strcmp(select, "3")) {
            result = 'u';
        } else if(!strcmp(select, "4")) {
            result = 'd';
        } else if(!strcmp(select, "q") || !strcmp(select, "Q")) {
            return 'e';
        } else {
            printf("\n\n[경고]\n보기 중에서 입력하십시오.\n\n");
            continue;
        }
    }
    return result;
}


char root_subject() {
    char result = 'e';
    while (1) {
        char select[10] = "";
        printf("과목 관리\n");
        printf("---------------------\n");
        printf("1. 과목 조회\n");
        printf("2. 과목 등록\n");
        printf("3. 과목 수정\n");
        printf("4. 과목 삭제\n");
        printf("Q. 나가기\n\n");
        printf(" > ");
        scanf("%s", select);
        if(!strcmp(select, "1")) {
            result = 's';
        } else if(!strcmp(select, "2")) {
            result = 'c';
        } else if(!strcmp(select, "3")) {
            result = 'u';
        } else if(!strcmp(select, "4")) {
            result = 'd';
        } else if(!strcmp(select, "q") || !strcmp(select, "Q")) {
            return 'e';
        } else {
            printf("\n\n[경고]\n보기 중에서 입력하십시오.\n\n");
            continue;
        }
    }
    return result;
}


void root_main() {
    bool login_success = false;
    login_success= root_login();
    if (login_success) {
        char result = root_menu(); 
        if (result == 'u') {
            result = root_user();
        } else if (result == 's') {
            result = root_subject();
        }    
    }
}


char select_class() {
    
    int grade = 0;
    char class[10] = "";

    printf("\n학년을 입력하십시오.\n\n > ");
    scanf("%d", &grade);
    printf("\n\n반을 입력하십시오.\n\n > ");
    scanf("%s", class);
    switch (grade) {
        case 1:
            if (!strcmp(class, "A") || !strcmp(class, "a")) {
                printf("1학년 A반");
            } else if(!strcmp(class, "B") || !strcmp(class, "b")) {
                printf("1학년 B반");
            } else if(!strcmp(class, "C") || !strcmp(class, "c")) {
                printf("1학년 C반");
            } else {
                printf("\n\n[경고]\nA, B, C반 중 입력하십시오.\n");
                select_class();
                
            }
            
            break;
        case 2:

            break;

        case 3:

            break;

        case 4:

            break;

        default :
            printf("학년을 다시 입력해 주십시오.");

            break;
    }
    return 'e';
}

char select_sub() {
    return 'e';
}

char select_pro() {
    return 'e';
}


int main() {
    
    char result = 'e';
    while(1) {
        result = main_menu();
        if (!strcmp(&result, "q")) {
            printf("\n\n프로그램을 종료합니다.\n\n");
            return 0;
        } else if (!strcmp(&result, "h")) {
            help("main_menu");
            continue;
        } else if (!strcmp(&result, "r")) {
            root_main();
            continue;
        } else if (!strcmp(&result, "e")) {
            printf("\n\n [경고] \n보기에서 입력해 주십시오.\n\tex) > 1\n\n");
        } else if (!strcmp(&result, "1")) {
            result = select_class();
            printf("1 선택");
            select_class();
        } else if (!strcmp(&result, "2")) {
            result = select_sub();
            printf("2 선택");
        } else if (!strcmp(&result, "3")) {
            result = select_pro();
            printf("3 선택");
        }

        printf("\n--------------\nresult: %c\n---------------------", result);
    }
    return 0;
}
