package MountChecker;
use strict;
use warnings;
use File::Basename;
# use base qw(ParentClass);
my $WORKING_DIR = dirname (__FILE__);
my $TEMP_DIR = $WORKING_DIR."/tmp";
my $DFH_FILE = $TEMP_DIR."/dfh";
my $FSTAB_FILE = $TEMP_DIR."/fstab";
my $LSBLK_FILE = $TEMP_DIR."/lsblk";

sub new {
	my $class = shift;
	my $self = {
	};
	bless $self, $class;
	return $self;
}

sub checkFstab {
	system("mkdir $TEMP_DIR");
	my ( $self, $hostname ) = @_;

	# Load data
	system("ssh $hostname \"df -h\" > $DFH_FILE");
	system("ssh $hostname \"cat /etc/fstab\" > $FSTAB_FILE");
	my @dfh_data = `cat $DFH_FILE`;
	my @fstab = `cat $FSTAB_FILE`;

	my $first_line = 1;
	my $mount_on_column_seq = 0;
	for my $response ( @dfh_data )
	{
		if ( $first_line )
		{
			# Find position of "Mounted on" column
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
			# root ("/") partition doest need to be added to fstab
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
				print "--- $device_name is not listed in fstab\n";
				print "Detail: $response\n";
			}

		}
	}
	system("rm -rf $TEMP_DIR");
}

sub checkAttachedVolume {
	my ( $self, $hostname ) = @_;
	system("mkdir $TEMP_DIR");
	system("ssh $hostname lsblk > $LSBLK_FILE");
	my @lsblk = `cat $LSBLK_FILE`;
	my $first_line = 1;
	my $MOUNTPOINT_column_seq = 0;

	for my $response ( @lsblk ) {
		if ( $first_line )
		{
			# Find position of "Mounted on" column
			for my $column (split(/\s+/,$response)) 
			{
				if ( ( $column =~ 'MOUNTPOINT') )
				{
					last;
				}
				else
				{
					$MOUNTPOINT_column_seq++;
				}
			}
			$first_line = 0;
			# print "$MOUNTPOINT_column_seq\n";
			next;
		}
		if ( $response =~ /^xvd/)
		{
			my $device_name = (split(/\s+/,$response))[0];
			my $mount_point = (split(/\s+/,$response))[$MOUNTPOINT_column_seq];
			if ( !$mount_point )
			{
				my $WARNING = 1;
				for my $subresponse ( @lsblk )
				{
					if ( $subresponse =~ $device_name )
					{
						my $sub_mount_point = (split(/\s+/,$subresponse))[$MOUNTPOINT_column_seq];
						if ( $sub_mount_point ) {
							$WARNING = 0;
						}
					}
				}
				if ( $WARNING )
				{
					print "--- $device_name should be mounted\n";
				}
			}
		}
	}

	system("rm -rf $TEMP_DIR");

}

1;