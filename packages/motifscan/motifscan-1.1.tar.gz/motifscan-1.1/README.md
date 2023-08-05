A Quick Start Guide for MotifScan(Draft)
Version 1.0.2

Obtain MotifScan
Download package from http://bioinfo.sibs.ac.cn/shaolab/opendata.php.

Then extract the package and build from the source:

tar -zxvf MotifScan_*.*.*.tar.gz

cd MotifScan_*.*.*
python setup install

or use option --prefix to specify the location you want to install.

python setup install --prefix=/home/jiawei

Under this circumstance, you should add your installation directory to PYTHONPATH and bash PATH:
export PYTHONPATH=/home/jiawei/lib/python2.7/dist-packges:$PYTHONPATH

export PATH=/home/jiawei/bin:$PATH


Motif Discovery
Search regions, motif candidate list and genome are required for a common motifscan task.

MotifScan -p  Example/SL2548_Peaks.bed -m Example/ motif_list_example.txt -g hg19 [-G hg19.fa]
	
-p region in bed format
-m motif name list
-g reference genome
-G genome sequence

Motif name list file looks like as follows::
Pou5f1
SOX10
ARID3A
Prrx2
Sox5
NFIC
Sox2
POU2F2
TEAD1
Sox3

MotifScan package contains the pre-compiled motifs stemmed from JASPAR. When running the MotifScan command for the first time, a directory named after .MotifScan will be created under the home directory (that is, /home/jiawei/.MotifScan) , then the pre-compiled motifs and other other required configuration files will be copied to that directory.

Also, you should specify the genome sequence via option –G for your first time running and Motifscan wiil format the sequence and store the formatted sequence in /home/jiawei/.MotifScan.

Compile Your Own Motif PWM
If you have some motifs (e.g. motif_pwm_example.txt) that not be included in our pre-complied motif collection, then you need to complie it by yourself via the following command.

MotifCompile -M  Example/motif_pwm_example.txt  -g hg19 -G hg19

-M motif raw matrix file
-g genome name specified
-G genome fasta file

Motif raw matrix file (motif_matrix_example.txt) should follow the format as below: motif id is followed by a positive weighted matrix, and columns are seperated by tabs.
>MA0599.1 KLF5
1429	0	0	3477	0	5051	0	0	0	3915
2023	11900	12008	9569	13611	0	13611	13611	13135	5595
7572	0	0	0	0	5182	0	0	0	0
2587	1711	1603	565	0	3378	0	0	476	4101


A binary file (python pickle) will be created under the directory /home/jiawei/.MotifScan/motif/hg19. Now you can add to your motif list file in I and run the MotifScan on that motif.

Note: It is a time-consuming step.
