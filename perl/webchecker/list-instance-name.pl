
use strict;
use warnings;
use JSON::RPC::Client;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use AWSEC2;

my $aws = new AWSEC2;
my $elb_info = $aws->elb('describe-load-balancers', {
	'load_balancer_name' => 'ultimate'
	});
my $instance_list = $elb_info->{'LoadBalancerDescriptions'}[0]{'Instances'};
my @instance_id_list;
for my $instance ( @{$instance_list} ) {
	my $instance_id = $instance->{'InstanceId'};
	push( @instance_id_list, $instance_id);
}

my $instances_info = $aws->ec2('describe-instances', {instance_ids=>\@instance_id_list});
my $icount =0;
for my $instance ( @{$instances_info->{Reservations}} )
{
	my $tags = $instance->{Instances}[0]{Tags};
	for my $tag ( @{$tags} )
	{
		if ( $tag->{Key} =~ 'Name' )
		{
			print $tag->{Value}. "-";
			$icount++;
		}
	}
}
print "\n Count : $icount\n";

# print Dumper(\@instance_id_list);
