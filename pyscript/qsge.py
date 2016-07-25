#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--input', dest='input', metavar='input', type=str, required=True,
                        help="input file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="out put dir")
    args = parser.parse_args()
    params = vars(args)
    return params

#!/usr/bin/perl -w
use strict;
use Getopt::Long;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname);
use File::Path qw(rmtree);
use Cwd qw(abs_path);
use Data::Dumper;

##get options from command line into variables and set default values
my ($Global,$Node, $Queue, $Interval, $Lines, $Maxjob, $Convert,$Secure,$Reqsub,$Resource,$Job_prefix,$Sub_Prjct_Id,$Verbose, $Help, $getmem, $dynamic);
GetOptions(
	"global"       => \$Global,
	"lines:i"      => \$Lines,
	"maxjob:i"     => \$Maxjob,
	"interval:i"   => \$Interval,
	"node:s"       => \$Node,
	"queue:s"      => \$Queue,
	"convert:s"    => \$Convert,
	"secure:s"     => \$Secure,
	"reqsub"       => \$Reqsub,
	"resource:s"   => \$Resource,
	"jobprefix:s"  => \$Job_prefix,
	"subprjctid:s" => \$Sub_Prjct_Id,
	"verbose"      => \$Verbose,
	"help"         => \$Help,
	"getmem"       => \$getmem,
	"dynamic"      => \$dynamic,
);
$Queue ||= "all.q";
$Interval ||= 30;
$Lines ||= 1;
$Maxjob ||= 30;
$Convert ||= 'no';
$Resource ||= "vf=1G";
$Job_prefix ||= "work";
&help if scalar @ARGV == 0 or $Help;

#global variables
my $work_shell_file = shift;
$work_shell_file = abs_path($work_shell_file);
my $work_shell_file_globle = $work_shell_file.".$$.globle";
my $work_shell_file_error = $work_shell_file.".$$.log";
my $Work_dir = $work_shell_file.".$$.qsub";
my $work_shell_file_reqsub = $work_shell_file.".$$.reqsub";
my $current_dir = abs_path(".");

### get mem ;  add by nixiaoming nixiaoming@genomics.cn
my $work_shell_mem = $work_shell_file.".$$.mem.log";
my %meminfo=();
my $whoami=`whoami`;chomp $whoami;

if ($Convert =~ /y/i) {
	absolute_path($work_shell_file,$work_shell_file_globle);
}else{
	$work_shell_file_globle = $work_shell_file;
}

if (defined $Global) {
	exit();
}
my $time='`date +%F'."'  '".'%H:%M`'; ### add by nixiaoming
## read from input file, make the qsub shell files

my $line_mark = 0;
my $Job_mark="0001";
my $sub_job_mark = "01";
mkdir $Work_dir;
my @Shell;  ## store the file names of qsub sell
my %Job_array;
open IN, $work_shell_file_globle || die "fail open $work_shell_file_globle";
while(<IN>){
	chomp;
	#s/&/;/g;
	next unless $_;
	if ($line_mark % $Lines == 0) {
		s/;\s*$//;  ##delete the last character ";", because two ";;" characters will cause error in qsub
		s/;\s*;/;/g;
		open OUT,">$Work_dir/$Job_prefix\_$Job_mark.sh" or die "failed creat $Job_prefix\_$Job_mark.sh\n";
		print OUT 'echo start at time '.$time."\n";
		print OUT $_.' &&  echo This-Work-is-Completed! && echo finish at time '.$time."\n";
		mkdir "$Work_dir/$Job_prefix\_$Job_mark.sh.split";
		open SPT,">$Work_dir/$Job_prefix\_$Job_mark.sh.split/$Job_prefix\_$Job_mark\_$sub_job_mark.sh" or die $!;
		print SPT 'echo start at time '.$time."\n";
		print SPT $_.' &&  echo This-Work-is-Completed! && echo finish at time '.$time."\n";
		close SPT;
		push @Shell,"$Work_dir/$Job_prefix\_$Job_mark.sh";

	}else {
		s/;\s*$//;  ##delete the last character ";", because two ";;" characters will cause error in qsub
		s/;\s*;/;/g;
		print OUT $_.' &&  echo This-Work-is-Completed! && echo finish at time '.$time."\n";
		open SPT,">$Work_dir/$Job_prefix\_$Job_mark.sh.split/$Job_prefix\_$Job_mark\_$sub_job_mark.sh" or die $!;
		print SPT $_.' &&  echo This-Work-is-Completed! && echo finish at time '.$time."\n";
		close SPT;
	}
	$Job_array{"$Work_dir/$Job_prefix\_$Job_mark.sh"}[$sub_job_mark-1] = "$Work_dir/$Job_prefix\_$Job_mark.sh.split/$Job_prefix\_$Job_mark\_$sub_job_mark.sh";
	$sub_job_mark ++;
	$sub_job_mark = sprintf("%02d",$sub_job_mark);
	if ($line_mark % $Lines == $Lines - 1) {
		close OUT;
		$sub_job_mark = "01";
		$Job_mark ++;
	}
	$line_mark++;
}
close IN;
close OUT;
#print STDERR "make the qsub shell files done\n" if($Verbose);

