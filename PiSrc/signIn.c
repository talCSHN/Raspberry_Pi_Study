#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 1024
int main()
{
	FILE *fp;
	char id[MAX_LENGTH];
	char pw[MAX_LENGTH];

	fp = fopen("userFile.txt", "w");
	if (fp == NULL) {
		perror("File Open Failed");
		return 1;
	}
	printf("Sign Up\n");
	while (1) {
		printf("ID : " );
		if (fgets(id, sizeof(id), stdin) == NULL) {
			return 1;
		}
		if (id[0] == '\n'){
			puts("Input your ID\n");
			continue;
		}
		break;
	}
	while (1) {
		printf("PW : ");
		if (fgets(pw, sizeof(pw), stdin) == NULL) {
   	    return 1;
   	}
		if (pw[0] == '\n') {
			puts("Input your PW\n");
			continue;
		}
		break;
	}
   id[strlen(id)-1] = '\0';
   pw[strlen(pw)-1] = '\0';
   fprintf(fp, "ID : %s\n", id);
   fprintf(fp, "PW : %s\n", pw);
   fclose(fp);

   printf("Saved\n");
   /////////////////////////////////////////////////////
   printf("Login\n");
   id[0] = '\0';
   pw[0] = '\0';
   char input_id[MAX_LENGTH];
   char input_pw[MAX_LENGTH];
   FILE *fp1 = fopen("userFile.txt", "r");
   if (!fp1) {
		perror("File Open Failed\n");
		return 1;
   }
   if (fscanf(fp1, "ID : %99[^\n]\n", id) != 1 || fscanf(fp1, "PW :  %99[^\n]\n", pw) != 1){
		perror("xxxxxxxxxx\n");
		fclose(fp1);
		return 1;
   }
   printf("ID : ");
   if (fgets(input_id, sizeof(id), stdin) == NULL){
		return 1;
   }
   printf("PW : ");
   if (fgets(input_pw, sizeof(pw), stdin) == NULL){
		return 1;
   }

	input_id[strlen(input_id)-1] = '\0';
	input_pw[strlen(input_pw)-1] = '\0';
   if (strcmp(input_id, id) == 0 && strcmp(input_pw, pw) == 0){
		printf("Login Success\n");
   }
   else {
		printf("Login Failed\n");
   }

   fclose(fp1);

	return 0;
}
