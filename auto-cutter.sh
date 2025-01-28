#!/bin/bash

# Variables
k_script_name=$(basename "$0")
k_auto_mode=0
k_edit_mode=0
k_in_path="in"
k_out_path="${k_in_path}_out"
k_video_extensions=("mkv" "mp4" "avi" "mov" "flv" "webm")
k_file_count=0

############################################################
## Prints help
############################################################
function print_help()
{
   echo -e "----------------------------------"
   echo -e "Usage: ./${k_script_name} [-i] <input_path> [-o] <output_path>"
   echo -e "----------------------------------"
   echo -e "This is \033[31m${k_script_name}\033[0m help!"
   echo -e "-h \t Prints this help"
   echo -e ""
   echo -e "-i \t Input edit video folder, default=\033[36m${k_in_path}\033[0m"
   echo -e "-o \t Ouput edited video folder, default=\033[36m${k_out_path}\033[0m"
   echo -e ""
}

############################################################
## Counts files in k_in_path
# TODO: Add path to a variable
############################################################
function count_files()
{
   find_command="find \"${k_in_path}\" -maxdepth 1 -type f " # Lets find how many k_video_extensions file do we have
   for ext in "${k_video_extensions[@]}"; do
      find_command+="\( -iname \"*.${ext}\" \)"
      if [[ "$ext" != "${k_video_extensions[-1]}" ]]; then
         find_command+=" -o " 
      fi
   done
   k_file_count=$(eval "$find_command" | wc -l) # Execute find ... | wc -l
}

############################################################
## Calls auto-editor in all files that k_in_path contains
############################################################
function auto_edit()
{
   # Check that auto-editor is installed
   if ! command -v auto-editor &> /dev/null; then
      echo -e "auto-editor is not installed, it is required for this execution"
      return 1
   fi

   # Check that out path exists
   echo -e "Output path: \033[36m${k_out_path}\033[0m"
   if [[ ! -d "${k_out_path}" ]]; then
      mkdir -p ${k_out_path}
   fi

   # Count files in in_path
   count_files

   # Prints info
   echo -e "Processing \033[33m${k_file_count}\033[0m files"
   local n_file=0

   # Iterate on all files
   ls -1 ${k_in_path} |
   while read -r file; do
      local found=0
      # If is part of k_video_extensions extensions.
      for ext in "${k_video_extensions[@]}"; do
         if [[ "$file" == *".$ext" ]]; then
            found=1
            break 
         fi
      done

      if [[ $found -eq 0 ]]; then 
         continue 
      fi

      ((n_file++))
      echo -e "File ${n_file} from ${k_file_count}"

      file_name="${file%.*}"
      file_out="${file_name}_OUT.${file##*.}"
      # Call auto-editor
      auto-editor "${k_in_path}/${file}" -q -c:v hevc_nvenc -b:v 100M -b:a 10M --no-open -o "${k_out_path}/${file_out}"
   done

   return 0
}

############################################################
## Main function
############################################################
function main()
{
   while getopts ":hi:o:" opt; do
      case $opt in
         h)
            print_help
            return 0
         ;;

         i)
            k_in_path=$OPTARG
            k_out_path="${k_in_path}_out"
         ;;

         o)
            k_out_path=$OPTARG
         ;;

         \?)
            echo "Invalid option: -$OPTARG" >&2
            return 1
         ;;
      esac
   done

   auto_edit
   return $?
}

# Checks if at least 1 parameter it's used
if [ $# -lt 1 ]; then
   print_help
   exit 1
else
   main "$@"
fi
