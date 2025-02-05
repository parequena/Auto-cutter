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

# Imports
import os
import glob
import yt_dlp # Just checks if yt-dlp is installed
import argparse
import auto_editor # Just checks if auto-editor is installed
from pathlib import Path
from subprocess import run

############################################################
## Variables
############################################################
video_extensions = ["mkv", "mp4"] # Extend!

############################################################
## Counts files in path
############################################################
def count_files(path):
   n_files = 0

   for ext in video_extensions:
      n_files += len(glob.glob("*." + ext, root_dir=path))

   return n_files

############################################################
## Edits one video
############################################################
def edit_video(name, name_out):
   cmd = [
        ["-q", ""]
      , ["-c:v", "hevc_nvenc" ]
      , ["-b:v", "100M" ]
      , ["-b:a", "10M" ]
      , ["--no-open", ""]
      , ["--edit", "(or audio:stream=0 audio:threshold=-6dB, audio:stream=1)"]
      , ["--margin", "0.6s,0.7sec"]
      , ["-o", name_out]
   ]

   run(["auto-editor" + name] + cmd)

   return

############################################################
## Calls auto-editor in all files from input file
############################################################
def auto_edit(input_folder, output_folder):
   if not os.path.exists(output_folder):
      print("Creating output directory: " + output_folder)
      os.makedirs(output_folder)
   
   n_files = count_files(input_folder)
   print("There are " + str(n_files) + " in input folder: " + input_folder)
   
   return

############################################################
## Main function
############################################################
def main():
   out_string = "_out"
   input_folder = "folder"
   output_folder = input_folder + out_string

   parser = argparse.ArgumentParser(description="Auto cutter python script, used to call auto-editor in a folder.")

   parser.add_argument("-i", "--input_folder", nargs="?", help="Input Auto-Editor Folder", default=input_folder)
   parser.add_argument("-o", "--output_folder", nargs="?", help="Output Auto-Editor Folder", default=output_folder)

   args = parser.parse_args()
   input_folder = args.input_folder
   
   if args.output_folder is not None:
      output_folder = args.output_folder
   else:
      output_folder = input_folder + out_string

   print("Input: " + input_folder)
   print("Output: " + output_folder)
   
   auto_edit(input_folder=input_folder, output_folder=output_folder)

   return


if __name__ == '__main__':
   main()
