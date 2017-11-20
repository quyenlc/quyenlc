mysql_host='172.21.149.150'
mysql_pass=''
mysql_user='root'
for i in $(mysql -u ${mysql_user} -p ${mysql_pass} -h ${mysql_host});
do
	echo ${i}
done