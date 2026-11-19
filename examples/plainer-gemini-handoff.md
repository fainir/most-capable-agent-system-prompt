# Verify a project handoff in Gemini CLI

Check that a project summary comes from the source note before you act on it. This exercise uses Plainer, a workspace built by this repository's author. The connection is included in Plainer Free. You need Gemini CLI with your own model access.

1. [Sign in to Plainer](https://plainer.app/connections) with an account that holds only sample files. Open your [Plainer workspace](https://plainer.app/) and save a note named **Release handoff** with this text.

   ```text
   Owner: Mia
   Next step: Review the staging checklist.
   ```

2. Add the Plainer MCP server in your terminal.

   ```sh
   gemini mcp add --transport http --scope user plainer https://plainer.app/mcp
   ```

3. In Gemini CLI, run `/mcp auth plainer`. Use the same Plainer account in your browser, choose **Read files**, and select **Allow access**. This allows the client to find and read files in that account.
4. Ask Gemini to “Find and read Release handoff in Plainer. Quote the owner and next step, give the source note's title, and tell me whether it includes a launch time.” Check that the reply names **Mia**, quotes **Review the staging checklist.**, cites **Release handoff**, and reports that the launch time is missing.
5. Reopen the note in Plainer and check that the two lines are unchanged. When you finish, go to [Connected clients](https://plainer.app/connections#connected-clients) and select **Disconnect** beside **Gemini CLI MCP Client**.

See the [Gemini CLI MCP guide](https://geminicli.com/docs/tools/mcp-server/) for client setup and troubleshooting. If you want more capacity for the Assistant inside Plainer, [compare Free and Pro](https://plainer.app/pricing/from-agent-guide).
