# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# define ID1 "Firuz"                // shopkeeper's name
# define PW1 "p@assw0rd"            // the password of shopkeeper 'Firuz'
# define ID2 "Eldor"                // shopkeeper's name
# define PW2 "pAsswOrd"             // the password of shopkeeper 'Eldor'

/* function prototype */

int print_file(FILE* fp);
// get the file pointer as its argument and then prints the contents in the file on console

int log_in();
// facilitates logging in. returns 1 if 'Firuz' has logged-in, and return 2 if 'Eldor' has logged-in.
// if log-in failed, then return -1.

int get_product_number(FILE * fp);
// gets the file pointer as its input and then return the number of line in the file.
// it will be used when we count how many structures are in structure pointer.

struct product* get_product_list(FILE * fp, int line_num);
// gets the file pointer and number of line in the file as inputs
// then return structure pointer which contains the data in the file.

int show_product(struct product* prod_ptr, int prod_length);
// gets structure pointer and the length of the pointer as inputs.
// then prints the data in the structure pointer from start to the end.

int management(int shopkeeper, struct product* prod_ptr, int* prod_length_ptr, char file_title[30]);
// function that is used for shopkeeper page

int compare_date(char a[11], char b[11]);
// gets two character as its input (yyyy-mm-dd). Returns 1 if a is sooner than b and if b is sooner than a, then returns 0.
// otherwise, returns -1.

struct product* sort_product(struct product* prod_ptr, int prod_length);
// gets structure pointer and length of the pointer as inputs.
// then sort the structure pointer with expire date and return sorted pointer.

struct product* add_products(struct product* prod_ptr, int prod_length, char file_title[30]);
// gets structure pointer, length of the pointer, and title of the file.
// it gets the data from the user and adds the data to both file and pointer.
// the function returns structure pointer which the data is added to.

int show_product_and_ID(struct product* prod_ptr, int prod_length);
// prints the data from inputted pointer on the screen.


int remove_products(struct product* prod_ptr, int prod_length, char file_title[30]);
// This function gets the ID to remove from the user.
// It removes the product from both file and structure pointer.

int edit_products(struct product* prod_ptr, int prod_length, char file_title[30]);
// This function gets the ID to edit and data from the user.
// It modifies the data of the product on both file and structure pointer.

int user(struct product* prod_ptr1, struct product* prod_ptr2, int prod_length1, int prod_length2);
// function that is used for customer page

int show_all_products(struct product* prod_ptr1, struct product* prod_ptr2, int prod_length1, int prod_length2);
// shows all products available in stores.

int search_product(struct product* prod_ptr1, struct product* prod_ptr2, int prod_length1, int prod_length2);
// this function gets first letter of the product from the user
// then searches products that starts from the letter, and show the products.


// product structure
struct product{
    char product_name[100];         // name of the product
    char price[10];                 // price of the product
    char quantity[5];               // quantity of the product
    char expire_date[11];           // expire date of the product
    int productID;                  // product ID. used when removing and editing products.
};

