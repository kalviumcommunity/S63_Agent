# System and User Prompts for AgentCLI

## System Prompt

```
You are an AI assistant integrated into AgentCLI, a terminal-based tool for interacting with documents. Your purpose is to help users extract information, answer questions, and perform tasks related to their documents.

As an agent, you have the following capabilities:
1. Understand and analyze text from various document formats (PDF, TXT, MD)
2. Perform semantic search over document content
3. Execute specific functions when requested
4. Provide clear, concise, and accurate responses

You should:
- Respond directly to user queries about document content
- Use available functions only when necessary to complete tasks
- Maintain context throughout the conversation
- Be honest about limitations when you cannot perform a task
- Format responses appropriately for terminal display

Your responses should be helpful, accurate, and tailored to the user's needs while working within the constraints of a terminal interface.
```

## User Prompt Template

```
I need you to help me with the following document: {document_name}. 

Here is some context about this document that may be helpful:
- Document type: {document_type}
- Relevant sections: {sections_to_focus_on}
- My current goal: {user_goal}

My question/request is: {user_query}

Please provide a clear and direct response based on the document content. If you need to use any special functions to complete this task, do so only when necessary.
```

## RTFC Framework Application

### Role
- The system prompt clearly defines the assistant's role as an AI integrated into AgentCLI
- Establishes the assistant as a document-focused helper working through a terminal interface
- Sets expectations for how the assistant should behave (helpful, accurate, honest about limitations)

### Task
- The system prompt outlines the primary tasks: extracting information, answering questions, and performing document-related functions
- The user prompt template includes a specific query/request field to clearly communicate the immediate task
- Includes the user's goal to provide context for the current task

### Format
- System prompt specifies that responses should be formatted appropriately for terminal display
- User prompt requests clear and direct responses based on document content
- Structure encourages concise, readable outputs suitable for CLI environment

### Context
- User prompt provides document name, type, and relevant sections to focus on
- Includes the user's current goal to help the assistant understand the broader context
- System prompt reminds the assistant to maintain conversation context

This implementation of the RTFC framework ensures the assistant understands its role within the AgentCLI ecosystem, the specific tasks it needs to perform, the appropriate format for responses in a terminal environment, and the necessary context to provide relevant assistance.

# Zero-Shot Prompting for AgentCLI

## What is Zero-Shot Prompting?

Zero-shot prompting is a technique where an AI model is asked to perform a task without being given specific examples of that task during the prompt. The model relies on its pre-trained knowledge to understand and execute the task based solely on instructions. This approach is particularly valuable when:

1. You need the AI to handle a wide variety of tasks without retraining
2. You want to test the AI's inherent capabilities without fine-tuning
3. You need flexibility to address unpredictable user requests
4. You want to minimize prompt length and complexity

## Zero-Shot Prompt for Document Analysis

```
Analyze the following {document_type} and perform the task described below without using examples:

[DOCUMENT CONTENT]

Task: {specific_task}

Provide your analysis in the following format:
1. Key findings
2. Relevant data points
3. Recommended actions

Be concise, accurate, and focus only on information directly relevant to the task.
```

## Zero-Shot Prompt for Data Extraction

```
From the provided {document_type}, extract the following information without examples:

[DOCUMENT CONTENT]

Information to extract:
- {data_point_1}
- {data_point_2}
- {data_point_3}

If any requested information is not present in the document, indicate this clearly. Do not invent or assume information not explicitly stated in the document.
```

## Zero-Shot Prompt for Comparative Analysis

```
Compare the following aspects of the document without prior examples:

[DOCUMENT CONTENT]

Aspects to compare:
1. {aspect_1} vs {aspect_2}
2. {aspect_3} across different sections
3. Consistency of {aspect_4} throughout the document

Present your findings in a structured format highlighting key similarities, differences, and patterns.
```

## Benefits of Zero-Shot Prompting for AgentCLI

