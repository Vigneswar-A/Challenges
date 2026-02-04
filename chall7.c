#include <stdio.h>

// gcc -w ./test.c -o ./test && ./test

int main() {
    char *flag = "flag{n0_w4y_c4nt_y0u_s33_m3}";
    char s[16];
    printf("Enter your name: ");
    fgets(s, 15, stdin);
    printf("Hello, ");
    printf(s);
    printf("Nice to meet you!\n");
    return 0;
}
