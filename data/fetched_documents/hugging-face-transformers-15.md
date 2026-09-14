Padding and truncation · Hugging Face
Hugging Face
Transformers documentation
Padding and truncation
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
Padding and truncation
Batched inputs are often different lengths, so they can’t be converted to fixed-size tensors. Padding and truncation are strategies for dealing with this problem, to create rectangular tensors from batches of varying lengths. Padding adds a special
padding token
to ensure shorter sequences will have the same length as either the longest sequence in a batch or the maximum length accepted by the model. Truncation works in the other direction by truncating long sequences.
In most cases, padding your batch to the length of the longest sequence and truncating to the maximum length a model can accept works pretty well. However, the API supports more strategies if you need them. The three arguments you need to know are:
padding
,
truncation
and
max_length
.
The
padding
argument controls padding. It can be a boolean or a string:
True
or
'longest'
: pad to the longest sequence in the batch (no padding is applied if you only provide a single sequence).
'max_length'
: pad to a length specified by the
max_length
argument or the maximum length accepted by the model if no
max_length
is provided (
max_length=None
). Padding will still be applied if you only provide a single sequence.
False
or
'do_not_pad'
: no padding is applied. This is the default behavior.
The
truncation
argument controls truncation. It can be a boolean or a string:
True
or
'longest_first'
: truncate to a maximum length specified by the
max_length
argument or the maximum length accepted by the model if no
max_length
is provided (
max_length=None
). This will truncate token by token, removing a token from the longest sequence in the pair until the proper length is reached.
'only_second'
: truncate to a maximum length specified by the
max_length
argument or the maximum length accepted by the model if no
max_length
is provided (
max_length=None
). This will only truncate the second sentence of a pair if a pair of sequences (or a batch of pairs of sequences) is provided.
'only_first'
: truncate to a maximum length specified by the
max_length
argument or the maximum length accepted by the model if no
max_length
is provided (
max_length=None
). This will only truncate the first sentence of a pair if a pair of sequences (or a batch of pairs of sequences) is provided.
False
or
'do_not_truncate'
: no truncation is applied. This is the default behavior.
The
max_length
argument controls the length of the padding and truncation. It can be an integer or
None
, in which case it will default to the maximum length the model can accept. If the model has no specific maximum input length, truncation or padding to
max_length
is deactivated.
The following table summarizes the recommended way to setup padding and truncation. If you use pairs of input sequences in any of the following examples, you can replace
truncation=True
by a
STRATEGY
selected in
['only_first', 'only_second', 'longest_first']
, i.e.
truncation='only_second'
or
truncation='longest_first'
to control how both sequences in the pair are truncated as detailed before.
Truncation
Padding
Instruction
no truncation
no padding
tokenizer(batch_sentences)
padding to max sequence in batch
tokenizer(batch_sentences, padding=True)
or
tokenizer(batch_sentences, padding='longest')
padding to max model input length
tokenizer(batch_sentences, padding='max_length')
padding to specific length
tokenizer(batch_sentences, padding='max_length', max_length=42)
padding to a multiple of a value
tokenizer(batch_sentences, padding=True, pad_to_multiple_of=8)
truncation to max model input length
no padding
tokenizer(batch_sentences, truncation=True)
or
tokenizer(batch_sentences, truncation=STRATEGY)
padding to max sequence in batch
tokenizer(batch_sentences, padding=True, truncation=True)
or
tokenizer(batch_sentences, padding=True, truncation=STRATEGY)
padding to max model input length
tokenizer(batch_sentences, padding='max_length', truncation=True)
or
tokenizer(batch_sentences, padding='max_length', truncation=STRATEGY)
padding to specific length
Not possible
truncation to specific length
no padding
tokenizer(batch_sentences, truncation=True, max_length=42)
or
tokenizer(batch_sentences, truncation=STRATEGY, max_length=42)
padding to max sequence in batch
tokenizer(batch_sentences, padding=True, truncation=True, max_length=42)
or
tokenizer(batch_sentences, padding=True, truncation=STRATEGY, max_length=42)
padding to max model input length
Not possible
padding to specific length
tokenizer(batch_sentences, padding='max_length', truncation=True, max_length=42)
or
tokenizer(batch_sentences, padding='max_length', truncation=STRATEGY, max_length=42)
Update
on GitHub
Transformers
→