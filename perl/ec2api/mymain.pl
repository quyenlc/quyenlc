use LWP::UserAgent;
use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use URI::Encode qw(uri_encode uri_decode);
use URI::Escape qw(uri_escape);
use Digest::SHA qw(sha256 sha256_hex hmac_sha256 hmac_sha256_hex sha256_base64); 
use Base16;
use Digest::SHA qw(hmac_sha256_hex hmac_sha256); 
use Encode qw(decode encode);

my $ua = LWP::UserAgent->new;
my $region 	= 'ap-southeast-1';
my $service = 'ec2';
my $host = 'ec2.ap-southeast-1.amazonaws.com';
my $end_point = "http://$host"; # Oregon
my $key_id = 'xxx';
my $access_key 		= 'xxx';
my $query_string 	= 'Action=DescribeInstances';
my $algorithm 		= "AWS4-HMAC-SHA256";
my $signed_header 	= 'host;x-amz-date';
my @date = localtime();
my $year = $date[5] + 1900;
my $date_string = $year.sprintf("%02d",$date[4]).sprintf("%02d",$date[3]);
my $request_date = $date_string.'T'.sprintf("%02d",$date[2]).sprintf("%02d",$date[1]).sprintf("%02d",$date[0])."Z";

$ua->timeout(10);
$ua->env_proxy;
$ua->default_header('host' => $host);
$ua->default_header('x-amz-date' => "$date_string");


# print Dumper(\%$ua->{def_headers});
# print $year;
my $credential_scope = $date_string."/$region/$service/aws4_request\n";
my $canonical_request = genCanonicalRequest($query_string);
my $b16_canonical_request = Base16::encode($canonical_request);
my $string_to_sign = $algorithm."\n".$request_date."\n".$credential_scope.$b16_canonical_request;
# print $string_to_sign;
my $kDate 		= hmac_sha256($date_string, "AWS4" . $access_key);
my $kRegion 	= hmac_sha256($region, $kDate);
my $kService 	= hmac_sha256($service, $kRegion);
my $kSigning 	= hmac_sha256("aws4_request", $kService);
my $signature 	= hmac_sha256_hex($string_to_sign, $kSigning);

my $authorization_header = $algorithm . ' ' . 'Credential=' . $key_id . '/' . 
	$credential_scope . ', ' .  'SignedHeaders=' . $signed_header . ', ' . 
	'Signature=' . $signature;
# $query_string.= "&X-Amz-Algorithm=$algorithm";
# $query_string.= "&X-Amz-Credential=". uri_escape("$key_id/".$date_string."/$region/$service/aws4_request");
# $query_string.= "&X-Amz-Date=$request_date";
# $query_string.= "&X-Amz-Expires=60";
# $query_string.= "&X-Amz-SignedHeaders=".uri_escape($signed_header);
# $query_string.= "&X-Amz-Signature=$signature";

my $url = "$end_point?".$query_string;
$ua->default_header(Authorization => $authorization_header);
print "\n URL: $url";
print "\n request: ";
print Dumper(\%$ua);
 my $response = $ua->get($url);
 print Dumper(\%$response);
 if ($response->is_success) {
     print $response->decoded_content;  # or whatever
 }
 else {
     die $response->status_line;
 }

print "\n--- End ---\n";
sub genCanonicalRequest {
	my ($query) = @_;
	my $canonical_method 	= 'GET';
	my $canonical_uri 		= '/';
	my $canonical_query 	= uri_escape($query);
	my $canonical_header 	= "host:$host\nx-amz-date:$date_string";
	my $payload = '';
	my $hashed_payload 		= sha256_hex($payload);
	my $canonical_form 		= "$canonical_method\n$canonical_uri\n$query\n$canonical_header\n$signed_header\n$hashed_payload";
	my $hashed_request 		= sha256($canonical_form);
	return $hashed_request;
}
# Example request: 
# 	https://ec2.amazonaws.com/?
# 	Action=RunInstances&ImageId=ami-2bb65342&MaxCount=3&MinCount=1&Placement.AvailabilityZone=us-east-1a&Monitoring.Enabled=true&
# 	Version=2015-10-01&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIDEXAMPLE%2F20130813%2Fus-east-1%2Fec2%2Faws4_request&
# 	X-Amz-Date=20130813T150206Z&X-Amz-SignedHeaders=content-type%3host%3x-amz-date&
# 	X-Amz-Signature=525d1a96c69b5549dd78dbbec8efe264102288b83ba87b7d58d4b76b71f59fd2
