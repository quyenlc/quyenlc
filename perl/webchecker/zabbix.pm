package Zabbix;

# use base qw(ParentClass);
use strict;
use warnings;
use JSON::RPC::Client;
use Data::Dumper;
use Qconfig;
use File::Basename;
use lib dirname (__FILE__);
# use lib $ENV{WEB_CHECKER_DIR};

my $client = new JSON::RPC::Client;
my $config = new Qconfig;
sub new {
	my $class = shift;
	$class = ref $class if ref $class;
	my $self = {
		'SERVER_IP' 	=> $config->{ZB_SRV_IP},
		'SERVER_URL' 	=> $config->{ZB_SRV_URL},
		'USER' 			=> $config->{ZB_SRV_USER},
		'PASS' 			=> $config->{ZB_SRV_PASS},
	};
	bless $self, $class;
	return $self;
}

sub genReqTpl {
	# Generate a template for requests
	my ( $self ) = @_;
	my $auth_id = $self->getAuthID();
	my $request = {
	    "jsonrpc" 	=> "2.0",
	    "auth" 		=> $auth_id,
	    "id" 		=> 1
	};
	return $request;
}

sub getAuthID {
	# Generate ID to authenticate for requests
	my ( $self ) = @_;
	my $json = {
		"jsonrpc" => "2.0",
		"method" => "user.login",
		"params" => {
			"user" 		=> $self->{'USER'},
			"password" 	=> $self->{'PASS'},
	},
	"id" => 1,
	};
	my $url = $self->{'SERVER_URL'};
	my $response = $client->call($url, $json);
	die "Authentication failed\n" unless $response->content->{'result'};
	return $response->content->{'result'};
}

sub getHost {
	my ( $self, $hostname ) = @_;
	my $request = $self->genReqTpl();
	$request->{'method'} = "host.get";

	my $params = {
		"output" 	=> "extend",
		"filter" 	=>  {
            "host" 		=> [ $hostname ]
        }
	};
	$request->{'params'} = $params;
	my $url = $self->{'SERVER_URL'};
	my $response = $client->call($url, $request);

	return $response;

}

sub getHostStatus {
	my ( $self, $hostname ) = @_;
	my $host_info_response = $self->getHost($hostname);
	if ( $host_info_response->{'content'}->{'result'}->[0])
	{
		# 0: Enabled, 1: Disabled
		my $status = $host_info_response->{'content'}->{'result'}->[0]->{'status'};
		return $status
	}
	else
	{
		return 2;
	}
}

sub testClassMethod {
	my ( $string ) = @_;
	return "\n".$string."\n";
}

1;