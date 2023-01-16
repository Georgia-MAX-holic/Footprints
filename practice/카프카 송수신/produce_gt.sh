echo " Kafka output"

cat R6.csv | while read line; do

	echo "$line"

	sleep 0.1

done | /bin/kafka-console-producer --bootstrap-server kafka-1:19092,kafka-2:29092,kafka-3:39092 --topic test1