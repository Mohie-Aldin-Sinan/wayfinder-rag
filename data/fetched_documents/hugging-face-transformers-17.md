Exporting to production · Hugging Face
Hugging Face
Transformers documentation
Exporting to production
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
Exporting to production
Export Transformers’ models to different formats for optimized runtimes and devices. Deploy the same model to cloud providers or run it on mobile and edge devices. You don’t need to rewrite the model from scratch for each deployment environment. Freely deploy across any inference ecosystem.
ExecuTorch
runs PyTorch models on mobile and edge devices. It exports a model into a graph of standardized operators, compiles the graph into an ExecuTorch program, and executes it on the target device. The runtime is lightweight and calculates the execution plan ahead of time.
Install
Optimum ExecuTorch
from source.
Copied
git
clone
https://github.com/huggingface/optimum-executorch.git
cd
optimum-executorch pip install
'.[dev]'
Export a Transformers model to ExecuTorch with the CLI tool.
Copied
optimum-cli
export
executorch \ --model
"Qwen/Qwen3-8B"
\ --task
"text-generation"
\ --recipe
"xnnpack"
\ --use_custom_sdpa \ --use_custom_kv_cache \ --qlinear 8da4w \ --qembedding 8w \ --output_dir=
"hf_smollm2"
Run the following command to view all export options.
Copied
optimum-cli
export
executorch --
help
ONNX
is a shared language for describing models from different frameworks. It represents models as a graph of standardized operators with well-defined types, shapes, and metadata. Models serialize into compact protobuf files that you can deploy across optimized runtimes and engines.
Optimum ONNX
exports models to ONNX with configuration objects. It supports many
architectures
and is easily extendable. Export models through the CLI tool or programmatically.
Install
Optimum ONNX
.
Copied
uv pip install optimum-onnx
optimum-cli
Specify a model to export and the output directory with the
--model
argument.
Copied
optimum-cli
export
onnx --model Qwen/Qwen3-8B Qwen/Qwen3-8b-onnx/
Run the following command to view all available arguments or refer to the
Export a model to ONNX with optimum.exporters.onnx
guide for more details.
Copied
optimum-cli
export
onnx --
help
To export a local model, save the weights and tokenizer files in the same directory. Pass the directory path to the
--model
argument and use the
--task
argument to specify the
task
. If you don’t provide
--task
, the system auto-infers it from the model or uses an architecture without a task-specific head.
Copied
optimum-cli
export
onnx --model path/to/local/model --task text-generation Qwen/Qwen3-8b-onnx/
Deploy the model with any
runtime
that supports ONNX, including ONNX Runtime.
Copied
from
transformers
import
AutoTokenizer
from
optimum.onnxruntime
import
ORTModelForCausalLM tokenizer = AutoTokenizer.from_pretrained(
"Qwen/Qwen3-8b-onnx"
) model = ORTModelForCausalLM.from_pretrained(
"Qwen/Qwen3-8b-onnx"
) inputs = tokenizer(
"Plants generate energy through a process known as "
, return_tensors=
"pt"
) outputs = model.generate(**inputs)
print
(tokenizer.batch_decode(outputs))
optimum.onnxruntime
Export Transformers’ models programmatically with Optimum ONNX. Instantiate a
ORTModel
with a model and set
export=True
. Save the ONNX model with
save_pretrained
.
Copied
from
optimum.onnxruntime
import
ORTModelForCausalLM
from
transformers
import
AutoTokenizer ort_model = ORTModelForCausalLM.from_pretrained(
"Qwen/Qwen3-8b"
, export=
True
) tokenizer = AutoTokenizer.from_pretrained(
"Qwen/Qwen3-8b"
) ort_model.save_pretrained(
"onnx/"
) tokenizer.save_pretrained(
"onnx/"
)
Update
on GitHub
←
Sharing
Contribute to Transformers
→