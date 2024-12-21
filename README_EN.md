English | [简体中文](README.md)

# NotebookQwen

#### Project Overview
This project is inspired by NotebookLlama and aims to extract text from the input URL, generate podcast text, and convert it into a video file.

The project mainly consists of the following steps:
1. Retrieve web content and save it as a text file.
2. Use LLM (Large Language Model) to generate podcast text.
3. Convert the generated podcast text into an audio file.
4. Convert the generated podcast text into image files.
5. Combine the audio and image files into a video file.

#### Demo

[Huawei Mate Brand Festival Summary: Mate 70, Mate X6, Pure HarmonyOS, Zunjie S800...](https://www.ithome.com/0/813/427.htm)

https://github.com/user-attachments/assets/e1a7100e-a30b-4b6d-8a65-824f338acada

```json
{
    "description": "Huawei Mate Brand Festival: A Feast of Technology and Innovation",
    "dialogues": [
        {
            "speaker": "Xiao Jian",
            "contents": [
                "Welcome to this episode of Tech Exploration Podcast!",
                "I'm Xiao Jian, and today we're going to talk about a tech feast.",
                "That is the recently concluded Huawei Mate Brand Festival."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Hi, Xiao Jian, it's great to discuss tech topics with you again.",
                "This Huawei Mate Brand Festival sounds really exciting.",
                "What are your initial impressions of this event?"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "It was indeed very exciting, especially the release of the Mate 70 series and the Mate X6 foldable phone.",
                "These two products not only have exquisite designs but also many technological breakthroughs.",
                "There is also the Pure HarmonyOS and a series of all-scenario products, which are truly dazzling."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Wow, that sounds really impressive!",
                "Especially this 'Pure HarmonyOS', I've always been curious about it.",
                "What does it actually mean?"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "'Pure HarmonyOS' refers to Huawei's completely self-developed operating system, no longer relying on third-party components.",
                "This means that the HarmonyOS will be more secure, stable, and provide a smoother user experience.",
                "This is an important milestone for domestic operating systems."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Yes, this is indeed a huge progress.",
                "The operating system is the core of the entire ecosystem, and complete self-development can enhance security and user experience.",
                "By the way, Xiao Jian, you mentioned the Mate 70 series, what are the special features of its design and performance?"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "The design of the Mate 70 series is very classic, adopting a central axis symmetrical design, with the rear camera module adorned with 'star light nails'.",
                "In terms of materials, it features 'golden silk brocade' and 'oriental brocade', giving a sense of high quality.",
                "As for the screen, the standard version is a 6.7-inch flat screen, while the Pro and Pro+ are 6.9-inch quad-curve screens."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Wow, 2500 nits of brightness, that's like being able to see clearly even in the dark!",
                "By the way, Xiao Jian, did you notice anything special about the Mate 70's camera at the launch event?"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "The camera of the Mate 70 is indeed very noteworthy.",
                "It debuts with the Maple Leaf Original Color Imaging System, equipped with a Maple Leaf Original Color Camera with 1.5 million multi-spectral channels.",
                "The color reproduction accuracy has been improved by 120%, and it also supports the AI Movie Texture Engine."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "That sounds really attractive!",
                "I love taking photos, especially when traveling.",
                "If I had a phone like this, I could definitely take a lot of beautiful pictures."
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "That's right, the three-network satellite communication function of the Mate X6 foldable phone is also very advanced.",
                "It supports Beidou satellite messages, Tiantong satellite communication, and low-orbit satellite internet.",
                "This means that even in areas without ground network coverage, users can send and receive messages via satellite."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Wow, that's really amazing!",
                "Imagine if you got lost in a remote area, you could still send a distress signal via satellite.",
                "This is literally a lifeline!"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "There are many other noteworthy products at this launch event.",
                "For example, the WATCH D2, which is Huawei's first dynamic blood pressure monitoring smartwatch.",
                "It can achieve 24-hour blood pressure monitoring and generate professional dynamic blood pressure reports."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Hearing you say this, I'm really tempted.",
                "Especially the WATCH D2, for someone like me who travels frequently, it's really useful to monitor blood pressure anytime."
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "There's also the FreeBuds Pro 4 earphones, which are Huawei's first TWS earphones equipped with Pure HarmonyOS.",
                "They support 48kHz/24bit lossless transmission, and the sound quality is excellent."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Hearing you say this, I can't wait to try these new products.",
                "Xiao Jian, what are your overall impressions of this launch event?"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "Overall, I think this launch event was very successful.",
                "Huawei not only demonstrated strong technological innovation capabilities but also showed an extreme pursuit of user experience.",
                "Every product is full of surprises, and I believe it will cause quite a stir in the market."
            ]
        },
        {
            "speaker": "Lao Chen",
            "contents": [
                "Yes, I'm also looking forward to the launch of these products.",
                "I hope they can bring more convenience and joy to our lives.",
                "Well, that's all for today's show, thank you all for listening, see you next time!"
            ]
        },
        {
            "speaker": "Xiao Jian",
            "contents": [
                "Thank you all, see you next time!"
            ]
        }
    ]
}
```

#### Directory Structure
```
project/
├── main.py
├── app.py
├── utils/
│   ├── config.py
│   ├── image.py
│   ├── llm.py
│   ├── log.py
│   ├── processing.py
│   ├── tts.py
│   └── video.py
├── web/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── model.py
│   ├── service.py
│   └── session.py
├── config-template.toml
└── config.toml
```

#### Install Dependencies
Make sure to install the following dependencies:
```sh
pip install -r requirements.txt
```

#### Configuration File
The project requires a configuration file `config.toml`, as shown below:

1. Copy the template file:
   ```sh
   cp config-template.toml config.toml
   ```

2. Modify the `config.toml` file content:
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

#### Run the Project
1. Ensure the `config.toml` file is correctly configured.
2. Run the main script `main.py` and pass the URL as a parameter.

```sh
python main.py https://mp.weixin.qq.com/s/sGEcVIxH6TkIjeWew-LSJg
```

#### API Endpoints

```sh
python app.py
```

The project provides the following API endpoints:

- **Create Task**
  - **URL**: `/v1/tasks`
  - **Method**: `POST`
  - **Request Body**:
    ```json
    {
      "name": "https://example.com/article"
    }
    ```
  - **Response**:
    - Success: `201 Created`
    - Failure: `400 Bad Request` or `500 Internal Server Error`

- **Get Task Status**
  - **URL**: `/v1/tasks/:task_id`
  - **Method**: `GET`
  - **Response**:
    - Success: `200 OK`
    - Failure: `404 Not Found` or `500 Internal Server Error`

- **Get Queue Status**
  - **URL**: `/v1/tasks/queue/status`
  - **Method**: `GET`
  - **Response**:
    - Success: `200 OK`
    - Failure: `500 Internal Server Error`

- **Cancel Task**
  - **URL**: `/v1/tasks/cancel/:task_id`
  - **Method**: `GET`
  - **Response**:
    - Success: `200 OK`
    - Failure: `404 Not Found`, `400 Bad Request`, or `500 Internal Server Error`

#### Acknowledgements
- [NotebookLlama](https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama)

I hope this README helps! If you have any questions or suggestions, please feel free to contact.