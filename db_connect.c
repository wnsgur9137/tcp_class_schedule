#include <stdio.h>
#include <mysql.h>

void connect() {
    MYSQL *conn;    // mysql과의 connect를 잡는데 지속적으로 사용되는 변수.
    MYSQL_RES *res; // 쿼리문에 대한 result 값을 받는 위치 변수.
    MYSQL_ROW orw;  // 쿼리문에 대한 실제 데이터값들이 들어있는 변수.
    
    char *server = "localhost";         // 서버의 경로.
    char *user = "root";
    char *password = "inhatc202044021";
    char *database = "tcpproject";

    conn = mysql_init(NULL);    // connection 변수 초기화.
    
    if (!mysql_real_connect(conn, server, user, password, NULL, 0, NULL, 0)) {
        fprintf(stderr, "%s\n", mysql_error(conn));
        exit(1);
    }

    res = mysql_use_result(conn);

}

void view() {
    char subject = "name";
    char time = "name";
    char professor = "";
    int grade = 0;
    char class = "A";
    char place = "";
}
