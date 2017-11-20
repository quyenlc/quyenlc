#!/usr/bin/perl

# use 5.16v2;
use strict;
use warnings;
use File::Basename;
my $WORKING_DIR = dirname (__FILE__);
my $TEMP_DIR = $WORKING_DIR."/tmp";
my $DFH_FILE = $TEMP_DIR."/dfh";
my $FSTAB_FILE = $TEMP_DIR."/fstab";
my $LSBLK_FILE = $TEMP_DIR."/lsblk";
my $HOST_NAME = $ARGV[0];
if ( !$HOST_NAME )
{
	# die( "\n Usage: perl path_to_main.pl host_name");
}
mkdir $TEMP_DIR;
system("df -h > $DFH_FILE");
my @dfh_data = `cat $DFH_FILE`;
system("cat /etc/fstab > $FSTAB_FILE");
my @fstab = `cat $FSTAB_FILE`;
system("lsblk > $LSBLK_FILE");
my @lsblk = `cat $LSBLK_FILE`;
my $first_line =1;
my $mount_on_column_seq =0;

# mounted volumes must listed in fstab
for my $response ( @dfh_data ) {
	if ( $first_line )
	{
		for my $column (split(/\s+/,$response)) 
		{
			if ( ( $column =~ 'Mounted') )
			{
				last;
			}
			else
			{
				$mount_on_column_seq++;
			}
		}
		$first_line = 0;
		# print "$mount_on_column_seq\n";
		next;
	}
	my $mount_point = (split(/\s+/,$response))[$mount_on_column_seq];
	if ( ( $response =~ /^\/dev/ ) && !( "/ " cmp $mount_point ) )
	{
		my $device_name = (split(/\s/, $response))[0];
		my $ERROR = 1;
		my $message = '';
		for my $fstab_line ( @fstab ) {
			if ( $fstab_line =~ /^\/dev/)
			{
				if ( $fstab_line =~ $device_name ) 
				{
					$ERROR = 0;
				}
			}
		}
		if ( $ERROR eq 1 )
		{
			print "$device_name is not listed in fstab\n";
		}

	}
}

# attached volume should be mounted
for my $response ( @lsblk ) {
	if ( $response =~ /^xvd/)
	{
		my $device_name = (split(/\s+/,$response))[0];
		my $mount_point = (split(/\s+/,$response))[6];
		if ( !$mount_point )
		{
			my $WARNING = 1;
			for my $subresponse ( @lsblk )
			{
				if ( $subresponse =~ $device_name )
				{
					my $sub_mount_point = (split(/\s+/,$subresponse))[6];
					if ( $sub_mount_point ) {
						$WARNING = 0;
					}
				}
			}
			if ( $WARNING )
			{
				print "$device_name should be mounted\n";
			}
		}
	}
}


# Cleanning time
system("rm -f $LSBLK_FILE");
system("rm -f $FSTAB_FILE");
system("rm -f $DFH_FILE");
system("rm -rf $TEMP_DIR");
print " --- End --- \n";
