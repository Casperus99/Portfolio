# AI concepts

## 6 Principles of responsible AI
- **Fairness** - unconscious bias; discriminatory outputs
- **Reliability and safety** - probabilistic; not infallible; should mitigate risk
- **Privacy and security** - secure; don't reveal private data
- **Inclusiveness** - open to everyone; don't exclude
- **Transparency** - like "magic"; make users aware; potential limitations
- **Accountability** - framework of governance; responsible AI principles

## Tokenization techniques
- **Text normalization** - remove punctuation; lower case
- **Stop word removal** - "the", "a", or "it"
- **N-gram extraction** - multi-term phrases, ex. "artificial intelligence"
- **Stemming** - stripping endings like "s", "ing", "ed"
- **Lemmatization** - base or dictionary form, ex. "global" → "globe"
- **Parts of speech (POS) tagging** - 

## Statistical text analysis
- **Frequency Analysis**
- **Term Frequency - Inverse Document Frequency (TF-IDF)** - compare word frequency to average
- **"Bag-of-words" machine learning techniques** - Naive Bayes; sentiment analysis
- **TextRank** - unsupervised graph-based; summarize

## Multimodal model (mix of text, audio, image and video)
TODO: How it is achieved

## Tips for better prompts
- **clear and specific** - explicit instructions > vague language
- **context** - topic, audience
- **examples**
- **structure** - like bullet points, tables, or numbered lists

## NLP concepts
- **Language detection** - text language
- **Key term extraction** - important words and phrases; determine the topics and themes
- **Entity detection** - named entities; places, people, dates
- **Personally identifiable information (PII) detection** - redacting personal details, sensitive information
- **Text classification** - ex. filtering email as spam
- **Sentiment analysis** - positive, neutral, or negative
- **Text summarization** - reducing the volume; retaining its points

## Computer vision tasks and techniques
- **Image classification** - photo of one item
- **Object detection** - rectangles on many items
- **Semantic segmentation** - classify individual pixels
- **Contextual image analysis** - description containing objects and activities in context

## *Diffusion* in Image Generation
1. Prompt -> set of related visual features
2. Iterative process; start with random pixels
3. Remove "noise" and compare to the prompt (features)
4. Desired scene is produced

## *Tagging* - associate image with metadata to summarize attributes

## Optical Character Recognition (OCR) - extracting text data from image

## Field extraction - OCR output mapped into labeled data fields


# AI applications on Azure

## Face recognition operations
- **Identification** - one-to-many
- **Verification** - one-to-one
- **Find similar faces** - similar faces that might or might not belong to the same person
- **Group faces** - divides a set of unknown faces into several smaller groups

## AudioVisual analysis
- **Transcript phrases** - audio transcription; speaker identification; precise timing
- **Timing information** - start and end time of the content; width + height;
- **Key frames** - intelligently selected key moments; timestamps
- **Camera shots** - camera shots change timestamps
- **Custom fields** - ex. "summary" or "sentiment"

## Simple client app with agent
```Python
# Connect to your Foundry project
project_client = AIProjectClient(
    endpoint=myEndpoint,
    credential=DefaultAzureCredential(),
)

# Get an existing agent
agent = project_client.agents.get(agent_name="learning-agent")

# Retrieve an OpenAI client object
openai_client = project_client.get_openai_client()

# Send prompt
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)
```

## Azure Language SDK
### Language detection
```Python
# Create the client
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Make a request using the client for language detection
result = client.detect_language([text])[0]

# It returns Language, ISO 6391 code and Confidence score
```
### PII detection
```Python
result = client.recognize_pii_entities([text])[0]

# Returns both the redacted version of the text and a list of the entities it found, including each entity's category and confidence score.
```

## Azure Speech SDK
### Speech-to-Text
```Python
# Create a recognizer with microphone input
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, 
    audio_config=audio_config
)

# Connect event handlers
speech_recognizer.recognized.connect(recognized_handler)
speech_recognizer.recognizing.connect(recognizing_handler)

# Start continuous recognition
speech_recognizer.start_continuous_recognition()
print("Say something...")

# Keep the program running
input("Press Enter to stop...")
speech_recognizer.stop_continuous_recognition()
```
### Speech Synthesis
```Python
# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='en-US-Ava:DragonHDLatestNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
```

