FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY assets /usr/share/nginx/html/assets
COPY ebooks /usr/share/nginx/html/ebooks
COPY s01_agent_loop /usr/share/nginx/html/s01_agent_loop
COPY s02_tool_use /usr/share/nginx/html/s02_tool_use
COPY s03_permission /usr/share/nginx/html/s03_permission
COPY s04_hooks /usr/share/nginx/html/s04_hooks
COPY s05_todo_write /usr/share/nginx/html/s05_todo_write
COPY s06_subagent /usr/share/nginx/html/s06_subagent
COPY s07_skill_loading /usr/share/nginx/html/s07_skill_loading
COPY s08_context_compact /usr/share/nginx/html/s08_context_compact
COPY s09_memory /usr/share/nginx/html/s09_memory
COPY s10_system_prompt /usr/share/nginx/html/s10_system_prompt
COPY s11_error_recovery /usr/share/nginx/html/s11_error_recovery
COPY s12_task_system /usr/share/nginx/html/s12_task_system
COPY s13_background_tasks /usr/share/nginx/html/s13_background_tasks
COPY s14_cron_scheduler /usr/share/nginx/html/s14_cron_scheduler
COPY s15_agent_teams /usr/share/nginx/html/s15_agent_teams
COPY s16_team_protocols /usr/share/nginx/html/s16_team_protocols
COPY s17_autonomous_agents /usr/share/nginx/html/s17_autonomous_agents
COPY s18_worktree_isolation /usr/share/nginx/html/s18_worktree_isolation
COPY s19_mcp_plugin /usr/share/nginx/html/s19_mcp_plugin
COPY s20_comprehensive /usr/share/nginx/html/s20_comprehensive

EXPOSE 80