int main(){
    FILE* start_option;                                     // in order to print the start option page,
    start_option = fopen("start_option.txt", "r");          // get the file and open,
    printf("\n\n");
    print_file(start_option);                               // then print the contents in the file.

    int start_choice;                                       // In start page, get the choice from user.
    scanf("%d", &start_choice);

    while (start_choice !=3){                               // since option 3 is exit, while selected option is not 3, we should do something.

            // making the products pointer by getting data from the file
            // "store_1_product.txt" contains the data of the products in G25 store 1.
            FILE* product_file1;                                    // get the product file.
            product_file1 = fopen("store_1_product.txt", "r");      // and open
            int product_num1 = get_product_number(product_file1);   // count the number of the products

            fseek(product_file1, 0L, SEEK_SET);                     // go back to the start of the file.
            struct product* store_1_product;                        // define structure pointer that will save the data of the product in G25 store 1.
            store_1_product = (struct product*) malloc(product_num1*sizeof(struct product));    // make the pointer
            memcpy(store_1_product, get_product_list(product_file1, product_num1), product_num1*sizeof(struct product));    // then copy the memory.


            // same thing as we did above.
            FILE* product_file2;
            product_file2 = fopen("store_2_product.txt", "r");
            int product_num2 = get_product_number(product_file2);
            fseek(product_file2, 0L, SEEK_SET);
            struct product* store_2_product;
            store_2_product = (struct product*) malloc(product_num2*sizeof(struct product));
            memcpy(store_2_product, get_product_list(product_file2, product_num2), product_num2*sizeof(struct product));

            fclose(product_file1);      // close files.
            fclose(product_file2);

            if (start_choice == 1){                             // if the user has selected option 1,
                int shopkeeper;                                 // integer variable that indicates shopkeeper

                if ((shopkeeper = log_in()) ==-1)               // log-in and then if log-in failed,
                    return 1;                                   // return 1 and finish current loop

                else if (shopkeeper==1){        // if shopkeeper is 'Firuz',
                    management(shopkeeper, store_1_product, &product_num1, "store_1_product.txt");
                    system("cls");          // clear screen
                    // execute management function with corresponding inputs.
                    // since we have to modify the length of the pointer because of adding the product, add & at the front of
                    // variable product_num1.
                }

                //Doing same as above
                else if (shopkeeper == 2){      // if shopkeeper is 'Eldor'
                    management(shopkeeper, store_2_product, &product_num2, "store_2_product.txt");
                    system("cls");          // clear screen
                    // execute management function with corresponding inputs.
                    }
                }

            else if (start_choice ==2){             // if the user selected option 2,
                user(store_1_product, store_2_product, product_num1, product_num2);     // execute function 'user'
            }
            printf("\n\n");
            print_file(start_option);           // print the start option menu.
            scanf("%d", &start_choice);         // get the choice from the user.
    }
    fclose(start_option);           // close file. (this file is start menu)

    return 0;           // finish the function.
}

// printing the contents in the files
int print_file(FILE* fp){

    char ch;                            // define char
    while ((ch = getc(fp)) != EOF) {    // then get character from the file and while it is not EOF,
        putchar(ch);                    // print the character on the screen
    }
    fseek(fp, 0L, SEEK_SET);            // After printing, go back to the start of the file.
    return 0;
}

// Log-in function
int log_in(){
    system("cls");          // clear screen
    int trial=0;                            // how many times the user had tried log-in. It it reaches 3, log-in fail.
    char log_in_id[10];                     // define variables to get id and password from the user
    char log_in_pw[15];
    int i = 0;                              // to limit the trials.

    puts("\n\n***SHOPKEEPER PAGE***");
    puts("==========================");

    for (i=0 ; i<3 ; i++){          // until i is smaller than 3,
        printf("Login: ");
        scanf("%s", log_in_id);     // get id
        fflush(stdin);
        printf("Password: ");
        scanf("%s", log_in_pw);    // and password from the user.
        fflush(stdin);              // clean the buffer.

        // check if the inputs are right.
        FILE* menu_ptr;                     // to print shopkeeper menu after log-in.
        menu_ptr = fopen("final_project_menu.txt", "r");        //"final_project_menu.txt" is shopkeeper menu

        if (strcmp(log_in_id, ID1)==0 && strcmp(log_in_pw, PW1)==0){        // if Firuz logged-in,
            system("cls");          // clear screen
            printf("\n***G25 Store 1***\n");    // print the statements
            printf("Shopkeeper : Firuz\n");
            print_file(menu_ptr);               // and menu
            return 1;                           // then return 1.
        }

        else if (strcmp(log_in_id, ID2)==0 && strcmp(log_in_pw, PW2)==0){   // if Eldor logged-in,
            system("cls");          // clear screen
            printf("\n***G25 Store 2***\n");    // print the statements
            printf("Shopkeeper : Eldor\n");
            print_file(menu_ptr);               // and menu
            return 2;                           // then return 1.
        }

        else            // when log-in failed,
            printf("\nYou have entered wrong login or password(%d/3 trials)\n", i+1); // notice the user that it's wrong.
    }

    printf("\nProgram exits.");     // when log-in eventually failed, (after 3 times)
    return -1;      // return -1.
}

