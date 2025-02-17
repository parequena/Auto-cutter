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
# Quote flag
#     auto-editor https://youtu.be/nnmZC7DN_EA --yt-dlp-extras "-q"


# Imports
import os
import glob
import argparse
import auto_editor # Just checks if auto-editor is installed
from pathlib import Path
from subprocess import run
from yt_dlp import YoutubeDL

##########################################################################################
## Variables
##########################################################################################
video_extensions = ["mkv", "mp4"] # Extend!
default_folder="folder"
out_string = "_out"
ae_cmd = ["--no-open", "-c:v", "hevc_nvenc", "-b:v", "10M", "-b:a", "10M", "--margin", "0.6s,0.7sec"]
quiet_mode=False

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
## \return file_names : List of file names containing those extensions
##########################################################################################
def get_file_names(path):
   file_names = []

   for ext in video_extensions:
      files = glob.glob("*." + ext, root_dir=path)

      for file in files:
         file_names += [file]

   return file_names



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
   global quiet_mode

   create_path(output_folder)

   # Used https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py
   # TODO: Integrate this script to add yt-dlp params
   yt_opts = {
      'extract_flat': 'discard_in_playlist',
      'format': 'bv[ext=mp4]+ba[ext=mp4]', # Enabled best video/audio format for mp4
      'fragment_retries': 5,
      'ignoreerrors': 'only_download',
      'noprogress': quiet_mode,
      'outtmpl': { 'default': output_folder + '/%(title)s.%(ext)s' },
      'postprocessors': [{'key': 'FFmpegConcat',
                           'only_multi_video': True,
                           'when': 'playlist'}],
      'quiet': quiet_mode,
      'retries': 5
   }

   with YoutubeDL(yt_opts) as ydl:
      _ = ydl.download(video)

   return



##########################################################################################
## Calls a subprocess to call auto-editor with some parameters
##########################################################################################
def call_auto_editor(name, name_out):
   global ae_cmd
   global quiet_mode

   cmd = [name]
   cmd.extend(["-o", name_out])
   cmd.extend(ae_cmd)

   if quiet_mode:
      cmd.extend(["-q"])

   # print("Calling: ", ["auto-editor"] + cmd)
   run(["auto-editor"] + cmd)

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
def edit_video(file_name):
   in_file, out_file = get_editor_file_names(file_name)
   call_auto_editor(in_file, out_file)

   return



##########################################################################################
## Iterates on a folder to call auto-editor with all files that contains that folder
##########################################################################################
def edit_folder(input_folder, output_folder):
   create_path(output_folder)
   
   n_files = count_files(input_folder)
   print("There are " + str(n_files) + " in input folder: " + input_folder)

   file_names = get_file_names(input_folder)
   n_file = 1
   for file in file_names:
      in_file, out_file = get_editor_file_names(file)

      print("File " + str(n_file) + "/" + str(n_files) + "\tName: " + file)

      file_path_in = input_folder + '/' + in_file
      file_path_out = output_folder + '/' + out_file

      call_auto_editor(file_path_in, file_path_out)
      n_file += 1
   
   return



##########################################################################################
## Main function
##########################################################################################
def process_video(input_folder, output_folder, video=None):
   if video is not None:
      if video.startswith(("https:", "http:", "www")):
         print("Downloading videos, this could be long...")
         call_yt_dlp(video, input_folder)
         edit_folder(input_folder, output_folder)
      else:
         edit_video(video)
   else:
      edit_folder(input_folder, output_folder)

   return



##########################################################################################
## Main function
##########################################################################################
def main():
   global quiet_mode

   # Create argument parser
   parser = argparse.ArgumentParser(
      description="Auto cutter python script, used to call auto-editor in a folder."
      )

   # Create parameters
   parser.add_argument("video", nargs='?', help="Input video or playlist to edit/download", default=None)
   parser.add_argument("-f", "--folder", nargs='?', help="Folder to work with", default=None)
   parser.add_argument("-q", "--quiet", action="store_true", help="Enables quiet mode for yt_dlp and auto-editor", default=False)

   # Parse arguments
   args = parser.parse_args()

   # First, global parameters
   quiet_mode = args.quiet

   # Then, other parameters.
   input_folder = args.folder
   if input_folder is None:
      input_folder = default_folder

   print("We currently support [" + ", ".join(video_extensions) + "] video extensions, skipping others!")
   process_video(input_folder, input_folder + out_string, args.video)

   return


if __name__ == '__main__':
   main()
