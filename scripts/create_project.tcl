# Recreate the source-managed Vivado project from this repository.
set script_dir [file normalize [file dirname [info script]]]
set repo_dir [file normalize [file join $script_dir ..]]
set build_dir [file normalize [file join $repo_dir build vivado]]
set part xc7z020clg400-2

file mkdir $build_dir
create_project acoustic_camera $build_dir -part $part -force

set_property ip_repo_paths [list \
    [file join $repo_dir ip_repo] \
    [file join $repo_dir hls_ip_repo calculate] \
    [file join $repo_dir hls_ip_repo delay] \
    [file join $repo_dir hls_ip_repo inter] \
    [file join $repo_dir hls_ip_repo vram_add]] [current_project]
update_ip_catalog

set src_root [file join $repo_dir srcs sources_1]
set bd_file [file join $src_root bd system system.bd]
add_files -norecurse $bd_file
add_files -norecurse [glob -nocomplain [file join $src_root imports rgb2dvi *.v]]
add_files -norecurse [glob -nocomplain [file join $src_root imports src *.v]]
add_files -norecurse [glob -nocomplain [file join $src_root ip * *.xci]]
add_files -fileset constrs_1 -norecurse \
    [file join $repo_dir srcs constrs_1 new ov5640_lcd.xdc]

generate_target all [get_files $bd_file]
set wrapper [make_wrapper -files [get_files $bd_file] -top]
add_files -norecurse $wrapper
set_property top system_wrapper [current_fileset]
update_compile_order -fileset sources_1
save_project_as -force acoustic_camera $build_dir
close_project
