set script_dir [file normalize [file dirname [info script]]]
source [file join $script_dir create_project.tcl]

set project_file [file join [file normalize [file join $script_dir .. build vivado]] acoustic-camera-repro.xpr]
open_project $project_file
launch_runs synth_1 -jobs 4
wait_on_run synth_1
if {[get_property STATUS [get_runs synth_1]] ne "synth_design Complete!"} {
    error "Synthesis did not complete successfully: [get_property STATUS [get_runs synth_1]]"
}
open_run synth_1
report_utilization -file [file join [get_property DIRECTORY [get_runs synth_1]] utilization.rpt]
report_timing_summary -file [file join [get_property DIRECTORY [get_runs synth_1]] timing_summary.rpt]
close_project
