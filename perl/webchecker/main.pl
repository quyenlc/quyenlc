#!/usr/bin/perl

# use 5.010;
use strict;
use warnings;
use JSON::RPC::Client;
use MIME::Lite::TT::HTML;
use Data::Dumper;
# use experimental 'smartmatch';
use File::Basename;
use lib dirname (__FILE__);
use Zabbix;
use AWSEC2;
use MYDNS;
use QMAIL;

# print $ENV{AWS_CONFIG_FILE};
my @excepted_instances = ();
my $qmail = new QMAIL;
my $ZAB_SRV = new Zabbix;
my $aws = new AWSEC2;
my $oMyDNS = new MYDNS;
my $type = "";
my $message = "";

# Get all web instances name
my $qres = $aws->filterInstance("tag:Name",["ult-n-web*"]);
if ( scalar @{$qres} == 0) 
{
    print "There is no instance with that filter\n";
}
for my $instance (@{$qres})
{
    my $instance_info = $instance->{'Instances'}[0];
    my $private_ipdd = $instance_info->{'PrivateIpAddress'};
    # print $private_ipdd;
    my $tags = $instance_info->{'Tags'};
    for my $tag (@{$tags})
    {
        if ( $tag->{'Key'} eq "Name" )
        {
            my $tag_name = $tag->{'Value'};
            if ( !grep(/$tag_name/, @excepted_instances) ) 
            {
                print " \n ---------- \n";
                print "\nChecking host ". $tag->{'Value'}. " ...\n";
                # Check on ELB
                my $ELB_status = $aws->checkOnELB($instance_info->{'InstanceId'});
                print "\n Status on ELB: $ELB_status\n";
                if ( $ELB_status == 0 )
                {
                    if ( !$type) {
                        $type = 'WARNING';
                    }
                    $message .= "<tr><td>$tag->{'Value'}</td><td>ELB</td><td>WARNING</td><td>Not added to ELB</td></tr>";
                }
                # Check on zabbix 
                my $zabbix_status = $ZAB_SRV->getHostStatus($tag->{'Value'});
                print "\n Status on Zabbix: $zabbix_status\n";
                if ( $zabbix_status != 0)
                {
                    $type = "CRITICAL";
                    if ( $zabbix_status == 1 )
                    {
                        # $message .= "Host $tag->{'Value'} hasn been disabled on Zabbix\n";
                        $message .= "<tr><td>$tag->{'Value'}</td><td>Zabbix</td><td>CRITICAL</td><td>Disabled on Zabbix</td></tr>";
                    }
                    else 
                    {
                        # $message .= "Host $tag->{'Value'} hasn't been added to Zabbix\n"; 
                        $message .= "<tr><td>$tag->{'Value'}</td><td>Zabbix</td><td>CRITICAL</td><td>Not added to Zabbix</td></tr>";
                    }
                }
                # Check on DNS database
                $oMyDNS->{'name'} = $tag->{'Value'};
                $oMyDNS->{'data'} = $private_ipdd;
                my $dns_status = $oMyDNS->validate();
                print "\n MyDNS database status: $dns_status";
                if ( $dns_status ne 1 )
                {
                    $type = 'CRITICAL';
                    if ( $dns_status eq -1 )
                    {
                        # $message .= "Host $tag->{'Value'} does not exist on MyDNS database\n";
                        $message .= "<tr><td>$tag->{'Value'}</td><td>MyDNS</td><td>CRITICAL</td><td>Not exist on Database</td></tr>";
                    }
                    else
                    {
                        $message .= "<tr><td>$tag->{'Value'}</td><td>MyDNS</td><td>CRITICAL</td><td>Wrong private ip on MyDNS. Value should be $private_ipdd instead of be $dns_status</td></tr>";
                        # $message .= "Host $tag->{'Value'} has wrong private ip on MyDNS. Value: ". $private_ipdd . "\n";
                    }
                }
            }
        }
    }
}
if ($type){
    $qmail->send($type, $message);  
    print "\n";
} else {
    print "\nEverythings are OK\n";
}
