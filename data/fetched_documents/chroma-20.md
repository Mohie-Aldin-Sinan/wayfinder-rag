Embedding Functions - Chroma Docs
/llms.txt
Use this file to discover all available pages before exploring further.
Chroma Docs
home page
Search...
⌘
K
Ask Assistant
⌘
I
Search...
Navigation
Embeddings
Embedding Functions
Docs
Chroma Cloud
Guides
Integrations
Reference
Embeddings
Embedding Functions
Copy page
Learn how to use embedding functions in Chroma to create vector representations of your data.
Copy page
Embeddings are numeric representations of your data that capture meaning in a form AI models can work with. They can represent text, images, and eventually audio and video. Chroma stores and indexes embeddings so you can efficiently search for similar content. You can generate them locally with an installed library or remotely through an API.
Python
TypeScript
Rust
​
Using Embedding Functions
Embedding functions can be linked to a collection and used whenever you call
add
,
update
,
upsert
or
query
.
For example, this is how you use the OpenAI embedding function:
# Set your OPENAI_API_KEY environment variable
from
chromadb.utils.embedding_functions
import
OpenAIEmbeddingFunction
collection
=
client.create_collection(
name
=
"my_collection"
,
embedding_function
=
OpenAIEmbeddingFunction(
model_name
=
"text-embedding-3-small"
)
# Chroma will use OpenAIEmbeddingFunction to embed your documents
collection.add(
ids
=
[
"id1"
,
"id2"
],
documents
=
[
"doc1"
,
"doc2"
]
)
You can also use embedding functions directly which can be handy for debugging.
from
chromadb.utils.embedding_functions
import
DefaultEmbeddingFunction
default_ef
=
DefaultEmbeddingFunction()
embeddings
=
default_ef([
"foo"
])
print
(embeddings)
# [[0.05035809800028801, 0.0626462921500206, -0.061827320605516434...]]
collection.query(
query_embeddings
=
embeddings)
​
Custom Embedding Functions
You can create your own embedding function to use with Chroma; it just needs to implement
EmbeddingFunction
.
from
typing
import
Dict, Any
from
chromadb
import
Documents, EmbeddingFunction, Embeddings
from
chromadb.utils.embedding_functions
import
register_embedding_function
@register_embedding_function
class
MyEmbeddingFunction
(
EmbeddingFunction
):
def
__init__
(
self
,
model
):
self
.model
=
model
def
__call__
(
self
,
input
: Documents) -> Embeddings:
# embed the documents somehow
return
embeddings
@
staticmethod
def
name
() ->
str
:
return
"my-ef"
def
get_config
(
self
) -> Dict[
str
, Any]:
return
dict
(
model
=
self
.model)
@
staticmethod
def
build_from_config
(
config
: Dict[
str
, Any]) ->
"EmbeddingFunction"
:
return
MyEmbeddingFunction(config[
'model'
])
​
Default: all-MiniLM-L6-v2
Chroma’s default embedding function uses the
Sentence Transformers
all-MiniLM-L6-v2
model to create embeddings. This embedding model can create sentence and document embeddings that can be used for a wide variety of tasks. This embedding function runs locally on your machine, and may require you to download the model files (this will happen automatically).
If you don’t specify an embedding function when creating a collection, Chroma will set it to be the
DefaultEmbeddingFunction
:
collection
=
client.create_collection(
name
=
"my_collection"
)
​
Using Embedding Functions
Embedding functions can be linked to a collection and used whenever you call
add
,
update
,
upsert
or
query
.
For example, this is how you use the OpenAI embedding function:
Install the
@chroma-core/openai
package:
npm
pnpm
bun
yarn
npm
install
@chroma-core/openai
pnpm
add
@chroma-core/openai
bun
add
@chroma-core/openai
yarn
add
@chroma-core/openai
Create a collection with the
OpenAIEmbeddingFunction
:
// Set your OPENAI_API_KEY environment variable
import
{
OpenAIEmbeddingFunction
}
from
"@chroma-core/openai"
;
collection
=
await
client
.
createCollection
({
name:
"my_collection"
,
embedding_function:
new
OpenAIEmbeddingFunction
({
modelName:
"text-embedding-3-small"
,
}),
});
// Chroma will use OpenAIEmbeddingFunction to embed your documents
await
collection
.
add
({
ids:
[
"id1"
,
"id2"
],
documents:
[
"doc1"
,
"doc2"
],
});
You can also use embedding functions directly which can be handy for debugging.
import
{
DefaultEmbeddingFunction
}
from
"@chroma-core/default-embed"
;
const
defaultEF
=
new
DefaultEmbeddingFunction
();
const
embeddings
=
await
defaultEF
.
generate
([
"foo"
]);
console
.
log
(
embeddings
);
// [[0.05035809800028801, 0.0626462921500206, -0.061827320605516434...]]
await
collection
.
query
({
queryEmbeddings:
embeddings
});
​
Custom Embedding Functions
You can create your own embedding function to use with Chroma; it just needs to implement
EmbeddingFunction
.
export
interface
MyEmbeddingConfig
{
model
:
string
;
}
export
class
MyEmbeddingFunction
implements
EmbeddingFunction
{
public
readonly
name
=
"my-embedding-function"
;
private
readonly
model
:
string
;
constructor
(
args
:
{
model
:
string
}) {
this
.
model
=
args
.
model
;
}
async
generate
(
texts
:
string
[])
:
Promise
<
number
[][]> {
// embed the documents somehow
return
[];
}
getConfig
()
:
MyEmbeddingConfig
{
return
{
model:
this
.
model
,
};
}
validateConfigUpdate
(
config
:
Record
<
string
,
any
>) {
if
(
"model"
in
config
) {
throw
new
ChromaValueError
(
"Model cannot be updated"
);
}
static
buildFromConfig
(
config
:
MyEmbeddingConfig
,
_client
?:
ChromaClient
,
)
:
MyEmbeddingFunction
{
return
new
MyEmbeddingFunction
(
config
);
}
We welcome contributions! If you create an embedding function that you think would be useful to others, please consider
submitting a pull request
.
​
Default: all-MiniLM-L6-v2
Chroma’s default embedding function uses the
Sentence Transformers
all-MiniLM-L6-v2
model to create embeddings. This embedding model can create sentence and document embeddings that can be used for a wide variety of tasks. This embedding function runs locally on your machine, and may require you to download the model files (this will happen automatically).
If you don’t specify an embedding function when creating a collection, install the
@chroma-core/default-embed
package:
npm
pnpm
bun
yarn
npm
install
@chroma-core/default-embed
pnpm
add
@chroma-core/default-embed
bun
add
@chroma-core/default-embed
yarn
add
@chroma-core/default-embed
Create a collection without providing an embedding function. It will automatically be set with the
DefaultEmbeddingFunction
:
const
collection
=
await
client
.
createCollection
({
name:
"my-collection"
});
The Rust client expects embeddings to be provided directly. Use your provider SDK to generate embeddings, then pass them to
add
,
query
, and other methods.
let
embeddings
=
vec!
[
vec!
[
0.05
,
0.06
,
-
0.06
]];
collection
.
add
(
vec!
[
"id1"
.
to_string
()],
embeddings
,
Some
(
vec!
[
Some
(
"doc1"
.
to_string
())]),
None
,
None
,
)
.
await
?
;
​
All Embedding Functions
Chroma provides lightweight wrappers around popular embedding providers, making it easy to use them in your apps. You can set an embedding function when you
create
a Chroma collection, to be automatically used when adding and querying data, or you can call them directly yourself.
Python
Typescript
Cloudflare Workers AI
✓
Cohere
✓
Google Generative AI
✓
Hugging Face
✓
-
Hugging Face Embedding Server
✓
Jina AI
✓
Mistral
✓
Morph
✓
OpenAI
✓
Sentence Transformers
✓
Together AI
✓
For TypeScript users, Chroma provides packages for a number of embedding model providers. The Chromadb python package ships with all embedding functions included.
Provider
Embedding Function Package
All (installs all packages)
@chroma-core/all
Cloudflare Workers AI
@chroma-core/cloudflare-worker-ai
Cohere
@chroma-core/cohere
Google Gemini
@chroma-core/google-gemini
Hugging Face Server
@chroma-core/huggingface-server
Jina
@chroma-core/jina
Mistral
@chroma-core/mistral
Morph
@chroma-core/morph
Ollama
@chroma-core/ollama
OpenAI
@chroma-core/openai
Perplexity
@chroma-core/perplexity
Qwen (via Chroma Cloud)
@chroma-core/chroma-cloud-qwen
Sentence Transformers
@chroma-core/sentence-transformer
Together AI
@chroma-core/together-ai
Voyage AI
@chroma-core/voyageai
We welcome contributions! If you create an embedding function that you think would be useful to others, please consider
submitting a pull request
.
Was this page helpful?
Yes
No
Suggest edits
Assistant
Responses are generated using AI and may contain mistakes.
Contact support