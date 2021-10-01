#dfsdfdsdsfdsf
use Termux::API;
use Data::Dumper;

my $termux=Termux::API->new();
$termux->sensor(-l);
#print Dumper($termux)
