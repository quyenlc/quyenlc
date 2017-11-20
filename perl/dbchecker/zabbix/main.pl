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
    #my $mem_info = "Mem:      71392   13558756    1812636          0     263524    2967220"; #test
    my @mem_info_array = split(/\s+/,$mem_info);
    my $total_memory = 1024 * $mem_info_array[1];

    my $innodb_buffer_pool_size = show_variable('innodb_buffer_pool_size');
    if ( $total_memory <= $innodb_buffer_pool_size )
    {
        return 1;
    }
    else
    {
        return 0;
    }

}

sub check_read_only
{
    my ($hostname) = @_;
    my $read_only = show_variable('read_only');
    # print "\n$read_only";
    if ( is_slave($hostname) == 1 )
    {
        if ( $read_only eq 'OFF' )
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
        if ( $read_only eq 'ON' )
        {
            return 1;
        }
        else
        {
            return 0;
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
    if ( $hostname =~ "-log")
    {
        return 1;
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
        print $Exit_Code
    }
    else 
    {
        my $buffer_size_status = check_buffer_size();
        my $read_only_status   = check_read_only($ARGV[0]);
        $Exit_Code += 10 * $buffer_size_status;
        $Exit_Code += $read_only_status;
        print $Exit_Code;
    }
}
