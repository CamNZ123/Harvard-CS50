#include <stdio.h>
#include <cs50.h>

int main (void) 
{   
    int Height;
    do {printf("Height: ");
        Height = get_int();}
    while (Height > 23 || Height <= -1);
    for (int i=0; i < Height; i++){
        for (int s = 0; s < Height - i - 1; s++){
            printf(" ");
        }
        for (int x = 0; x < i + 1 ; x++){
            printf("#");
        }
        printf("  ");
        for (int x = 0; x < i + 1; x++){
            printf("#");
        }
        printf("\n");
    }
}