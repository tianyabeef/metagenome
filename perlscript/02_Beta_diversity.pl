#!/usr/bin/env perl
=pod
Description: Beta-diversity analysis, contains Anosim, PCoA and NMDS
Author: Zhong wendi
Create date: 20151022
=cut
use warnings;
use strict;
use Getopt::Long;
use File::Basename 'dirname';
use Cwd 'abs_path';

my ($profile, $grp_tab, $method, $run, $help);
GetOptions(
		"profile|p=s" => \$profile,
		"grp_tab|g=s" => \$grp_tab,
		"method|m=s"  => \$method,
		"run|r!"      => \$run,
		"help|h!"     => \$help);
&help unless defined $profile and -e $profile and defined $grp_tab and -e $grp_tab and defined $method and not defined $help;
my $src_dir = dirname(abs_path($0));
my $Rscript_dir = $src_dir . "/../Rscript";

## shell
open SH, ">beta_div.sh" or die $!;
print SH <<_SHELL_;
Rscript $Rscript_dir/02_Beta_diversity.R $Rscript_dir/02_Beta_diversity.fun.R $profile $grp_tab $method
_SHELL_
close SH;

# run
system("sh beta_div.sh") if defined $run;

sub help{
	print STDERR <<"_USAGE_" and exit 1;

description: Beta-diversity analysis, contains Anosim, PCoA and NMDS
usage: perl $0 [options]
options:
	-p <string>  profile.
	-g <string>  group table of samples.
	-m <string>  method to calculate the distance matrix.
	-r <options> autorun.
	-h <options> print this help infomation.
note:
	Methods contain the distance method in function "dist" and "vegdist" in "vegan" R package.
e.g.:
	perl $0 -p profile -g grp.tab -m bray -r

_USAGE_
}