1. **Efficiency**: Eliminates the need for extensive example preparation, reducing prompt size and processing time
2. **Flexibility**: Allows the system to handle a wide range of document types and tasks without specialized training
3. **Scalability**: Enables the system to adapt to new document formats and query types without modification
4. **Reduced Bias**: Minimizes the risk of biasing the model toward specific examples
5. **Simplicity**: Provides a cleaner user experience with straightforward prompts

## Implementation Considerations

When implementing zero-shot prompting in AgentCLI:

1. Use clear, specific instructions that define the task boundaries
2. Provide structured output formats to guide response generation
3. Include explicit constraints to prevent hallucination or invention of data
4. Balance between specificity (for accuracy) and generality (for flexibility)
5. Consider the model's inherent capabilities and limitations when designing prompts

# One-Shot Prompting for AgentCLI

## What is One-Shot Prompting?

One-shot prompting is a technique where an AI model is provided with a single example of the desired task before being asked to perform a similar task. This approach bridges the gap between zero-shot prompting (no examples) and few-shot prompting (multiple examples). One-shot prompting is particularly effective when:

1. You need to demonstrate a specific format or approach
2. The task has nuances that are difficult to explain but easy to demonstrate
3. You want to guide the model's response style without extensive examples
4. You need to balance efficiency with performance improvement

## One-Shot Prompt for Document Summarization

```
I'll show you how to summarize a document effectively with one example, then I'd like you to apply the same approach to a new document.

Example Document:
"The quarterly financial report indicates a 12% increase in revenue compared to the previous quarter. Operating expenses remained stable at approximately $2.3 million. The R&D department exceeded their budget by 5%, but this was offset by lower-than-expected marketing costs. The board has approved a new investment initiative for the upcoming fiscal year."

Example Summary:
- Revenue: 12% increase from previous quarter
- Operating expenses: Stable at $2.3M
- Budget variances: R&D exceeded by 5%, offset by lower marketing costs
- Future plans: New investment initiative approved for next fiscal year

Now, please summarize the following document using the same approach:

[DOCUMENT CONTENT]

Focus on key metrics, financial data, notable variances, and future plans. Present your summary in a bulleted list format similar to the example.
```

## One-Shot Prompt for Document Question Answering

```
I'll demonstrate how to answer a question based on document content with one example, then I'd like you to answer a new question using the same approach.

Example Document:
"The project timeline has been adjusted due to supply chain delays. The initial phase will now begin on March 15th instead of February 1st. All subsequent milestones have been shifted accordingly, with the final delivery now expected by November 30th. The budget remains unchanged despite these delays."

Example Question: When will the project be completed?
Example Answer: According to the document, the final delivery is now expected by November 30th due to supply chain delays that have shifted all project milestones.

New Document:
[DOCUMENT CONTENT]

Question: {specific_question}

Please answer the question based solely on the information provided in the document. Follow the example format by providing a direct answer that references the relevant information from the document.
```

## One-Shot Prompt for Action Item Extraction

```
I'll show you how to extract action items from a document with one example, then I'd like you to extract action items from a new document using the same approach.

Example Document:
"During the meeting, Sarah agreed to finalize the presentation by Thursday. John will coordinate with the IT department to ensure the conference room is properly equipped. The team needs to review the proposal before next Monday's client meeting. Alex mentioned he would distribute the updated market analysis once it's completed, likely by mid-week."

Example Action Items Extracted:
1. [Sarah] Finalize the presentation by Thursday
2. [John] Coordinate with IT department for conference room equipment
3. [Team] Review the proposal before Monday's client meeting
4. [Alex] Distribute updated market analysis by mid-week

New Document:
[DOCUMENT CONTENT]

Please extract all action items from this document following the format shown in the example. For each action item, include the responsible party in brackets, the specific action, and any mentioned deadline.
```

## Benefits of One-Shot Prompting for AgentCLI

1. **Improved Accuracy**: Provides a clear example of the expected output format and style
2. **Reduced Ambiguity**: Demonstrates exactly what kind of information to focus on
3. **Efficiency Balance**: More effective than zero-shot without the overhead of multiple examples
4. **Format Consistency**: Ensures responses follow a specific structure
5. **Learning Acceleration**: Helps the model quickly understand task-specific nuances

