# ytdlpllm

`ytdlpllm` is a command-line tool that uses a Large Language Model (LLM) to convert your natural language instructions into `yt-dlp` commands.

## How it Works

This tool acts as a wrapper around `yt-dlp`, allowing you to describe what you want to do in plain English. `ytdlpllm` then uses an LLM to generate the appropriate `yt-dlp` command and executes it for you.

This project defaults to using a local [Ollama](https://ollama.ai/) installation, which allows you to run the LLM on your own machine.

## Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/m-ren/ytdlpllm.git
    cd ytdlpllm
    ```

2.  **Install the dependencies:**
    ```sh
    pip install .
    ```

## Usage

To use `ytdlpllm`, simply run the command followed by your instructions in quotes:

```sh
ytdlpllm "your instructions here"
```

### Configuration

By default, `ytdlpllm` connects to a local Ollama instance at `http://localhost:11434/v1` and uses the `llama3:latest` model. You can customize this using the following command-line arguments:

*   `--openai_model`: Specify a different model to use.
*   `--openai_base_url`: Specify a different base URL for the API.

If you want to use the official OpenAI API, you can set the `OPENAI_API_KEY` environment variable and specify the model and base URL accordingly.

### Examples

#### Basic Audio Download
```sh
ytdlpllm "download the audio from this youtube video: <URL>"
```
**Output Command:** `yt-dlp -x --audio-format mp3 <URL>`

---

#### Advanced Playlist Filtering
```sh
ytdlpllm "from the playlist <PLAYLIST_URL>, download the first 5 videos that have 'tutorial' in the title"
```
**Output Command:** `yt-dlp --playlist-items 1-5 --match-filter "title~='(?i)tutorial'" <PLAYLIST_URL>`

---

#### Custom File Naming
```sh
ytdlpllm "download the video <URL> and name the file with the upload date, title, and video ID"
```
**Output Command:** `yt-dlp -o "%(upload_date)s_%(title)s_%(id)s.%(ext)s" <URL>`

---

#### SponsorBlock Integration
```sh
ytdlpllm "download the video <URL> and remove the sponsor segments"
```
**Output Command:** `yt-dlp --sponsorblock-remove sponsor <URL>`


## Acknowledgements

This project was inspired by and forked from [gstrenge/llmpeg](https://github.com/gstrenge/llmpeg).

## License

`ytdlpllm` is licensed under the MIT License. See the `LICENSE` file for more details.