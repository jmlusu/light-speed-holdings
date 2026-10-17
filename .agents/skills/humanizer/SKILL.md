---
name: humanizer
description: Rewrites AI-generated or generic text into clear, natural language using active voice, varied sentence length, and specific concrete examples. Use when you want to humanize text, remove AI slop, clarify dense prose, or rewrite content so it sounds like a real person wrote it. Say things like "humanize this", "make this sound more natural", "rewrite without AI patterns", or "fix the wording".
---
# Humanizer

## Instructions

### Step 1: Scan for AI slop patterns
Identify banned words and phrases (Elevate, Hustle, Revolutionize, Fostering, Reimagine, Subsequently, Showcase, Profound, Groundbreaking, To Bridge, Highlight, Whispering, Delve, It's like having, Synergies, Insights, Whisper, Enablement, Meanwhile, There's no denying, Game changer, Deep dive, Leverage, Unleash, Harness, Paradigm, Ecosystem, Cross-functional, Think outside the box, Touch point, Across Different, human oversight, to bridge). Flag any occurrence.

### Step 2: Rewrite with active voice and concrete language
Replace vague terms with specific examples. Use "you" and "your" when addressing the reader. Vary sentence length naturally. Include a number or concrete detail when possible (e.g., "reduced from 5 days to 2").

### Step 3: Check sentence flow
Read each sentence aloud. If it sounds stiff or AI-generated, break it into shorter pieces or rephrase with more specific verbs. Remove empty structures like "not only/just X, but also Y" and "From X to Y".

### Step 4: Verify no banned phrases remain
Run a final pass checking every banned word/phrase is absent. If any remain, rewrite the surrounding sentence.

## Examples

User says "humanize this text" → scan → rewrite → return improved version with natural flow.
User says "make this sound more human" → same workflow; result reads without AI filler.
User says "fix the wording in this paragraph" → identify patterns → rewrite with active voice and concrete details.

## Troubleshooting

- **Output still feels AI-generated**: check for remaining banned phrases; break longer sentences into shorter, more varied ones.
- **Too casual or too formal**: adjust the balance of "you"/"your" usage and sentence complexity for the target audience.
- **No relevant numbers or examples**: embed a specific detail from the context (e.g., "the 2023 report" instead of "the report") rather than forcing unrelated statistics.