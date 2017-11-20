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

my $method = 'GET';
my $service = 'ec2';
my $host = 'ec2.ap-southeast-1.amazonaws.com';
my $region = 'ap-southeast-1';
my $endpoint = 'http://ec2.ap-southeast-1.amazonaws.com';
my $request_parameters = 'Action=DescribeInstances&Version=2013-10-15';

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
sub sign {
	my ($key, $msg) = @_;
	return hmac_sha256(encode('UTF-8', $msg, Encode::FB_CROAK), $key);
}

sub getSignatureKey{
	my ($key, $dateStamp, $regionName, $serviceName) = @_;
	my $kdate = sign(encode('UTF-8', 'AWS4'.$key, Encode::FB_CROAK), $dateStamp);
	my $kRegion = sign( $kdate, $regionName);
	my $kService = sign($kRegion, $serviceName);
	my $kSigning = sign($kService, 'aws4_request');
	return $kSigning;
}

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
my $access_key = 'xxx';
my $secret_key = 'xxx';

# Create a date for headers and the credential string
my @date = localtime();
my $year = $date[5] + 1900;
my $datestamp = $year.sprintf("%02d",$date[4]).sprintf("%02d",$date[3]);
my $amzdate = $datestamp.'T'.sprintf("%02d",$date[2]).sprintf("%02d",$date[1]).sprintf("%02d",$date[0])."Z";

# ************* TASK 1: CREATE A CANONICAL REQUEST *************
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Step 1 is to define the verb (GET, POST, etc.)--already done.

# Step 2: Create canonical URI--the part of the URI from domain to query 
# string (use '/' if no path)
my $canonical_uri = '/' ;

# Step 3: Create the canonical query string. In this example (a GET request),
# request parameters are in the query string. Query string values must
# be URL-encoded (space=%20). The parameters must be sorted by name.
# For this example, the query string is pre-formatted in the request_parameters variable.
my $canonical_querystring = $request_parameters;

# Step 4: Create the canonical headers and signed headers. Header names
# and value must be trimmed and lowercase, and sorted in ASCII order.
# Note that there is a trailing \n.
my $canonical_headers = 'host:' . $host . "\n" . 'x-amz-date:' . $amzdate . "\n";

# Step 5: Create the list of signed headers. This lists the headers
# in the canonical_headers list, delimited with ";" and in alpha order.
# Note: The request can include any headers; canonical_headers and
# signed_headers lists those that you want to be included in the 
# hash of the request. "Host" and "x-amz-date" are always required.
my $signed_headers = 'host;x-amz-date';

# Step 6: Create payload hash (hash of the request body content). For GET
# requests, the payload is an empty string ("").
my $payload_hash = sha256_hex('');

# Step 7: Combine elements to create create canonical request
my $canonical_request = $method . "\n" . $canonical_uri . "\n" . $canonical_querystring . "\n" . $canonical_headers . "\n" . $signed_headers . "\n" . $payload_hash;


# ************* TASK 2: CREATE THE STRING TO SIGN*************
# Match the algorithm to the hashing algorithm you use, either SHA-1 or
# SHA-256 (recommended)
my $algorithm = 'AWS4-HMAC-SHA256';
my $credential_scope = $datestamp . '/' . $region . '/' . $service . '/' . 'aws4_request';
my $string_to_sign = $algorithm . "\n" .  $amzdate . "\n" .  $credential_scope . "\n" .  sha256_hex($canonical_request);


# ************* TASK 3: CALCULATE THE SIGNATURE *************
# Create the signing key using the function defined above.
my $signing_key = getSignatureKey($secret_key, $datestamp, $region, $service);

# Sign the string_to_sign using the signing_key
my $signature = hmac_sha256_hex($string_to_sign, encode('UTF-8', $signing_key, Encode::FB_CROAK)) ;


# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
# The signing information can be either in a query string value or in 
# a header named Authorization. This code shows how to use a header.
# Create authorization header and add to request headers
my $authorization_header = $algorithm . ' ' . 'Credential=' . $access_key . '/' . $credential_scope . ', ' .  'SignedHeaders=' . $signed_headers . ', ' . 'Signature=' . $signature;

# The request can include any headers, but MUST include "host", "x-amz-date", 
# and (for this scenario) "Authorization". "host" and "x-amz-date" must
# be included in the canonical_headers and signed_headers, as noted
# earlier. Order here is not significant.
# Python note: The 'host' header is added automatically by the Python 'requests' library.
my $ua = LWP::UserAgent->new;
$ua->timeout(10);
$ua->env_proxy;
my @header = (
	'x-amz-date' => $amzdate,
	host => $host,
	Authenticate => $authorization_header,
);

# ************* SEND THE REQUEST *************
my $request_url = $endpoint . '?' . $canonical_querystring;

print "\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++";
print 'Request URL = ' . $request_url. "\n";
my $response = $ua->get($request_url, @header);
 print Dumper(\%$response);
 if ($response->is_success) {
     print $response->decoded_content;  # or whatever
 }
 else {
     die $response->status_line;
 } 
