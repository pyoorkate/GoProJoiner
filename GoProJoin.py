import os
import re
import subprocess

print("Very basic GoPro File Sort-and-Concatinator\n")
# Written using ChatGPT, a lot of fiddling to get it to kinda work, then me polishing the turd
print("Operates in current working directory & assumes FFMPEG is available in your path\n\n")

video_files = os.listdir('.')

primary_segments = sorted([x for x in video_files if re.search(r'^GOPR\d+\.MP4$', x)])
secondary_segments = sorted([x for x in video_files if re.search(r'^GP\d+\.MP4$', x)])

# Identify whether the user wants all files combined together, or each camera start
# as a separate file
allasone = ""
print("Choose output type")
print("==================\n")
print("(A)ll as one file")
print("(I)ndividual files for each camera start\n")
allasone = input("Ouput type: ")

while allasone != "A" and allasone != "I":
	allasone = input("Ouput type (either A or I): ")


# Do they want to output to a different directory (just here because my friend's script was posher than mine)
# Get an output directory, if this is blank use the current working directory
output_directory = input("Output file directory (leave blank for current working directory): ")
if output_directory == "":
	output_directory = os.getcwd()

output_directory_exists = os.path.exists(output_directory)
if output_directory_exists == False:
	create_dir = input ("Directory does not exist. Create directory? (Y/N): ")
	while create_dir != "Y" and create_dir != "N":
		create_dir = input ("Directory does not exist. Create directory? (Y/N): ")

	if create_dir == "Y":
		# Okay then, I'll make the directory myself you lazy toad
		os.mkdir(output_directory)
	
	if create_dir == "N":
		# We could loop back and ask them a directory again, but...I can't be bothered.
		print ("Directory does not exist, user declined creation")
		print ("Program terminating")
		exit ()


if allasone == "A":
	print("The following files and segments have been located:/n")
	# Create a new file to write the sorted filenames to
	with open("sorted_files.txt", "w") as f:
		for i, primary_file in enumerate(primary_segments):
			print(f"Primary Segment {i+1}")
			print(primary_file)
			# Write the primary segment file name to the output file
			f.write("file\t" + primary_file + "\n")
			primary_segment_num = int(re.search(r'^GOPR(\d+)\.MP4$', primary_file).group(1))
			matching_secondary_segments = sorted([x for x in secondary_segments if primary_segment_num == int(re.search(r'^GP\d+(\d{4})\.MP4$', x).group(1)[:4])])
			print("Secondary segments")
			for secondary_file in matching_secondary_segments:
				print(secondary_file)
				# Write the secondary segment filenames to output file
				f.write("file\t" + secondary_file + "\n")

	print("List Complete...")
	outputname = input("Please enter filename for joined output: ")
	# join together yon filename and the path input earlier
	output_full_filename = os.path.join(output_directory, outputname)
	# Call FFMPEG using the full filename and directory for output
	subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', output_full_filename, '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', outputname ])
	print(f"Hopefully you have a file called {outputname} in {output_directory}. It should have all the files combined in one.")
	exit()

if allasone == "I":
	segmentcount = 0
	#we'll increment this counter for every file segment, that way when we get to writing the files we know how many.
	# Don't open file yet...because we need that to happen separately for each segment.
	print("The following files and segments have been located:/n")
	for i, primary_file in enumerate(primary_segments):
		segmentcount = segmentcount + 1
		print(f"Primary Segment {i+1}")
		print(primary_file)
		with open("sorted_file%s.txt" % i, "w") as f:
			# Write the primary segment file name to the output file
			f.write("file\t" + primary_file + "\n")
			primary_segment_num = int(re.search(r'^GOPR(\d+)\.MP4$', primary_file).group(1))
			matching_secondary_segments = sorted([x for x in secondary_segments if primary_segment_num == int(re.search(r'^GP\d+(\d{4})\.MP4$', x).group(1)[:4])])
			print("Secondary segments")
			for secondary_file in matching_secondary_segments:
				print(secondary_file)
				# Write the secondary segment filenames to output file
				f.write("file\t" + secondary_file + "\n")
		f.close()

	print("List Complete...")
	outputname = input("Please enter basename for joined output: ")
	# initiate loop to call FFMPEG
	# subtract one from segment count because the filenames start at 0, and segment count started at 1.
	# I could use another variable here, but why would I?
	segmentcount = segmentcount - 1
	while segmentcount > -1:
		# Munge together a filename containing the current segment and the all the other bits of the name
		current_segment_file = "sorted_files" + str(segmentcount) + ".txt"
		# join together yon filename and the path input earlier
		output_full_filename = os.path.join(output_directory, current_segment_file)
		print(f"Launching FFMPEG for " + output_full_filename )
		# Call FFMPEG using the sorted_files filename as a source and outputting to outputname
		subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', output_full_filename, '-c', 'copy', '-map', '0:0', '-map', '0:1', '-map', '0:3', outputname ])
		segmentcount = segmentcount - 1
		
		
	print(f"Tada! You have many files. You are truly blessed.")
	exit()
	
else:
	print("Uncaught error (I mean, I did tons of error checking, so this is totally unexpected... ;) )")
	exit()
	
