Python & JS/TS Observability SDKs - Langfuse
Langfuse v4: up to 165× faster ·
Read more
Langfuse v4 is here: real-time, up to 165× faster ·
Read more
Docs
Overview
Example Project
Ask AI
Get Started
Start Tracing
Use Prompt Management
Set up Evals
Products
Observability
Overview
Get Started
Concepts
Best Practices
Features
SDKs
Overview
Instrumentation
Advanced Features
Troubleshooting & FAQ
Upgrade Path
Python Reference ↗
JS/TS Reference ↗
Integrations ↗
Troubleshooting & FAQ
Prompt Management
Evaluation
Platform
Metrics
API & Data Platform
Assistant
Administration
Security & Guardrails
Versions & Compatibility
More
Glossary
Roadmap
Langfuse v4 is live
Docs MCP Server
SDK & API References
Security & Compliance ↗
Support ↗
Overview
Docs
Observability
SDKs
Overview
Copy page
Langfuse SDKs
Langfuse offers two SDKs:
Python SDK v4
JS/TS SDK v5
Other Languages
via OpenTelemetry
Upgrading from Python SDK v3 or JS/TS SDK v4? Follow the
upgrade paths
(
Python v3 → v4
,
JS/TS v4 → v5
).
The Langfuse SDKs are the recommended way to create
custom observations and traces
and use the Langfuse
prompt-management
and
evaluation
features. Both SDKs work with
Langfuse Cloud
(hosted by Langfuse, free tier, no infrastructure to run) and
self-hosted Langfuse
with the same code; only the credentials and base URL differ.
Key benefits
Based on
OpenTelemetry
, so you can use any OTEL-based instrumentation library for your LLM stack.
Fully
async requests
, meaning Langfuse adds almost no latency.
Interoperable with Langfuse
native integrations
.
Accurate latency tracking via synchronous timestamps.
IDs available for downstream use.
Great DX when nesting observations.
Cannot break your application: SDK errors are caught and logged.
This section documents tracing related features of the Langfuse SDK. To use the Langfuse SDK for
prompt management
and
evaluation
, visit their respective documentation.
Requirements for self-hosted Langfuse
+
SDK
Minimum self-hosted server version
Notes
Python SDK v3 and v4
≥ 3.63.0
Observations API v2 and Metrics API v2 require Langfuse v4
JS/TS SDK v4 and v5
≥ 3.63.0
Observations API v2 and Metrics API v2 require Langfuse v4
Langfuse Cloud always satisfies these minimums. See the
self-hosted compatibility matrix
for the full picture per server version, and
Versions & Compatibility
for Langfuse Cloud.
Legacy documentation
+
This documentation is for the latest versions of the Langfuse SDKs.
Legacy Python SDK v3 documentation
Legacy TypeScript SDK v4 documentation
Quickstart
Follow the quickstart guide to get the first trace into Langfuse. See the
setup
section for more details.
Python SDK
JS/TS SDK
1. Install package:
pip
install
langfuse
2. Add credentials:
.env
LANGFUSE_SECRET_KEY
=
"sk-lf-..."
LANGFUSE_PUBLIC_KEY
=
"pk-lf-..."
LANGFUSE_BASE_URL
=
"https://cloud.langfuse.com"
# 🇪🇺 EU region
# Other Langfuse data regions include 🇺🇸 US: https://us.cloud.langfuse.com, 🇯🇵 Japan: https://jp.cloud.langfuse.com and ⚕️ HIPAA: https://hipaa.cloud.langfuse.com
3. Instrument your application:
Instrumentation means adding code that records what’s happening in your application so it can be sent to Langfuse. There are three main ways of instrumenting your code with the Python SDK.
In this example we will use the
context manager
. You can also use the
decorator
or create
manual observations
.
from
langfuse
import
get_client
langfuse
=
get_client()
# Create a span using a context manager
with
langfuse.start_as_current_observation(
as_type
=
"span"
,
name
=
"process-request"
)
as
span:
# Your processing logic here
span.update(
output
=
"Processing complete"
)
# Create a nested generation for an LLM call
with
langfuse.start_as_current_observation(
as_type
=
"generation"
,
name
=
"llm-response"
,
model
=
"gpt-3.5-turbo"
)
as
generation:
# Your LLM call logic here
generation.update(
output
=
"Generated response"
)
# All spans are automatically closed when exiting their context blocks
# Flush events in short-lived applications
langfuse.flush()
When should I call
langfuse.flush()
?
4. Run your application and see the trace in Langfuse:
See the
trace in Langfuse
.
1. Install packages:
npm
install
@langfuse/tracing
@langfuse/otel
@opentelemetry/sdk-node
2. Set environment variables:
.env
LANGFUSE_SECRET_KEY
=
"sk-lf-..."
LANGFUSE_PUBLIC_KEY
=
"pk-lf-..."
LANGFUSE_BASE_URL
=
"https://cloud.langfuse.com"
# 🇪🇺 EU region
# Other Langfuse data regions include 🇺🇸 US: https://us.cloud.langfuse.com, 🇯🇵 Japan: https://jp.cloud.langfuse.com and ⚕️ HIPAA: https://hipaa.cloud.langfuse.com
3. Initialize OpenTelemetry:
Create an
instrumentation.ts
to register the Langfuse span processor so traces reach Langfuse.
instrumentation.ts
import
{ NodeSDK }
from
"@opentelemetry/sdk-node"
;
import
{ LangfuseSpanProcessor }
from
"@langfuse/otel"
;
export
const
sdk
=
new
NodeSDK
({
spanProcessors
:
[
new
LangfuseSpanProcessor
()],
});
sdk.
start
();
Import this file at the top of your app's entry point (e.g.,
index.ts
).
4. Instrument your app:
Instrumentation means adding code that records what’s happening in your application so it can be sent to Langfuse. There are three main ways of instrumenting your code with the TypeScript SDK.
In this example we will use the
context manager
. You can also use the
decorator
or create
manual observations
.
index.ts
import
{ sdk }
from
"./instrumentation"
;
import
{ startActiveObservation }
from
"@langfuse/tracing"
;
async
function
main
() {
await
startActiveObservation
(
"my-first-trace"
,
async
(
span
)
=>
{
span.
update
({
input
:
"Hello, Langfuse!"
,
output
:
"This is my first trace!"
,
});
}
// Shutdown flushes events and is required for short-lived applications
main
().
finally
(()
=>
sdk.
shutdown
());
When do I need to use
shutdown()
?
5. Run your application and see the trace in Langfuse:
npx
tsx
index.ts
See the
trace in Langfuse
.
Setup
This section covers all detail of setting up the Langfuse SDKs. Follow the
Quickstart
guide to create your first trace.
Install the SDK
Python SDK
JS/TS SDK
Pip install the
Langfuse Python SDK
.
pip
install
langfuse
The Langfuse JS/TS SDK is designed to be modular. Install the relevant packages for a full tracing setup:
npm
install
@langfuse/tracing
@langfuse/otel
@opentelemetry/sdk-node
Here's an overview of the available packages for the TypeScript SDK:
Package
Description
Environment
@langfuse/core
Core utilities, types, and logger shared across packages.
Universal JS
@langfuse/client
Client for features like prompts, datasets, and scores.
Universal JS
@langfuse/browser
Browser-safe client for public-key score ingestion.
Browser
@langfuse/tracing
Core OpenTelemetry-based tracing functions (
startObservation
, etc.).
Universal JS
@langfuse/otel
The
LangfuseSpanProcessor
to export traces to Langfuse.
Node.js ≥ 20
@langfuse/openai
Automatic tracing integration for the OpenAI SDK.
Universal JS
@langfuse/langchain
CallbackHandler for tracing LangChain applications.
Universal JS
Configure credentials
To authenticate with Langfuse, add your Langfuse credentials as environment variables. You can get your credentials by signing up for a free
Langfuse Cloud
account or by
self-hosting Langfuse
.
If you are self-hosting Langfuse or using a
data region
other than the default (EU,
https://cloud.langfuse.com
), ensure you configure the base URL argument or the
LANGFUSE_BASE_URL
environment variable.
You can also pass the credentials
directly to the constructor
.
.env
LANGFUSE_SECRET_KEY
=
"sk-lf-..."
LANGFUSE_PUBLIC_KEY
=
"pk-lf-..."
LANGFUSE_BASE_URL
=
"https://cloud.langfuse.com"
# 🇪🇺 EU region
# Other Langfuse data regions include 🇺🇸 US: https://us.cloud.langfuse.com, 🇯🇵 Japan: https://jp.cloud.langfuse.com and ⚕️ HIPAA: https://hipaa.cloud.langfuse.com
Initialize OpenTelemetry (JS/TS only)
Python SDK
JS/TS SDK
The Python SDK automatically sets up OpenTelemetry when
initializing the client
.
By default, the SDK exports Langfuse + GenAI/LLM spans. To customize this, use
should_export_span
(recommended).
blocked_instrumentation_scopes
still works but is deprecated and planned for removal in a future version.
The JS/TS SDK's tracing is built on top of OpenTelemetry, so you need to set up the OpenTelemetry SDK. The
LangfuseSpanProcessor
is the key component that sends traces to Langfuse.
instrumentation.ts
import
{ NodeSDK }
from
"@opentelemetry/sdk-node"
;
import
{ LangfuseSpanProcessor }
from
"@langfuse/otel"
;
const
sdk
=
new
NodeSDK
({
spanProcessors
:
[
new
LangfuseSpanProcessor
()],
});
sdk.
start
();
By default, the processor exports Langfuse + GenAI/LLM spans. To customize this, use
shouldExportSpan
.
For more options to configure the
LangfuseSpanProcessor
such as masking, filtering, and more, see
advanced features
.
Learn more in the
OpenTelemetry JS getting-started guide
.
Next.js users:
If you are using Next.js, you can register the
LangfuseSpanProcessor
via
registerOTel
from
@vercel/otel
as long as you are on
@vercel/otel
v2 or later.
Earlier versions did not support the OpenTelemetry JS SDK v2
on which the
@langfuse/tracing
and
@langfuse/otel
packages are based; this was resolved in
@vercel/otel
v2. The
NodeSDK
setup described above also works and carries no version requirement.
See here for a full example for the Vercel AI SDK with NextJS on Vercel
.
Client Setup
Python SDK
JS/TS SDK
Initialize the Langfuse client with
get_client()
to interact with Langfuse. It will automatically use the environment variables you set above.
Initialize client
from
langfuse
import
get_client
langfuse
=
get_client()
# Verify connection
if
langfuse.auth_check():
print
(
"Langfuse client is authenticated and ready!"
)
else
:
print
(
"Authentication failed. Please check your credentials and host."
)
The Langfuse client is a singleton. It can be accessed anywhere in your application using the
get_client()
function.
Alternative: Configure via constructor
+
Optionally, you can initialize the client via
Langfuse()
to pass in configuration options (see below). Otherwise, it is created automatically when you call
get_client()
based on environment variables.
If you create multiple
Langfuse
instances with the same
public_key
, the singleton instance is reused and new arguments are ignored.
Initialize client
from
langfuse
import
Langfuse
langfuse
=
Langfuse(
public_key
=
"your-public-key"
,
secret_key
=
"your-secret-key"
,
base_url
=
"https://cloud.langfuse.com"
,
# 🇪🇺 EU region
# Other Langfuse data regions include 🇺🇸 US: https://us.cloud.langfuse.com, 🇯🇵 Japan: https://jp.cloud.langfuse.com and ⚕️ HIPAA: https://hipaa.cloud.langfuse.com
)
All key configuration options are listed in the
Python SDK reference
.
Initialize the
LangfuseClient
to interact with Langfuse. The client will automatically use the environment variables you set above.
client.ts
import
{ LangfuseClient }
from
"@langfuse/client"
;
const
langfuse
=
new
LangfuseClient
();
Alternative: Configure via constructor
+
You can also pass the Langfuse credentials directly to the constructor:
client.ts
import
{ LangfuseClient }
from
"@langfuse/client"
;
const
langfuse
=
new
LangfuseClient
({
publicKey
:
"your-public-key"
,
secretKey
:
"your-secret-key"
,
baseUrl
:
"https://cloud.langfuse.com"
,
// or your self-hosted instance
});
Use the SDK
With the SDK set up, you can:
Instrument your application
Use
Langfuse Prompt Management
Run
Experiments
and create
Scores
Query data
OpenTelemetry foundation
The Langfuse SDKs are built on top of
OpenTelemetry
. This provides:
Standardization
with the wider observability ecosystem and tooling.
Robust context propagation
so nested spans stay connected, even across async workloads.
Attribute propagation
to keep
userId
,
sessionId
,
metadata
,
version
, and
tags
aligned across observations.
Ecosystem interoperability
meaning third-party instrumentations automatically appear inside Langfuse traces.
The following diagram shows how Langfuse maps to native OpenTelemetry concepts:
OTel Trace
: An OTel-trace represents the entire lifecycle of a request or transaction as it moves through your application and its services. A trace is typically a sequence of operations, like an LLM generating a response followed by a parsing step. The root (first) span created in a sequence defines the OTel trace. OTel traces do not have a start and end time, they are defined by the root span.
OTel Span
: A span represents a single unit of work or operation within a trace. Spans have a start and end time, a name, and can have attributes (key-value pairs of metadata). Spans can be nested to create a hierarchy, showing parent-child relationships between operations.
Langfuse Trace
: A Langfuse trace is the set of observations that share a
trace_id
, plus shared attributes such as
session_id
and
user_id
. It shares the same ID as the OTel trace. Trace attributes are set via specific OTel span attributes and can be propagated to all child observations with
propagate_attributes()
(see Attribute Propagation below). Overall input and output belong on the root observation; trace-level input/output is deprecated in Langfuse v4.
Langfuse Observation
: In Langfuse terminology, an "observation" is a Langfuse-specific representation of an OTel span. It can be a generic span (Langfuse-span), a specialized "generation" (Langfuse-generation), a point-in-time event (Langfuse-event), or
other observation types
.
Langfuse Span
: A Langfuse-span is a generic OTel span in Langfuse, designed for non-LLM operations.
Langfuse Generation
: A Langfuse-generation is a specialized type of OTel span in Langfuse, designed specifically for Large Language Model (LLM) calls. It includes additional fields like
model
,
model_parameters
,
usage_details
(tokens), and
cost_details
.
Langfuse Event
: A Langfuse-event tracks a point in time action.
Other observation types
: Langfuse supports other observation types such as tool calls, RAG retrieval steps, etc.
Context Propagation
: OpenTelemetry automatically handles the propagation of the current trace and span context. This means when you call another function (whether it's also traced by Langfuse, an OTel-instrumented library, or a manually created span), the new span will automatically become a child of the currently active span, forming a correct trace hierarchy.
Attribute Propagation
: Certain trace attributes (
user_id
,
session_id
,
metadata
,
version
,
tags
, and request-scoped
environment
in the Python SDK) can be automatically propagated to all child observations using
propagate_attributes()
. This ensures consistent attribute coverage across all observations in a trace. See the
instrumentation docs
for details.
The Langfuse SDKs provide wrappers around OTel spans (
LangfuseSpan
,
LangfuseGeneration
) that offer convenient methods for interacting with Langfuse-specific features like scoring and media handling, while still being native OTel spans under the hood. You can also use these wrapper objects to add Langfuse trace attributes via
update_trace()
or use
propagate_attributes()
for automatic propagation to all child observations.
Learn more
Instrument your app
Advanced features
Upgrade path
Troubleshooting & FAQ
Python API reference
JS/TS API reference
Other languages
Langfuse maintains SDKs for Python and JavaScript/TypeScript. For other languages, you can use our
OpenTelemetry endpoint
to instrument your application and use the
public API
to use Langfuse prompt management, evaluation, and querying.
Instrumentation
To instrument your application, you can send OpenTelemetry spans to the
Langfuse OTel endpoint
. For this, you can use the following OpenTelemetry SDKs:
JetBrains Tracy for Kotlin/Java
OpenTelemetry Java
OpenTelemetry .NET
OpenTelemetry Go
OpenTelemetry C++
OpenTelemetry Erlang/Elixir
OpenTelemetry Ruby
OpenTelemetry PHP
OpenTelemetry Rust
OpenTelemetry Swift
Prompt management, evaluation, and querying:
To use other Langfuse features, you can use the
public API
to integrate Langfuse from any runtime. We also maintain a
list of community-maintained SDKs
.
Was this page helpful?
Good
Bad
Support
Last updated on
Web Callouts
Instrumentation
Langfuse SDKs
Quickstart
Setup
Install the SDK
Configure credentials
Initialize OpenTelemetry (JS/TS only)
Client Setup
Use the SDK
OpenTelemetry foundation
Learn more
Other languages
Instrumentation
Prompt management, evaluation, and querying:
Actions
Give us feedback
Edit this page on GitHub
Contributors
Last edited
Jannik Maierhöfer
Marc Klingen
Max Deichmann
+
5
more
Ask AI
A