# X Thread - Post 11: Lessons From Building LightSpeed

🧵 Ten posts, one framework, and now the honest close: the lessons from actually building an AI-native company, including the ones that cost me time. If you are building in Malawi or SADC, these are the six I would hand you first. 🧵

1/7 🗂️ Lesson 1: The registry is the product. Not the agents, not the models: the enumerated inventory with scope and permissions. When I finally enforced it (ADR-032), it came back at 152 registered agents, most dormant. Consolidating to 90 was the precondition for everything else being true.

2/7 📉 Lesson 2: Reliability failures are governance data, not embarrassment. My scheduler missed runs. I let it surface in the metrics, because a system that hides its misses trains you to distrust its hits. An honest null beats a green dashboard nobody believes.

3/7 🪜 Lesson 3: Autonomy is earned per action class, never granted at onboarding. The five-tier sequence is a ratchet: promotion requires measured reliability in your own queue; demotion is always available when the queue says otherwise.

4/7 🚪 Lesson 4: One human standard, applied uniformly. The per-department dialect ("legal is stricter," "sales moves fast") is how drift starts. One matrix, one approval sweep, one expired-approval count, reported weekly.

5/7 🌍 Lesson 5: Sovereignty is a default you install, not a claim you make. Data in-country, models registered, foreign models behind safeguards - evidenceable at audit time, or stop claiming it.

6/7 💰 Lesson 6: Cost is a dial you watch, not a contract you sign. Per-model, per-department variable cost from week one made the 90-day pilot honest: per-agent cost on the invoice, renegotiated from evidence, not hope.

7/7 📥 What I got wrong: capability before measurement, demos before audit trails. Starting again, I would invert: registry → queue → 3 traceable KPIs → forbidden list → one tier → then agents. Download the Malawi Agentic AI Monitor to explore how these patterns apply in-Malawi context.

#AINative #StartupLessons #Malawi #SADC #AgenticAI