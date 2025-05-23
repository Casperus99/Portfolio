# Prompt Engineering
It's more like AI-coworking. It's about good practices when working with AI to improve effectiveness and get what you really want.


## Basics

- Well diefined inputs. Trash input = trash output.
- Temperature - controls creativity.

Prompt should be clear and consize. Avoid any kind of confusion. Talking like to a stranger (or young, kinda austistic genius). Provide specifics that create context. But not too much and too little. Encourage AI to be creative and explore different solutions.

BEST PRACTICIES:
-   Start with a clear action verb
-   Be specific about the outcome
-   Iterate and experiment with different versions

- CLARITY - CONTEXT - CREATIVITY (3xC or CCC)

- KEYWORDS like "step by step" or "detailed instructions" make AI more focused and logical.

- Set appropriate expectations regarding the consistency of the output

Iterative process:
-   REVIEW OUTPUT -> ADJUST PROMPT -> TEST -> REVIEW OUTPUT...
-   Make small changes with every iteration

Review for:
-   Accuracy
-   Relevance
-   Engagement
-   or any charasteristics you are looking for

Possible changes:
-   Adjust phrasing
-   Add key words
-   Provide more context

### Basic system of working with an AI model
1.  FOCUS ON THE TOPIC
    -   Avoid deviations from the problem
    -   Be very specific
    -   Try to ask the AI for alternatives and suggestions
    -   Imagine that you are talking to a smart but unexperienced person
    -   Periodically refocus on key points
2.  ASSUME NOTHING
    -   Do not assume AI understands everything or even provided context
    -   Take into consideration limited context that may lead to forgetting
    -   Validate responses. AI may hallucinate.
3.  START WITH SIMPLE PROMPTS
    -   Use simple language
    -   Gradually add complexity
4.  ITERATE AND IMPROVE
5.  PRACTICE MAKES BETTER

- AI always tries to respond to the answer, even when it leads to hallucination. Try to tell him that he can say "I don't know" if he really can't.

### ROLE PROMPTING
A technique where you assign a specific role or identity to the AI.
E.x.
- "As a historian, make ..."
- "As a scientist, make ..."
- "AS a teacher, make ..."

### GUIDED ITERATION
Working together with the AI to refine and improve a prompt.
E.x.
- "We will work together to refine the summary through an iterative process"

### NESTED PROMPTING
Embedding a prompt within another prompt. A bit like breaking one big task into specific smaller ones, but in one prompt.
E.x.
- "Explain [...]. Next, discuss [...]."
- "List 5 facts [...]. Next, create a blog [...]."


## Advanced Prompt Engineerig Techniques

### CHAIN-OF-THOUGHT
Step by step approach that breaks a complex task into smaller and easier actions. You have more control of the process. You can specify instructions and required approach for every step. You can use this approach in one prompt or as a way of talking with AI chat.

### CHAOS PROMPTING
Technique used for generating new ideas by providing random and unexpected prompts to stimulate creativity and novelty. This can be achieved using tools such as random word generators, image associations, or other nonlinear prompts that disrupt established mental models.

### WRITING CODE WITH AI
1.  Define the application functional & non-functional requirements
    -   Document the app's puprose, target audience, desired features and any constraints
    -   Make sure you include non-functional requirements such as security, performance, compliance and others
2.  Choose the technology stack
    -   Decide on the programming language, development frameworks, libraries, tools
    -   Ask AI model for suggestions or a list of advantages/disadvantages of your selection
3.  Break down the project into smaller tasks
    -   You will achieve better results if you divide your code into smaller, more manageable pieces
    -   Take into account the max_token limitations of the A.I. model
4.  Start a conversation with AI
    -   Provide all the data you have gathered in the previous steps to AI in a prompt designed to be comprehensive but concise
    -   Progress gradually and iterate in small increments
5.  Seek guidance on architecture and design patterns
    -   If needed, ask AI for architecture and design patterns that  might be suitable for your project
    -   It's always a good idea to have a high-level design in place before starting to write the actual code
