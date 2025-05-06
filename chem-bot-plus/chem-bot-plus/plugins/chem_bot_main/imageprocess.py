from PIL import Image,ImageSequence
import os
def image_symmetrize(file_path:str,direction:str)->str:
	with Image.open(file_path) as img:
		file_name = os.path.basename(file_path)
		file_dir=os.path.dirname(file_path)
		file_name_without_extension, file_extension = os.path.splitext(file_name)
		if img.format=='GIF':
			file2=file_dir+'\\'+file_name_without_extension+'.'+direction+file_extension
			frames=[frame.copy() for frame in ImageSequence.Iterator(img)]
			new_frames:list[Image.Image]=[]
			for frame in frames:
				new_frame=_frame_symmetrize(frame,direction)
				new_frames.append(new_frame)
			new_frames[0].save(file2,'GIF',save_all=True,append_images=new_frames[1:],loop=0)
			return file2
		else:
			img2=_frame_symmetrize(img,direction)
			file2=file_dir+'\\'+file_name_without_extension+'.'+direction+file_extension
			img2.save(file2)
			return file2

def _frame_symmetrize(img:Image.Image,direction:str):
	source=(0,0,0,0)
	target=(0,0,0,0)
	type=Image.Transpose.FLIP_LEFT_RIGHT
	if direction=='左':
		source=(0,0,img.width//2,img.height)
		target=(img.width-img.width//2,0,img.width,img.height)
		type=Image.Transpose.FLIP_LEFT_RIGHT
	elif direction=='右':
		source=(img.width//2,0,img.width,img.height)
		target=(0,0,img.width-img.width//2,img.height)
		type=Image.Transpose.FLIP_LEFT_RIGHT
	elif direction=='上':
		source=(0,0,img.width,img.height//2)
		target=(0,img.height-img.height//2,img.width,img.height)
		type=Image.Transpose.FLIP_TOP_BOTTOM
	elif direction=='下':
		source=(0,img.height//2,img.width,img.height)
		target=(0,0,img.width,img.height-img.height//2)
		type=Image.Transpose.FLIP_TOP_BOTTOM
	img2=img.copy()
	img2.paste(img.crop(source).transpose(type),target)
	return img2
