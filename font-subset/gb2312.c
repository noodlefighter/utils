#include <stdio.h>

int main()
{
  for (int i = 0xB0; i <= 0xF7; ++i) {
    for (int j = 0xA1; j<= 0xFE; ++j) {
      printf("%c%c", (char)i, (char)j);
    }
  }
  return 0;
}
