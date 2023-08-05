#!/bin/sh
# Finding ID:	RHEL-07-030330
# Version:	RHEL-07-030330_rule
# SRG ID:	SRG-OS-000342-GPOS-00133
# Finding Level:	medium
# 
# Rule Summary:
#	The operating system must off-load audit records onto a different
#	system or media from the system being audited.
#
# CCI-001851 
#    NIST SP 800-53 Revision 4 :: AU-4 (1) 
#
#################################################################
# Standard outputter function
diag_out() {
   echo "${1}"
}

diag_out "----------------------------------------"
diag_out "STIG Finding ID: RHEL-07-030330"
diag_out "   The operating system must off-load"
diag_out "   audit records onto a different"
diag_out "   system or media from the system"
diag_out "   being audited."
diag_out "----------------------------------------"
