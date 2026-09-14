Overview · Hugging Face
Hugging Face
Transformers documentation
Overview
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
Overview
Transformers provides multiple inference optimization techniques to make models fast, affordable, and accessible. Options include alternative attention mechanisms for reduced memory traffic, code compilation for faster execution, and optimized kernels for throughput. Stack these techniques for maximum performance.
Memory and speed are closely related but not the same. Shrinking your memory footprint makes a model “faster” because there is less data to move around. Pure speed optimizations don’t always reduce memory and sometimes increase usage. Choose the appropriate optimization based on your use case and hardware.
Use the table below to pick an optimization technique.
Technique
Speed
Memory
Compilation
✅
Attention backends
✅
Kernels
✅
Quantization
✅
Caching
✅
Parallelism
✅
Continuous batching
✅
This guide gives you a quick start on Transformers optimizations.
Compilation
torch.compile
reduces Python overhead, fuses operations, and creates kernels tuned for your shapes and hardware. The first run warms it up and subsequent runs use the faster compiled path.
Pass a
fixed size cache
to
generate()
to trigger
torch.compile
automatically.
Copied
import
torch
from
transformers
import
AutoTokenizer, AutoModelForCausalLM tokenizer = AutoTokenizer.from_pretrained(
"Qwen/Qwen3-0.6B"
) model = AutoModelForCausalLM.from_pretrained(
"Qwen/Qwen3-0.6B"
, dtype=torch.float16, device_map=
"auto"
)
input
= tokenizer(
"The French Bread Law states"
, return_tensors=
"pt"
).to(model.device) output = model.generate(**
input
, do_sample=
False
, max_new_tokens=
20
, cache_implementation=
"static"
) tokenizer.batch_decode(output, skip_special_tokens=
True
)[
0
]
Avoid calling
torch.compile(model)
outside of
generate()
to prevent the model from recompiling every step.
Attention backends
Alternative
attention backends
lower memory traffic. For example, FlashAttention tiles attention computations and avoids large intermediate tensors to reduce memory footprint.
Set
attn_implementation
in
from_pretrained()
to load an optimized attention backend.
Copied
from
transformers
import
AutoModelForCausalLM model = AutoModelForCausalLM.from_pretrained(
"Qwen/Qwen3-0.6B"
, attn_implementation=
"flash_attention_2"
)
Kernels
Kernels fuse operations to boost throughput and reduce memory usage. The
Kernels
library loads optimized compute kernels from the
Hub
in a flexible and version-safe way.
The example below loads an optimized FlashAttention-2 kernel without installing the package.
Copied
import
torch
from
transformers
import
AutoModelForCausalLM model = AutoModelForCausalLM.from_pretrained(
"Qwen/Qwen3-0.6B"
, attn_implementation=
"kernels-community/flash-attn2"
)
Quantization
shrinks the size of every parameter which lowers memory footprint and increases speed because you can do more operations.
Pass a quantization config to the
quantization_config
argument in
from_pretrained()
. Each quantization backend has a different config with different arguments. The example below quantizes a model to 4-bits and configures the computation dtype with the
bitsandbytes
backend.
Copied
import
torch
from
transformers
import
AutoModelForCausalLM, BitsAndBytesConfig bnb_config = BitsAndBytesConfig(load_in_4bit=
True
, bnb_4bit_compute_dtype=torch.bfloat16) model = AutoModelForCausalLM.from_pretrained(
"allenai/Olmo-3-7B-Think"
, quantization_config=bnb_config )
Caching
speeds up generation by reusing past keys and values instead of recomputing them for every token. To offset and reduce the memory cost of storing past keys and values, Transformers supports offloading the cache to the CPU. Only the current layer remains on the GPU.
Use the
cache_implementation
argument in
generate()
to set a cache strategy.
Copied
import
torch
from
transformers
import
AutoTokenizer, AutoModelForCausalLM tokenizer = AutoTokenizer.from_pretrained(
"Qwen/Qwen3-0.6B"
) model = AutoModelForCausalLM.from_pretrained(
"Qwen/Qwen3-0.6B"
, attn_implementation=
"kernels-community/flash-attn2"
) inputs = tokenizer(
"The Le Décret Pain states that a baguette must,"
, return_tensors=
"pt"
) outputs = model.generate(**inputs, do_sample=
False
, max_new_tokens=
50
, cache_implementation=
"offloaded"
)
Parallelism
distributes a model across devices so models too big for one device run fast. This approach uses more memory due to sharding overhead and communication to sync results.
Tensor parallelism
splits a model layer across devices. Set the number of devices with
DistributedConfig(tp_size=N)
and pass it to
from_pretrained()
to enable it.
Copied
from
transformers
import
AutoModelForCausalLM, DistributedConfig distributed_config = DistributedConfig(tp_size=
4
) model = AutoModelForCausalLM.from_pretrained(
"meta-llama/Meta-Llama-3-8B-Instruct"
, distributed_config=distributed_config, )
print
(model._tp_plan)
Continuous batching
maximizes throughput by keeping the GPU busy with dynamic scheduling and chunked prefill.
Serving
applications use it to process multiple incoming requests concurrently.
Use
generate_batch()
to enable continuous batching.
Copied
import
torch
from
transformers
import
AutoModelForCausalLM, AutoTokenizer
from
transformers.generation
import
ContinuousBatchingConfig, GenerationConfig model = AutoModelForCausalLM.from_pretrained(
"Qwen/Qwen3-0.6B"
, attn_implementation=
"paged|sdpa"
, device_map=
"auto"
, torch_dtype=torch.bfloat16, ) tokenizer = AutoTokenizer.from_pretrained(
"Qwen/Qwen3-0.6B"
) prompts = [
"The Le Décret Pain states that a baguette must"
,
"Explain gravity in one sentence."
,
"Name the capital of France."
, ] inputs = [tokenizer.encode(p)
for
p
in
prompts] generation_config = GenerationConfig( max_new_tokens=
32
, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id, do_sample=
False
, ) continuous_batching_config = ContinuousBatchingConfig(max_batch_tokens=
512
) outputs = model.generate_batch( inputs=inputs, generation_config=generation_config, continuous_batching_config=continuous_batching_config, )
for
request_id, output
in
outputs.items(): text = tokenizer.decode(output.generated_tokens, skip_special_tokens=
True
)
print
(
f"[
{request_id}
]
{text}
"
)
Update
on GitHub
←
Perplexity of fixed-length models
Attention backends
→