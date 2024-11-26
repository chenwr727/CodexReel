English | [简体中文](README.md)

### NotebookQwen 

#### Project Overview
This project is inspired by NotebookLlama and aims to extract text from a given URL, generate podcast scripts, and convert them into video files. 

The project workflow is divided into the following steps:
1. Extract webpage content and save it as a text file.
2. Use LLM (Large Language Model) to generate podcast scripts.
3. Convert the generated podcast script into audio files.
4. Convert the podcast script into image files.
5. Combine the generated audio and image files into video files.

#### Demo

[9.1 Rating! A Must-Watch Chinese Film, *Good Stuff*](https://mp.weixin.qq.com/s/sGEcVIxH6TkIjeWew-LSJg)

[![9.1 Rating! A Must-Watch Chinese Film, *Good Stuff*](https://img.youtube.com/vi/Hg27tPm9xfY/0.jpg)](https://www.youtube.com/watch?v=Hg27tPm9xfY)

```json
[
    {
        "speaker": "Speaker 1",
        "content": "Hello, everyone! Welcome to today’s show! I’m your host, and today we’re diving into a very special film—*Good Stuff*. This movie has garnered widespread acclaim and sparked extensive discussion, especially among those interested in feminist topics. It’s truly a thought-provoking and heartwarming experience you won’t want to miss. Joining us today is my good friend and guest with unique insights into cinema. Welcome to the show!"
    },
    {
        "speaker": "Speaker 2",
        "content": "Thank you for having me! I watched *Good Stuff* and found it really refreshing—there’s a rare sense of warmth and lightheartedness. What makes this film so unique?"
    },
    {
        "speaker": "Speaker 1",
        "content": "Great question! What’s unique about this film is how it delicately and humorously explores feminism and modern urban life. Nowadays, many films highlight women’s strength and independence but often feel overly intense. *Good Stuff* tells these stories in a light and enjoyable way, leaving you feeling uplifted—like a warm cup of tea on a cold winter day."
    },
    {
        "speaker": "Speaker 2",
        "content": "I agree, it’s a truly comforting film. The female characters are especially vivid, each with unique traits and stories. Could you tell us more about them?"
    },
    {
        "speaker": "Speaker 1",
        "content": "Absolutely. The protagonist is Wang Tiemei, a single mother played by Song Jia. She’s an incredibly capable and independent woman juggling work challenges and raising her daughter, Wang Moli, affectionately called ‘Little Kid.’ Moli is a precocious, witty girl who often says surprising things. Another key character is Xiao Ye, played by Zhong Chuxi. She’s a band lead singer with a cheerful exterior but hidden scars. The interactions among these three women are heartwarming—they support and uplift each other, creating a beautiful dynamic."
    },
    {
        "speaker": "Speaker 2",
        "content": "The friendship among the women is truly inspiring. That scene where Xiao Ye is followed, and Tiemei rides a scooter to protect her, was incredibly touching. This sisterhood is so relatable—it reminds me of moments in real life, like strangers stepping in to help on public transport. This spirit of mutual support is so vital."
    },
    {
        "speaker": "Speaker 1",
        "content": "Exactly! That scene was powerful. It not only showcased women supporting each other but also conveyed an uplifting message: women can rely on each other to overcome life’s challenges. Interestingly, the male characters in the film are more like background elements, highlighting the women’s growth and independence. For instance, the ‘problematic’ Dr. Hu may be irritating but helps Xiao Ye realize what she truly wants. These characters amplify the women’s stories rather than overshadow them."
    },
    {
        "speaker": "Speaker 2",
        "content": "I felt the same. Dr. Hu’s actions were frustrating, but Xiao Ye’s growth was heartening. There are so many thoughtful details in the film—like feminist Easter eggs, including books by Chizuko Ueno and RBG-inspired T-shirts. These details add depth and resonate with the audience, tying the story together beautifully."
    },
    {
        "speaker": "Speaker 1",
        "content": "Exactly, those details are the film’s charm. They enrich the story while celebrating the beauty of life. For example, the scene where Tiemei leans on a stranger’s shoulder on the subway, and another woman steps in to support her—it’s heartwarming. These small moments show that kindness is all around us. Ultimately, *Good Stuff* isn’t just a feminist film—it’s about growth, love, and life. It resonates with everyone, regardless of gender, making it a must-watch."
    },
    {
        "speaker": "Speaker 2",
        "content": "I completely agree. This film is a gem. Thank you for sharing your insights today—it gave us a deeper appreciation of *Good Stuff*. I hope everyone goes to the theater to support this amazing movie!"
    },
    {
        "speaker": "Speaker 1",
        "content": "Thank you for tuning in! If you enjoyed our content, don’t forget to like and share it with your friends. See you in the next episode!"
    },
    {
        "speaker": "Speaker 2",
        "content": "See you!"
    }
]
```

#### Directory Structure
```
project/
├── main.py
├── utils/
│   ├── config.py
│   ├── image.py
│   ├── llm.py
│   ├── log.py
│   ├── processing.py
│   ├── tts.py
│   └── video.py
├── config-template.toml
└── config.toml
```

#### Installation
Ensure the following dependencies are installed:
```sh
pip install -r requirements.txt
```

#### Configuration
The project requires a `config.toml` file. Here’s how to set it up:

1. Copy the template file:
   ```sh
   cp config-template.toml config.toml
   ```

2. Edit `config.toml`:
   ```toml
   [llm]
   api_key = "YOUR_LLM_API_KEY"
   base_url = "https://api.example.com"
   model = "your_model_name"
   prompt_writer = "Your initial prompt for generating the podcast"
   prompt_rewriter = "Your rewriter prompt for refining the podcast"

   [tts]
   api_key = "YOUR_TTS_API_KEY"
   model = "your_tts_model_name"
   voices = ["voice1", "voice2"]
   ```

#### Running the Project
1. Ensure `config.toml` is properly configured.
2. Run the main script with the URL to process:

```sh
python main.py https://mp.weixin.qq.com/s/sGEcVIxH6TkIjeWew-LSJg
```

#### Acknowledgments
- [NotebookLlama](https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama)

We hope this README is helpful! Feel free to reach out with any questions or suggestions.