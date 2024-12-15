DELETE FROM ORDERS_DTL
WHERE
  ORDER_NO IN (
    SELECT
      ORDER_NO
    FROM
      ORDERS
    WHERE
      ORDER_DATE BETWEEN '2010-01-01' AND '2010-12-31'
  );

DELETE FROM ORDERS
WHERE
  ORDER_DATE BETWEEN '2010-01-01' AND '2010-12-31';

SELECT
  *
FROM
  ORDERS AS ORD
  LEFT JOIN ORDERS_DTL AS DTL;
