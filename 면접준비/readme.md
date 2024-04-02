# sql 

### NAME 컬럼의 중복을 제거하고 COUNT 할때
      SELECT COUNT(DISTINCT (NAME)) FROM ANIMAL_INS
### NULL 인 내역을 "NONE"으로 바꾸려 할떄 
      SELECT IFNULL(NAME, "No name") AS NAME
### JOIN 맺는법 
      LEFT JOIN 
       BOOK_SALES 
       ON BOOK.BOOK_ID = BOOK_SALES.BOOK_ID

### 케이스별 
      CASE 
        WHEN OUT_DATE <= "2022-05-01" THEN "출고완료"
        WHEN OUT_DATE >= "2022-05-02" THEN "출고대기"
        ELSE "출고미정"
