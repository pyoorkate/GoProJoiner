# GoProJoiner
Python script to sort GoPro/SJCAM files into the correct order and join them together so that you have all the chapters either a single file (in the correct order) or into individual segments for each camera start. For GoPros, this uses the filenaming convention to detect order, so it isn't thrown by camera date/time issues, or time-stamping issues caused by copying files.

For SJCAMs (I only have a Pro8 so it uses that file name convention) then it uses exiftools to extract the timestamp and the file duration. If there's a greater than two second gap between the start+duration and the start of the next file it assumes this is a new chapter.

It operates in current working directory & assumes FFMPEG and EXIFTOOLS are available in your path; it will attempt to make a directory for you if you ask it to output to a directory that doesn't exist.
It currently performs no error checking to confirm it's not going to overwrite files in the output directory.
It currently performs no error checking to confirm it's not going to append data to existing "sorted_file.txt" / "sorted_files.txt". If those files do exist in the folder it's going to result in FFMPEG errors.

I take no responsibilty for any horrific things this does.

Don't expect me to ever do anything else with it unless it breaks for me.
