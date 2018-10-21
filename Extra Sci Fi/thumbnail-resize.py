import os

# ffmpeg -i input.jpg -vf scale=320:240 output_320x240.jpg
# Bilibibli: 1146x717 

directory = "./"
for filename in os.listdir(directory):
    if filename.endswith(".jpg"): 
        infile = os.path.join(directory, filename)
        outfile = os.path.join(directory, filename[0:2]) + '_out.jpg'

        os.system('ffmpeg -y -i "' + infile + '" -vf scale=1146:717 ' + outfile)
        # print(outfile)
        # print(infile)
    else:
        continue