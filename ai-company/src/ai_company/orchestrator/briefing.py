import yaml
from pathlib import Path
from datetime import datetime
from ai_company.orchestrator.message_bus import MessageBus

class BriefingGenerator:
    def __init__(self, registry_path="company-registry.yaml"):
        self.registry_path = Path(registry_path)
        self.bus = MessageBus()

    def generate(self):
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        agents = {a['id']: a for a in data['company']['agents']}
        pending_tasks = {}
        
        # Gather all pending tasks
        for task_dict in self.bus._load_tasks():
            if task_dict['status'] == 'pending':
                receiver = task_dict['receiver_id']
                if receiver not in pending_tasks:
                    pending_tasks[receiver] = []
                pending_tasks[receiver].append(task_dict)
                
        print("📊 Generating Daily Executive Briefing...")
        
        today = datetime.now().strftime('%Y-%m-%d')
        briefing_md = f"# 🌅 Daily Executive Briefing for {data['company']['name']}\n"
        briefing_md += f"**Date:** {today}\n\n"
        
        active_agents = 0
        for aid, tasks in pending_tasks.items():
            if aid in agents:
                agent = agents[aid]
                active_agents += 1
                briefing_md += f"## 🎯 Action Required: {agent['name']} ({agent['title']})\n"
                briefing_md += f"**Department:** {agent['department']} | **Reports To:** {agent['reports_to']}\n\n"
                briefing_md += "**OpenCode Execution Prompt:**\n```text\n"
                briefing_md += f"You are the {agent['title']}. You have {len(tasks)} pending task(s) in your inbox.\n\n"
                for task in tasks:
                    sender_name = agents.get(task['sender_id'], {}).get('name', task['sender_id'])
                    briefing_md += f"TASK ID: {task['id']}\n"
                    briefing_md += f"FROM: {sender_name}\n"
                    briefing_md += f"INSTRUCTION: {task['instruction']}\n\n"
                briefing_md += "Please execute these tasks using your available tools.\n```\n\n---\n\n"
                
        if active_agents == 0:
            briefing_md += "✅ **No pending tasks.** The company is idle or waiting for executive directives.\n"
            
        output_path = Path(".opencode/daily_briefing.md")
        output_path.write_text(briefing_md, encoding='utf-8')
        print(f"✅ Briefing generated at: {output_path}")
        
        return active_agents, len(pending_tasks)
