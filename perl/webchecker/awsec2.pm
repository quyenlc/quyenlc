package AWSEC2;

# use base qw(ParentClass);
use Data::Dumper;
use AWS::CLIWrapper;
use Qconfig;
use File::Basename;
use lib dirname (__FILE__);
# use lib $ENV{WEB_CHECKER_DIR};

our  @ISA = qw(AWS::CLIWrapper);

# * Change this on production
my $config = new Qconfig;
$load_balancer_name = $config->{LOAD_BALANCER_NAME};
$ENV{AWS_CONFIG_FILE} = $config->{HOME_DIR}. '/' . $config->{AWS_CONFIG_FILE};
sub new {
	my ( $class, %params ) = @_;
	my $self = $class->SUPER::new(%params);
	my $res = $self->elb('describe-load-balancers');
	for my $elb ( @{$res->{'LoadBalancerDescriptions'}} )
	{
		if ( $elb->{'LoadBalancerName'} == $load_balancer_name) {
			$self->{'instance_list'} = $elb->{'Instances'};
		}
	}
	bless $self, $class;
	return $self;
}
sub filterInstance {
	my ( $self, $key, $value ) = @_;
	my %params = (
		$key => $value,
		'instance-state-code' => ['16'],
		);
	
	my @filters;
	for $key (keys %params){
		$filter = {
			Name 	=> $key,
			Values 	=> $params{$key}
		};
		push(@filters, $filter);
	}
	# print Dumper(\@filters);
	my $qres = $self->ec2(
		'describe-instances', {
		filters => \@filters,
		}
	);
	return $qres->{'Reservations'};
}

sub checkOnELB {
	$existence = 0;
	my ( $self, $instance_id ) = @_;
	for my $current_instance_id_hash ( @{$self->{'instance_list'}} )
	{
		if ( $current_instance_id_hash->{'InstanceId'} eq $instance_id ) {
			$existence = 1;
		}
	}

	return $existence;
}
1;