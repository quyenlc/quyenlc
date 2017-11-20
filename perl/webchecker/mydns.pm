package MYDNS;

# use base qw(ParentClass);
use DBI;
use strict;
# use lib "./";
use Qconfig;

my $config = new Qconfig;
my $server_ip 	= $config->{WC_DB_HOST};
my $driver 		= $config->{WC_DB_DRIVER};
my $user_name 	= $config->{WC_DB_USER};
my $pass 		= $config->{WC_DB_PASS};
my $dbname 		= $config->{WC_DB_NAME};
my $port 		= $config->{WC_DB_PORT};
sub new {
	my $class = shift;
	# $class = ref $class if ref $class;
	my $self = {
		"id" 	=> shift,
		"zone" 	=> shift,
		"name" 	=> shift,
		"aux"	=> shift,
		"ttl" 	=> shift,
		"type" 	=> shift
	};
	my $data_source = "dbi:". $driver. ":database=". $dbname. ";host=". $server_ip. ";port=". $port;
	my $dbh = DBI->connect( $data_source, $user_name, $pass ) or die "\nUser: $user_name - Password: $pass - " . $DBI::errstr;
	my $sth = $dbh->prepare("SELECT name,data FROM rr WHERE name like 'ult-n-web-%'");
	$sth->execute() or die $DBI::errstr;
	my @instance_list;
	while ( my @row = $sth->fetchrow_array ) {
		my %instance = (
			name 	=> @row[0],
			value 	=> @row[1],
		);
		push (@instance_list, \%instance);
	}
	$self->{'instance_list'} = \@instance_list;
	bless $self, $class;
	return $self;
}

sub connectDB {
	my ( $self ) = @_;
	my $data_source = "dbi:". $driver. ":database=". $dbname. ";host=". $server_ip. ";port=". $port;
	my $dbh = DBI->connect( $data_source, $user_name, $pass ) or die "\nUser: $user_name - Password: $pass - " . $DBI::errstr;
	return $dbh;
}

sub LoadData {
	my ( $self, $hostname ) = @_;
	my $connector = $self->connectDB();
	my $sth = $connector->prepare("SELECT * FROM rr WHERE name =\"$hostname\"");
	$sth->execute() or die $DBI::errstr;
	my $icount = 0;
	while ( my @row = $sth->fetchrow_array )
	{
		$self->{'id'} 	= $row[0];
		$self->{'zone'} = $row[1];
		$self->{'name'} = $row[2];
		$self->{'data'} = $row[3];
		$self->{'aux'} 	= $row[4];
		$self->{'ttl'} 	= $row[5];
		$self->{'type'} = $row[6];
		$icount++;
	}
	return $icount;
}

sub validate {
	my ( $self ) = @_;
	for my $record ( @{$self->{instance_list}}) {
		if ( $record->{name} eq $self->{name} ) {
			if ( $record->{value} eq $self->{data}) {
				return 1;
			} else {
				return $record->{data};
			}
		}
	}
	return -1;
}



1;