## Implementation Considerations

When implementing one-shot prompting in AgentCLI:

1. Choose representative examples that clearly demonstrate the desired behavior
2. Ensure the example is simple enough to be understood but complex enough to showcase the task
3. Match the example domain to the target domain when possible
4. Explicitly state how the example should guide the approach to the new task
5. Consider creating domain-specific examples for different document types

# Multi-Shot Prompting for AgentCLI

## What is Multi-Shot Prompting?

Multi-shot prompting (also known as few-shot prompting) is a technique where an AI model is provided with multiple examples of a task before being asked to perform a similar task. By showing several examples with different variations, the model can better understand patterns, edge cases, and nuances of the desired behavior. Multi-shot prompting is particularly effective when:

1. The task is complex or has multiple variations that need to be demonstrated
2. You need to show how to handle different scenarios or edge cases
3. The format or approach needs to be reinforced through repetition
4. You want to maximize accuracy and consistency for critical tasks
5. The task requires understanding subtle patterns that are best illustrated through multiple examples

## Multi-Shot Prompt for Document Classification

```
I'll show you how to classify documents into categories with multiple examples, then I'd like you to classify a new document using the same approach.

Example 1:
Document: "The quarterly earnings report shows a 15% increase in revenue and a 12% increase in profit margins. The board has approved a dividend payment of $0.45 per share to be distributed next month."
Classification: Financial Report
Reasoning: Contains financial metrics (revenue, profit margins), mentions earnings and dividend payments, and has a formal reporting tone.

Example 2:
Document: "Team, please review the attached product specifications before our meeting on Thursday. We need to finalize the feature list and address any technical concerns before moving to the development phase."
Classification: Internal Communication
Reasoning: Addressed to a team, contains action items, mentions a meeting, and discusses an internal project process.

Example 3:
Document: "The new privacy policy will take effect on June 1st. Users will need to accept the updated terms to continue using the service. Key changes include enhanced data protection measures and more transparent data usage reporting."
Classification: Policy Document
Reasoning: Announces policy changes, mentions terms and conditions, specifies an effective date, and outlines regulatory or compliance information.

Now, please classify the following document:

[DOCUMENT CONTENT]

Provide your classification along with reasoning that explains the key indicators that led to your classification decision.
```

## Multi-Shot Prompt for Sentiment Analysis

```
I'll demonstrate how to analyze the sentiment of document passages with multiple examples, then I'd like you to analyze a new document using the same approach.

Example 1:
Passage: "We're extremely pleased with the new system implementation. Response times have improved by 40%, and user feedback has been overwhelmingly positive. This represents a significant achievement for our team."
Sentiment: Strongly Positive
Key Indicators: "extremely pleased," "improved," "overwhelmingly positive," "significant achievement"

Example 2:
Passage: "The project was completed on schedule, though we encountered some minor challenges with the third-party integration. Overall, the system meets the requirements, but there are a few areas that could be enhanced in future updates."
Sentiment: Neutral to Slightly Positive
Key Indicators: "completed on schedule" (positive), "minor challenges" (negative), "meets requirements" (positive), "could be enhanced" (slightly negative)

Example 3:
Passage: "Unfortunately, the latest update has caused significant performance issues. Users are reporting frequent crashes, and response times have increased by 25%. We need to address these critical problems immediately before they impact customer retention."
Sentiment: Strongly Negative
Key Indicators: "unfortunately," "significant performance issues," "frequent crashes," "critical problems"

Example 4:
Passage: "The new feature has received mixed feedback. Some users appreciate the added functionality, while others find it confusing and unnecessary. We should consider making it optional in the next release."
Sentiment: Mixed
Key Indicators: "mixed feedback," both "appreciate" (positive) and "confusing and unnecessary" (negative)

Now, analyze the sentiment of the following document:

[DOCUMENT CONTENT]

Provide your sentiment analysis along with the key indicators that informed your assessment. Be sure to consider the overall tone, specific word choices, and context.
```

## Multi-Shot Prompt for Data Extraction with Varying Formats