// the function counting the number of lines in the file
int get_product_number(FILE * fp){      // gets file pointer as its input.
    char temp[200];                 // getting the data from the file line by line.
    int line_num = 0;               // define integer variable that indicates the number of the line.

    while (fgets(temp, sizeof(temp), fp) != NULL) { // while cursor reaches the end of the file
        line_num++;             // increase line_num by 1.
        }
    fseek(fp, 0L, SEEK_SET);            // go back to the start of the file.
    return line_num;                // returns the number of line in the file.
}

// get product list from text file
struct product* get_product_list(FILE * fp, int line_num){

    struct product* prod_ptr;           // structure pointer that contains the data of the products in the store.
    prod_ptr = (struct product*) malloc(line_num * sizeof(struct product));     // allocate memory using line_num

    fseek(fp, 0L, SEEK_SET);        // go to the start of the file
    char temp2[200];               // string that contains the data in the file line by line.

    int i=0;                        // index of the structure in the pointer.

    while (fgets(temp2, sizeof(temp2), fp) != NULL){    // from the start to the end of the file, get the string from file.
        if (temp2[strlen(temp2)-1]=='\n'){                  // if temp2 ends with new line,
            temp2[strlen(temp2)-1] = '\0';                      // modify it to null because we will use strtok
        }

        char * temp_prod_info = strtok(temp2, ",");     // character pointer that will get the data from temp2
                                                        // since data of the product is connected using ',' , use strtok to get one by one.

        if (temp_prod_info == NULL){                    // if the name of the product is NULL, then just assign "" to the product
            strcpy((prod_ptr+i)->product_name, "");
            strcpy((prod_ptr+i)->price, "");
            strcpy((prod_ptr+i)->quantity,"");
            strcpy((prod_ptr+i)->expire_date,"");
        }

        else {
            strcpy((prod_ptr+i) -> product_name, temp_prod_info);       // get product name

            temp_prod_info = strtok(NULL, ",");                         // then get price
            strcpy((prod_ptr+i) -> price ,temp_prod_info);              // and copy to structure pointer prod_ptr

            temp_prod_info = strtok(NULL, ",");                         // then get quantity
            strcpy((prod_ptr+i) -> quantity , temp_prod_info);          // and copy to structure pointer prod_ptr

            temp_prod_info = strtok(NULL, ",");                         // finally get expire date
            strcpy((prod_ptr+i) -> expire_date, temp_prod_info);        // and copy to structure pointer prod_ptr

            (prod_ptr+i) -> productID = i+1;                            // this is not shown in the file, but in order to facilitate some functionalities,
                                                                        // I will assign the value to productID.
        }

        i++;        // increase i by one to go the the next structure product.
    }
    return prod_ptr;        // return the structure pointer
}

