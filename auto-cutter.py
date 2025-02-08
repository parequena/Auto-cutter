# Auto-cutter.py
# Made by: Pablo Requena
# If you want to get in touch with me, here are my social networks
#     - Twitter :    https://x.com/conPdePABLO
#     - BlueSky :    https://bsky.app/profile/theapoca.bsky.social
#     - Youtube :    https://www.youtube.com/@conpdepab
#     - Instagram :  https://www.instagram.com/conpdepab/
#     - LinkedIn :   https://www.linkedin.com/in/parequena/

# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <https://unlicense.org>

# Usefull commands
# Convert to mp4
#     ffmpeg -i <INPUT> -map 0:v -map 0:a:0 -map 0:a:1 -c:v copy -c:a copy -disposition:a:0 default -disposition:a:1 default <OUTPUT>
# Download best video/audio in mp4
#     yt-dlp -f bv[ext=mp4]+ba[ext=mp4] <VIDEO_URL>
# Download best audio in mp3
#     yt-dlp -f ba[ext=mp4] -x --audio-format mp3 <VIDEO_URL>
# Small video for testing
#     https://www.youtube.com/watch?v=P38h4lQNJPQ

# Imports
import os
import glob
import yt_dlp # Just checks if yt-dlp is installed
import argparse
import auto_editor # Just checks if auto-editor is installed
from pathlib import Path
from subprocess import run

##########################################################################################
## Variables
##########################################################################################
video_extensions = ["mkv", "mp4"] # Extend!
default_folder="folder"
out_string = "_out"
ae_cmd = ["-q", "--no-open", "-c:v", "auto", "-b:v", "10M", "-b:a", "10M"]
yt_cmd = ["-q", "-f", "bv[ext=mp4]+ba[ext=mp4]"]

##########################################################################################
## Counts files in path with video_extensions extensions
##
## \return n_files : Number of files containing those extensions
##########################################################################################
def count_files(path):
   n_files = 0

   for ext in video_extensions:
      n_files += len(glob.glob("*." + ext, root_dir=path))

   return n_files



##########################################################################################
## Get's all files from path with video_extension extensions
##
## \return fileNames : List of file names containing those extensions
##########################################################################################
def get_fileNames(path):
   fileNames = []

   for ext in video_extensions:
      files = glob.glob("*." + ext, root_dir=path)

      for file in files:
         fileNames += [file]

   return fileNames



##########################################################################################
## Creates a path if doen't exist
##########################################################################################
def create_path(path):
   if not os.path.exists(path):
      print("Creating directory: " + path)
      os.makedirs(path)
   
   return 



##########################################################################################
## Calls a subprocess to call yt-dlp with some parameters
##########################################################################################
def call_yt_dlp(video, output_folder):
   global yt_cmd
   
   create_path(output_folder)

   # print("Calling: ", ["yt-dlp", video] + yt_cmd)
   run(["yt-dlp", video] + yt_cmd, cwd=output_folder)

   return



##########################################################################################
## Calls a subprocess to call auto-editor with some parameters
##########################################################################################
def call_auto_editor(name, name_out):
   global ae_cmd

   ae_cmd += ["-o", name_out]

   # print("Calling: ", ["auto-editor", name] + ae_cmd)
   run(["auto-editor", name] + ae_cmd)

   return



##########################################################################################
## Gets input and output file names based on the original name
##
## \return in_file : Input file name (should be equal than original_name)
## \return out_file : Output file name (should be same than in_file but with out_string
##                    before extension)
##########################################################################################
def get_editor_file_names(original_name):
   name, ext = os.path.splitext(original_name)
   in_file = name + ext
   out_file = name + out_string + ext

   return in_file, out_file



##########################################################################################
## Calls auto-editor with only one file
##########################################################################################
def edit_video(fileName):
   in_file, out_file = get_editor_file_names(fileName)
   call_auto_editor(in_file, out_file)

   return



##########################################################################################
## Iterates on a folder to call auto-editor with all files that contains that folder
##########################################################################################
def edit_folder(input_folder, output_folder):
   create_path(output_folder)
   
   n_files = count_files(input_folder)
   print("There are " + str(n_files) + " in input folder: " + input_folder)

   fileNames = get_fileNames(input_folder)
   for file in fileNames:
      in_file, out_file = get_editor_file_names(file)
      file_path_in = input_folder + '/' + in_file
      file_path_out = output_folder + '/' + out_file

      call_auto_editor(file_path_in, file_path_out)
   
   return



##########################################################################################
## TODO
##########################################################################################
def auto_editor_arg_parser(args):
   global ae_cmd

   print("Prev")
   print(ae_cmd)
   ae_cmd = args
   
   print("Post")
   print(ae_cmd)
   
   return



##########################################################################################
## Main function
##########################################################################################
def main():
   # Create argument parser
   parser = argparse.ArgumentParser(
      description="Auto cutter python script, used to call auto-editor in a folder."
      )

   # Create parameters
   parser.add_argument("video", nargs='?', help="Input video or playlist to edit/download", default=None)
   parser.add_argument("-f", "--folder", nargs='?', help="Folder to work with", default=None)
   # parser.add_argument("-ae", "--auto_editor_args", nargs='+', help="Arguments to pass to auto-editor.  Use quotes to group multiple arguments, e.g., '-q --no-open'", default=ae_cmd)

   # Parse arguments
   args = parser.parse_args()
   input_folder = args.folder
   if input_folder is None:
      input_folder = default_folder
   output_folder = input_folder + out_string
   video = args.video
   # auto_editor_arg_parser(args.auto_editor_args)

   print("We currently support [" + ", ".join(video_extensions) + "] video extensions, skipping others!")
   
   if video is not None:
      if video.startswith(("https:", "http:", "www")):
         call_yt_dlp(video, input_folder)
         edit_folder(input_folder, output_folder)
      else:
         edit_video(video)
   else:
      edit_folder(input_folder, output_folder)

   return


if __name__ == '__main__':
   main()
