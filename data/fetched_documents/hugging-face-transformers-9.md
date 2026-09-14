Text generation · Hugging Face
Hugging Face
Transformers documentation
Text generation
Transformers
🏡 View all docs
AWS Trainium & Inferentia
Accelerate
Argilla
AutoTrain
Bitsandbytes
CLI
Chat UI
Dataset viewer
Datasets
Deploying on AWS
Diffusers
Distilabel
Evaluate
Google Cloud
Google TPUs
Gradio
Hub
Hub Python Library
Huggingface.js
Inference Endpoints (dedicated)
Inference Providers
Kernels
LeRobot
Leaderboards
Lighteval
Microsoft Azure
OpenEnv
Optimum
PEFT
Reachy Mini
Safetensors
Sentence Transformers
TRL
Tasks
Text Embeddings Inference
Text Generation Inference
Tokenizers
Trackio
Transformers
Transformers.js
Xet
smolagents
timm
Search documentation
main
v5.17.0
v5.15.1
v5.14.0
v5.13.1
v5.12.0
v5.11.0
v5.10.4
v5.9.0
v5.8.1
v5.7.0
v5.6.2
v5.5.4
v5.4.0
v5.3.0
v5.2.0
v5.1.0
v5.0.0
v4.57.6
v4.56.2
v4.55.4
v4.53.3
v4.52.3
v4.51.3
v4.50.0
v4.49.0
v4.48.2
v4.47.1
v4.46.3
v4.45.2
v4.44.2
v4.43.4
v4.42.4
v4.41.2
v4.40.2
v4.39.3
v4.38.2
v4.37.2
v4.36.1
v4.35.2
v4.34.1
v4.33.3
v4.32.1
v4.31.0
v4.30.0
v4.29.1
v4.28.1
v4.27.2
v4.26.1
v4.25.1
v4.24.0
v4.23.1
v4.22.2
v4.21.3
v4.20.1
v4.19.4
v4.18.0
v4.17.0
v4.16.2
v4.15.0
v4.14.1
v4.13.0
v4.12.5
v4.11.3
v4.10.1
v4.9.2
v4.8.2
v4.7.0
v4.6.0
v4.5.1
v4.4.2
v4.3.3
v4.2.2
v4.1.1
v4.0.1
v3.5.1
v3.4.0
v3.3.1
v3.2.0
v3.1.0
v3.0.2
v2.11.0
v2.10.0
v2.9.1
v2.8.0
v2.7.0
v2.6.0
v2.5.1
v2.4.1
v2.3.0
v2.2.2
v2.1.1
v2.0.0
v1.2.0
v1.1.0
v1.0.0
doc-builder-html
AR
DE
EN
ES
FR
HI
IT
JA
KO
PT
RO
TE
TR
ZH
You are viewing
main
version, which requires
installation from source
. If you'd like regular pip install, checkout the latest stable version (
v5.17.0
).
Join the Hugging Face community
and get access to the augmented documentation experience
Collaborate on models, datasets and Spaces
Faster examples with accelerated inference
Switch between documentation themes
Sign Up
to get started
Copy page
Text generation
Text generation is the most popular application for large language models (LLMs). A LLM is trained to generate the next word (token) given some initial text (prompt) along with its own generated outputs up to a predefined length or when it reaches an end-of-sequence (
EOS
) token.
In Transformers, the
generate()
API handles text generation, and it is available for all models with generative capabilities. This guide will show you the basics of text generation with
generate()
and some common pitfalls to avoid.
For the following commands, please make sure
transformers serve
is running
.
Copied
transformers chat Qwen/Qwen2.5-0.5B-Instruct
Default generate
Before you begin, it’s helpful to install
bitsandbytes
to quantize really large models to reduce their memory usage.
Copied
!pip install -U transformers bitsandbytes
Bitsandbytes supports multiple backends in addition to CUDA-based GPUs. Refer to the multi-backend installation
guide
to learn more.
Load a LLM with
from_pretrained()
and add the following two parameters to reduce the memory requirements.
device_map="auto"
enables Accelerates’
Big Model Inference
feature for automatically initiating the model skeleton and loading and dispatching the model weights across all available devices, starting with the fastest device (GPU).
quantization_config
is a configuration object that defines the quantization settings. This examples uses bitsandbytes as the quantization backend (see the
Quantization
section for more available backends) and it loads the model in
4-bits
.
Copied
from
transformers
import
AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig quantization_config = BitsAndBytesConfig(load_in_4bit=
True
) model = AutoModelForCausalLM.from_pretrained(
"mistralai/Mistral-7B-v0.1"
, device_map=
"auto"
, quantization_config=quantization_config)
Tokenize your input, and set the
padding_side()
parameter to
"left"
because a LLM is not trained to continue generation from padding tokens. The tokenizer returns the input ids and attention mask.
Process more than one prompt at a time by passing a list of strings to the tokenizer. Batch the inputs to improve throughput at a small cost to latency and memory.
Copied
tokenizer = AutoTokenizer.from_pretrained(
"mistralai/Mistral-7B-v0.1"
, padding_side=
"left"
) model_inputs = tokenizer([
"A list of colors: red, blue"
], return_tensors=
"pt"
).to(model.device)
Pass the inputs to
generate()
to generate tokens, and
batch_decode()
the generated tokens back to text.
Copied
generated_ids = model.generate(**model_inputs) tokenizer.batch_decode(generated_ids, skip_special_tokens=
True
)[
0
]
"A list of colors: red, blue, green, yellow, orange, purple, pink,"
Generation configuration
All generation settings are contained in
GenerationConfig
. In the example above, the generation settings are derived from the
generation_config.json
file of
mistralai/Mistral-7B-v0.1
. A default decoding strategy is used when no configuration is saved with a model.
Inspect the configuration through the
generation_config
attribute. It only shows values that are different from the default configuration, in this case, the
bos_token_id
and
eos_token_id
.
Copied
from
transformers
import
AutoModelForCausalLM model = AutoModelForCausalLM.from_pretrained(
"mistralai/Mistral-7B-v0.1"
, device_map=
"auto"
) model.generation_config GenerationConfig {
"bos_token_id"
:
1
,
"eos_token_id"
:
2
}
You can customize
generate()
by overriding the parameters and values in
GenerationConfig
. See
this section below
for commonly adjusted parameters.
Copied
# enable beam search sampling strategy
model.generate(**inputs, num_beams=
4
, do_sample=
True
)
generate()
can also be extended with external libraries or custom code:
the
logits_processor
parameter accepts custom
LogitsProcessor
instances for manipulating the next token probability distribution;
the
stopping_criteria
parameters supports custom
StoppingCriteria
to stop text generation;
other custom generation methods can be loaded through the
custom_generate
flag (
docs
).
Refer to the
Generation strategies
guide to learn more about search, sampling, and decoding strategies.
Saving
Create an instance of
GenerationConfig
and specify the decoding parameters you want.
Copied
from
transformers
import
AutoModelForCausalLM, GenerationConfig model = AutoModelForCausalLM.from_pretrained(
"my_account/my_model"
) generation_config = GenerationConfig( max_new_tokens=
50
, do_sample=
True
, top_k=
50
, eos_token_id=model.config.eos_token_id )
Use
save_pretrained()
to save a specific generation configuration and set the
push_to_hub
parameter to
True
to upload it to the Hub.
Copied
generation_config.save_pretrained(
"my_account/my_model"
, push_to_hub=
True
)
Leave the
config_file_name
parameter empty. This parameter should be used when storing multiple generation configurations in a single directory. It gives you a way to specify which generation configuration to load. You can create different configurations for different generative tasks (creative text generation with sampling, summarization with beam search) for use with a single model.
Copied
from
transformers
import
AutoModelForSeq2SeqLM, AutoTokenizer, GenerationConfig tokenizer = AutoTokenizer.from_pretrained(
"google-t5/t5-small"
) model = AutoModelForSeq2SeqLM.from_pretrained(
"google-t5/t5-small"
) translation_generation_config = GenerationConfig( num_beams=
4
, early_stopping=
True
, decoder_start_token_id=
0
, eos_token_id=model.config.eos_token_id, pad_token=model.config.pad_token_id, ) translation_generation_config.save_pretrained(
"/tmp"
, config_file_name=
"translation_generation_config.json"
, push_to_hub=
True
) generation_config = GenerationConfig.from_pretrained(
"/tmp"
, config_file_name=
"translation_generation_config.json"
) inputs = tokenizer(
"translate English to French: Configuration files are easy to use!"
, return_tensors=
"pt"
) outputs = model.generate(**inputs, generation_config=generation_config)
print
(tokenizer.batch_decode(outputs, skip_special_tokens=
True
))
Common Options
generate()
is a powerful tool that can be heavily customized. This can be daunting for a new users. This section contains a list of popular generation options that you can define in most text generation tools in Transformers:
generate()
,
GenerationConfig
,
pipelines
, the
chat
CLI, …
Option name
Type
Simplified description
max_new_tokens
int
Controls the maximum generation length. Be sure to define it, as it usually defaults to a small value.
do_sample
bool
Defines whether generation will sample the next token (
True
), or is greedy instead (
False
). Most use cases should set this flag to
True
. Check
this guide
for more information.
temperature
float
How unpredictable the next selected token will be. High values (
>0.8
) are good for creative tasks, low values (e.g.
<0.4
) for tasks that require “thinking”. Requires
do_sample=True
.
num_beams
int
When set to
>1
, activates the beam search algorithm. Beam search is good on input-grounded tasks. Check
this guide
for more information.
repetition_penalty
float
Set it to
>1.0
if you’re seeing the model repeat itself often. Larger values apply a larger penalty.
eos_token_id
list[int]
The token(s) that will cause generation to stop. The default value is usually good, but you can specify a different token.
Pitfalls
The section below covers some common issues you may encounter during text generation and how to solve them.
Output length
generate()
returns up to 20 tokens by default unless otherwise specified in a models
GenerationConfig
. It is highly recommended to manually set the number of generated tokens with the
max_new_tokens
parameter to control the output length.
Decoder-only
models returns the initial prompt along with the generated tokens.
Copied
model_inputs = tokenizer([
"A sequence of numbers: 1, 2"
], return_tensors=
"pt"
).to(model.device)
default length
max_new_tokens
Copied
generated_ids = model.generate(**model_inputs) tokenizer.batch_decode(generated_ids, skip_special_tokens=
True
)[
0
]
'A sequence of numbers: 1, 2, 3, 4, 5'
Decoding strategy
The default decoding strategy in
generate()
is
greedy search
, which selects the next most likely token, unless otherwise specified in a models
GenerationConfig
. While this decoding strategy works well for input-grounded tasks (transcription, translation), it is not optimal for more creative use cases (story writing, chat applications).
For example, enable a
multinomial sampling
strategy to generate more diverse outputs. Refer to the
Generation strategy
guide for more decoding strategies.
Copied
model_inputs = tokenizer([
"I am a cat."
], return_tensors=
"pt"
).to(model.device)
greedy search
multinomial sampling
Copied
generated_ids = model.generate(**model_inputs) tokenizer.batch_decode(generated_ids, skip_special_tokens=
True
)[
0
]
Padding side
Inputs need to be padded if they don’t have the same length. But LLMs aren’t trained to continue generation from padding tokens, which means the
padding_side()
parameter needs to be set to the left of the input.
right pad
left pad
Copied
model_inputs = tokenizer( [
"1, 2, 3"
,
"A, B, C, D, E"
], padding=
True
, return_tensors=
"pt"
).to(model.device) generated_ids = model.generate(**model_inputs) tokenizer.batch_decode(generated_ids, skip_special_tokens=
True
)[
0
]
'1, 2, 33333333333'
Prompt format
Some models and tasks expect a certain input prompt format, and if the format is incorrect, the model returns a suboptimal output. You can learn more about prompting in the
prompt engineering
guide.
For example, a chat model expects the input as a
chat template
. Your prompt should include a
role
and
content
to indicate who is participating in the conversation. If you try to pass your prompt as a single string, the model doesn’t always return the expected output.
Copied
from
transformers
import
AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig tokenizer = AutoTokenizer.from_pretrained(
"HuggingFaceH4/zephyr-7b-alpha"
) model = AutoModelForCausalLM.from_pretrained(
"HuggingFaceH4/zephyr-7b-alpha"
, device_map=
"auto"
, quantization_config=BitsAndBytesConfig(load_in_4bit=
True
) )
no format
chat template
Copied
prompt =
"""How many cats does it take to change a light bulb? Reply as a pirate."""
model_inputs = tokenizer([prompt], return_tensors=
"pt"
).to(model.device) input_length = model_inputs.input_ids.shape[
1
] generated_ids = model.generate(**model_inputs, max_new_tokens=
50
)
print
(tokenizer.batch_decode(generated_ids[:, input_length:], skip_special_tokens=
True
)[
0
])
"Aye, matey! 'Tis a simple task for a cat with a keen eye and nimble paws. First, the cat will climb up the ladder, carefully avoiding the rickety rungs. Then, with"
Resources
Take a look below for some more specific and specialized text generation libraries.
Optimum
: an extension of Transformers focused on optimizing training and inference on specific hardware devices
Outlines
: a library for constrained text generation (generate JSON files for example).
SynCode
: a library for context-free grammar guided generation (JSON, SQL, Python).
Text Generation Inference
: a production-ready server for LLMs.
Text generation web UI
: a Gradio web UI for text generation.
logits-processor-zoo
: additional logits processors for controlling text generation.
Update
on GitHub
←
Adding a new pipeline
Decoding methods
→