#include <stdio.h>

// gcc -w ./test.c -o ./test -no-pie && ./test


void win(){
    char *flag = "flag{n0_w4y_c4nt_y0u_s33_m3}";
    printf("%s\n", flag);
}

int main() {
    char s[16];
    gets(s);
    return 0;
}
