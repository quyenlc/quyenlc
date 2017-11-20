package Qconfig;
use File::Basename;
use lib dirname (__FILE__);

# use base qw(ParentClass);
sub new {
	my $class = shift;
	my $self = {
		HOME_DIR 			=> dirname (__FILE__),
		AWS_CONFIG_FILE 	=> "ec2envvar",
		LOAD_BALANCER_NAME 	=> "ultimate",
		MAIL_HTML_TPL 		=> "test.html.tt",
		WC_DB_HOST 			=> "localhost",
		WC_DB_DRIVER 		=> 'mysql',
		WC_DB_USER 			=> 'mydns',
		WC_DB_PASS 			=> '123456a@A',
 		WC_DB_NAME 			=> "marveldns",
 		WC_DB_PORT 			=> 3306,
 		ZB_SRV_IP 			=> "mon.marvel.denagames-asia.com",
 		ZB_SRV_URL 			=> "http://mon.marvel.denagames-asia.com/zabbix/api_jsonrpc.php",
 		ZB_SRV_USER 		=> "infra-test",
 		ZB_SRV_PASS 		=> "Punch123!",
	};
	bless $self, $class;
	return $self;
}

1;