## Azure Computer Vision SDK
### Image Analysis
```Python
response = client.responses.create(
    model=os.getenv("MODEL_NAME"),  # your deployment name 
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this image? Provide 3 bullet points."},
                {"type": "input_image", "image_url": image_url}
            ],
        }
    ],
)

# A single request can include text input and image input together
# Images can be provided as URLs or as base64‑encoded image data
# The model processes both inputs simultaneously to generate a response
```
### Image Generation
```Python
response = client.responses.create(
    model=os.environ["MODEL_NAME"],  # your deployment name in Foundry
    input=prompt,
    tools=[{"type": "image_generation"}],
)

# Find encoded image in the given output
image_base64 = next(
    item.result for item in response.output
    if item.type == "image_generation_call"
)

# Decode image and save
with open("foundry_generated.png", "wb") as f:
    f.write(base64.b64decode(image_base64))
```
## Video generation (Foundry REST interface)
A **REST API** (Representational State Transfer API) is a web interface that lets programs communicate using HTTP. An SDK as a developer-friendly toolkit built on top of that interface. You can always work with the underlying REST API, especially if an SDK in the programming language you are familiar with does not exist. You can use curl (short for Client URL) to call, or talk to, the REST API. **Curl** is a command line tool used to send and receive data over the internet. At its core, curl: makes HTTP requests (and other protocols), sends data to a server, and receives and prints the server’s response.
### Create a video job
```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/videos" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "sora-2",
    "prompt": "A cinematic close-up of raindrops sliding down a neon-lit window at  night.",
    "size": "1280x720",
    "seconds": "8"
  }'
```
### Poll job status until completed
```bash
curl -X GET "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/videos/{video_id}" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
```
### Download the completed video
```bash
curl -L "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/videos/{video_id}/content?variant=video" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  --output output.mp4
```

## Azure Content Understanding
**Schema-based extraction:** OCR only finds raw text - schemas determine what to find (semantically) and how to label it.
**Analyzer:** Packaged flow of taking input, apllying the schema and providing structured output. Azure offers prebuilt analyzers.
### Document Understanding
```Python
client = ContentUnderstandingClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# 1) start analysis with analyzer id + inputs
analyzer_id = "prebuilt-invoice"
inputs = [
    {"url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"}
]

# 2) wait for the Long Running Operation (LRO) to complete
poller = client.begin_analyze(analyzer_id=analyzer_id, inputs=inputs)  # starts LRO
result = poller.result()  # waits for completion (polling handled by SDK)

# 3) read structured fields + markdown
# The result typically includes extracted "fields" and "markdown" per input content item.
for content in result.contents:
    print(content.markdown) # Just all fields printed together
    print(content.fields)
```
### Audio or video analyzers
```Python
# Exactly the same as higher. The only difference is that analyzer_id points to a different prebuilt analyzer.
```

## Foundry IQ
**Foundry IQ:** Managed knowledge layer. Connects various data from different sources into knowledge base that can be then retrieved by agents.
- **base**: top-level; collection of related sources; controls retrieval behavior
- **source**: connection to indexed or remote content
- **retrieval**: plans searches, finds relevant content, ranks results and returns a unified response with source references
### Write instructions for grounded answers
Connecting a knowledge base doesn't guarantee that an agent uses it consistently. Agent instructions should state the expected behavior. For example:
Effective instructions define:
- **When to retrieve**: Identify the questions or domains that require the knowledge base.
- **How to use evidence**: Require answers to stay grounded in retrieved content.
- **How to cite**: Ask for source references that users can inspect.
- **What to do when evidence is missing**: Tell the agent to acknowledge uncertainty or refer the user to an appropriate person or process.
### Test and improve the experience
- Straightforward questions with one clear source.
- Questions that require information from multiple sources.
- Ambiguous questions that should trigger clarification.
- Questions for which the knowledge base has no answer.
- Questions from users with different source permissions.
- Content containing text that attempts to change the agent's instructions.