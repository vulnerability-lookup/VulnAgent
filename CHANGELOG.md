# Changelog

## Release 0.2.0 (2026-03-24)

- New Chinese vulnerability severity classification tool (classify_severity_zh) using CIRCL/vulnerability-severity-classification-chinese-macbert-base.
- TOML configuration file support (~/.config/vulnagent/config.toml or VULNAGENT_CONFIG env var) for XMPP server, agent names, passwords, and LLM provider settings.
- Dynamic tool listing in startup output instead of hardcoded tool names.
- Chat agent target JID derived from configuration instead of hardcoded.
- Coordinator routing function uses configuration for agent JIDs instead of hardcoded @localhost.
- Fixed Panel rendering in chat agent when metadata is present.
- Removed unused module-level tools list in vlai.py.

## Release 0.1.0 (2026-01-21)

First stable release of VulnAgent.

Support of remote or local LLM provider.
Configuration of the Assistant Agent (using the LLM provider).
5 tools linked to the LLM agent.
Chat Agent to send prompts to the Assistant Agent.
Coordinator Agent.
