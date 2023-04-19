import os
import re
import subprocess

print("Very basic GoPro File Sort-and-Concatinator")
# Written using ChatGPT, a lot of fiddling to get it to kinda work, then me polishing the turd
print("Operates in current working directory & assumes FFMPEG is available in your path")

video_files = os.listdir('.')

primary_segments = sorted([x for x in video_files if re.search(r'^GOPR\d+\.MP4$', x)])
secondary_segments = sorted([x for x in video_files if re.search(r'^GP\d+\.MP4$', x)])


# Create a new file to write the sorted filenames to
with open("sorted_files.txt", "w") as f:

	for i, primary_file in enumerate(primary_segments):
		print(f"Primary Segment {i+1}")
		print(primary_file)
		# Write the primary segment file name to the output file
		f.write("file\t" + primary_file + "\n")
		primary_segment_num = int(re.search(r'^GOPR(\d+)\.MP4$', primary_file).group(1))
		matching_secondary_segments = sorted([x for x in secondary_segments if primary_segment_num == int(re.search(r'^GP\d+(\d{4})\.MP4$', x).group(1)[:4])])
		print("Matched Secondary segments")
		for secondary_file in matching_secondary_segments:
			print(secondary_file)
			# Write the secondary segment filenames to output file
			f.write("file\t" + secondary_file + "\n")

print("List Complete...")
outputname = input("Please enter filename for joined output: ")
# Call FFMPEG using the sorted_files filename as a source and outputing to outputname
subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', 'sorted_files.txt', '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', outputname ])
