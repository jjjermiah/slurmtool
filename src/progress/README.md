# User Stories for the Progress Module

## Basic Progress Management

1. **Global Manager**:  
   As a developer, I want a reusable global progress manager (`MultiProgress`)
   so I can manage multiple progress bars simultaneously without conflicts or
   creating multiple instances.

2. **Styled Progress Bars**:  
   As a developer, I want to create styled progress bars to display specific
   information (e.g., byte transfers, elapsed time, custom messages) in a
   visually appealing way.

3. **Indeterminate Spinner**:  
   As a developer, I want an indeterminate spinner for long-running tasks so
   that I can show progress even when the duration is unknown.

## Task Wrapping

4. **Sync Task Wrapping**:  
   As a developer, I want to wrap synchronous operations in a progress spinner
   so that the user knows the application is busy.

5. **Async Task Wrapping**:  
   As a developer, I want to wrap asynchronous operations in a progress spinner
   so that the UI is non-blocking and responsive.

## Dynamic Progress Updates

6. **Dynamic Message Updates**:  
   As a developer, I want to dynamically update the message or progress of a
   progress bar to reflect the state of the current task.

## Task Lifecycle Management

7. **Group Task Progress**:  
   As a developer, I want to group and track the progress of multiple subtasks
   within a single progress bar so that users can see high-level and detailed
   task progress.

8. **Lifecycle Management**:  
   As a developer, I want an easy way to mark tasks as started or completed
   without manually updating state.