// facilitates shopkeeper menu
int management(int shopkeeper, struct product* prod_ptr, int* prod_length_ptr, char file_title[30]){

    int choice_num;             // the choice that the shopkeeper had chosen.

    FILE* menu_ptr;             // file pointer menu_ptr to print shopkeeper menu
    menu_ptr = fopen("final_project_menu.txt", "r");            //for menu printing

    printf("\nEnter your choice : ");       // get the choice from the user
    scanf("%d", &choice_num);

    while (choice_num != 6){            // since option 6 is log-out, we should to something until the shopkeeper chooses option 6.

        if (choice_num == 1){       // if shopkeeper chose option 1 (show products)

            // just to print statements that depends on who the shopkeeper is.
            if (shopkeeper == 1){
                system("cls");          // clear screen
                printf("\n\n***G25 Store 1***");
                printf("\nShopkeeper : Firuz\n");
            }
            else if (shopkeeper == 2){
                system("cls");          // clear screen
                printf("\n\n***G25 Store 2***");
                printf("\nShopkeeper : Eldor\n");
            }

            printf("=============================================\n");
            printf("\tProduct Name\tPrice\tQuantity\tExpire Date\n\n");
            show_product(prod_ptr, *prod_length_ptr);           // print the data of the products in the shop.
            system("cls");          // clear screen
        }

        else if (choice_num == 2){                  // if the shopkeeper chose option 2 (sort by expire date)

            // just to print statements that depends on who the shopkeeper is.
            if (shopkeeper == 1){
                system("cls");          // clear screen
                printf("\n\n***G25 Store 1***");
                printf("\nShopkeeper : Firuz\n");
            }
            else if (shopkeeper == 2){
                system("cls");          // clear screen
                printf("\n\n***G25 Store 2***");
                printf("\nShopkeeper : Eldor\n");
            }

            printf("=============================================\n");
            printf("\tProducts List by Expire Date : ");
            printf("\n\tProduct Name\tPrice\tQuantity\tExpire Date\n\n");
            show_product(sort_product(prod_ptr, *prod_length_ptr), *prod_length_ptr);   // sort and show products.
            system("cls");          // clear screen
        }

        else if (choice_num == 3){      // if shopkeepr chose option 3 (add products)
            system("cls");          // clear screen

            // just to print statements that depends on who the shopkeeper is.
            if (shopkeeper == 1){
                system("cls");          // clear screen
                printf("\n\n***G25 Store 1***");
                printf("\nShopkeeper : Firuz\n");
                printf("====================================\n");
            }
            else if (shopkeeper == 2){
                system("cls");          // clear screen
                printf("\n\n***G25 Store 2***");
                printf("\nShopkeeper : Eldor\n");
                printf("====================================\n");
            }

            prod_ptr = realloc(prod_ptr, (*prod_length_ptr+1)*sizeof(struct product));      // re-allocate the length of the pointer
            memcpy(prod_ptr, add_products(prod_ptr, *prod_length_ptr, file_title), (*prod_length_ptr+1)*sizeof(struct product));
                    // then copy the memory of the structure pointer than contains new product
            *prod_length_ptr += 1;      // and then increase the length of structure pointer by 1.
            system("cls");          // clear screen
        }

        else if (choice_num ==4){       // if shopkeeper chose option 4 (remove products)
            system("cls");          // clear screen
            show_product_and_ID(prod_ptr, *prod_length_ptr);            // show the products with id to let user to choose which to remove
            remove_products(prod_ptr, *prod_length_ptr, file_title);    // then remove the product
            system("cls");          // clear screen
        }

        else if (choice_num ==5){       // if shopkeeper chose option 5 (edit products)
            system("cls");          // clear screen
            edit_products(prod_ptr, *prod_length_ptr, file_title);      // show the products with id and then edit the product.
            system("cls");          // clear screen
        }

        else {      // if shopkeeper entered other than 1~5,
            return 0;       // return 0 and finish the function.
        }

        printf("\n");
        print_file(menu_ptr);                   // print shopkeeper menu
        printf("\nEnter your choice : ");       // get the choice from shopkeeper
        scanf("%d", &choice_num);
    }

    show_product(prod_ptr, *prod_length_ptr);   // show final result (product list)
    return 0;
}

// show products in structure pointer
int show_product(struct product* prod_ptr, int prod_length){
    int i = 0;                          // index of the structure pointer
    for (i=0; i < prod_length; i++){                        // until index reaches the end,
        if (strcmp(prod_ptr[i].product_name, "") != 0) {        // if the product is removed, then do not show the removed one.

            // print the data of the product
            printf("\t%s", prod_ptr[i].product_name);
            printf("\t%s", prod_ptr[i].price);
            printf("\t%s", prod_ptr[i].quantity);
            printf("\t%s\n", prod_ptr[i].expire_date);
        }
    }
/*
    printf("Press enter to continue.");         // press enter to continue.
    fflush(stdin);  // clean buffer
    char ch = getchar();
*/
    system("PAUSE");
    return 0;
}

