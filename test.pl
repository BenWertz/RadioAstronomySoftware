#dfsdfdsdsfdsf
use Termux::API;
use Data::Dumper;

my $termux=Termux::API->new();
print($termux->sensor(-s=>"Samsung Orientation Sensor"));
#print Dumper($termux)
