FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY assets /usr/share/nginx/html/assets
COPY s01_agent_loop s02_tool_use s03_permission s04_hooks s05_todo_write /usr/share/nginx/html/
COPY s06_subagent s07_skill_loading s08_context_compact s09_memory s10_system_prompt /usr/share/nginx/html/
COPY s11_error_recovery s12_task_system s13_background_tasks s14_cron_scheduler s15_agent_teams /usr/share/nginx/html/
COPY s16_team_protocols s17_autonomous_agents s18_worktree_isolation s19_mcp_plugin s20_comprehensive /usr/share/nginx/html/

EXPOSE 80