// compare dates and return integer to show which one is sooner.
int compare_date(char a[11], char b[11]){
    int a_year = atoi(strtok(a, "-"));              // get 'yyyy' in 'yyyy-mm-dd' and make it to integer to enable compare
    int a_month = atoi(strtok(NULL, "-"));          // get 'mm' in 'yyyy-mm-dd' and make it to integer to enable compare
    int a_day = atoi(strtok(NULL, "-"));            // get 'dd' in 'yyyy-mm-dd' and make it to integer to enable compare

    // same as above
    int b_year = atoi(strtok(b, "-"));
    int b_month = atoi(strtok(NULL, "-"));
    int b_day = atoi(strtok(NULL, "-"));

    int compare;

    if (a_year > b_year) compare = 0;                  // if the year of a is bigger than that of b, b is sooner -> compare = 0
    else if (a_year < b_year) compare = 1;             // else if the year of a is smaller than that of b, a is sooner -> compare = 1

    // when year of a and b is same
    else if (a_month > b_month) compare = 0;           // if the month of a is bigger than that of b, b is sooner -> compare = 0
    else if (a_month < b_month) compare = 1;           // if the month of b is bigger than that of a, a is sooner -> compare = 1

    // when year and month of a and b is same.
    else if (a_day > b_day) compare = 0;               // if the day of a is bigger than that of b, b is sooner -> compare = 0
    else if (a_day < b_day) compare = 1;               // if the day of b is bigger than that of a, a is sooner -> compare = 1

    switch (compare){               // if the value of compare is..
    case 0 :            // 0,
        return 0;       // then return 0
        break;
    case 1 :            // 1,
        return 1;       // then return 1
        break;
    default :           // otherwise
        return -1;      // return -1
        break;
    }
}

// sort product by expire date
struct product* sort_product(struct product* prod_ptr, int prod_length){
    struct product* sorted_prod_ptr;            // define new structure pointer.
    sorted_prod_ptr = (struct product*) malloc(prod_length * sizeof(struct product));       // allocate memory
    memcpy(sorted_prod_ptr, prod_ptr, prod_length*sizeof(struct product));
    // copy memory from prod_ptr (not sorted pointer) to sorted_prod_ptr (sorted pointer)

    int i = 0, j = 0;           // to compare two products
    struct product temp;        // product structure 'temp' -> used to change the data in structures.
    for (i = 0; i < prod_length; i++){              // repeat following statements from 'prod_length' times to sort
        for (j = 0; j < prod_length-1 ; j++){
                // I will compare jth structure product in the pointer and (j+1)th structure product in the pointer

            char date1[11];                                 // char pointer that gets the expire date of jth product
            strcpy(date1, sorted_prod_ptr[j].expire_date);      // string copy
            char date2[11];                                 // char pointer that gets the expire date of (j+1)th product
            strcpy(date2, sorted_prod_ptr[j+1].expire_date);    // string copy

            if ((strcmp(date1, "")!=0) && (strcmp(date2,"")!=0)){   // if the product has removed (shopkeeper option 4), don't compare
                if (compare_date(date1, date2)==0){                 // if date2 is sooner,

                    // change the position of jth product and (j+1)th product
                    temp = sorted_prod_ptr[j];                      // temporary structure for switching position
                    sorted_prod_ptr[j] = sorted_prod_ptr[j+1];      // change the data in jth product to (j+1)th product
                    sorted_prod_ptr[j+1] = temp;                    // change the data in (j+1)th product to jth product (before change)
                }
            }
        }
    }
    return sorted_prod_ptr;     // return sorted_prod_ptr
}

