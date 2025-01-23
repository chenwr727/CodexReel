# NotebookQwen

NotebookQwen is an automated video generation project inspired by NotebookLlama. It retrieves content from a specified URL, generates a podcast script, synthesizes speech, creates images, and ultimately produces a video.

#### Demo

[Huawei Mate Brand Gala Summary: Mate 70, Mate X6, Pure HarmonyOS, Zunjie S800...](https://www.ithome.com/0/813/427.htm)

https://github.com/user-attachments/assets/b9ce609d-5171-4c20-b281-d7a740e99c70

```json
{
    "topic": "Huawei Gala",
    "dialogues": [
        {
            "speaker": "Xiaojian",
            "contents": [
                "Everyone, today we're going to talk about Huawei's latest gadgets.",
                "The Mate 70 series is truly 'the most powerful' phone!",
                "This name isn't just for show."
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "Most powerful?",
                "That sounds impressive,",
                "it feels like a superhero among phones!",
                "If this phone went out with me,",
                "I'd give it a superhero cape!"
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "Do you think it needs a cape?",
                "It already has fancy names like 'Jin Si Jin Xian' and 'Dong Fang Jin Se',",
                "going out with you,",
                "it would be renamed to 'Jin Yi Wei'!"
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "Haha, I was also thinking about the screen,",
                "it supports dynamic refresh rates from 1-120Hz!",
                "Do you think my Laochen could speak faster than my wife with this?",
                "She's quite fast!"
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "That's hard to say,",
                "if she speaks with intent, 120Hz won't catch up,",
                "and besides, your right hand is too slow!",
                "But the Mate 70's camera is really good,",
                "50 million pixel zoom,",
                "capturing distant scenery is 'cross-generational'."
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "I heard the Mate 70 can also do satellite messaging?",
                "That's so cool,",
                "you could even chat with aliens!",
                "I could ask them,",
                "'What's your phone brand?'"
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "Haha, aliens would probably tell you,",
                "they call it 'Galaxy Phone',",
                "supports cosmic network,",
                "signal is stronger than your data plan!"
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "Talking about data plans, I thought of the 'Zunjie S800'!",
                "It starts faster than a plane,",
                "0-100 km/h in 3.3 seconds,",
                "could I fly to Beijing for coffee?"
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "Of course you could!",
                "If the new nanny didn't keep up, sitting in the car and saying,",
                "'I checked, it's snowing today,'",
                "you could tell her,",
                "'No problem, I'm a high-speed pass!'"
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "High-speed pass!",
                "Jump on top and activate 'Autopilot Mode',",
                "that's the feeling of soul out of body."
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "Exactly! Did you know,",
                "there's also a watch released this time,",
                "priced at 23,999 RMB, even with gold inlaid.",
                "If I wear this watch,",
                "could people think I'm carrying a God of Wealth?"
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "God of Wealth!",
                "Maybe I should get one too,",
                "see which grandma in the neighborhood notices me first.",
                "I'm the 'Noble Master'?"
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "Haha, hope you don't lose your reading glasses,",
                "otherwise you might end up putting a screen protector on it,",
                "and it becomes a brick,",
                "blocking the sun!"
            ]
        },
        {
            "speaker": "Laochen",
            "contents": [
                "Good point!",
                "This Huawei Gala is like a grand play,",
                "combining high-tech and luxury,",
                "but ultimately,",
                "we need to live life with heart,",
                "to make life shine!"
            ]
        },
        {
            "speaker": "Xiaojian",
            "contents": [
                "Exactly!",
                "No matter how advanced the technology,",
                "the joy in life is created by us!",
                "Hope everyone can shine like Huawei's new products,",
                "emitting the brightest light!",
                "Thank you all!"
            ]
        }
    ]
}
```

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Project Features](#project-features)
- [Directory Structure](#directory-structure)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
.
├── app.py
├── config-template.toml
├── config.toml
├── main.py
├── requirements.txt
├── run.sh
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── image.py
│   ├── llm.py
│   ├── log.py
│   ├── processing.py
│   ├── tts.py
│   └── video.py
└── web/
    ├── __init__.py
    ├── config.py
    ├── crud.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── service.py
    └── web.py
```

## Installation

1. Clone the repository to your local machine:

   ```sh
   git clone https://github.com/chenwr727/NotebookQwen.git
   cd NotebookQwen
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `config-template.toml` and rename it to `config.toml`:

   ```sh
   cp config-template.toml config.toml
   ```

2. Edit the `config.toml` file to fill in the appropriate API keys and configurations.

## Running the Project

### Start Services

1. Start the FastAPI application:

   ```sh
   python app.py
   ```

2. Start the Streamlit application:

   ```sh
   streamlit run web.py --server.port 8000
   ```

### Use Scripts

1. Run the `main.py` script to process a specified URL:

   ```sh
   python main.py <url>
   ```

### Use Shell Script

1. Manage services using the `run.sh` script:

   ```sh
   # Start services
   ./run.sh start

   # Stop services
   ./run.sh stop

   # Restart services
   ./run.sh restart
   ```

## Project Features

- Retrieve and parse content from a specified URL.
- Generate a podcast script using LLM (Language Model).
- Synthesize speech and generate audio files.
- Create images.
- Assemble and generate the final video file.
- Provide APIs based on FastAPI and a Web interface based on Streamlit.

## Directory Structure

- `app.py`: Entry point for the FastAPI application.
- `main.py`: Main script that processes URLs and generates videos.
- `utils/`: Utility modules including configuration loading, logging, image generation, LLM processing, speech synthesis, and video processing.
- `web/`: Web-related modules including database, models, CRUD operations, and services.
- `web.py`: Entry point for the Streamlit application.
- `run.sh`: Shell script to manage services.
- `config-template.toml`: Configuration template file.
- `requirements.txt`: List of project dependencies.

## Examples

Here is an example command to process a specified URL and generate a video:

```sh
python main.py https://example.com/article
```

## Contributing

We welcome contributions! Please submit Pull Requests or report issues. Steps to contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -am 'Add some feature'`).
4. Push to the new branch (`git push origin feature/new-feature`).
5. Submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.