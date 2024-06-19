import argparse
import logging
from pathlib import Path

import whisper
#import mlx_whisper
from summarization import SummarizationFactory


def setup_logging(verbose=False):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    return logger

def transcribe_audio(audio_file_path, logger):
    logger.info("Starting audio transcription...")
    model = whisper.load_model("medium.en")
    result = model.transcribe(str(audio_file_path)) 
    # result = mlx_whisper.transcribe(
    #     str(audio_file_path), 
    #     path_or_hf_repo="mlx-community/whisper-medium.en-mlx-8bit",
    #     verbose=True
    # )
    logger.debug(f"Transcription result: {result}")
    logger.info("Transcription completed.")
    return result["text"]


def meeting_minutes(summarizer, logger):
    logger.info("Running meeting_minutes function...")
   
    abstract_summary = summarizer.prompt("abstract_summary")
    logger.debug("Abstract Summary extracted.")
   
    key_points = summarizer.prompt("key_points")
    logger.debug("Key Points extracted.")
    
    action_items = summarizer.prompt("action_items")
    logger.debug("Action Items extracted.")
    
    key_quotes = summarizer.prompt("key_quotes")
    logger.debug("Key Quotes extracted.")
    
    sentiment = summarizer.prompt("sentiment_analysis")
    logger.debug("Sentiment Analysis completed.")
    
    return {
        "abstract_summary": abstract_summary,
        "key_points": key_points,
        "action_items": action_items,
        "key_quotes": key_quotes,
        "sentiment_analysis": sentiment,
    }


def save_as_markdown(minutes, md_file_path, logger):
    logger.info("Saving meeting minutes as markdown...")
    with open(md_file_path, "w") as md_file:
        md_file.write(f"# Abstract Summary\n\n{minutes['abstract_summary']}\n\n")
        md_file.write(f"## Key Points\n\n{minutes['key_points']}\n\n")
        md_file.write(f"## Action Items\n\n{minutes['action_items']}\n\n")
        md_file.write(f"## Key Quotes\n\n{minutes['key_quotes']}\n\n")
        md_file.write(f"## Sentiment Analysis\n\n{minutes['sentiment_analysis']}\n\n")
    logger.info(f"Meeting minutes saved to {md_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe and summarize meeting audio files."
    )
    parser.add_argument(
        "--audio-path",
        required=True,
        type=str,
        help="Relative path to the audio file from project root",)
    parser.add_argument(
        "--force-transcribe",
        action="store_true",
        help="Force transcription step even if an existing transcript is found.",)
    parser.add_argument(
        "--persona",
        type=str,
        choices=personas.keys(),
        default="default",
        help="Choose a persona for the AI analysis. Default is 'default'.",)
    parser.add_argument(
        "--summarizer", 
        type=str, 
        default="openai",
        help="Type of AI model to run the summarization operations")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging for debugging purposes.",)

    args = parser.parse_args()

    logger = setup_logging(args.verbose)
    audio_path = Path(args.audio_path)
    project_root = audio_path.parent.parent
    summarizer_type = args.summarizer
    force_transcription = args.force_transcribe 
    persona = args.persona

    if not audio_path.exists():
        logger.error("The specified audio file does not exist.")
        return

    transcript_folder = project_root / "transcript" 
    transcript_folder.mkdir(parents=True, exist_ok=True)
    text_file_name = audio_path.stem + ".txt"
    text_file_path = transcript_folder / text_file_name

    if force_transcription or not text_file_path.exists():
        logger.debug(f"Trascript Not Found at -- {text_file_path}")
        logger.info("Transcribing audio...")
        transcribed_text = transcribe_audio(audio_path, logger)

        with open(text_file_path, "w") as file:
            file.write(transcribed_text)
        logger.info(f"Transcription saved to {text_file_path}")

    else:
        logger.info(f"Using existing transcription found at {text_file_path}")
        with open(text_file_path, "r") as file:
            transcribed_text = file.read()

    summary_folder = project_root / "summary"
    summary_folder.mkdir(parents=True, exist_ok=True)
    md_file_name = audio_path.stem + "." + summarizer_type + ".md"
    md_file_path = summary_folder / md_file_name

    summarizer = SummarizationFactory.get_summarizer(summarizer_type, logger)
    summarizer.persona = persona
    summarizer.transcript = transcribed_text

    minutes = meeting_minutes(summarizer, logger)
    save_as_markdown(minutes, md_file_path, logger)

    # what did that just cost?
    print(summarizer.expense())

if __name__ == "__main__":
    main()