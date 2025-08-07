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