// adding product
struct product* add_products(struct product* prod_ptr, int prod_length, char file_title[30]){
    // data that will get from shopkeeper
    char new_prod_name[100];
    char new_prod_price[10];
    char new_prod_quant[5];
    char new_prod_date[11];


    struct product* new_prod_ptr;           // define new structure pointer
    new_prod_ptr = (struct product*) malloc(prod_length * sizeof(struct product));  // allocate memory
    memcpy(new_prod_ptr, prod_ptr, prod_length*sizeof(struct product));             // then copy products before adding

    new_prod_ptr = realloc(new_prod_ptr, (prod_length+1)*sizeof(struct product));   // then re-allocate new structure pointer (resize)

    // get new product data
    printf("Add new Product: ");

    printf("\nProduct Name : ");
    scanf("%s", new_prod_name);             // since I used scanf, the software will wait until the user enters anything
    strcpy((new_prod_ptr+(prod_length))->product_name, new_prod_name);

    printf("\nPrice (per item) : ");
    scanf("%s", new_prod_price);
    strcpy((new_prod_ptr+(prod_length)) -> price, new_prod_price);

    printf("Quantity : ");
    scanf("%s", new_prod_quant);
    strcpy((new_prod_ptr+(prod_length)) -> quantity , new_prod_quant);

    printf("Expire Date : ");
    scanf("%s", new_prod_date);
    strcpy((new_prod_ptr+(prod_length)) -> expire_date, new_prod_date);

    (new_prod_ptr+(prod_length))->productID = prod_length+1;        //to facilitate functionalities, assign value to productID

    FILE* wrfp;     // the file that contains the data of the product. (here, it will be either "store_1_product.txt" or "store_2_product.txt"
    wrfp = fopen(file_title, "w");          // open the file
    fseek(wrfp, 0L, SEEK_SET);              // go to the start of the file

    int i = 0;          // line by line

    for (i=0; i < prod_length+1 ; i++){         // re-write the products list file.
        if (i!=0) fputs("\n",wrfp);                 // if it is first line, do not put new line to the file
        // put the data to the files
        // then the file will contain previous products and added product
        fputs(new_prod_ptr[i].product_name, wrfp);
        fputs(",", wrfp);
        fputs(new_prod_ptr[i].price, wrfp);
        fputs(",", wrfp);
        fputs(new_prod_ptr[i].quantity, wrfp);
        fputs(",", wrfp);
        fputs(new_prod_ptr[i].expire_date, wrfp);
    }
    fclose(wrfp);       // close the file.

    return new_prod_ptr;        // return structure pointer that has the data of added product
}

// function that shows product and its ID together
int show_product_and_ID(struct product* prod_ptr, int prod_length){
    int i = 0;

    printf("\n================================================");
    printf("\nProducts List : \n");
    printf("\t%s", "ProductID");
    printf("\t%s", "Product Name");
    printf("\t%s", "Price");
    printf("\t%s", "Quantity");
    printf("\t%s\n", "Expire Date");

    for (i=0; i < prod_length; i++){                        // to the end of the file
        if (strcmp(prod_ptr[i].product_name, "") != 0){         // if the product has removed, do not print the product
            // print the data of the products including productID
            printf("\t%d", prod_ptr[i].productID);
            printf("\t%s", prod_ptr[i].product_name);
            printf("\t%s", prod_ptr[i].price);
            printf("\t%s", prod_ptr[i].quantity);
            printf("\t%s\n", prod_ptr[i].expire_date);
        }
    }
    printf("================================================\n");

    return 0;
}

