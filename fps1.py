# Import everything needed to edit video clips
from moviepy.editor import *

# loading video gfg
clip = VideoFileClip("Nihira.mp4")


new_clip = clip.set_fps(2)
# new clip with new fps
# new_clip = clip.set_fps(100)
# count = clip.fps
# print(count)
new_clip.write_videofile('new2.mp4')
