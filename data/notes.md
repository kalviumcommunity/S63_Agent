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