```
I'll show you how to extract structured information from documents with varying formats through multiple examples, then I'd like you to extract information from a new document.

Example 1 (Formal Report):
Document: "Project Status Report: As of March 15, 2023, the database migration is 75% complete. The project manager, Sarah Johnson, estimates completion by April 10, 2023. Current budget spent: $45,000 of allocated $60,000."

Extracted Information:
- Project: Database migration
- Status: 75% complete
- Responsible Person: Sarah Johnson (Project Manager)
- Expected Completion: April 10, 2023
- Budget: $45,000 spent of $60,000 allocated

Example 2 (Email):
Document: "Subject: Conference Room Booking
Hi team, I've reserved Conference Room A for our client meeting with Acme Corp. The meeting is scheduled for Tuesday, May 5th from 2:00 PM to 4:00 PM. Please prepare your presentations by Monday. Contact me (john.smith@company.com) if you have any conflicts.
Regards, John"

Extracted Information:
- Event: Client meeting with Acme Corp
- Location: Conference Room A
- Date: Tuesday, May 5th
- Time: 2:00 PM to 4:00 PM
- Preparation Deadline: Monday, May 4th
- Contact: john.smith@company.com

Example 3 (Meeting Minutes):
Document: "Marketing Strategy Meeting - Minutes
Date: June 12, 2023
Attendees: Mark Wilson, Lisa Chen, Robert Garcia, Emma Davis
Key Decisions:
1. Increase social media budget by 20% for Q3
2. Launch new product campaign on July 15
3. Hire two additional content creators by end of month
Next meeting: June 26, 2023"

Extracted Information:
- Meeting Type: Marketing Strategy
- Date Held: June 12, 2023
- Participants: Mark Wilson, Lisa Chen, Robert Garcia, Emma Davis
- Decisions Made:
  * Increase social media budget by 20% for Q3
  * Launch new product campaign on July 15
  * Hire two additional content creators by end of month
- Follow-up Meeting: June 26, 2023

Now, please extract structured information from the following document:

[DOCUMENT CONTENT]

Identify the document type first, then extract all relevant information in a structured format similar to the examples. Adapt your extraction approach based on the document's format and content type.
```

## Benefits of Multi-Shot Prompting for AgentCLI

1. **Enhanced Accuracy**: Multiple examples help the model understand complex patterns and variations
2. **Robust Handling of Edge Cases**: Examples can demonstrate how to handle unusual or challenging scenarios
3. **Improved Consistency**: Reinforces the expected format and approach through repetition
4. **Better Pattern Recognition**: Helps the model identify subtle patterns across different examples
5. **Reduced Hallucination**: Multiple examples provide stronger guardrails against making up information
6. **Adaptability**: Demonstrates how to handle different document formats and structures

## Implementation Considerations

When implementing multi-shot prompting in AgentCLI:

1. **Balance Quantity and Quality**: Include enough examples to demonstrate patterns without making the prompt too long
2. **Showcase Diversity**: Select examples that demonstrate different aspects of the task or different types of inputs
3. **Order Strategically**: Consider placing simpler examples first, followed by more complex ones
4. **Explain Reasoning**: When possible, include the reasoning behind each example to make the pattern more explicit
5. **Match Complexity**: Ensure the examples are of similar complexity to the actual tasks the agent will perform
6. **Consider Token Limits**: Be mindful of the model's context window and optimize examples for efficiency
7. **Domain Relevance**: Use examples from the same domain or industry as the target documents

# Chain of Thought Prompting for AgentCLI

## What is Chain of Thought Prompting?

Chain of Thought (CoT) prompting is a technique that encourages an AI model to break down complex reasoning tasks into a series of intermediate steps before arriving at a final answer. Rather than producing an immediate response, the model is prompted to "think aloud" and show its reasoning process step by step. This approach significantly improves performance on tasks requiring multi-step reasoning, logical deduction, mathematical problem-solving, or complex analysis.

Chain of Thought prompting is particularly effective when:

1. The task requires complex reasoning or problem-solving
2. Multiple steps are needed to reach a conclusion
3. Transparency in the decision-making process is important
4. The problem benefits from structured, sequential thinking
5. Verification of the reasoning process is as important as the final answer

