package Base16;
 
require 5.005_62;
use strict;
use warnings;
 
# use vars qw( $VERSION );
# $VERSION = '1.2';
 
sub import {
        *encode = \&encode_base16;
        *decode = \&decode_base16;
}
 
sub decode_base16 {
        my $arg = shift;
        my $ret = "";
        for(my $i=0;$i<length($arg);$i+=2){
                my $tmp = substr($arg,$i,2);
                my $int = hex($tmp);
                $ret .= chr ($int);
        }
        return $ret;
}
 
sub encode_base16 {
        my $arg = shift;
        my $ret = "";
        for(my $i=0;$i<length($arg);$i+=1){
                my $tmp = ord(substr($arg,$i,1));
                #$ret .= sprintf "%x", $tmp;#old
                $ret .= sprintf "%02x", $tmp;#new
        }
        return $ret;
}
 
1;