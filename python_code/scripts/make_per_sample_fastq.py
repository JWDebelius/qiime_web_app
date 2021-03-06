#!/usr/bin/env python
# File created on 02 May 2012
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.util import (parse_command_line_parameters, make_option,\
                       get_options_lookup,create_dir)
from cogent.parse.fasta import MinimalFastaParser
from minimal_converted_fastq_fasta_parser import MinimalConvertedFastqFastaParser
from qiime.parse import parse_mapping_file
from os.path import join, split, splitext
from string import strip


options_lookup=get_options_lookup()

script_info = {}
script_info['brief_description'] = "Make per-sample FASTQ files"
script_info['script_description'] = "This script will convert a split-library fna/qual into per-sample fastqs"
script_info['script_usage'] = [("Example:","","%prog -i seqs.fna -q seqs.qual -o per_sample_fastq")]
script_info['output_description']= "The output will be per-sample fastq files"
script_info['required_options'] = [\
 # Example required option
 options_lookup['fasta_as_primary_input'],
 make_option('-q','--input_qual_fp',type="existing_filepath",
  help='path to the input quality file'),
 options_lookup['output_dir'],
]
script_info['optional_options'] = [\
 # Example optional option
 # options_lookup['output_dir'],
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    
    # get cmd-line options
    fasta_fp=opts.input_fasta_fp
    qual_fp=opts.input_qual_fp
    output_dir=opts.output_dir
    
    # create output dir
    create_dir(output_dir)
    output_fps={}

    # open sequence files
    sequences=MinimalFastaParser(open(fasta_fp,'U'))
    qual_sequences=MinimalConvertedFastqFastaParser(open(qual_fp,'U'))
    
    # iterate over seqs
    for seq_name, seq in sequences:
        
        # iterate over qual
        qual_seq_name, qual_seq = qual_sequences.next()
                
        # verify headers from seq and qual match
        if seq_name == qual_seq_name:
            # get the SampleID
            samp_id = '_'.join(seq_name.split()[0].split('_')[:-1])
            samp_filename = 'seqs_%s' % (str(samp_id))
            # open files for output
            if not output_fps.has_key(str(samp_filename)):
                output_fps[str(samp_filename)] = open(join(output_dir, '%s.fastq' % (str(samp_filename))),'w')
            
            # write out the fastq format for seqs
            output_fps[str(samp_filename)].write('@%s\n%s\n+\n%s\n' % (seq_name,seq,qual_seq))
        else:
            print seq_name
    
    # close the files
    for s_id in output_fps:
        output_fps[str(s_id)].close()
    
    

if __name__ == "__main__":
    main()