## run jobs by qsub, until all the jobs are really finished
my $qsub_cycle = 1;
while (scalar @Shell) {

	## throw jobs by qsub
	##we think the jobs on died nodes are unfinished jobs
	my %Alljob; ## store all the job IDs of this cycle
	my %Main_id;
	my %Sub_id;
	my %Error;  ## store the unfinished jobs of this cycle
	my $job_cmd = "qsub -cwd -S /bin/bash -terse";
	my $Host = "";$Host = "-l h=$Node" if defined $Node;
	my @Queue_array = &set_parameter($Lines,$Queue);
	my @Resource_array = &set_parameter($Lines,$Resource);
	my $Project = "";$Project = "-v Project=$Sub_Prjct_Id" if defined $Sub_Prjct_Id;
	open QSUB,">$work_shell_file_reqsub" or die $!;

	for (my $i=0; $i<@Shell; $i++) {
		while (1) {
			my $run_num = run_count(\%Alljob,\%meminfo,\%Main_id);
			my $hold_jid;
			my $job_id;
			if ($i < $Maxjob || ($run_num != -1 && $run_num < $Maxjob) ) {
				print QSUB "hold_jid=`$job_cmd $Host $Queue_array[0] $Resource_array[0] $Project -o $Shell[$i].out.log -e $Shell[$i].err.log $Job_array{$Shell[$i]}[0]`\n" if $qsub_cycle == 1;
				$hold_jid = `$job_cmd $Host $Queue_array[0] $Resource_array[0] $Project -o $Shell[$i].out.log -e $Shell[$i].err.log $Job_array{$Shell[$i]}[0]`;chomp $hold_jid;
				$job_id = $hold_jid;
				$Main_id{$hold_jid} = $job_id;
				$Sub_id{$job_id}[0] = $hold_jid;
				foreach my $j(1 .. $#{$Job_array{$Shell[$i]}}){
					print QSUB "hold_jid=`$job_cmd $Host $Queue_array[$j] $Resource_array[$j] $Project -hold_jid \$hold_jid -o $Shell[$i].out.log -e $Shell[$i].err.log $Job_array{$Shell[$i]}[$j]`\n" if $qsub_cycle == 1;
					$hold_jid = `$job_cmd $Host $Queue_array[$j] $Resource_array[$j] $Project -hold_jid $hold_jid -o $Shell[$i].out.log -e $Shell[$i].err.log $Job_array{$Shell[$i]}[$j]`;chomp $hold_jid;
					$Main_id{$hold_jid} = $job_id;
					$Sub_id{$job_id}[$j] = $hold_jid;
				}
				$Alljob{$job_id} = $Shell[$i];  ## job id => shell file name
				print STDERR "throw job $job_id in the $qsub_cycle cycle\n" if($Verbose);
				last;
			}else{
				print STDERR "wait for throwing next job in the $qsub_cycle cycle\n" if($Verbose);
				sleep $Interval;
			}
		}
	}
	close QSUB;
	###waiting for all jobs fininshed
	while (1) {
		my $run_num = run_count(\%Alljob,\%meminfo,\%Main_id);
		last if($run_num == 0);
		print STDERR "There left $run_num jobs runing in the $qsub_cycle cycle\n" if(defined $Verbose);

		if(defined $getmem){ ### get mem ;  add by nixiaoming nixiaoming@genomics.cn
			open GETMEM,'>',$work_shell_mem or die "can't open the mem info $work_shell_mem\n";
			print GETMEM "User:\t\t$whoami\nShellPath:\t$Work_dir\n";
			foreach my $main_id(sort keys %Sub_id){
				foreach my $i(0 .. $#{$Sub_id{$main_id}}){
					my $sub_id = $Sub_id{$main_id}[$i];
					my $shell = $Job_array{$Alljob{$main_id}}[$i];
					my $jobinfo = "";
					if (defined $meminfo{$sub_id}){
						$jobinfo = $meminfo{$sub_id};
						$jobinfo =~ s/usage\s*\w*:\s*//g;
					}
					print GETMEM "$whoami\t$sub_id\t$shell\t$jobinfo\n";
				}
			}
			close GETMEM;
		}
		sleep $Interval;
	}

	print STDERR "All jobs finished, in the firt cycle in the $qsub_cycle cycle\n" if($Verbose);


	##run the secure mechanism to make sure all the jobs are really completed
	open OUT, ">>$work_shell_file_error" || die "fail create $$work_shell_file_error";
#	chdir($Work_dir); ##enter into the qsub working directoy
	foreach my $job_id (sort keys %Alljob) {
		my $shell_file = $Alljob{$job_id};
		#check the .o file
		&check_log($shell_file,$job_id,\%Error);

	}

	##make @shell for next cycle, which contains unfinished tasks
	@Shell = ();
	foreach my $job_id (sort keys %Error) {
		my $shell_file = $Error{$job_id};
		`mv $shell_file.out.log $shell_file.out.log.cycle_$qsub_cycle`;
		`mv $shell_file.err.log $shell_file.err.log.cycle_$qsub_cycle`;
		push @Shell,$shell_file;
	}

	$qsub_cycle++;
	if($qsub_cycle > 2){
		print OUT "\n\nProgram stopped because the reqsub cycle number has reached 10, the following jobs unfinished:\n";
		foreach my $job_id (sort keys %Error) {
			my $shell_file = $Error{$job_id};
			print OUT $shell_file."\n";
		}
		print OUT "Please check carefully for what errors happen, and redo the work, good luck!";
		die "\nProgram stopped because the reqsub cycle number has reached 10\n";
	}

	print OUT "All jobs finished!\n" if scalar @Shell == 0;
#	chdir($current_dir); ##return into original directory
	close OUT;

	if(defined $getmem){ ### get mem ;  add by nixiaoming nixiaoming@genomics.cn
		open GETMEM,'>',$work_shell_mem or die "can't open the mem info $work_shell_mem\n";
		print GETMEM "User:\t\t$whoami\nShellPath:\t$current_dir/$Work_dir\n";
		foreach my $main_id(sort keys %Sub_id){
			foreach my $i(0 .. $#{$Sub_id{$main_id}}){
				my $sub_id = $Sub_id{$main_id}[$i];
				my $shell = $Job_array{$Alljob{$main_id}}[$i];
				my $jobinfo = "";
				if (defined $meminfo{$sub_id}){
					$jobinfo = $meminfo{$sub_id};
					$jobinfo =~ s/usage\s*\w*:\s*//g;
				}
				print GETMEM "$whoami\t$sub_id\t$shell\t$jobinfo\n";
			}
		}
	}
	print STDERR "The secure mechanism is performed in the $qsub_cycle cycle\n" if($Verbose);
	last unless defined $Reqsub;
}
#system "echo qsub-sge.pl finished |mail -s '$work_shell_file finished' zhongwd";
print STDERR "\nqsub-sge.pl finished\n" if($Verbose);


