Quick Start - Ragas
Skip to content
Quick Start: Get Evaluations Running in a Flash
Get started with Ragas in minutes. Create a complete evaluation project with just a few commands.
Step 1: Create Your Project
Choose one of the following methods:
uvx (Recommended)
Install Ragas First
No installation required.
uvx
automatically downloads and runs ragas:
uvx
ragas
quickstart
rag_eval
cd
rag_eval
Install ragas first, then create the project:
pip
install
ragas
quickstart
rag_eval
cd
rag_eval
Step 2: Install Dependencies
Install the project dependencies:
uv
sync
Or if you prefer
pip
:
pip
install
-e
.
Step 3: Set Your API Key
By default, the quickstart example uses OpenAI. Set your API key and you're ready to go. You can also use some other provider with a minor change:
OpenAI (Default)
Anthropic Claude
Google Gemini
Local Models (Ollama)
Custom / Other Providers
export
OPENAI_API_KEY
=
"your-openai-key"
The quickstart project is already configured to use OpenAI. You're all set!
Set your Anthropic API key:
export
ANTHROPIC_API_KEY
=
"your-anthropic-key"
Then update the LLM initialization in
evals.py
:
from
anthropic
import
Anthropic
from
ragas.llms
import
llm_factory
client
=
Anthropic
(
api_key
=
os
.
environ
.
get
(
"ANTHROPIC_API_KEY"
))
llm
=
llm_factory
(
"claude-3-5-sonnet-20241022"
,
provider
=
"anthropic"
,
client
=
client
)
Set up your Google credentials:
export
GOOGLE_API_KEY
=
"your-google-api-key"
Then update the LLM initialization in
evals.py
:
Option 1: Using Google's Official Library (Recommended)
import
google.generativeai
as
genai
from
ragas.llms
import
llm_factory
genai
.
configure
(
api_key
=
os
.
environ
.
get
(
"GOOGLE_API_KEY"
))
client
=
genai
.
GenerativeModel
(
"gemini-2.0-flash"
)
llm
=
llm_factory
(
"gemini-2.0-flash"
,
provider
=
"google"
,
client
=
client
)
# Adapter is auto-detected as "litellm" for google provider
For more Gemini options and detailed setup, see the
Google Gemini Integration Guide
.
Install and run Ollama locally, then update the LLM initialization in
evals.py
:
from
openai
import
OpenAI
from
ragas.llms
import
llm_factory
# Create an OpenAI-compatible client for Ollama
client
=
OpenAI
(
api_key
=
"ollama"
,
# Ollama doesn't require a real key
base_url
=
"http://localhost:11434/v1"
)
llm
=
llm_factory
(
"mistral"
,
provider
=
"openai"
,
client
=
client
)
For any LLM with OpenAI-compatible API:
from
openai
import
OpenAI
from
ragas.llms
import
llm_factory
client
=
OpenAI
(
api_key
=
"your-api-key"
,
base_url
=
"https://your-api-endpoint"
)
llm
=
llm_factory
(
"model-name"
,
provider
=
"openai"
,
client
=
client
)
For more details, learn about
LLM integrations
.
Project Structure
Your generated project includes:
rag_eval/
├──
README.md
# Project documentation
├──
pyproject.toml
# Project configuration
├──
rag.py
# Your RAG application
├──
evals.py
# Evaluation workflow
├──
__init__.py
# Makes this a Python package
└──
evals/
├──
datasets/
# Test data files
├──
experiments/
# Evaluation results
└──
logs/
# Execution logs
Step 4: Run Your Evaluation
Run the evaluation script:
uv
run
python
evals.py
Or if you installed with
pip
:
python
evals.py
The evaluation will: - Load test data from the
load_dataset()
function in
evals.py
- Query your RAG application with test questions - Evaluate responses - Display results in the console - Save results to CSV in the
evals/experiments/
directory
Congratulations! You have a complete evaluation setup running. 🎉
Customize Your Evaluation
Add More Test Cases
Edit the
load_dataset()
function in
evals.py
to add more test questions:
from
ragas
import
Dataset
def
load_dataset
():
"""Load test dataset for evaluation."""
dataset
=
Dataset
(
name
=
"test_dataset"
,
backend
=
"local/csv"
,
root_dir
=
"."
,
)
data_samples
=
[
{
"question"
:
"What is Ragas?"
,
"grading_notes"
:
"Ragas is an evaluation framework for LLM applications"
,
},
{
"question"
:
"How do metrics work?"
,
"grading_notes"
:
"Metrics evaluate the quality and performance of LLM responses"
,
},
# Add more test cases here
]
for
sample
in
data_samples
:
dataset
.
append
(
sample
)
dataset
.
save
()
return
dataset
Customize Evaluation Metrics
The template includes a
DiscreteMetric
for custom evaluation logic. You can customize the evaluation by:
Modify the metric prompt
- Change the evaluation criteria
Adjust allowed values
- Update valid output categories
Add more metrics
- Create additional metrics for different aspects
Example of modifying the metric:
from
ragas.metrics
import
DiscreteMetric
from
ragas.llms
import
llm_factory
my_metric
=
DiscreteMetric
(
name
=
"custom_evaluation"
,
prompt
=
"Evaluate this response:
{response}
based on:
{context}
. Return 'excellent', 'good', or 'poor'."
,
allowed_values
=
[
"excellent"
,
"good"
,
"poor"
],
)
What's Next?
Learn the concepts
: Read the
Evaluate a Simple LLM Application
guide for deeper understanding
Custom metrics
:
Create your own metrics
using simple decorators
Production integration
:
Integrate evaluations into your CI/CD pipeline
RAG evaluation
: Evaluate
RAG systems
with specialized metrics
Agent evaluation
: Explore
AI agent evaluation
Test data generation
:
Generate synthetic test datasets
for your evaluations
Getting Help
📚
Full Documentation
💬
Join our Discord Community
🐛
Report Issues
December 12, 2025
December 11, 2025
GitHub
Back to top