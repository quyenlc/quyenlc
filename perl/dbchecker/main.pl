#!/usr/bin/perl

# use 5.16v2;
use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
my $result = 0;
my $hostname = '';


sub check_mysql_status {
    # my @response = `mysql -u root -p'123456a\@A' -e 'select \@\@hostname;'`; #local
    my @response = `mysql -e 'select \@\@hostname;'`; # production
    $hostname = $response[1];
    if ( $hostname )
    {
        return 200;
    }
    else 
    {
        return 100; 
    }
}

sub check_buffer_size
{
    my @mem_info = `free -k| grep Mem`;
    my $mem_info = $mem_info[0];
    # my $mem_info = "Mem:      3371392   13558756    1812636          0     263524    2967220"; #test
    my @mem_info_array = split(/\s+/,$mem_info);
    my $valid_size = 1024 * $mem_info_array[1] * 80 /100; # valid size should lesser 80% of total memory

    my $innodb_buffer_pool_size = show_variable('innodb_buffer_pool_size');
    if ( $valid_size < $innodb_buffer_pool_size )
    {
        return 0;
    }
    else
    {
        return 1;
    }

}

sub check_read_only
{
    my ($hostname) = @_;
    my $read_only = show_variable('read_only');
    if ( is_slave($hostname) == 1 )
    {
        if ( $read_only eq 'OFF' )
        {
            return 0;
        }
        else 
        {
            return 1;
        }
    }
    else 
    {
        if ( $read_only eq 'ON' )
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
}

sub show_variable
{
    my ($variable_name ) = @_;
    # my @response = `mysql -u root -p'123456a\@A' -e \"show global variables like '$variable_name'\"`;
    my @response = `mysql -e \"show global variables like '$variable_name'\"`;
    my $response_info = $response[1];
    my @response_infoto_array = split(/\s+/,$response_info);
    my $value = $response_infoto_array[1];
    return $value;
}

sub is_slave
{
    my ($hostname) = @_;
    # $hostname = 'ult-n-db11-m'; #test
    if ( $hostname )
    {
        if ( $hostname =~ "-log")
        {
            return 1;
        }
        else 
        {
            return 0;
        }
    }
    else 
    {
        return 0;
    }
}
MAIN: {
    my $Exit_Code = check_mysql_status();
    if ($Exit_Code == 100)
    {
        print 0;
    }
    else 
    {
        my $variable = $ARGV[0];
        if ( $variable eq "buffer_size" )
        {
            my $buffer_size_status = check_buffer_size();
            print $buffer_size_status;
        }
        elsif ( $variable eq "read_only" )
        {
            my $host_check = '';
                 if ( $ARGV[1] )
            {
                $host_check = $ARGV[1];
            }
            my $read_only_status   = check_read_only($ARGV[1]);
            print $read_only_status;
        }
    }
}

# ******************************************************************************** #
# Sync script
# Create a script with following content and run with root
# 
# ********************************************************************************* #
# for i in {01..19};
# do
#     scp /opt/bin/zabbix/chk_mysql_config.pl rds${i}-log:/opt/bin/zabbix/
#     scp /opt/bin/zabbix/zabbix_agentd.d/userparameter_mysql.conf rds${i}-log:/opt/bin/zabbix/zabbix_agentd.d/
#     scp /opt/bin/zabbix/zabbix_agentd.d/userparameter_mysql.conf rds${i}-log:/etc/zabbix/zabbix_agentd.d/
#     ssh rds${i}-log "chown zabbix:zabbix /opt/bin/zabbix/chk_mysql_config.pl && cd /etc/zabbix && ln -s /opt/bin/zabbix/chk_mysql_config.pl && chown zabbix:zabbix /etc/zabbix/chk_mysql_config.pl && service zabbix-agent restart";
#     scp /opt/bin/zabbix/chk_mysql_config.pl rds${i}-m:/opt/bin/zabbix/
#     scp /opt/bin/zabbix/zabbix_agentd.d/userparameter_mysql.conf rds${i}-m:/opt/bin/zabbix/zabbix_agentd.d/
#     scp /opt/bin/zabbix/zabbix_agentd.d/userparameter_mysql.conf rds${i}-m:/etc/zabbix/zabbix_agentd.d/
#     ssh rds${i}-m "chown zabbix:zabbix /opt/bin/zabbix/chk_mysql_config.pl && cd /etc/zabbix && ln -s /opt/bin/zabbix/chk_mysql_config.pl && chown zabbix:zabbix /etc/zabbix/chk_mysql_config.pl && service zabbix-agent restart";
# done
# ********************************************************************************* #