#python PyDicomStreamli.py -i /home/warmachine/codes/AI-Medical-Scan-Reader/testfiles/series-00000/ -o output_video.mp4 -r 24 -w 1920 -H 1080 -O
import argparse
import os
import tempfile
from pathlib import Path
from PIL import Image
import ffmpeg
import pydicom

def join(separator, *args):
    return separator.join(args)

def dicom_to_image(input_file, output_file):
    """
    Convert a DICOM file to a standard image format.
    """
    ds = pydicom.dcmread(input_file)  # Load the DICOM file
    pixel_array = ds.pixel_array  # Extract pixel data

    # Normalize pixel values to 8-bit (0-255)
    image = Image.fromarray((pixel_array / pixel_array.max() * 255).astype('uint8'))
    image = image.convert("RGB")  # Ensure compatibility
    image.save(output_file)

def find_largest_dimensions(file_list):
    """
    Determine the largest width and height from a list of images.
    """
    max_width, max_height = 0, 0
    for file in file_list:
        with Image.open(file) as img:
            width, height = img.size
            max_width = max(max_width, width)
            max_height = max(max_height, height)
    return max_width, max_height

def convert_dicom_to_images(input_files, tempdir):
    """
    Convert DICOM files to images and save them as PPM.
    """
    image_files = []
    for i, input_file in enumerate(input_files):
        image_file = tempdir / f"frame_{i:06d}.png"
        dicom_to_image(input_file, image_file)
        image_files.append(image_file)
    return image_files

def create_video_with_ffmpeg(image_files, output_file, rate, width, height):
    """
    Use FFmpeg to create a video from the processed image files.
    """
    input_pattern = str(image_files[0].parent / "frame_%06d.png")
    ffmpeg.input(input_pattern, framerate=rate).output(
        str(output_file),
        vf=f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        pix_fmt="yuv420p"
    ).run(overwrite_output=True)

def main():
    parser = argparse.ArgumentParser(description="Convert DICOM files to a video.")
    parser.add_argument("-i", "--input", required=True, help="Input folder containing DICOM files")
    parser.add_argument("-o", "--output", default="result.mp4", help="Output video file")
    parser.add_argument("-r", "--rate", type=int, default=12, help="Frame rate for the video")
    parser.add_argument("-w", "--width", type=int, help="Width of the video frames")
    parser.add_argument("-H", "--height", type=int, help="Height of the video frames")
    parser.add_argument("-O", "--overwrite", action="store_true", help="Overwrite output file if it exists")
    args = parser.parse_args()

    input_folder = Path(args.input)
    output_file = Path(args.output)

    # Check if output file exists
    if output_file.exists() and not args.overwrite:
        raise FileExistsError(f"Output file already exists: {output_file}")

    # Find all input DICOM files
    input_files = sorted(input_folder.glob("*.dcm"))
    if not input_files:
        raise FileNotFoundError(f"No DICOM files found in input folder: {input_folder}")

    print(f"Found {len(input_files)} DICOM frames")

    # Use temporary directory to store intermediate images
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)
        print("Converting DICOM files to images...")
        image_files = convert_dicom_to_images(input_files, tempdir_path)

        # Determine scaling dimensions
        if not args.width or not args.height:
            width, height = find_largest_dimensions(image_files)
            print(f"Calculated scale dimensions: {width}x{height}")
        else:
            width, height = args.width, args.height

        print("Creating video with FFmpeg...")
        create_video_with_ffmpeg(image_files, output_file, args.rate, width, height)

    print(f"Video saved successfully as: {output_file}")

if __name__ == "__main__":
    main()
