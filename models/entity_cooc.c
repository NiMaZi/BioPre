#include <stdio.h>
#include <stdlib.h>

int main()
{
	unsigned short mat[48155][48155];
	for(int i=0;i<48155;i++){
		for(int j=0;j<48155;j++){
			mat[i][j]=0;
		}
	}
	return 0;
}