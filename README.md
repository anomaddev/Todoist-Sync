# Todoist Xcode Sync

A Python tool that automatically syncs TODO statements from Xcode projects to Todoist projects.

## Features

- Scans Xcode project files for TODO statements
- Syncs new TODOs to a specified Todoist project
- Removes completed TODOs from Todoist when marked as done in code
- Supports multiple file types (Swift, Objective-C, etc.)
- Configurable project settings

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Todoist API token:
   ```
   TODOIST_API_TOKEN=your_api_token_here
   TODOIST_PROJECT_ID=your_project_id_here
   ```

3. Get your Todoist API token:
   - Go to https://app.todoist.com/app/settings/integrations/developer
   - Copy your API token

4. Get your project ID:
   - Use the Todoist API or web interface to find your project ID
   - Or run the tool with `--list-projects` to see available projects

## Usage

### Basic sync
```bash
python todoist_sync.py /path/to/your/xcode/project
```

### List available Todoist projects
```bash
python todoist_sync.py --list-projects
```

### Sync with specific project
```bash
python todoist_sync.py /path/to/your/xcode/project --project-id 123456
```

### Dry run (preview changes)
```bash
python todoist_sync.py /path/to/your/xcode/project --dry-run
```

## Configuration

The tool looks for TODO statements in the following formats:
- `// TODO: description`
- `/* TODO: description */`
- `# TODO: description`
- `// FIXME: description`

## How it works

1. **Scanning**: Recursively scans all source files in the Xcode project
2. **Parsing**: Extracts TODO statements with their file paths and line numbers
3. **Syncing**: Compares with existing Todoist tasks and syncs changes
4. **Cleanup**: Removes completed tasks from Todoist when TODOs are marked as done

## File Structure

```
Todoist-Sync/
├── todoist_sync.py      # Main sync script
├── xcode_parser.py      # Xcode project parser
├── todoist_client.py    # Todoist API client
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
└── README.md          # This file
``` 