// get the ID of the product to remove from shopkeeper and remove it from both file and structure pointer.
int remove_products(struct product* prod_ptr, int prod_length, char file_title[30]){
    int removing_id;                            // ID of the product to remove
    printf("\nEnter ID of removing product : ");
    scanf("%d", &removing_id);

    // make the name, price, quantity and expire date of removing product to ""
    strcpy(prod_ptr[removing_id-1].product_name, "");
    strcpy(prod_ptr[removing_id-1].price, "");
    strcpy(prod_ptr[removing_id-1].quantity, "");
    strcpy(prod_ptr[removing_id-1].expire_date, "");

    FILE* rmfp;                         // products list file
    rmfp = fopen(file_title, "w");      // open and re-write
    int i = 0;
    int j = 0;
    for (i=0; i < prod_length; i++){        // until i reaches the end,
                j++;
                if (j != 1) fputs("\n", rmfp);              // when we removed first line, we shouldn't change the line.

                // write data of remaining products to the file
                fputs(prod_ptr[i].product_name, rmfp);
                fputs(",", rmfp);
                fputs(prod_ptr[i].price, rmfp);
                fputs(",", rmfp);
                fputs(prod_ptr[i].quantity, rmfp);
                fputs(",", rmfp);
                fputs(prod_ptr[i].expire_date , rmfp);
    }
    fclose(rmfp);       // close the file

    printf("\nThe product has successfully removed");   // inform the user
    printf("\nHow the product list changed : ");        //show how the products list has changed
    show_product_and_ID(prod_ptr, prod_length);
    system("PAUSE");        // pause system to check
    printf("\n");

    return 0;
}

// edit the data of the products
int edit_products(struct product* prod_ptr, int prod_length, char file_title[30]){
    show_product_and_ID(prod_ptr, prod_length);         // first, show products with its ID.
    int editing_id;                                     // and then get the id of the product to edit.
    printf("\nEnter ID of editing product : ");
    scanf("%d", &editing_id);

    // variables to save new descriptions of the product from the user.
    char edit_new_name[100];
    char edit_new_price[10];
    char edit_new_quantity[5];
    char edit_new_date[11];

    printf("Editing Product : \n");
    printf("Product ID : %d", editing_id);

    // get the data from the user
    printf("\nProduct Name : ");
    scanf("%s", edit_new_name);
    printf("Price (per item) : ");
    scanf("%s", edit_new_price);
    printf("Quantity : ");
    scanf("%s", edit_new_quantity);
    printf("Expire Date : ");
    scanf("%s", edit_new_date);

    // change the data
    strcpy(prod_ptr[editing_id-1].product_name, edit_new_name);
    strcpy(prod_ptr[editing_id-1].price, edit_new_price);
    strcpy(prod_ptr[editing_id-1].quantity, edit_new_quantity);
    strcpy(prod_ptr[editing_id-1].expire_date, edit_new_date);

    // change the file
    FILE* edtfp;                        // products list file
    edtfp = fopen(file_title, "w");     // re-write the file

    int i = 0;                              // index of structure in the structure pointer
    for (i=0; i < prod_length; i++){        // until i reaches the end
        if (i != 0) fputs("\n", edtfp);         // writing first product, we shouldn't put new line to the file.

        // write the data of products
        fputs(prod_ptr[i].product_name, edtfp);
        fputs(",", edtfp);
        fputs(prod_ptr[i].price, edtfp);
        fputs(",", edtfp);
        fputs(prod_ptr[i].quantity, edtfp);
        fputs(",", edtfp);
        fputs(prod_ptr[i].expire_date , edtfp);
    }
    fclose(edtfp);      // close file

    printf("\nHow the product list changed : ");        // show how the products list has changed
    show_product_and_ID(prod_ptr, prod_length);
    system("PAUSE");    // pause system to check
    printf("\n");

    return 0;
}

// user option menu
int user(struct product* prod_ptr1, struct product* prod_ptr2, int prod_length1, int prod_length2){
    FILE* user_menu;                                // to print user menu
    user_menu = fopen("customer_page.txt", "r");    // open file
    print_file(user_menu);                          // and print the contents of the file

    int user_option;                // get the option from the user
    scanf("%d", &user_option);

    while (user_option != 3){           // until the user chose 3 (Go to start page), execute following codes

        if (user_option == 1){              // if the user chose option 1,
            system("cls");          // clear screen
            show_all_products(prod_ptr1, prod_ptr2, prod_length1, prod_length2);    // show all available products in stores
            system("cls");          // clear screen
        }

        else if(user_option == 2) {         // if the user chose option 2,
            system("cls");          // clear screen
            search_product(prod_ptr1, prod_ptr2, prod_length1, prod_length2);       // search the product starting with the letter the user gave
            system("cls");          // clear screen
        }

        printf("\n\n");
        print_file(user_menu);              // print user menu again
        scanf("%d", &user_option);          // get new option from user.
    }
    system("cls");          // clear screen
    return 0;
}

