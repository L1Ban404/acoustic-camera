# Recreate, implement, and generate a bitstream for the source-managed design.
set script_dir [file normalize [file dirname [info script]]]
source [file join $script_dir create_project.tcl]

set project_file [file join [file normalize [file join $script_dir .. build vivado]] acoustic-camera-repro.xpr]
open_project $project_file

launch_runs impl_1 -to_step route_design -jobs 4
wait_on_run impl_1
set impl_status [get_property STATUS [get_runs impl_1]]
if {![string match "*Complete!*" $impl_status]} {
    error "Implementation did not complete successfully: $impl_status"
}

open_run impl_1
set run_dir [get_property DIRECTORY [get_runs impl_1]]
report_drc -file [file join $run_dir drc.rpt]
report_utilization -file [file join $run_dir utilization.rpt]
report_timing_summary -file [file join $run_dir timing_summary.rpt]

set drc_errors [get_drc_violations -quiet -filter {SEVERITY == Error}]
if {[llength $drc_errors] > 0} {
    error "Implementation has [llength $drc_errors] blocking DRC violation(s); see [file join $run_dir drc.rpt]"
}

write_bitstream -force [file join $run_dir acoustic-camera-repro.bit]
close_project