6.  Request code snippets and examples
    -   Start asking for code
    -   But don't forget to:
        -   replace any placeholder values returned with proper values
        -   test and validate every line of code
        -   customize the code if necessary to meet your requirements
7.  Troubleshoot and debug
    -   Test your code and return to AI with any error messages you may receive if you cannot debug it yourself
    -   You may also ask the A.I. for potential solutions, debugging techniques or best practicies
8.  Optimize and refactor code
    -   AI models can also help you optimize your code to achieve better:
        -   performance
        -   readability
        -   maintability
9.  Review and test the app
    -   Make sure it meets the initial requirements and functions as intended
    -   Ask for advice on testing strategies, tools and best practices
    -   Don't forget about the non-functional requirements
10. Deploy and maintain
    -   Make sure the app is correctly deployed in the production
        environment
    -   Take care of any required maintenance activities
    -   Ask for suggestions on deployment strategies, server
        configurations or automating maintenance tasks

-   If the AI model truncates the script, you can simply ask him to
    continue
-   AI can identify bugs, security vulnerabilities or style
    inconsistencies
-   AI can also automatically generate comments and documentation for
    your code
-   It can also build more intuitive and natural interfaces for users
-   Identify ambiguities, inconsistencies and missing information in
    requirements
-   Translate code from one language to another
-   Generate test cases and test data for your code

### PROMPT COMPRESSION TECHNIQUES
We can ask the AI to compress the given text so that it retains the meaning but results in the minimum number of tokens which could be fed into a LLM like yourself as-is and produce the same output. Make sure that you use the same model for decompressing which you used for compressing.
E.x.
-   It can be used to summirize long conversations and continue them in other sessions.

### PROBLEM SOLVING BY AI
-   Fishbone analysis
-   S.W.O.T. analysis
-   Look for another specific and well-known methods

### AI-ASSISTED QUESTIONING
It's another way of solving real-life problems with AI. This approach focuses on encouraging the AI to ask necessary questions to better understand your problem and provide more accurate responses. You have to ensure that AI asks relevant questions.

1.  Identify the problem - describe in detail the problem you are trying to solve. Be as specific as possible.
2.  Request questions - prompt the AI to come up with a list of questions to better understand the problem.
3.  Answer the questions - proide the necessary context by responding to the questions.
4.  Iterate and refine - keep answering any new questions until the AI model has gathered sufficient context
5.  Ask for solutions - it\'s time to ask for solutions or recommendations based on the data you provided.
E.x.
-   "Here is my problem {problem}. I need you to improve my sales. List a set of questions that you would like me to answet first in order to better understand the context of my problem."


## Use Cases in Everyday Tasks
-   Email templates
    -   relationship with the receiver
    -   purpose of the email
    -   desired tone
-   Social media
    -   chosen platform
    -   indented audience
    -   purpose pf the post

-   Most often AI models have been trained on data available up to certain point in the past so they don't have to know most up-to-date knowledge.

-   AI agents tend to understand UML language which can help in creating complex diagrams or graphs

### Research and Information Curation
-   Identifying relevant sources using AI
-   Extracting key information and summarizing content
-   Analyzing data & deriving insights

### Professional Development and Lifelong Learning
-   Identify skill gaps and learning opportunities
    -   Evaluating your professional strengths and weaknesses based on your professional background
-   Personalized learning plans
    -   Curating and preparing relevant training materials and learning paths
-   Stay informed
    -   Finding relevant information for your professional goals


## Ethics and Considerations

### Different Types of Biases
AI models are trained on data from the internet. Therefore it can copy it's biases.

-   gender bias
-   racial or ethnic bias
-   socio-economic bias
-   geographical bias
-   others

Actions against biases:
-   inclusive language in prompts
-   ballanced examples
-   variety of inputs


-   Add "notalk; justgo" at the end of your prompt to inform AI model that you don't want any additional comments


## Others
- Try to add some information about you (user profile) and information on how you want model to answer
- If you change your configuration often, you can save it as shortcuts (like" "--table" - give the answer in table format) but you have to remember that you have them
- You can require from model to add the note at the end of the response regarding his confidence in the scale of 1 to 10