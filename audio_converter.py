import os
from pathlib import Path
import click
from typing import Dict
import ffmpeg
import logging

class AudioConverter:
    # Supported input formats
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.mp4']
    
    def __init__(self, input_file: str, output_dir: str = "output"):
        """Initialize the audio converter.
        
        Args:
            input_file: Path to the input file (supported formats: mp4, mp3, wav, m4a, aac, ogg, flac)
            output_dir: Directory to save the output files (default: "output")
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.input_path = Path(input_file).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
            
        if self.input_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {self.input_path.suffix}. "
                f"Supported formats are: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        # Store file type for format-specific handling
        self.is_video = self.input_path.suffix.lower() == '.mp4'
    
    def _get_media_info(self) -> Dict:
        """Get audio/video information using ffmpeg."""
        try:
            probe = ffmpeg.probe(str(self.input_path))
            
            # For MP4, also show video info if available
            if self.is_video:
                streams_info = {
                    'audio': next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None),
                    'video': next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
                }
                
                if streams_info['video']:
                    self.logger.info("Video information:")
                    self.logger.info(f"  Resolution: {streams_info['video'].get('width', 'unknown')}x{streams_info['video'].get('height', 'unknown')}")
                    self.logger.info(f"  Duration: {probe.get('format', {}).get('duration', 'unknown')} seconds")
                    self.logger.info(f"  Bitrate: {int(probe.get('format', {}).get('bit_rate', 0)) // 1000} kbps")
                
                return streams_info['audio'] if streams_info['audio'] else {}
            
            # For non-video files, just get audio info
            return next(s for s in probe['streams'] if s['codec_type'] == 'audio')
            
        except ffmpeg.Error as e:
            self.logger.error(f"Error reading media info: {e.stderr.decode() if hasattr(e, 'stderr') else str(e)}")
            raise

    def _convert_to_wav(self, output_path: Path) -> None:
        """Convert media to WAV format using ffmpeg."""
        try:
            # Prepare ffmpeg command
            stream = ffmpeg.input(str(self.input_path))
            
            # For video files, we need to specify that we only want audio
            if self.is_video:
                self.logger.info("Extracting and converting audio from video...")
                stream = stream.audio
            else:
                self.logger.info("Converting audio...")
            
            # Set up the output with our required parameters
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec='pcm_s16le',  # 16-bit PCM
                ac=1,                # mono
                ar=16000,            # 16kHz
                loglevel='error',    # Reduce ffmpeg output
                y=None              # Overwrite output file if exists
            )
            
            # Run the conversion
            self.logger.info("Processing audio to speech recognition format...")
            stream.run(capture_stdout=True, capture_stderr=True)
            self.logger.info(f"Converted to: {output_path}")
            
        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if hasattr(e, 'stderr') else str(e)
            self.logger.error(f"FFmpeg error: {error_message}")
            raise Exception(f"Audio conversion failed: {error_message}")

    def process(self) -> str:
        """Process the input file: extract audio and convert to WAV.
        
        Returns:
            Path to the final WAV file
        """
        output_path = self.output_dir / "output.wav"
        
        self.logger.info(f"Processing file: {self.input_path}")
        self.logger.info(f"Input format: {self.input_path.suffix}")
        
        try:
            # Get media information
            audio_info = self._get_media_info()
            if audio_info:
                self.logger.info("Audio information:")
                self.logger.info(f"  Codec: {audio_info.get('codec_name', 'unknown')}")
                self.logger.info(f"  Sample rate: {audio_info.get('sample_rate', 'unknown')} Hz")
                self.logger.info(f"  Channels: {audio_info.get('channels', 'unknown')}")
                self.logger.info(f"  Bit rate: {int(audio_info.get('bit_rate', 0)) // 1000} kbps")
        except Exception as e:
            self.logger.warning(f"Could not get media info: {e}")
        
        # Convert to WAV format
        self._convert_to_wav(output_path)
        
        return str(output_path)

@click.command()
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.option('--output-dir', default='output', help='Directory to save the output files')
@click.option('--list-formats', is_flag=True, help='List supported audio formats')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose (DEBUG) logging')
@click.option('--quiet', '-q', is_flag=True, help='Suppress informational (INFO) logging')
def main(input_file: str, output_dir: str, list_formats: bool, verbose: bool, quiet: bool):
    """Convert audio/video files to WAV format suitable for speech recognition.
    
    This utility can handle various audio and video formats and convert them to a standardized WAV format:
    - Mono channel
    - 16kHz sample rate
    - 16-bit PCM encoding
    
    For video files (MP4):
    - Automatically extracts audio track
    - Shows video information (resolution, duration, bitrate)
    - Optimizes conversion for speech recognition
    
    Supported input formats: MP3, WAV, M4A, AAC, OGG, FLAC, MP4 (video)
    """
    if list_formats:
        click.echo("Supported input formats:")
        for fmt in AudioConverter.SUPPORTED_FORMATS:
            click.echo(f"  {fmt}")
        return

    if not input_file:
        click.echo("Error: INPUT_FILE is required unless --list-formats is used.", err=True)
        # Show help message
        context = click.get_current_context()
        click.echo(context.get_help())
        context.exit(1)

    # Configure logging
    log_level = logging.INFO
    if verbose:
        log_level = logging.DEBUG
    if quiet:
        log_level = logging.WARNING
    
    logging.basicConfig(
        level=log_level,
        format='%(levelname)-8s %(message)s'
    )
        
    try:
        converter = AudioConverter(input_file, output_dir)
        output_path = converter.process()
        logging.info(f"Success! Final WAV file: {output_path}")
        logging.info("The WAV file is now ready for speech recognition.")
    except Exception as e:
        logging.error(f"Operation failed: {str(e)}", exc_info=verbose)
        raise click.Abort()

if __name__ == "__main__":
    main()