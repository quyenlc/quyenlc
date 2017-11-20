for i in {02..19};
do
    scp zabbix/* rds${i}-log:/opt/bin/zabbix/
    scp userparameter_mysql.conf rds${i}-log:/etc/zabbix/zabbix_agentd.d/
    ssh rds${i}-log "cd /etc/zabbix && ln -s /opt/bin/zabbix/chk_read_only.sh"
    ssh rds${i}-log "cd /etc/zabbix && ln -s /opt/bin/zabbix/chk_buffer_size.sh"
    
    scp zabbix/* rds${i}-m:/opt/bin/zabbix/
    scp userparameter_mysql.conf rds${i}-m:/etc/zabbix/zabbix_agentd.d/
    ssh rds${i}-m "cd /etc/zabbix && ln -s /opt/bin/zabbix/chk_read_only.sh"
    ssh rds${i}-m "cd /etc/zabbix && ln -s /opt/bin/zabbix/chk_buffer_size.sh"
done
