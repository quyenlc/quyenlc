#!/usr/bin/perl

# use 5.16v2;
use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use MountChecker;
use AWSEC2;

my $WORKING_DIR = dirname (__FILE__);
my $TEMP_DIR = $WORKING_DIR."/tmp";
my $DFH_FILE = $TEMP_DIR."/dfh";
my $FSTAB_FILE = $TEMP_DIR."/fstab";
my $LSBLK_FILE = $TEMP_DIR."/lsblk";

# Get all hostname
my $awscli = new AWSEC2;
my $qres = $awscli->ec2(
	'describe-instances', {
		filters => [
			{
				Name 	=>'instance-state-code',
				Values 	=> ['16'],
			}
		]
	}
);
my $mc = new MountChecker;
	
for my $instance ( @{$qres->{Reservations}} )
{
	my $Tags = $instance->{Instances}[0]{Tags};
	for my $tag ( @{$Tags} )
	{
		if ( $tag->{Key} =~ "Name")
		{
			print " * Checking $tag->{Value} \n";
			# $mc->checkFstab($tag->{Value});
			# $mc->checkAttachedVolume($tag->{Value});
			print " * End Checking $tag->{Value}\n";
		}
	}
}

print " --- End --- \n";