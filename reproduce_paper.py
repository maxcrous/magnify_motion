from motion_magnify import motion_magnify

# files can be found at http://people.csail.mit.edu/mrub/evm/#code
# baby1
print('baby1')
motion_magnify(video_path='videos/input/baby1.mp4',
               output_path='videos/output/baby1.mp4',
               motion=True,
               alpha=20,
               filter_type='iir',
               r_low=0.05,
               r_high=0.4,
               lambda_c=16)


# baby2
print('baby2')
motion_magnify(video_path='videos/input/baby2.mp4',
               output_path='videos/output/baby2.mp4',
               motion=False,
               alpha=150,
               filter_type='ideal',
               low=140/60,
               high=160/60,
               max_layer=5)

# camera
print('camera')
motion_magnify(video_path='videos/input/camera.mp4',
               output_path='videos/output/camera.mp4',
               motion=True,
               alpha=150,
               filter_type='butter',
               low=45,
               high=100,
               fps=300,
               lambda_c=20)

# subway
print('subway')
motion_magnify(video_path='videos/input/subway.mp4',
               output_path='videos/output/subway.mp4',
               motion=True,
               alpha=60,
               filter_type='butter',
               low=3.6,
               high=6.2,
               lambda_c=90,
               fps=30)

# wrist
print('wrist')
motion_magnify(video_path='videos/input/wrist.mp4',
               output_path='videos/output/wrist.mp4',
               motion=True,
               alpha=10,
               filter_type='iir',
               r_low=0.05,
               r_high=0.4,
               lambda_c=16)

# shadow
print('shadow')
motion_magnify(video_path='videos/input/shadow.mp4',
               output_path='videos/output/shadow.mp4',
               motion=True,
               alpha=5,
               filter_type='butter',
               low=0.5,
               high=10,
               lambda_c=5)

# guitar, amplify E
print('guitar, E')
motion_magnify(video_path='videos/input/guitar.mp4',
               output_path='videos/output/guitar_E.mp4',
               motion=True,
               alpha=50,
               filter_type='ideal',
               low=72,
               high=92,
               fps=600,
               lambda_c=10)

# guitar, amplify A
print('guitar, A')
motion_magnify(video_path='videos/input/guitar.mp4',
               output_path='videos/output/guitar_A.mp4',
               motion=True,
               alpha=100,
               filter_type='ideal',
               low=100,
               high=120,
               fps=600,
               lambda_c=10)

# face1
print('face1')
motion_magnify(video_path='videos/input/face1.mp4',
               output_path='videos/output/face1.mp4',
               motion=False,
               alpha=50,
               filter_type='ideal',
               low=50/60,
               high=60/60,
               max_layer=4,
               lambda_c=4)

# face2, motion
print('face2, motion')
motion_magnify(video_path='videos/input/face2.mp4',
               output_path='videos/output/face2_motion.mp4',
               motion=True,
               alpha=20,
               filter_type='butter',
               low=0.5,
               high=10,
               lambda_c=80)

# face2, color
print('face2, color')
motion_magnify(video_path='videos/input/face2.mp4',
               output_path='videos/output/face2_color.mp4',
               motion=False,
               alpha=50,
               filter_type='ideal',
               low=50/60,
               high=60/60,
               max_layer=6,
               lambda_c=50)


# face3
print('face3')
motion_magnify(video_path='videos/input/face3.mp4',
               output_path='videos/output/face3.mp4',
               motion=False,
               alpha=70,
               filter_type='ideal',
               low=0.9,
               high=1.1,
               max_layer=4)



