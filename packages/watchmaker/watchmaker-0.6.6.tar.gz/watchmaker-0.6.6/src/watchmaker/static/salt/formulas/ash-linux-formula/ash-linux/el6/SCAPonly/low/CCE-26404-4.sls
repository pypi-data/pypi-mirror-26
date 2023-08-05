# This Salt test/lockdown implements a SCAP item that has not yet been
# merged into the DISA-published STIGS
#
# Security identifiers:
# - CCE-26404-4
#
# Rule ID: kernel_module_squashfs_disabled
#
# Rule Summary: Disable Mounting of squashfs
#
# Rule Text: Linux kernel modules which implement filesystems that are 
#            not needed by the local system should be disabled.
#
#################################################################

{%- set scapId = 'CCE-26404-4' %}
{%- set helperLoc = 'ash-linux/el6/SCAPonly/low/files' %}
{%- set fsDrv = 'squashfs' %}
{%- set moduleConf = '/etc/modprobe.d/' + fsDrv + '.conf' %}

script_{{ scapId }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ scapId }}.sh
    - cwd: '/root'

append_{{ scapId }}-directive:
  file.append:
    - name: '{{ moduleConf }}'
    - mode: '0644'
    - text: |
        # Added per SCAP-ID {{ scapId }}
        install {{ fsDrv }} /bin/false
    - unless: 'grep {{ fsDrv }} {{ moduleConf }}'
