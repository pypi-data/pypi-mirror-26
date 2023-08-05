#!/bin/bash
#
# Finding ID:	RHEL-07-040331
# Version:	RHEL-07-040331_rule
# SRG ID:	SRG-OS-000480-GPOS-00227
# Finding Level:	high
# 
# Rule Summary:
#	There must be no shosts.equiv files on the system.
#
# CCI-000366 
#    NIST SP 800-53 :: CM-6 b 
#    NIST SP 800-53A :: CM-6.1 (iv) 
#    NIST SP 800-53 Revision 4 :: CM-6 b 
#
#################################################################
# Standard outputter function
diag_out() {
   echo "${1}"
}

diag_out "----------------------------------------"
diag_out "STIG Finding ID: RHEL-07-040331"
diag_out "   There must be no shosts.equiv files"
diag_out "   on the system."
diag_out "----------------------------------------"

