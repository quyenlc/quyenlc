use LWP::UserAgent;
use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use AWS::CLIWrapper;

my $awscli = new AWS::CLIWrapper;
my $qres = $awscli->ec2(
        'describe-instances',
    );
for my $instance ( @{$qres->{'Reservations'}} ) {
    my $Tags = $instance->{Instances}[0]{Tags};
    for my $tag ( @{$Tags} )
    {
        if ( $tag->{Key} =~ "Name")
        {
            print "$tag->{Value}\n"
        }
    }

}
# print Dumper(\$qres->{'Reservations'});