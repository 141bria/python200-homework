# Part 1: Cloud Concepts#

Q1:

- The core economic model of cloud competing is pay-as-you-go. Instead of owning your servers you're renting computing resources and paying for what you use, allowing you scale up/down depending on your needs. The cloud provider handles the physical equipnent and maintenance. while you're responsibile for your data and who can access it.

Q2:

- Vertical scaling is increasing the CPU or RAM on one machine, while horizontal scaling is adding more servers to spread the work across multiple machines.
  For example, Vertical scaling would be upgrading the RAM or CPU on a MacBook. Horizontal scaling would be using mutliple servers to handle a large AI workload instead of relying solely on one machine.

  Scenario 1: Horizontal Scaling because there's a sudden spike in traffic of users so adding more servers would help handle the new demand.

  Scenario 2: Vertical Scaling because the Data Scientist needs a faster GPU and more RAM on one machine.

  Scenario 3: Horizontal Scaling becausethe workload increased and spreading the work across multiple machines would make processing more efficient.

Q3:
Gmail - is SaaS because you don't have to code anything, you just create your account and use the features already available.
Azure Virtual Machines - is Iaas because you're renting a virtual computer instead of buying one.
AWS S3 (Simple Storage Service) - is Iaas because you're renting cloud storage for your files and data.
GitHub Codespaces - Paas because igit add assignments_08/t provides an online enviroment where you can write and run your own code.
Snowflake - Saas since it's a managed platform that lets you store, organize, & analyze data.
Supabase - Baas since it provides ready to use back end services like databases, storage, and authnetication.

IaaS - Infrastruture as a Service you're basically renting equipment & managing most of the software. i.e Azure Virtual Machines
As a developer I would be repsonsibile for manaing the os, software, and udpates.
PaaS - Platform as a Serive I bring the code & the provider handles the infrastructure. i.e Github codespaces as a developer I'd be resposnible for mamaning my code & the enviroment
SaaS - Software as a Service I'd log in and use the software that's already been built . i.e microsoft word through mircosoft 365 as the user I'd be repsosnible for files and the account I have while the provider handles the software and maintenance.

Q4:
A managed data platform like Databricks or Snowflake provides the tools and resources you need to work with data without having to manage all of the infrasctructure yourself. While AWS or GCP, you have more control over how you set things up, but being resposibile for managing more of it. With a managed data platform you gain conveince and less respobility but you give up some control and flexibility.

# Part 2: Cloud Landscape

Q1:

1. AWS:

- Their primary strength is being the broadest service catalog of any provider.
- A large enterprise would be most likey to use it.

2. GCP:

- Their primary strength is data/machine learning.
- An organization that does a lot with analytics would be most liklely to use it.

3. Microsoft Azure:

- Their primary strength of the intergration Microsoft products.
- A goverment organziation would be most likey to use it.

Q2:
There were three reasons why CTD swithced from Azure to Supabase:

1. Access - Azure required more time consuming steps that could potentially cause more problems down the line depending on mutiple factors such as someone joining late, waititing for apporval to be let in, and eventually be blocked for days; While Supabase has relatively less steps and being able to join on your own without neededing approval.
2. Pedagogical fit - Supabase stores data more conveintly as relational database making it easier to search through & makes it easier to learn how to work with structured data.
3. Pipeline coherence - Supabase has their pipeline as two tables showing the relaitionship between them making it easier to inspect and debug.
   This suggest that we should consider more than just features when starting a new project. Such as who will need to access it, is it a good pedagogical fit, and if it has Pipeline coherence checking for these things can help us be set up for success.

Q3:

1. You need to store 10 TB of image files and retrieve them by filename from any machine.

- object storage - GCP - cloud Storage

2. You need to run an ML training job on a GPU for four hours, then shut it down.

- ML platform - GCP - Vertex AI

3. You need to host a web API that automatically scales up when traffic spikes and scales down when it quiets.

- Serverless compute - AWS - Lambda

4. You need to send structured data to a large language model and get a text response back.

- LLM API - Azure - Azure OpenAI

Q4:
I would create some chatbox or an AI assistant that gathers information about someone's daily routine, like their name, email and how they would want to track their schedule and have it create a daily agenda for them.
I would use GCP Vertex AI to generate the agenda and AWS S3 to store all the files.
One benefit of using one provider is that everything would be in one place essentially making it easier to manage and access. But in turn it could give up some flexibilyt in choosing different services that might work better for my project.
