Video to Text & Summarization with Whisper and GPT-3
==============================

---

This is a machine learning project that uses OpenAI's Whisper and GPT-3 to transcribe and summarize spoken word from long audio files into much more consumable text summaries.
Demo notebook [here](https://github.com/fbcom/audio-to-text-summarizer/blob/main/notebooks/demo.ipynb).

## Why I Made This

---
I am an engineer, I like to improve things that bug me.

**The Problem**

```text 
I have too many long videos of lectures, talks, and podcasts
in my "watch later" playlists and I can't possibly all watch.
```

**The Solution**

```text
1. Don't watch the 1h video!
2. Read the summary of the video in 5 minutes instead.
3. Optional: Read (searchable) transcript if you want more details.
4. Optional: Decide to actually watch the original video. 
```

# Setup

---
Prerequisites:

* Python 3.8+
* ffmpeg in your PATH (get it [here](https://ffmpeg.org/download.html))
* OpenAI API key (get one [here](https://beta.openai.com/))
* GPU with CUDA support (optional, but highly recommended for fast transcription)

Virtual environment and installing dependencies:

```text
1. Navigate to the directory where you want to create the virtual environment.
2. Create a new virtual environment: `python3 -m venv env`.
3. Activate the virtual environment: `source env/bin/activate`.
4. Install dependencies from `requirements.txt`: `pip install -r requirements.txt`.
5. Start working on your project within the virtual environment.
6. Deactivate the virtual environment: `deactivate`.
```

Configuring the the models and API:

```text
1. Copy the file 'dot.env' to '.env' in the root directory.
2. Never add '.env' to your version control system.
3. Edit the '.env' file and add your OpenAI API key.
4. Keep or change the other parameters in '.env' as you see fit.
```
Installing and running Jupyter Notebooks:

```text
1. Activate your virtual environment.
2. Install Jupyter Notebooks: `pip install jupyter`.
3. Start the notebook server: `jupyter notebook`.
4. Open the Jupyter Notebook interface in your web browser (should happen automatically).
5. Navigate to the notebooks folder and click on _demo.ipynb_
6. Press the play button to run the cells of the notebook.
```
## Known issues

---

**Problem:** Video download fails

**Solution:** Upgrade _yt-dlp_ to a later version.

You can do this by uninstalling the current version and installing the latest version.

1. To uninstall the current version, run the command: `pip uninstall yt-dlp`.
2. Then, to install the latest version, run the command: `pip install yt-dlp`.

Hopefully, the API didn't change, so you won't have to modify any code that uses yt-dlp.

## Optimizations

---

Possible improvements to this project are:

* Reduce processing time: Auto-detect optimal Whisper model (=smallest without sacrificing transcription quality + language specific).
* Reduce download volume: Auto-detect the best audio quality from URL and only download that audio track.
* Increase overall throughput: Parallelize the extraction pipeline to max resource utilisation.
* Usability: Develop an interactive UI (w/FastAPI?) to run this tool outside a notebook, and make it deployable as a web service.
* Utility: Cast the processing pipeline into a shell script or CLI tool that allows to run it in headless mode (e.g. on a server).

## Project Organization

---

    ├── LICENSE
    ├── README.md
    ├── requirements.txt                    <- The requirements file for reproducing the environment.
    │
    ├── data
    │   ├── video_features                  <- video downloads are stored here
    │   ├── audio_features                  <- audio extracts are stored here
    │   ├── text_features                   <- text transcripts are stored here
    │   └── text_summaries                  <- text summaries are stored here
    │
    ├── notebooks                           <- Jupyter notebooks, contains the demo. 
    │
    │
    └── src                                 <- Source code for use in this project.
        ├── __init__.py         
        ├── util                            
        │   ├── __init__.py
        │   ├── fs.py                       <-- file system helper functions   
        │   └── videodownloader.py          <-- wrapper class for downloading videos using yt-dlp
        ├── audio2text
        │   ├── __init__.py
        │   └── whisperwrapper.py           <-- wrapper class for transcribing audio using Whisper (local)
        ├── text2summary
        ├── __init__.py
        │   └── gpt3wrapper.py              <-- wrapper class to talk to OpenAI's GPT-3 API 
        └── video2audio
            ├── __init__.py
            └── ffmpegaudioextraction.py    <-- wrapper class to convert video to audio using ffmpeg

---
