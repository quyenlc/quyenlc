package QMAIL;
use MIME::Lite::TT::HTML;
use Qconfig;
use File::Basename;
use lib dirname (__FILE__);
#Check working process
# use lib $ENV{WEB_CHECKER_DIR};

my %options;
my $config = new Qconfig;
$options{INCLUDE_PATH} = $config->{HOME_DIR};
my $template_file = $config->{MAIL_HTML_TPL};

sub new {
	my $class = shift;
	my $self = {
		From        =>  'web-monitor@hn-infra.dena.vn',
        Template    =>  {
            html    =>  $template_file,
        },
        TmplOptions =>  \%options,  
	};
	bless $self, $class;
	$self;
}

sub send {
	my ( $self, $type, $message ) = @_;
    my $data = {
        first_name  => 'Quyen',
        type        => $type,
        message     => $message,
    };
    my $header = {
        To      => 'quyen.le@dena.jp',
        Subject => $type. " when checking web instances",
    };
	my $msg = MIME::Lite::TT::HTML->new(
            From        =>  $self->{From},
            To          =>  $header->{To},
            Subject     =>  $header->{Subject},
            Template    =>  $self->{Template},
            TmplOptions =>  $self->{TmplOptions},
            TmplParams  =>  $data,
 	);
    print "\n Sending report...\n";
 	$msg->send;
}

1;