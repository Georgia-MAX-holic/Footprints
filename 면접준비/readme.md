# sql 

### NAME 컬럼의 중복을 제거하고 COUNT 할때
   SELECT COUNT(DISTINCT (NAME)) FROM ANIMAL_INS
### NULL 인 내역을 "NONE"으로 바꾸려 할떄 
   SELECT IFNULL(NAME, "No name") AS NAME