####################################################
################### Sub Routines ###################
####################################################
sub help{
	my $help = <<_HELP_;
Usage

  perl qsub-sge.pl <jobs.txt>
  --global            only output the global shell, but do not excute
  --queue <str>       specify the queue to use, default all.q; now can set queue for each step, split by colon
  --interval <num>    set interval time of checking by qstat, default 30 seconds
  --lines <num>       set number of lines to form a job, default 1
  --maxjob <num>      set the maximum number of jobs to throw out, default 30
  --convert <yes/no>  convert local path to absolute path, default yes
  --secure <mark>     set the user defined job completition mark, default no need
  --reqsub            reqsub the unfinished jobs untill they are finished, default no
  --resource <str>    set the required resource used in qsub -l option, default vf=1G ;now can set resource for each step, split by colon
  --jobprefix <str>   set the prefix tag for qsubed jobs, default work
  --subprjctid *<str> set the sub project id
  --verbose           output verbose information to screen
  --help              output help information to screen
  --getmem            output the usage (example: cpu=00:26:45, mem=111.63317 GBs, io=0.00000, vmem=259.148M, maxvmem=315.496M);

Exmple

  1.work with default options (the most simplest way)
  perl qsub-sge.pl ./work.sh

  2.work with user specifed options: (to select queue, set checking interval time, set number of lines in each job, and set number of maxmimun running jobs)
  perl qsub-sge.pl --queue all.q -interval 1 -lines 3 -maxjob 10  ./work.sh

  3.do not convert path because it is already absolute path (Note that errors may happen when convert local path to absolute path automatically)
  perl qsub-sge.pl --convert no ./work.sh

  4.add user defined job completion mark (this can make sure that your program has executed to its last sentence)
  perl qsub-sge.pl -inter 1  -secure "my job finish" ./work.sh

  5.reqsub the unfinished jobs until all jobs are really completed (the maximum allowed reqsub cycle is 10000)
  perl qsub-sge.pl --reqsub ./work.sh

  6.work with user defined memory usage
  perl qsub-sge.pl --resource vf=1.9G ./work.sh

  7.recommend combination of usages for common applications (I think this will suit for 99% of all your work)
nohup qsge --queue all.q --resource vf=1G --maxjob 10 --jobprefix work --lines 1 --getmem work.sh &
_HELP_
	print $help and exit;
}

