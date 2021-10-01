#dfsdfdsdsfdsf
use Termux::API;
use Data::Dumper;

my $termux=Termux::API->new();
$termux->tts_speak("Heck yeah.")
#print Dumper($termux)
