# Helfer MCP server for Claude

## Installation Instructions
1. [Install Claude Desktop](https://claude.ai/download) Subscription Required for some models. We recommend at least Sonnet 4.
2. Create new Writing style
![create_style](https://github.com/user-attachments/assets/24c37694-b617-44b3-9b4c-994fb3ddd40a)

![custom_style](https://github.com/user-attachments/assets/2f7f9771-656b-4a05-b5e5-e9b3e5203c11)

![describe_style](https://github.com/user-attachments/assets/6fe97466-651a-49fc-be03-d8f5a1ae7535)

![create_custom_style](https://github.com/user-attachments/assets/c75c63f5-e3f7-4db6-9deb-a92179c97103)


3. Use this Prompt to start with, You can tune it to your preferences, for example to show only static tables instead of creating iteractive dashboards:
  ```
Use helfer tool to answer question about data. The answer may contain HTML tables, extract the HTML text and create artifact to show results in nice interactive html artifact. 
Provide key highlights. If result does not answer the user question then try to run multiple sql queries to helfer and summarize the results.
Then at the end also show the explanation from Helfer and show the generated sql in a code snippet artifact using sql syntax
```
  Don't forget to select the style you just created.
![select_style](https://github.com/user-attachments/assets/fc494683-8056-4191-b4a6-4b18b342f1b5)

4. [Download this repo](https://github.com/helpwithmetrics/helfer-mcp/archive/refs/heads/main.zip), and extract it. Make sure to figure out the path to the downloaded files.
5. Install uv:

  For Mac ([with brew](https://brew.sh/)):
  ```bash
  brew install uv
  ```
 
  For Windows:
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
6. Get started by opening up the Claude menu on your computer and select “Settings…” Please note that these are not the Claude Account Settings found in the app window itself.

This is what it should look like on a Mac (in windows there's a Menu icon next in the top left corner of the window):

<img width="322" alt="quickstart-menu" src="https://github.com/user-attachments/assets/093177c2-74e6-4318-a195-5f3ea2e07990" />

Then hit the "Edit Config" button. This will open a Finder (File Explorer) window. Open the file `claude_desktop_config.json` with your favorite editor.

<img width="844" alt="quickstart-developer" src="https://github.com/user-attachments/assets/f398076a-d675-4dc8-b073-58bce72f820b" />

7. Add this content to your claude config file, replace the path with the correct path to your downloaded files:

  For Mac:

  ```json
{
  "mcpServers": {
    "helfer": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/john/Downloads/helfer-mcp-main",
        "run",
        "helfer.py"
      ]
    }
  }
}
  ```

  For Windows:
  ```json
{
  "mcpServers": {
    "helfer": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\JOHN\\Downloads\\helfer-mcp-main",
        "run",
        "helfer.py"
      ]
    }
  }
}
  ```
  8. Open the `.env` file inside your `helfer-mcp-main` folder and input your username and password for Helfer AI.
  ```
HELFER_USERNAME=<username>
HELFER_PASSWORD=<password>
  ```
  For Mac the file may be not visible from finder, you can edit it from the terminal:
  ```
   nano /Users/john/Downloads/helfer-mcp-main/.env
  ```
  9. Restart Claude and make sure MCP tools from Helfer are enabled.

![mcps](https://github.com/user-attachments/assets/9250ad77-cb5c-48a2-941d-3001919d37d1)

![helfer-tools](https://github.com/user-attachments/assets/0e55ec6b-4834-448e-a36d-3a8316bd23c3)

  10. Start your prompts with `ask helfer` , for example:
![prompt-example](https://github.com/user-attachments/assets/c1829294-370f-4ddf-bfb1-7d07013407c8)

