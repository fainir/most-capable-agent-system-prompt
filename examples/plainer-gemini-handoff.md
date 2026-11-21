# Verify a project handoff in Gemini CLI

Check that a project summary comes from the source note before you act on it. This exercise uses Plainer, a workspace built by this repository's author. The connection is included in Plainer Free. You need Gemini CLI with your own model access.

1. [Open Plainer’s Gemini CLI connection guide](https://plainer.app/connections/from-gemini-handoff). Choose **Sign in to Plainer** if needed, using an account that holds only sample files. Open your [Plainer workspace](https://plainer.app/) and save a note named **Release handoff** with this text.

   ```text
   Owner: Mia
   Next step: Review the staging checklist.
   ```

2. Install the [Plainer extension](https://github.com/fainir/plainer-code/releases/tag/1.0.0) in your terminal. If `gemini extensions list` already shows `plainer-files` or `gemini mcp list` shows a manually configured `plainer` server, go to step 3.

   ```sh
   gemini extensions install https://github.com/fainir/plainer-code
   ```

   For manual registration, open **Register the server manually** in the connection guide and run the command there instead.

3. Start a new Gemini CLI session and run `/mcp auth plainer`. Use the same Plainer account in your browser, choose **Read files**, and select **Allow access**. This allows the client to find and read files in that account.
4. Ask Gemini to “Find and read Release handoff in Plainer. Quote the owner and next step, give the source note's title, and tell me whether it includes a launch time.” Check that the reply names **Mia**, quotes **Review the staging checklist.**, cites **Release handoff**, and reports that the launch time is missing.
5. Reopen the note in Plainer and check that the two lines are unchanged. When you finish, go to [Connected clients](https://plainer.app/connections#connected-clients) and select **Disconnect** beside **Gemini CLI MCP Client**.

See the [Gemini CLI MCP guide](https://geminicli.com/docs/tools/mcp-server/) for client setup and troubleshooting. If you want more capacity for the Assistant inside Plainer, [compare Free and Pro](https://plainer.app/pricing/from-agent-guide).
