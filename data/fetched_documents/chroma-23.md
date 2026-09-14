Getting Started - Chroma Docs
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
Overview
Getting Started
Docs
Chroma Cloud
Guides
Integrations
Reference
Overview
Getting Started
Copy page
Chroma is the open-source data infrastructure for AI. It comes with everything you need to get started built-in, and runs on your machine.
Copy page
Python
TypeScript
Rust
For production, Chroma offers
Chroma Cloud
- a fast, scalable, and serverless database-as-a-service. Get started in 30 seconds - $5 in free credits included.
​
Install with AI
Give the following prompt to Claude Code, Cursor, Codex, or your favorite AI agent. It will quickly set you up with Chroma.
Chroma Cloud
OSS
In this directory create a new Python project with Chroma set up.
Use a virtual environment.
Write a small example that adds some data to a collection and queries it.
Do not delete the data from the collection when it's complete.
Run the script when you are done setting up the environment and writing the
script. The output should show what data was ingested, what was the query,
and the results.
Your own summary should include this output so the user can see it.
First, install `chromadb`.
The project should be set up with Chroma Cloud. When you install `chromadb`,
you get access to the Chroma CLI. You can run `chroma login` to authenticate.
This will open a browser for authentication and save a connection profile
locally.
You can also use `chroma profile show` to see if the user already has an
active profile saved locally. If so, you can skip the login step.
Then create a DB using the CLI with `chroma db create chroma-getting-started`.
This will create a DB with this name.
Then use the CLI command `chroma db connect chroma-getting-started --env-file`.
This will create a .env file in the current directory with the connection
variables for this DB and account, so the CloudClient can be instantiated
with chromadb.CloudClient(api_key=os.getenv("CHROMA_API_KEY"), ...).
See all 28 lines
In this directory create a new Python project with Chroma set up.
Use a virtual environment.
Write a small example that adds some data to a collection and queries it.
Do not delete the data from the collection when it's complete.
Run the script when you are done setting up the environment and writing the
script. The output should show what data was ingested, what was the query,
and the results.
Your own summary should include this output so the user can see it.
Use Chroma's in-memory client: `chromadb.Client()`
​
Install Manually
1
Install
pip
poetry
uv
pip
install
chromadb
poetry
add
chromadb
uv
pip
install
chromadb
2
Create a Chroma Client
Python
import
chromadb
chroma_client
=
chromadb.Client()
3
Create a collection
Collections are where you’ll store your embeddings, documents, and any additional metadata. Collections index your embeddings and documents, and enable efficient retrieval and filtering. You can create a collection with a name:
Python
collection
=
chroma_client.create_collection(
name
=
"my_collection"
)
4
Add some text documents to the collection
Chroma will store your text and handle embedding and indexing automatically. You can also customize the embedding model. You must provide unique string IDs for your documents.
Python
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
"This is a document about pineapple"
,
"This is a document about oranges"
]
)
5
Query the collection
You can query the collection with a list of query texts, and Chroma will return the n most similar results. It’s that easy!
Python
results
=
collection.query(
query_texts
=
[
"This is a query document about hawaii"
],
# Chroma will embed this for you
n_results
=
2
# how many results to return
)
print
(results)
If n_results is not provided, Chroma will return 10 results by default. Here we only added 2 documents, so we set n_results=2.
6
Inspect Results
From the above - you can see that our query about hawaii is semantically most similar to the document about pineapple.
Python
{
'documents'
: [[
'This is a document about pineapple'
,
'This is a document about oranges'
]],
'ids'
: [[
'id1'
,
'id2'
]],
'distances'
: [[
1.0404009819030762
,
1.243080496788025
]],
'uris'
:
None
,
'data'
:
None
,
'metadatas'
: [[
None
,
None
]],
'embeddings'
:
None
,
}
7
Try it out yourself
What if we tried querying with “This is a document about florida”? Here is a full example.
Python
import
chromadb
chroma_client
=
chromadb.Client()
# switch \`create_collection\` to \`get_or_create_collection\` to avoid creating a new collection every time
collection
=
chroma_client.get_or_create_collection(
name
=
"my_collection"
)
# switch \`add\` to \`upsert\` to avoid adding the same documents every time
collection.upsert(
documents
=
[
"This is a document about pineapple"
,
"This is a document about oranges"
],
ids
=
[
"id1"
,
"id2"
]
)
results
=
collection.query(
query_texts
=
[
"This is a query document about florida"
],
# Chroma will embed this for you
n_results
=
2
# how many results to return
)
print
(results)
See all 21 lines
​
Next steps
In this guide we used Chroma’s
in-memory client
for simplicity. It starts a Chroma server in-memory, so any data you ingest will be lost when your program terminates. You can use the
persistent client
or run Chroma in
client-server mode
if you need data persistence.
Learn how to
Deploy Chroma
to a server
Join Chroma’s
Discord Community
to ask questions and get help
Follow Chroma on
X (@trychroma)
for updates
For production, Chroma offers
Chroma Cloud
- a fast, scalable, and serverless database-as-a-service. Get started in 30 seconds - $5 in free credits included.
​
Install with AI
Give the following prompt to Claude Code, Cursor, Codex, or your favorite AI agent. It will quickly set you up with Chroma.
Chroma Cloud
OSS
In this directory create a new Typescript project with Chroma set up.
Write a small example that adds some data to a collection and queries it.
Do not delete the data from the collection when it's complete.
Run the script when you are done setting up the environment and writing the
script. The output should show what data was ingested, what was the query,
and the results.
Your own summary should include this output so the user can see it.
First, install `chromadb`.
The project should be set up with Chroma Cloud. When you install `chromadb`,
you get access to the Chroma CLI. You can run `chroma login` to authenticate.
This will open a browser for authentication and save a connection profile
locally.
You can also use `chroma profile show` to see if the user already has an
active profile saved locally. If so, you can skip the login step.
Then create a DB using the CLI with `chroma db create chroma-getting-started`.
This will create a DB with this name.
Then use the CLI command `chroma db connect chroma-getting-started --env-file`.
This will create a .env file in the current directory with the connection
variables for this DB and account, so the CloudClient can be instantiated
with: new CloudClient().
See all 27 lines
In this directory create a new Typescript project with Chroma set up.
Write a small example that adds some data to a collection and queries it.
Do not delete the data from the collection when it's complete.
Run the script when you are done setting up the environment and writing the
script. The output should show what data was ingested, what was the query,
and the results.
Your own summary should include this output so the user can see it.
You will have to run a local Chroma server to make this work. When you install
`chromadb` you get access to the Chroma CLI, which can start a local server
for you with `chroma run`.
Make sure to instruct the user on how to start a local Chroma server in your
summary.
​
Install Manually
1
Install
npm
pnpm
bun
yarn
npm
install
chromadb
@chroma-core/default-embed
pnpm
add
chromadb
@chroma-core/default-embed
bun
add
chromadb
@chroma-core/default-embed
yarn
add
chromadb
@chroma-core/default-embed
2
Create a Chroma Client
Run the Chroma backend:
npm
pnpm
bun
yarn
docker
npx
chroma
run
--path
./getting-started
pnpm
exec
chroma
run
--path
./getting-started
bunx
chroma
run
--path
./getting-started
yarn
chroma
run
--path
./getting-started
docker
pull
chromadb/chroma
docker
run
-p
8000:8000
chromadb/chroma
Then create a client which connects to it:
TypeScript ESM
TypeScript CJS
import
{
ChromaClient
}
from
"chromadb"
;
const
client
=
new
ChromaClient
();
const
{
ChromaClient
}
=
require
(
"chromadb"
);
const
client
=
new
ChromaClient
();
3
Create a collection
Collections are where you’ll store your embeddings, documents, and any additional metadata. Collections index your embeddings and documents, and enable efficient retrieval and filtering. You can create a collection with a name:
TypeScript
const
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
});
4
Add some text documents to the collection
Chroma will store your text and handle embedding and indexing automatically. You can also customize the embedding model. You must provide unique string IDs for your documents.
TypeScript
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
"This is a document about pineapple"
,
"This is a document about oranges"
,
],
});
5
Query the collection
You can query the collection with a list of query texts, and Chroma will return the n most similar results. It’s that easy!
TypeScript
const
results
=
await
collection
.
query
({
queryTexts:
[
"This is a query document about hawaii"
],
// Chroma will embed this for you
nResults:
2
,
// how many results to return
});
console
.
log
(
results
);
If n_results is not provided, Chroma will return 10 results by default. Here we only added 2 documents, so we set n_results=2.
6
Inspect Results
From the above - you can see that our query about hawaii is semantically most similar to the document about pineapple.
TypeScript
{
documents
: [
[
'This is a document about pineapple'
,
'This is a document about oranges'
]
],
ids
: [
[
'id1'
,
'id2'
]
],
distances
: [[
1.0404009819030762
,
1.243080496788025
]],
uris
:
null
,
data
:
null
,
metadatas
: [[
null
,
null
]],
embeddings
:
null
}
7
Try it out yourself
What if we tried querying with “This is a document about florida”? Here is a full example.
TypeScript
import
{
ChromaClient
}
from
"chromadb"
;
const
client
=
new
ChromaClient
();
// switch `createCollection` to `getOrCreateCollection` to avoid creating a new collection every time
const
collection
=
await
client
.
getOrCreateCollection
({
name:
"my_collection"
,
});
// switch `addRecords` to `upsertRecords` to avoid adding the same documents every time
await
collection
.
upsert
({
documents:
[
"This is a document about pineapple"
,
"This is a document about oranges"
,
],
ids:
[
"id1"
,
"id2"
],
});
const
results
=
await
collection
.
query
({
queryTexts:
[
"This is a query document about florida"
],
// Chroma will embed this for you
nResults:
2
,
// how many results to return
});
console
.
log
(
results
);
See all 23 lines
​
Next steps
We offer
first class support
for various embedding providers via our embedding function interface. Each embedding function ships in its own npm package.
Learn how to
Deploy Chroma
to a server
Join Chroma’s
Discord Community
to ask questions and get help
Follow Chroma on
X (@trychroma)
for updates
Our Rust docs are hosted on
docs.rs
!
​
Install Manually
cargo
add
chroma
​
Create a Chroma Client
Run the Chroma backend:
chroma
run
--path
./getting-started
Then create a client which connects to it:
use
chroma
::
ChromaHttpClient
;
let
client
=
ChromaHttpClient
::
new
(
Default
::
default
());
​
Create a collection
let
collection
=
client
.
create_collection
(
"my_collection"
,
None
,
None
)
.
await
?
;
​
Add some text documents to the collection
The Rust client expects embeddings to be provided directly. Generate embeddings with your provider SDK, then pass them along with documents.
let
embeddings
=
vec!
[
vec!
[
0.1
,
0.2
,
0.3
],
vec!
[
0.4
,
0.5
,
0.6
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
(),
"id2"
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
"This is a document about pineapple"
.
to_string
()),
Some
(
"This is a document about oranges"
.
to_string
()),
]),
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
Query the collection
let
results
=
collection
.
query
(
vec!
[
vec!
[
0.1
,
0.2
,
0.3
]],
Some
(
2
),
None
,
None
,
None
)
.
await
?
;
​
Next steps
Read the Rust API docs on
docs.rs
Learn how to
Deploy Chroma
to a server
Join Chroma’s
Discord Community
to ask questions and get help
Was this page helpful?
Yes
No
Suggest edits
Assistant
Responses are generated using AI and may contain mistakes.
Contact support