sub absolute_path{
	my($in_file,$out_file)=@_;
	my($current_path,$shell_absolute_path);

	#get the current path ;
	$current_path=abs_path(".");

	#get the absolute path of the input shell file;
	if ($in_file=~/([^\/]+)$/) {
		my $shell_local_path=$`;
		if ($in_file=~/^\//) {
			$shell_absolute_path = $shell_local_path;
		}
		else{$shell_absolute_path="$current_path"."/"."$shell_local_path";}
	}

	#change all the local path of programs in the input shell file;
	open (IN,"$in_file");
	open (OUT,">$out_file");
	while (<IN>) {
		chomp;
		##s/>/> /; ##convert ">out.txt" to "> out.txt"
		##s/2>/2> /; ##convert "2>out.txt" to "2> out.txt"
		my @words=split /\s+/, $_;

		##improve the command, add "./" automatically
		for (my $i=1; $i<@words; $i++) {
			if ($words[$i] !~ /\//) {
				if (-f $words[$i]) {
					$words[$i] = "./$words[$i]";
				}elsif($words[$i-1] eq ">" || $words[$i-1] eq "2>"){
					$words[$i] = "./$words[$i]";
				}
			}

		}
#		for (my $i=0;$i<@words ;$i++) {
#			if (($words[$i]!~/^\//) && ($words[$i]=~/\//)) {
#				$words[$i]= "$shell_absolute_path"."$words[$i]";
#			}
#		}
		print OUT join(" ", @words), "\n";
	}
	close IN;
	close OUT;
}


##get the IDs and count the number of running jobs
##the All job list and user id are used to make sure that the job id belongs to this program
##add a function to detect jobs on the died computing nodes.
sub run_count {
	my $all_p = shift;
	my $mem_p = shift;
	my $main_id_p = shift;
	my $run_num = 0;
	my %run = ();
	my $user = $ENV{"USER"} || $ENV{"USERNAME"};
	my $qstat_result = `qstat -u $user`;
	$user = substr($user, 0, 12);
	if ($qstat_result =~ /failed receiving gdi request/ || ($qstat_result !~ /^\s*$/ && $qstat_result !~ /job\-ID/)) {
		$run_num = -1;
		return $run_num; ##系统无反应
	}
	my @jobs = split /\n/,$qstat_result;
	my %died;
	died_nodes(\%died) if (@jobs > 0); ##the compute node is down, 有的时候节点已死，但仍然是正常状态
	foreach my $job_line (@jobs) {
		$job_line =~s/^\s+//;
		my @job_field = split /\s+/,$job_line;
		if (exists $main_id_p->{$job_field[0]}){
			my $node_name = "";
			$node_name = $1 if ($job_field[7] =~ /(compute-\d+-\d+)/);
			if ( !exists $died{$node_name} && ($job_field[4] eq "qw" || $job_field[4] eq "r" || $job_field[4] eq "t" ||  $job_field[4] eq "hqw") ) {
				$run{$main_id_p->{$job_field[0]}} = $all_p->{$main_id_p->{$job_field[0]}}; ##job id => shell file name
				if ((defined $getmem) && ($job_field[4] eq "r")){### get mem ;  add by nixiaoming nixiaoming@genomics.cn
					my $jobinfo=`qstat -j $job_field[0] 2>&1 |grep usage `;
					chomp $jobinfo;
					$mem_p->{$job_field[0]}=$jobinfo; ##??
				}
			}else{
				`qdel $job_field[0]`;
			}
		}
	}
	$run_num = scalar keys %run;
	return $run_num; ##qstat结果中的处于正常运行状态的任务，不包含那些在已死掉节点上的僵尸任务
}


##HOSTNAME                ARCH         NCPU  LOAD  MEMTOT  MEMUSE  SWAPTO  SWAPUS
##compute-0-24 lx26-amd64 8 - 15.6G - 996.2M -
sub died_nodes{
	my $died_p = shift;
	my @lines = split /\n/,`qhost`;
	shift @lines for (1 .. 3); ##remove the first three title lines
	foreach  (@lines) {
		my @t = split /\s+/;
		my $node_name = $t[0];
		my $memory_use = $t[5];
		$died_p->{$node_name} = 1 if($t[3]=~/-/ || $t[4]=~/-/ || $t[5]=~/-/ || $t[6]=~/-/ || $t[7]=~/-/);
	}
}

sub check_log{
	my ($shell_file,$job_id,$Error_p) = @_;

	##read the .o file
	my $content;
	if (-f "$shell_file.out.log") {
		#open IN,"$shell_file.o$job_id" || warn "fail $shell_file.o$job_id";
		#$content = join("",<IN>);
		#close IN;
		$content = `tail -n 1000 $shell_file.out.log`;
	}
	##check whether the job has been killed during running time
	if ($content !~ /This-Work-is-Completed!/) {
		$Error_p -> {$job_id} = $shell_file;
		print OUT "In qsub cycle $qsub_cycle, In $shell_file.o$job_id,  \"This-Work-is-Completed!\" is not found, so this work may be unfinished\n";
	}

	##read the .e file
	if (-f "$shell_file.err.log") {
		#open IN,"$shell_file.e$job_id" || warn "fail $shell_file.e$job_id";
		#$content = join("",<IN>);
		#close IN;
		$content = `tail  -n 1000 $shell_file.err.log`;
	}
	##check whether the C/C++ libary is in good state
	if ($content =~ /GLIBCXX_3.4.9/ && $content =~ /not found/) {
		$Error_p->{$job_id} = $shell_file;
		print OUT "In qsub cycle $qsub_cycle, In $shell_file.e$job_id,  GLIBCXX_3.4.9 not found, so this work may be unfinished\n";
	}
		##check whether iprscan is in good state
	if ($content =~ /iprscan: failed/) {
		$Error_p->{$job_id} = $shell_file;
		print OUT "In qsub cycle $qsub_cycle, In $shell_file.e$job_id, iprscan: failed , so this work may be unfinished\n";
	}
		##check the user defined job completion mark
	if (defined $Secure && $content !~ /$Secure/) {
		$Error_p->{$job_id} = $shell_file;
		print OUT "In qsub cycle $qsub_cycle, In $shell_file.o$job_id,  \"$Secure\" is not found, so this work may be unfinished\n";
	}
}

sub set_parameter{
	my ($lines,$par) = @_;
	my $head;
	if($par =~ s/(.*=)//g){
		$head = "-l ".$1;
	}else {
		$head = "-q ";
	}
	my @par = split /:/,$par;
	my @new_par;
	foreach my $i(0 .. $lines){
		my $j = $i % scalar @par;
		$new_par[$i] = $head.$par[$j];
	}
	return @new_par;
}