## Chain of Thought Prompt for Document Analysis

```
I need you to analyze the following document and identify potential issues, inconsistencies, or areas of improvement. Please think through your analysis step by step, showing your reasoning process before providing your final conclusions.

[DOCUMENT CONTENT]

Please follow these steps in your analysis:

1. First, identify the main purpose and key components of the document
2. Next, examine the structure and organization of the content
3. Then, analyze the clarity and completeness of the information presented
4. Check for any logical inconsistencies or contradictions
5. Evaluate the document against best practices for this type of content
6. Finally, summarize your findings and provide specific recommendations for improvement

For each step, explain your thought process and observations before moving to the next step. This will help me understand how you arrived at your conclusions.
```

## Chain of Thought Prompt for Troubleshooting Technical Issues

```
I need you to help troubleshoot a technical issue described in the following document. Please think through the problem step by step, showing your reasoning process as you identify potential causes and solutions.

[DOCUMENT CONTENT]

Please follow these steps in your troubleshooting process:

1. First, identify the specific symptoms and behaviors described in the document
2. Next, list possible causes that could explain these symptoms
3. For each potential cause, evaluate its likelihood based on the information provided
4. Determine what additional information would be helpful to confirm or rule out each cause
5. Suggest diagnostic steps to gather this information, in order of priority
6. Based on the most likely causes, recommend specific solutions to try
7. Finally, suggest preventive measures to avoid similar issues in the future

For each step, explain your thought process before moving to the next step. This will help me understand your troubleshooting methodology and learn from your approach.
```

## Chain of Thought Prompt for Decision Analysis

```
I need you to analyze a decision scenario described in the following document. Please think through the decision-making process step by step, showing your reasoning as you evaluate options and arrive at a recommendation.

[DOCUMENT CONTENT]

Please follow these steps in your decision analysis:

1. First, clearly define the decision that needs to be made and its context
2. Identify all stakeholders who would be affected by this decision
3. List all available options or alternatives mentioned in the document
4. For each option, analyze its potential benefits, drawbacks, and risks
5. Consider both short-term and long-term implications of each option
6. Evaluate how each option aligns with stated goals or constraints
7. Compare the options based on your analysis
8. Recommend the best course of action with justification
9. Suggest how to mitigate any risks associated with your recommended option

For each step, explain your thought process before moving to the next step. This will make your reasoning transparent and help me understand how you arrived at your recommendation.
```

## Benefits of Chain of Thought Prompting for AgentCLI

1. **Enhanced Problem-Solving**: Enables the agent to tackle complex reasoning tasks by breaking them down into manageable steps
2. **Transparency**: Makes the agent's reasoning process visible and auditable, building user trust
3. **Error Detection**: Allows users to identify where reasoning might have gone wrong in the chain
4. **Educational Value**: Helps users learn problem-solving approaches by observing the agent's step-by-step process
5. **Improved Accuracy**: Reduces errors by encouraging methodical thinking rather than jumping to conclusions
6. **Better Handling of Ambiguity**: Provides space to consider multiple interpretations or approaches
7. **Self-Correction**: Enables the agent to catch and correct its own mistakes during the reasoning process

## Implementation Considerations

When implementing Chain of Thought prompting in AgentCLI:

1. **Balance Verbosity and Conciseness**: Ensure the reasoning steps are detailed enough to be useful but not overwhelming
2. **Structure the Reasoning Process**: Provide clear guidance on the expected steps or framework for thinking
3. **Domain-Specific Reasoning**: Adapt the reasoning structure to match the domain (technical troubleshooting vs. document analysis)
4. **Allow for Iteration**: Enable the agent to revise earlier steps if later reasoning reveals flaws
5. **Combine with Other Techniques**: Chain of Thought can be enhanced by combining with zero-shot, one-shot, or multi-shot approaches
6. **Consider Output Format**: Determine whether to present the full reasoning chain or just highlight key steps
7. **Manage Token Usage**: Be mindful that Chain of Thought responses use more tokens than direct answers