import os
import pymysql.cursors
import time

now_ts = time.time()
updated_at = str(int(now_ts))
log_file = os.path.dirname(os.path.realpath(__file__)) + r"\DNSLogs\rr"
log_reader = open(log_file,'r')
connection = pymysql.connect(host='172.21.149.150',
                             user='quyenle_ams',
                             password='12345678',
                             db='quyenle_ams3',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
for line in log_reader.readlines():
    dhcp_info = line.split(';')
    # print ("Hostname: " + dhcp_info[0] + " - MAC Address:" + dhcp_info[1] + ' - IP: ' + dhcp_info[2])
    mac_addr = "".join(dhcp_info[1].split('-'))
    ip_addr = dhcp_info[2]
    hostname = dhcp_info[0]
    if "punch.local" in hostname:
        hostname = ".".join(hostname.split(".")[:-2])
    query = "SELECT * FROM dhcp WHERE LOWER(mac_addr) LIKE LOWER('%" + mac_addr + "')"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            #print(result)
            if result != None:
                if result['created_at'] == None:
                    result['created_at'] = updated_at
                query = "UPDATE dhcp SET mac_addr = '" + mac_addr + "', ip_addr = '"+ ip_addr + "', hostname = '" + hostname + "', updated_at = " + updated_at + ", created_at = " + str(result['created_at']) + " WHERE `mac_addr` = '" + result['mac_addr'] + "'"
            else :
                query = "INSERT INTO dhcp (device_id,mac_addr, ip_addr, hostname, created_at) VALUES (0,'"+ mac_addr +"', '"+ ip_addr +"', '"+ hostname +"', " + str(int(now_ts)) + ")"
            #print(query)
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print("Query: " + query)
        print("Cannot execute query. Detail: " + str(e))

        break

connection.close()