// showing all of the products available in stores.
int show_all_products(struct product* prod_ptr1, struct product* prod_ptr2, int prod_length1, int prod_length2){
    int i =0;           // index of structure in structure pointer.

    printf("\n\n***CUSTOMER PAGE***\n");
    printf("=========================================\n");
    printf("\tShow all products:\n");
    printf("\tProduct Name\tStore Name\tShopkeeper\tPrice\tQuantity\tExpire Date\n");

    for (i = 0; i < prod_length1; i++){             // until the end of the pointer.
        if (atoi(prod_ptr1[i].quantity) != 0) {             // if quantity of product is not zero,

            // print the data of the product in prod_ptr1 (G25 store 1)
            printf("\t%s\t%s\t%s\t", prod_ptr1[i].product_name, "G25 Store 1", "Firuz");
            printf("%s\t%s\t%s\n", prod_ptr1[i].price, prod_ptr1[i].quantity, prod_ptr1[i].expire_date);
            }
    }

    // print the data of the product in prod_ptr2 (G25 store 2)
    for (i = 0; i < prod_length2; i++){
        if (atoi(prod_ptr2[i].quantity) != 0) {
            printf("\t%s\t%s\t%s\t", prod_ptr2[i].product_name, "G25 Store 2", "Eldor");
            printf("%s\t%s\t%s\n", prod_ptr2[i].price, prod_ptr2[i].quantity, prod_ptr2[i].expire_date);
            }
    }

    system("PAUSE");        // press any key to continue

    return 0;
}

// gets the letter from the user and search for the product that its name starting with given letter
int search_product(struct product* prod_ptr1, struct product* prod_ptr2, int prod_length1, int prod_length2){
    int i =0;                   // index of the structure in structure pointer

    printf("\n\n***CUSTOMER PAGE***\n");
    printf("=========================================\n");
    printf("\tSearch Product (Enter first letter):");

    char ch;                // define char ch - indicates the starting letter
    fflush(stdin);
    scanf("%c", &ch);           // save it on variable ch.

    printf("\nResults: \n");
    printf("\tProduct Name\tStore Name\tShopkeeper\tPrice\tQuantity\tExpire Date\n");

    // search for the product satisfying given condition from G25 store 1
    for (i = 0; i < prod_length1; i++){

        // if quantity is not zero, and product name starts with given letter, print data of the product to the screen
        if ((strcmp(prod_ptr1[i].quantity, "0")!=0) && (prod_ptr1[i].product_name[0] == ch)){
            printf("\t%s\t%s\t%s\t", prod_ptr1[i].product_name, "G25 Store 1", "Firuz");
            printf("%s\t%s\t%s\n", prod_ptr1[i].price, prod_ptr1[i].quantity, prod_ptr1[i].expire_date);
            }
    }

    // search for the product satisfying given condition from G25 store 2
    // and print the products
    for (i = 0; i < prod_length2; i++){
        if ((strcmp(prod_ptr1[i].quantity, "0")!=0) && (prod_ptr2[i].product_name[0] == ch)){
            printf("\t%s\t%s\t%s\t", prod_ptr2[i].product_name, "G25 Store 2", "Eldor");
            printf("%s\t%s\t%s\n", prod_ptr2[i].price, prod_ptr2[i].quantity, prod_ptr2[i].expire_date);
            }
    }

    system("PAUSE");        // press any key to continue

    return 0;

}
