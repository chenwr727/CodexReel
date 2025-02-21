# URL2VideoStudio 🎬

> Transform articles into engaging video content with one click!

## 📖 Introduction

URL2VideoStudio is an innovative automated video generation tool that intelligently transforms any article into engaging dialogue videos. Inspired by NotebookLlama, this project leverages advanced AI technology to achieve fully automated text-to-video production.

### ✨ Key Features

- 🤖 **Smart Content Understanding** - Automatically extract and comprehend article essence
- 🎭 **Multi-Role Dialogue** - AI-driven dialogue generation for engaging content
- 🔍 **Intelligent Media Matching** - Semantic-based video material matching
- 🗣️ **AI Voice Synthesis** - Natural and fluid multi-character voiceovers
- 🎥 **Professional Video Production** - Automated editing and composition

### 🎯 Use Cases

- 📰 News Visualization - Quick conversion of news into short videos
- 📚 Article Visualization - Make content more expressive
- 🎤 Podcast Creation - Automated dialogue-style podcasts
- 📱 Short Video Production - Batch production of quality short videos
- 🎮 Gaming Content - Video transformation of game guides and news

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Service**: OpenAI GPT API
- **Voice Synthesis**: Tongyi TTS
- **Video Processing**: FFmpeg
- **Data Storage**: SQLite

## 🚀 Quick Start

### Requirements

- Python 3.10+
- FFmpeg
- ImageMagick

### Installation

1. Clone the repository:
```bash
git clone https://github.com/chenwr727/URL2VideoStudio.git
cd URL2VideoStudio
```

2. Create and activate conda environment:
```bash
conda create -n url2video python=3.10
conda activate url2video
```

3. Install dependencies:
```bash
pip install -r requirements.txt
conda install -c conda-forge ffmpeg
```

### Configuration

1. Copy configuration template:
```bash
copy config-template.toml config.toml
```

2. Edit `config.toml` with required parameters:
- OpenAI API Key
- Tongyi TTS Service Key
- Pexels API Key
- Other optional settings

## 📂 Project Structure

```
URL2VideoStudio/
├── api/                    # API interface module
│   ├── crud.py            # Database operations
│   ├── database.py        # Database configuration
│   ├── models.py          # Data models
│   ├── router.py          # Route definitions
│   └── service.py         # Business logic
├── schemas/               # Data model definitions
│   ├── config.py         # Configuration models
│   ├── task.py           # Task models
│   └── video.py          # Video models
├── services/             # External service integration
│   ├── llm.py           # LLM service
│   ├── pexels.py        # Video material service
│   ├── tts.py           # Voice synthesis service
│   └── video.py         # Video processing service
├── utils/                # Utility modules
│   ├── config.py        # Configuration management
│   ├── log.py           # Logging tools
│   ├── subtitle.py      # Subtitle processing
│   ├── text.py          # Text processing
│   └── video.py         # Video utilities
└── web.py               # Web interface entry
```

## 🖥️ Usage

### Web Interface

1. Start the API service:
```bash
python app.py
```

2. Launch the web interface:
```bash
streamlit run web.py --server.port 8000
```

### Command Line

Process a single URL:
```bash
python main.py https://example.com/article
```

## 📝 Examples

> Note: The following demo videos are edited and compressed for preview purposes only. You can generate complete videos by clicking on the titles to access the original articles.

<table>
    <thead>
        <tr>
            <th align="center"><g-emoji class="g-emoji" alias="arrow_forward">▶️</g-emoji> <a href="https://mp.weixin.qq.com/s/31AxWlPevYdI_CLErHReEQ">Europe: The Awkwardness of Being Seated at the Kids' Table</a></th>
            <th align="center"><g-emoji class="g-emoji" alias="arrow_forward">▶️</g-emoji> <a href="https://mp.weixin.qq.com/s/tQMKS6HBH5bFVwa7otJaww">How Does the Northeast Tycoon Maintain IP Heat with Nezha?</a></th>
            <th align="center"><g-emoji class="g-emoji" alias="arrow_forward">▶️</g-emoji> <a href="https://m.ithome.com/html/831514.htm">Non-invasive Blood Glucose Monitor: Technology Makes Life Easier</a></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center"><video src="https://github.com/user-attachments/assets/452561f5-acb5-4225-9e8b-eb080f8b0a7d"></video></td>
            <td align="center"><video src="https://github.com/user-attachments/assets/a28b6e03-3685-4014-a856-6a57adb86be1"></video></td>
            <td align="center"><video src="https://github.com/user-attachments/assets/e5dab72d-041c-436e-aa51-de9edfe1ba6d"></video></td>
        </tr>
    </tbody>
</table>

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [NotebookLlama](https://github.com/NotebookLlama) - Project inspiration
- All contributors and users