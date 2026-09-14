Models · Hugging Face
Hugging Face
Transformers documentation
Models
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
Models
The base class
PreTrainedModel
implements the common methods for loading/saving a model either from a local file or directory, or from a pretrained model configuration provided by the library (downloaded from HuggingFace’s Hub).
PreTrainedModel
also implements a few methods which are common among all the models to:
resize the input token embeddings when new tokens are added to the vocabulary
The other methods that are common to each model are defined in
ModuleUtilsMixin
and
GenerationMixin
.
PreTrainedModel
class
transformers.
PreTrainedModel
<
source
>
(
config
: PreTrainedConfig
*inputs
**kwargs
)
Base class for all models.
PreTrainedModel
takes care of storing the configuration of the models and handles methods for loading, downloading and saving models as well as a few methods common to all models to:
resize the input embeddings
Class attributes (overridden by derived classes):
config_class
(
PreTrainedConfig
) — A subclass of
PreTrainedConfig
to use as configuration class for this model architecture.
base_model_prefix
(
str
) — A string indicating the attribute associated to the base model in derived classes of the same architecture adding modules on top of the base model.
main_input_name
(
str
) — The name of the principal input to the model (often
input_ids
for NLP models,
pixel_values
for vision models and
input_values
for speech models).
can_record_outputs
(dict):
push_to_hub
<
source
>
(
repo_id
: str
commit_message
: str | None = None
commit_description
: str | None = None
private
: bool | None = None
token
: bool | str | None = None
revision
: str | None = None
create_pr
: bool = False
max_shard_size
: int | str | None = '50GB'
tags
: list[str] | None = None
)
Parameters
repo_id
(
str
) — The name of the repository you want to push your model to. It should contain your organization name when pushing to a given organization.
commit_message
(
str
,
optional
) — Message to commit while pushing. Will default to
"Upload model"
.
commit_description
(
str
,
optional
) — The description of the commit that will be created
private
(
bool
,
optional
) — Whether to make the repo private. If
None
(default), the repo will be public unless the organization’s default is private. This value is ignored if the repo already exists.
token
(
bool
or
str
,
optional
) — The token to use as HTTP bearer authorization for remote files. If
True
(default), will use the token generated when running
hf auth login
(stored in
~/.huggingface
).
revision
(
str
,
optional
) — Branch to push the uploaded files to.
create_pr
(
bool
,
optional
, defaults to
False
) — Whether or not to create a PR with the uploaded files or directly commit.
max_shard_size
(
int
or
str
,
optional
, defaults to
"50GB"
) — Only applicable for models. The maximum size for a checkpoint before being sharded. Checkpoints shard will then be each of size lower than this size. If expressed as a string, needs to be digits followed by a unit (like
"5MB"
).
tags
(
list[str]
,
optional
) — List of tags to push on the Hub.
Upload the model file to the 🤗 Model Hub.
Examples:
Copied
from
transformers
import
AutoModel model = AutoModel.from_pretrained(
"google-bert/bert-base-cased"
)
# Push the model to your namespace with the name "my-finetuned-bert".
model.push_to_hub(
"my-finetuned-bert"
)
# Push the model to an organization with the name "my-finetuned-bert".
model.push_to_hub(
"huggingface/my-finetuned-bert"
)
add_model_tags
<
source
>
(
tags
: list[str] | str
)
Parameters
tags
(
Union[list[str], str]
) — The desired tags to inject in the model
Add custom tags into the model that gets pushed to the Hugging Face Hub. Will not overwrite existing tags in the model.
Examples:
Copied
from
transformers
import
AutoModel model = AutoModel.from_pretrained(
"google-bert/bert-base-cased"
) model.add_model_tags([
"custom"
,
"custom-bert"
])
# Push the model to your namespace with the name "my-custom-bert".
model.push_to_hub(
"my-custom-bert"
)
can_generate
<
source
>
(
)
→
bool
Returns
bool
Whether this model can generate sequences with
.generate()
.
Returns whether this model can generate sequences with
.generate()
, from the
GenerationMixin
or one with a similar interface.
Under the hood, on classes where this function returns True, some generation-specific changes are triggered: for instance, the model instance will have a populated
generation_config
attribute.
cuda
(
*args
**kwargs
)
A mock value for a dotted path (e.g.
torch.float32
): attribute access chains, calls behave as pass-through decorators,
repr
is the dotted path, and using it as a base class substitutes a plain-
type
base (PEP 560
__mro_entries__
), so real subclasses keep a normal metaclass and
inspect.signature
reads their real
__init__
instead of a mock’s.
dequantize
<
source
>
(
dtype
= None
)
Potentially dequantize the model in case it has been quantized by a quantization method that support dequantization.
disable_input_require_grads
<
source
>
(
)
Removes the
_require_grads_hook
.
enable_input_require_grads
<
source
>
(
)
Enables the gradients for the input embeddings. This is useful for fine-tuning adapter weights while keeping the model weights fixed.
from_pretrained
<
source
>
(
pretrained_model_name_or_path
: str | os.PathLike | None
*model_args
config
: transformers.configuration_utils.PreTrainedConfig | str | os.PathLike | None = None
cache_dir
: str | os.PathLike | None = None
ignore_mismatched_sizes
: bool = False
force_download
: bool = False
local_files_only
: bool = False
token
: str | bool | None = None
revision
: str = 'main'
use_safetensors
: bool | None = None
weights_only
: bool = True
fusion_config
: dict[str, bool | dict[str, typing.Any]] | None = None
disable_mmap
: bool | None = None
**kwargs
)
Parameters
pretrained_model_name_or_path
(
str
or
os.PathLike
,
optional
) — Can be either:
A string, the
model id
of a pretrained model hosted inside a model repo on huggingface.co.
A path to a
directory
containing model weights saved using
save_pretrained()
, e.g.,
./my_model_directory/
.
None
if you are both providing the configuration and state dictionary (resp. with keyword arguments
config
and
state_dict
).
model_args
(sequence of positional arguments,
optional
) — All remaining positional arguments will be passed to the underlying model’s
__init__
method.
config
(
Union[PreTrainedConfig, str, os.PathLike]
,
optional
) — Can be either:
an instance of a class derived from
PreTrainedConfig
,
a string or path valid as input to
from_pretrained()
.
Configuration for the model to use instead of an automatically loaded configuration. Configuration can be automatically loaded when:
The model is a model provided by the library (loaded with the
model id
string of a pretrained model).
The model was saved using
save_pretrained()
and is reloaded by supplying the save directory.
The model is loaded by supplying a local directory as
pretrained_model_name_or_path
and a configuration JSON file named
config.json
is found in the directory.
state_dict
(
dict[str, torch.Tensor]
,
optional
) — A state dictionary to use instead of a state dictionary loaded from saved weights file.
This option can be used if you want to create a model from a pretrained configuration but load your own weights. In this case though, you should check if using
save_pretrained()
and
from_pretrained()
is not a simpler option.
cache_dir
(
Union[str, os.PathLike]
,
optional
) — Path to a directory in which a downloaded pretrained model configuration should be cached if the standard cache should not be used.
ignore_mismatched_sizes
(
bool
,
optional
, defaults to
False
) — Whether or not to raise an error if some of the weights from the checkpoint do not have the same size as the weights of the model (if for instance, you are instantiating a model with 10 labels from a checkpoint with 3 labels).
force_download
(
bool
,
optional
, defaults to
False
) — Whether or not to force the (re-)download of the model weights and configuration files, overriding the cached versions if they exist.
proxies
(
dict[str, str]
,
optional
) — A dictionary of proxy servers to use by protocol or endpoint, e.g.,
{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}
. The proxies are used on each request.
output_loading_info(
bool
,
optional
, defaults to
False
) — Whether or not to also return a dictionary containing missing keys, unexpected keys and error messages.
local_files_only(
bool
,
optional
, defaults to
False
) — Whether or not to only look at local files (i.e., do not try to download the model).
token
(
str
or
bool
,
optional
) — The token to use as HTTP bearer authorization for remote files. If
True
, or not specified, will use the token generated when running
hf auth login
(stored in
~/.huggingface
).
revision
(
str
,
optional
, defaults to
"main"
) — The specific model version to use. It can be a branch name, a tag name, or a commit id, since we use a git-based system for storing models and other artifacts on huggingface.co, so
revision
can be any identifier allowed by git.
To test a pull request you made on the Hub, you can pass
revision="refs/pr/<pr_number>"
.
attn_implementation
(
str
,
optional
) — The attention implementation to use in the model (if relevant). Can be any of
"eager"
(manual implementation of the attention)
"sdpa"
(using
F.scaled_dot_product_attention
)
"flash_attention_2"
(using
Dao-AILab/flash-attention
)
"flash_attention_3"
(using
Dao-AILab/flash-attention/hopper
)
"flash_attention_4"
(using
Dao-AILab/flash-attention/flash_attn/cute
). By default, if available, SDPA will be used. The default is otherwise the manual
"eager"
implementation.
Accept HF kernel references in the form:
/
[@
][:
]
and
are any non-"/" and non-":" sequences.
“@
” is optional (branch, tag, or commit-ish), e.g. “@main”, “@v1.2.0”, “@abc123”.
”:
” is optional and selects a function inside the kernel repo.
Both options can appear together and in this order only: @revision first, then :kernel_name.
We intentionally allow a leading ”
|” prefix (e.g., “flash|…”) because the code strips it before loading; ’|’ is not excluded in the character classes here.
Examples that match: “org/model” “org/model@main” “org/model:custom_kernel” “org/
model@v1.2.3
:custom_kernel”
experts_implementation
(
str
,
optional
) — The experts implementation to use in the model (if relevant). Can be any of:
"eager"
(sequential implementation of the experts matrix multiplications).
"batched_mm"
(using
torch.bmm
).
"grouped_mm"
(using
torch.nn.functional.grouped_mm
).
By default, if the model supports it,
"grouped_mm"
will be used. The default is otherwise the manual
"eager"
implementation.
Parameters for big model inference
dtype
(
str
or
torch.dtype
,
optional
, defaults to
"auto"
) — Override the default
torch_dtype
and load the model under a specific
dtype
. The different options are:
torch.float16
or
torch.bfloat16
or
torch.float
: load in a specified
dtype
, ignoring the model’s
config.dtype
if one exists. If not specified
the model will get loaded in
torch.float
(fp32).
"auto"
- A
dtype
or
torch_dtype
entry in the
config.json
file of the model will be attempted to be used. If this entry isn’t found then next check the
dtype
of the first weight in the checkpoint that’s of a floating point type and use that as
dtype
. This will load the model using the
dtype
it was saved in at the end of the training. It can’t be used as an indicator of how the model was trained. Since it could be trained in one of half precision dtypes, but saved in fp32.
A string that is a valid
torch.dtype
. E.g. “float32” loads the model in
torch.float32
, “float16” loads in
torch.float16
etc.
For some models the
dtype
they were trained in is unknown - you may try to check the model’s paper or reach out to the authors and ask them to add this information to the model’s card and to insert the
dtype
or
torch_dtype
entry in
config.json
on the hub.
device_map
(
str
or
dict[str, Union[int, str, torch.device]]
or
int
or
torch.device
,
optional
) — A map that specifies where each submodule should go. It doesn’t need to be refined to each parameter/buffer name, once a given module name is inside, every submodule of it will be sent to the same device. If we only pass the device (
e.g.
,
"cpu"
,
"cuda:1"
,
"mps"
, or a GPU ordinal rank like
1
) on which the model will be allocated, the device map will map the entire model to this device. Passing
device_map = 0
means put the whole model on GPU 0.
To have Accelerate compute the most optimized
device_map
automatically, set
device_map="auto"
. For more information about each option see
designing a device map
.
max_memory
(
Dict
,
optional
) — A dictionary device identifier to maximum memory if using
device_map
. Will default to the maximum memory available for each GPU and the available CPU RAM if unset.
distributed_config
(
DistributedConfig
,
optional
) — Configuration for native distributed loading with tensor parallelism or FSDP2. Pass
DistributedConfig(tp_size=N)
to use a model’s predefined tensor parallel plan,
DistributedConfig(tp_plan=...)
to specify a tensor parallel plan, or
DistributedConfig(fsdp_size=N)
for FSDP2. Requires
torchrun
and an initialized process group when
tp_size > 1
or
fsdp_size > 1
. Mutually exclusive with
device_map
.
device_mesh
(
torch.distributed.DeviceMesh
,
optional
) — A torch device mesh. If not provided would default to world size. Used only for tensor parallel for now. If provided, it has to contain dimension named
"tp"
in case it’s > 1 dimensional, this dimension will be used for tensor parallelism
offload_folder
(
str
or
os.PathLike
,
optional
) — If the
device_map
contains any value
"disk"
, the folder where we will offload weights.
offload_buffers
(
bool
,
optional
) — Whether or not to offload the buffers with the model parameters.
quantization_config
(
Union[QuantizationConfigMixin,Dict]
,
optional
) — A dictionary of configuration parameters or a QuantizationConfigMixin object for quantization (e.g bitsandbytes, gptq).
subfolder
(
str
,
optional
, defaults to
""
) — In case the relevant files are located inside a subfolder of the model repo on huggingface.co, you can specify the folder name here.
variant
(
str
,
optional
) — If specified load weights from
variant
filename,
e.g.
pytorch_model.
.bin.
use_safetensors
(
bool
,
optional
, defaults to
None
) — Whether or not to use
safetensors
checkpoints. Defaults to
None
. If not specified and
safetensors
is not installed, it will be set to
False
.
weights_only
(
bool
,
optional
, defaults to
True
) — Indicates whether unpickler should be restricted to loading only tensors, primitive types, dictionaries and any types added via torch.serialization.add_safe_globals(). When set to False, we can load wrapper tensor subclass weights.
disable_mmap
(
bool
,
optional
) — Whether to disable memory mapping when loading safetensors checkpoints. When
None
(default), it is auto-detected to
True
when the checkpoint lives on an
hf-mount
FUSE filesystem (used by HF Spaces/Endpoints), where mmap + parallel page-faults can deadlock. When
True
, files are read fully into memory and parsed with
safetensors.torch.load
. When
False
, the default memory-mapped loader is always used.
fusion_config
(
dict[str, bool | dict[str, Any]]
,
optional
) — Optional fusion configuration applied before model instantiation. Each key enables a fusion family and its value can either be
True
to enable that fusion with default options or a dictionary of family-specific options. For example,
{"patch_embeddings": True}
enables patch embedding fusion. This should only be used as an inference optimization, as it can slightly change outputs. If omitted,
from_pretrained()
falls back to
config.fusion_config
when available. Refer to the fusion mapping guide in
docs/source/en/fusion_mapping.md
for more details.
key_mapping
(`dict[str, str],
optional
) — A potential mapping of the weight names if using a model on the Hub which is compatible to a Transformers architecture, but was not converted accordingly.
kwargs
(remaining dictionary of keyword arguments,
optional
) — Can be used to update the configuration object (after it being loaded) and initiate the model (e.g.,
output_attentions=True
). Behaves differently depending on whether a
config
is provided or automatically loaded:
If a configuration is provided with
config
,
**kwargs
will be directly passed to the underlying model’s
__init__
method (we assume all relevant updates to the configuration have already been done)
If a configuration is not provided,
kwargs
will be first passed to the configuration class initialization function (
from_pretrained()
). Each key of
kwargs
that corresponds to a configuration attribute will be used to override said attribute with the supplied
kwargs
value. Remaining keys that do not correspond to any configuration attribute will be passed to the underlying model’s
__init__
function.
Instantiate a pretrained pytorch model from a pre-trained model configuration.
The model is set in evaluation mode by default using
model.eval()
(Dropout modules are deactivated). To train the model, you should first set it back in training mode with
model.train()
.
The warning
Weights from XXX not initialized from pretrained model
means that the weights of XXX do not come pretrained with the rest of the model. It is up to you to train those weights with a downstream fine-tuning task.
The warning
Weights from XXX not used in YYY
means that the layer XXX is not used by YYY, therefore those weights are discarded.
Activate the special
“offline-mode”
to use this method in a firewalled environment.
Examples:
Copied
>>>
from
transformers
import
BertConfig, BertModel
>>>
# Download model and configuration from huggingface.co and cache.
>>>
model = BertModel.from_pretrained(
"google-bert/bert-base-uncased"
)
>>>
# Model was saved using *save_pretrained('./test/saved_model/')* (for example purposes, not runnable).
>>>
model = BertModel.from_pretrained(
"./test/saved_model/"
)
>>>
# Update configuration during loading.
>>>
model = BertModel.from_pretrained(
"google-bert/bert-base-uncased"
, output_attentions=
True
)
>>>
assert
model.config.output_attentions ==
True
get_compiled_call
<
source
>
(
compile_config
: transformers.generation.configuration_utils.CompileConfig | None
)
Return a
torch.compile
‘d version of
self.__call__
. This is useful to dynamically choose between non-compiled/compiled
forward
during inference, especially to switch between prefill (where we don’t want to use compiled version to avoid recomputing the graph with new shapes) and iterative decoding (where we want the speed-ups of compiled version with static shapes).
get_decoder
<
source
>
(
)
Best-effort lookup of the
decoder
module.
Order of attempts (covers ~85 % of current usages):
self.decoder/self.language_model/self.text_model
self.base_model
(many wrappers store the decoder here)
self.base_model.get_decoder()
(nested wrappers)
fallback: raise for the few exotic models that need a bespoke rule
get_encoder
<
source
>
(
modality
: str | None = None
)
Best-effort lookup of the
encoder
module. If provided with
modality
argument, it looks for a modality-specific encoder in multimodal models (e.g. “image_encoder”) By default the function returns model’s text encoder if any, and otherwise returns
self
.
Possible
modality
values are “image”, “video” and “audio”.
get_expanded_tied_weights_keys
<
source
>
(
all_submodels
: bool = False
)
Return the expanded tied weight keys (in case they contain modules or regex patterns) for only the current model, or recursively for all submodels if
all_submodels=True
(i.e. it will re-check the config values for all submodels).
For almost all models, we only require to tie the embeddings, so the model has an internal property
_tied_weights_keys = {"lm_head.weight": "model.embed_tokens.weight"}
. In this case, the mapping is already “expanded”, i.e. it already contains full parameters, and this function will simply return a copy of the property. For more complex patterns, e.g. for
DFineForObjectDetection
, we have the following attribute
Copied
_tied_weights_keys = {
r"bbox_embed.(?![0])\d+"
:
"bbox_embed.0"
,
r"class_embed.(?![0])\d+"
:
"class_embed.0"
,
"model.decoder.class_embed"
:
"class_embed"
,
"model.decoder.bbox_embed"
:
"bbox_embed"
, }
In this case, the function looks up all the model's parameters and buffers, and matches all the params,
returning the following:
Copied
{
'bbox_embed
.
1.
layers.
0.
bias':
'bbox_embed
.
0.
layers.
0.
bias',
'bbox_embed
.
1.
layers.
0.
weight':
'bbox_embed
.
0.
layers.
0.
weight',
'bbox_embed
.
1.
layers.
1.
bias':
'bbox_embed
.
0.
layers.
1.
bias',
'bbox_embed
.
1.
layers.
1.
weight':
'bbox_embed
.
0.
layers.
1.
weight',
'bbox_embed
.
1.
layers.
2.
bias':
'bbox_embed
.
0.
layers.
2.
bias',
'bbox_embed
.
1.
layers.
2.
weight':
'bbox_embed
.
0.
layers.
2.
weight',
'bbox_embed
.
2.
layers.
0.
bias':
'bbox_embed
.
0.
layers.
0.
bias',
'bbox_embed
.
2.
layers.
0.
weight':
'bbox_embed
.
0.
layers.
0.
weight', ...
'class_embed
.
1.
bias':
'class_embed
.
0.
bias',
'class_embed
.
1.
weight':
'class_embed
.
0.
weight',
'class_embed
.
2.
bias':
'class_embed
.
0.
bias',
'class_embed
.
2.
weight':
'class_embed
.
0.
weight', ...
'model
.decoder.class_embed.
0.
bias':
'class_embed
.
0.
bias',
'model
.decoder.class_embed.
0.
weight':
'class_embed
.
0.
weight',
'model
.decoder.class_embed.
1.
bias':
'class_embed
.
0.
bias',
'model
.decoder.class_embed.
1.
weight':
'class_embed
.
0.
weight', ...
'model
.decoder.bbox_embed.
0.
layers.
0.
bias':
'bbox_embed
.
0.
layers.
0.
bias',
'model
.decoder.bbox_embed.
0.
layers.
0.
weight':
'bbox_embed
.
0.
layers.
0.
weight',
'model
.decoder.bbox_embed.
0.
layers.
1.
bias':
'bbox_embed
.
0.
layers.
1.
bias',
'model
.decoder.bbox_embed.
0.
layers.
1.
weight':
'bbox_embed
.
0.
layers.
1.
weight', ... }
i.e. all the parameters matching the regex and modules patterns in `_tied_weights_keys`
get_experts_implementation
<
source
>
(
)
Return the experts implementation of this model and its submodels, as a
dict
in the form accepted by
set_experts_implementation
(
""
for this model, and one entry per sub_config). This is the counterpart of
set_experts_implementation
, e.g. to snapshot the current implementation and later restore it.
get_memory_footprint
<
source
>
(
return_buffers
= True
)
Parameters
return_buffers
(
bool
,
optional
, defaults to
True
) — Whether to return the size of the buffer tensors in the computation of the memory footprint. Buffers are tensors that do not require gradients and not registered as parameters. E.g. mean and std in batch norm layers. Please see:
https://discuss.pytorch.org/t/what-pytorch-means-by-buffers/120266/2
Get the memory footprint of a model. This will return the memory footprint of the current model in bytes. Useful to benchmark the memory footprint of the current model and design some tests. Solution inspired from the PyTorch discussions:
https://discuss.pytorch.org/t/gpu-memory-that-model-uses/56822/2
get_parameter_or_buffer
<
source
>
(
target
: str
)
Return the parameter or buffer given by
target
if it exists, otherwise throw an error. This combines
get_parameter()
and
get_buffer()
in a single handy function. If the target is an
_extra_state
attribute, it will return the extra state provided by the module. Note that it only work if
target
is a leaf of the model.
gradient_checkpointing_disable
<
source
>
(
)
Deactivates gradient checkpointing for the current model.
gradient_checkpointing_enable
<
source
>
(
gradient_checkpointing_kwargs
= None
every_n_layers
: int = 1
offload
: bool = False
)
Parameters
every_n_layers
(
int
,
optional
, defaults to 1) — Checkpoint only every
every_n_layers
-th decoder layer, leaving the rest to keep their activations.
1
checkpoints every layer, which is the usual all-or-nothing behavior. Larger values trade memory back for speed, which is worth it whenever the memory freed by full checkpointing is going unused.
offload
(
bool
,
optional
, defaults to
False
) — Hold the activations saved for the recompute in pinned host memory rather than on the accelerator. This frees
layers x sequence x hidden
bytes of device memory, which is what dominates at long sequence lengths, and costs a device-to-host copy in the forward and a host-to-device copy in the backward. Both copies run on the compute stream, so the step gets slower.
gradient_checkpointing_kwargs
(dict,
optional
) — Additional keyword arguments passed along to the
torch.utils.checkpoint.checkpoint
function.
Activates gradient checkpointing for the current model.
We pass the
__call__
method of the modules instead of
forward
because
__call__
attaches all the hooks of the module.
https://discuss.pytorch.org/t/any-different-between-model-input-and-model-forward-input/3690/2
init_weights
<
source
>
(
)
Initialize and tie the weights if needed. If using a custom
PreTrainedModel
, you need to implement any initialization logic in
_init_weights
.
initialize_weights
<
source
>
(
)
This is equivalent to calling
self.apply(self._initialize_weights)
, but correctly handles composite models. This function dynamically dispatches the correct
init_weights
function to the modules as we advance in the module graph along the recursion. It can handle an arbitrary number of sub-models. Without it, every composite model would have to recurse a second time on all sub-models explicitly in the outer-most
_init_weights
, which is extremely error prone and inefficient.
is_custom_code
<
source
>
(
)
Return whether the current model is custom code, i.e. either code loaded from the hub, or defined in any user-specific module/session.
is_remote_code
<
source
>
(
)
Return whether the current model is custom code, i.e. code loaded from the hub, or class that we just registered via
register_for_auto_class
.
mark_tied_weights_as_initialized
<
source
>
(
loading_info
)
Adds the
_is_hf_initialized
flag on parameters that will be tied, in order to avoid initializing them later as they will be tied (overwritten) anyway. This is very important as most embeddings are tied, and they are huge params (vocabularies are often 256k), so running inits on them is very costly.
named_non_persistent_buffers
<
source
>
(
recurse
: bool = True
remove_duplicate
: bool = True
)
Similar to
named_buffers
, but only yield non-persistent ones. It is handy as it’s not perfectly straightforward to know if they are persistent or not
post_init
<
source
>
(
)
A method executed at the end of each Transformer model initialization, to execute code that needs the model’s modules properly initialized (such as weight initialization). It is also used to obtain all correct static properties (parallelism plans, tied_weights_keys, _keep_in_fp32_modules, etc) correctly in the case of composite models (that is, the top level model should know about those properties from its children).
register_for_auto_class
<
source
>
(
auto_class
= 'AutoModel'
)
Parameters
auto_class
(
str
or
type
,
optional
, defaults to
"AutoModel"
) — The auto class to register this new model with.
Register this class with a given auto class. This should only be used for custom models as the ones in the library are already mapped with an auto class.
resize_token_embeddings
<
source
>
(
new_num_tokens
: int | None = None
pad_to_multiple_of
: int | None = None
mean_resizing
: bool = True
)
→
torch.nn.Embedding
Parameters
new_num_tokens
(
int
,
optional
) — The new number of tokens in the embedding matrix. Increasing the size will add newly initialized vectors at the end. Reducing the size will remove vectors from the end. If not provided or
None
, just returns a pointer to the input tokens
torch.nn.Embedding
module of the model without doing anything.
pad_to_multiple_of
(
int
,
optional
) — If set will pad the embedding matrix to a multiple of the provided value.If
new_num_tokens
is set to
None
will just pad the embedding to a multiple of
pad_to_multiple_of
.
This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability
>= 7.5
(Volta), or on TPUs which benefit from having sequence lengths be a multiple of 128. For more details about this, or help on choosing the correct value for resizing, refer to this guide:
https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#requirements-tc
mean_resizing
(
bool
) — Whether to initialize the added embeddings from a multivariate normal distribution that has old embeddings’ mean and covariance or to initialize them with a normal distribution that has a mean of zero and std equals
config.initializer_range
.
Setting
mean_resizing
to
True
is useful when increasing the size of the embeddings of causal language models, where the generated tokens’ probabilities won’t be affected by the added embeddings because initializing the new embeddings with the old embeddings’ mean will reduce the kl-divergence between the next token probability before and after adding the new embeddings. Refer to this article for more information:
https://nlp.stanford.edu/~johnhew/vocab-expansion.html
Returns
torch.nn.Embedding
Pointer to the input tokens Embeddings Module of the model.
Resizes input token embeddings matrix of the model if
new_num_tokens != config.vocab_size
.
Takes care of tying weights embeddings afterwards if the model class has a
tie_weights()
method.
save_pretrained
<
source
>
(
save_directory
: str | os.PathLike
is_main_process
: bool = True
state_dict
: dict | None = None
push_to_hub
: bool = False
max_shard_size
: int | str = '50GB'
variant
: str | None = None
token
: str | bool | None = None
save_peft_format
: bool = True
save_original_format
: bool = True
distributed_checkpoint
: bool = False
**kwargs
)
Parameters
save_directory
(
str
or
os.PathLike
) — Directory to which to save. Will be created if it doesn’t exist.
is_main_process
(
bool
,
optional
, defaults to
True
) — Whether the process calling this is the main process or not. Useful when in distributed training like TPUs and need to call this function on all processes. In this case, set
is_main_process=True
only on the main process to avoid race conditions.
state_dict
(nested dictionary of
torch.Tensor
) — The state dictionary of the model to save. Will default to
self.state_dict()
, but can be used to only save parts of the model or if special precautions need to be taken when recovering the state dictionary of a model (like when using model parallelism).
push_to_hub
(
bool
,
optional
, defaults to
False
) — Whether or not to push your model to the Hugging Face model hub after saving it. You can specify the repository you want to push to with
repo_id
(will default to the name of
save_directory
in your namespace).
max_shard_size
(
int
or
str
,
optional
, defaults to
"50GB"
) — The maximum size for a checkpoint before being sharded. Checkpoints shard will then be each of size lower than this size. If expressed as a string, needs to be digits followed by a unit (like
"5MB"
).
If a single weight of the model is bigger than
max_shard_size
, it will be in its own checkpoint shard which will be bigger than
max_shard_size
.
variant
(
str
,
optional
) — If specified, weights are saved in the format model.
.safetensors.
token
(
str
or
bool
,
optional
) — The token to use as HTTP bearer authorization for remote files. If
True
, or not specified, will use the token generated when running
hf auth login
(stored in
~/.huggingface
).
save_peft_format
(
bool
,
optional
, defaults to
True
) — For backward compatibility with PEFT library, in case adapter weights are attached to the model, all keys of the state dict of adapters needs to be prepended with
base_model.model
. Advanced users can disable this behaviours by setting
save_peft_format
to
False
.
save_original_format
(
bool
,
optional
, defaults to
True
) — For backward compatibility with the previous versions of
transformers
you can save the checkpoint with its reverse mapping. The reverse mapping needs to exists even if the model was loaded from a None legacy checkpoint.
distributed_checkpoint
(
bool
,
optional
, defaults to
False
) — When saving an FSDP-wrapped model, use the distributed checkpoint (DCP) path instead of gathering weights to CPU first. Every rank must call this method; rank 0 writes the consolidated Hugging Face safetensors. When
False
, FSDP weights are gathered to CPU on rank 0 via
gather_full_state_dict
before writing. Native FSDP requires
torch>=2.7
.
kwargs
(
dict[str, Any]
,
optional
) — Additional key word arguments passed along to the
push_to_hub()
method.
Save a model and its configuration file to a directory, so that it can be re-loaded using the
from_pretrained()
class method.
set_attn_implementation
<
source
>
(
attn_implementation
: str | dict
allow_all_kernels
: bool = False
)
Parameters
attn_implementation
(
str
or
dict
) — The attention implementation to set for this model. It can be either a
str
, in which case it will be dispatched to all submodels if relevant, or a
dict
where keys are the sub_configs name, in which case each submodel will dispatch the corresponding value.
allow_all_kernels
(
bool
, optional) — Whether to load kernels from unverified hub repos, if
attn_implementation
is a custom kernel outside of the
kernels-community
hub repository.
Set the requested
attn_implementation
for this model.
set_decoder
<
source
>
(
decoder
)
Symmetric setter. Mirrors the lookup logic used in
get_decoder
.
set_encoder
<
source
>
(
encoder
modality
: str | None = None
)
Symmetric setter. Mirrors the lookup logic used in
get_encoder
.
set_experts_implementation
<
source
>
(
experts_implementation
: str | dict
)
Parameters
experts_implementation
(
str
or
dict
) — The experts implementation to set for this model. It can be either a
str
, in which case it will be dispatched to all submodels if relevant, or a
dict
where keys are the sub_configs name, in which case each submodel will dispatch the corresponding value.
Set the requested
experts_implementation
for this model.
set_use_kernels
<
source
>
(
use_kernels
kernel_config
: transformers.utils.kernel_config.KernelConfig | None = None
mode
: Mode | None = None
)
Parameters
use_kernels
(
bool
) — Whether or not to use the
kernels
library to kernelize some layers of the model.
kernel_config
(
KernelConfig
,
optional
) — The kernel configuration to use to kernelize the model. If
None
, the default kernel mapping will be used.
mode
(
Mode
,
optional
) — The mode that should be applied during
kernelize
. Optional, defaults to either training or inference mode based on the internal
training
flag.
Set whether or not to use the
kernels
library to kernelize some layers of the model.
tie_weights
<
source
>
(
missing_keys
: set[str] | None = None
recompute_mapping
: bool = True
)
Tie the model weights. If
recompute_mapping=False
(default when called internally), it will rely on the
model.all_tied_weights_keys
attribute, containing the
{target: source}
mapping for the tied params. If
recompute_mapping=True
, it will re-check all internal submodels and their config to determine the params that need to be tied. This is the default when
model.tie_weights()
is called on its own, outside of
__init__
, and
from_pretrained
, in case the config values were changed somewhere.
Note that during
from_pretrained
, tying is
symmetric
: if the mapping says “tie target -> source” but
source
is missing in the checkpoint while
target
exists, we
swap
source and target so we can still tie everything to the parameter that actually exists.
to
(
*args
**kwargs
)
A mock value for a dotted path (e.g.
torch.float32
): attribute access chains, calls behave as pass-through decorators,
repr
is the dotted path, and using it as a base class substitutes a plain-
type
base (PEP 560
__mro_entries__
), so real subclasses keep a normal metaclass and
inspect.signature
reads their real
__init__
instead of a mock’s.
warn_if_padding_and_no_attention_mask
<
source
>
(
input_ids
attention_mask
)
Shows a one-time warning if the input_ids appear to contain padding and no attention mask was given.
Custom models should also include a
_supports_assign_param_buffer
, which determines if superfast init can apply on the particular model. Signs that your model needs this are if
test_save_and_load_from_pretrained
fails. If so, set this to
False
.
ModuleUtilsMixin
class
transformers.modeling_utils.
ModuleUtilsMixin
<
source
>
(
)
A few utilities for
torch.nn.Modules
, to be used as a mixin.
num_parameters
<
source
>
(
only_trainable
: bool = False
exclude_embeddings
: bool = False
)
→
int
Parameters
only_trainable
(
bool
,
optional
, defaults to
False
) — Whether or not to return only the number of trainable parameters
exclude_embeddings
(
bool
,
optional
, defaults to
False
) — Whether or not to return only the number of non-embeddings parameters
Returns
int
The number of parameters.
Get number of (optionally, trainable or non-embeddings) parameters in the module.
Pushing to the Hub
class
transformers.utils.
PushToHubMixin
<
source
>
(
)
A Mixin containing the functionality to push a model or tokenizer to the hub.
push_to_hub
<
source
>
(
repo_id
: str
commit_message
: str | None = None
commit_description
: str | None = None
private
: bool | None = None
token
: bool | str | None = None
revision
: str | None = None
create_pr
: bool = False
max_shard_size
: int | str | None = '50GB'
tags
: list[str] | None = None
)
Parameters
repo_id
(
str
) — The name of the repository you want to push your {object} to. It should contain your organization name when pushing to a given organization.
commit_message
(
str
,
optional
) — Message to commit while pushing. Will default to
"Upload {object}"
.
commit_description
(
str
,
optional
) — The description of the commit that will be created
private
(
bool
,
optional
) — Whether to make the repo private. If
None
(default), the repo will be public unless the organization’s default is private. This value is ignored if the repo already exists.
token
(
bool
or
str
,
optional
) — The token to use as HTTP bearer authorization for remote files. If
True
(default), will use the token generated when running
hf auth login
(stored in
~/.huggingface
).
revision
(
str
,
optional
) — Branch to push the uploaded files to.
create_pr
(
bool
,
optional
, defaults to
False
) — Whether or not to create a PR with the uploaded files or directly commit.
max_shard_size
(
int
or
str
,
optional
, defaults to
"50GB"
) — Only applicable for models. The maximum size for a checkpoint before being sharded. Checkpoints shard will then be each of size lower than this size. If expressed as a string, needs to be digits followed by a unit (like
"5MB"
).
tags
(
list[str]
,
optional
) — List of tags to push on the Hub.
Upload the {object_files} to the 🤗 Model Hub.
Examples:
Copied
from
transformers
import
{object_class} {
object
} = {object_class}.from_pretrained(
"google-bert/bert-base-cased"
)
# Push the {object} to your namespace with the name "my-finetuned-bert".
{
object
}.push_to_hub(
"my-finetuned-bert"
)
# Push the {object} to an organization with the name "my-finetuned-bert".
{
object
}.push_to_hub(
"huggingface/my-finetuned-bert"
)
Update
on GitHub
←
Logging
Text generation
→