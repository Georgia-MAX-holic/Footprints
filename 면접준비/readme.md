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
        END 

### Date 포맷팅 
      DATE_FORMAT(OUT_DATE, '%Y-%m-%d') AS OUTDATE

### 컬럼 텍스트 합치기 
      CONCAT(USERS.CITY, " " , USERS.STREET_ADDRESS1 , " " , USERS.STREET_ADDRESS2) AS 전체주소 , 
### 하이픈 넣기 
      CONCAT (SUBSTR(USERS.TLNO, 1, 3) , "-" , SUBSTR(USERS.TLNO, 4, 4 ) ,"-", SUBSTR(USERS.TLNO, 8 ,4 )) AS 전화번호 
      -- 첫 숫자 ~ 3까지 ( 010 ) , 4번째 숫자 ~ 4번째 까지 ( 1234 ) , 8번쨰 ~ 4 번째 까지 ( 5678 ) 
