#!/usr/bin/perl 

if ($#ARGV != 1){
    print "This script is to block some residues from docking. ";
    print "If you know that some residues are not in the binding sides, ";
    print "please list their residue numbers in a file with one number per line. ";   
    print "This program changes the ACE types of listed residues to 19 ";
    print "and prints the new pdb on the screen.\n";
    print "Attention: It only deals with single chain PDB. ";
    print "For proteins with multiple chain, please block them chain by chain.\n";
    print "Useage:\n";
    print "$0 [PDB file] [residue list file]\n";
    die;
}

$file = $ARGV[0];
$list = $ARGV[1];

open (LIST, "<$list") || die "\nCannot open file $list\n\n";
@residue_number = <LIST>;
close LIST;
chomp @residue_number;

open (PDB, "<$file") || die "\nCannot open file $file\n\n";
while ($line = <PDB>){
    if ($line =~ /^ATOM/){
	$res_num = substr($line, 22, 4);
      LINE: for ($i=0; $i<@residue_number; $i++){
	  if ($res_num == $residue_number[$i]){
	      substr($line, 55, 2)=19;
	      last LINE;
	  }
      }
	printf ("$line");
    }
}
close PDB;

