# AI Meeting Transcription and Analysis Tool

This Python application leverages the power of OpenAI's Whisper and GPT models, as well as Anthropic's Claude model, to transcribe and analyze meeting audio recordings. The tool provides valuable insights by generating a summary, extracting key points, identifying action items, highlighting key quotes, and performing sentiment analysis on the meeting content.

## Features

- Transcribe audio recordings using OpenAI's Whisper or Apple's mlx-whisper library
- Analyze transcriptions using OpenAI's GPT-4o model or Anthropic's Claude model
- Generate a comprehensive meeting summary in Markdown format
- Extract key points, action items, and key quotes from the meeting
- Perform sentiment analysis on the meeting content
- Estimate the cost of using each AI model based on token usage

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-meeting-tool.git
   ```

2. Install the required Whisper dependencies (which include `ffmpeg`):
   * option 1 - follow the [Setup](https://github.com/openai/whisper?tab=readme-ov-file#setup) section of the OpenAI Whisper Python Library
   * option 2 - if you are on Apple Silicon, follow the [Setup](https://github.com/ml-explore/mlx-examples/tree/main/whisper#setup) section of the Apple MLX Whisper Python Library
     * if you follow this option, modify lines [7 and 8](app/main.py#L7), and lines [23 - 29](app/main.py#L23) of `main.py` to switch between the OpenAI interface and the MLX interface. 

3. Install the OpenAI and Anthropic Python Libraries
   ```
   pip install openai
   pip install anthropic
   ```

4. Set up your OpenAI and Anthropic API keys:
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   ```
   If you do not yet have keys, follow the instructions here for [OpenAI](https://platform.openai.com/docs/quickstart) and for [Anthropic](https://docs.anthropic.com/en/docs/getting-access-to-claude) to gain access. 


## Project Structure

The application assumes the following directory structure for your audio analysis. 

```
your-project/
│
├── audio/
│   └── your-audio-file.mp3
│
├── summary/
│   ├── your-audio-file.openai.md
│   └── your-audio-file.anthropic.md
│
├── transcript/
    └── your-audio-file.txt
```

- `audio/`: Place your input audio files (e.g., MP3 or WAV) in this directory.
- `summary/`: The generated meeting summaries will be saved as Markdown files in this directory. The file names will include the name of the audio file and the AI model used for analysis (e.g., `your-audio-file.openai.md` or `your-audio-file.anthropic.md`).
- `transcript/`: The transcribed text from the audio files will be saved as plain text files in this directory.

Make sure to follow this directory structure when setting up your project. Place your audio files in the `audio/` directory, and the application will generate the corresponding transcripts in the `transcript/` directory and the meeting summaries in the `summary/` directory. 


## Usage

1. After placing your meeting audio file in the `audio` directory as described above, move to step 2. 

2. Run the application with the desired AI model:
   ```
   python app/main.py --audio-path project/audio/meeting-recording.mp3 --summarizer openai
   ```
   Replace `project/audio/meeting-recording.mp3` with the actual path to your audio file, and choose either `openai` or `anthropic` for the `--summarizer` option.

3. The application will transcribe the audio using Whisper and analyze the transcription using the selected AI model. The generated meeting summary will be saved as a Markdown file in the `summary` directory.

## Configuration Options

- `--audio-path`: Path to the audio file to be transcribed and analyzed (required).
- `--summarizer`: AI model to use for analysis. Options: `openai` or `anthropic` (default: `openai`).
- `--force-transcribe`: Force re-transcription of the audio file, even if a transcription already exists (optional).
- `--persona`: Choose a persona for the AI analysis. Options: `default`, `analyst`, `pragmatist`, `optomist`, `skeptic`, or `visionary` (default: `default`).
- `--verbose`: Enable verbose logging for debugging purposes (optional).

## Customization

You can customize the analysis prompts and personas by modifying the `prompts.py` file. Add or remove prompts to tailor the analysis to your specific needs. Additionally, you can create new personas to adjust the tone and focus of the AI-generated summaries.

## Example

To help you get started and understand the outputs generated by the AI meeting transcription and analysis tool, there is an included example folder in this repository. The example folder contains a real-world meeting audio recording, as well as the the corresponding transcript and AI-generated summaries of this meeting.

### Audio Source

The audio file used in this example is a recording of a [Seattle City Council meeting from March of 1977](https://www.digitalarchives.wa.gov/Record/View/5F0FE850787E245429B1F5AB422E0C95). The original recording is stored on the Washington State Archives - Digital Archives website. This audio file is used for demonstration purposes only.

### Example Contents
By exploring the example folder, you can get a better understanding of the tool's output format and the level of insight and analysis provided by the different AI models. Feel free to compare the summaries generated by OpenAI ([summary](example/summary/19770328.full-city-council.openai.md)) and Anthropic ([summary](example/summary/19770328.full-city-council.anthropic.md)) to see which one best suits your needs. Please note that the example meeting recording and its associated outputs are provided for illustrative purposes only and may not reflect the specific nature or content of your own meetings.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

