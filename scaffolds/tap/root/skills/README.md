# Skills

This directory holds shared skills: skills that two or more agents use, at
`skills/<name>/SKILL.md`, bound to those agents by `domains:` in the
frontmatter. A skill that only one agent uses is an owned skill and lives at
`agents/<agent>/skills/<name>/SKILL.md` with no `domains:` line.

Skills follow the AgentSkills format. The directory name must match the `name`
frontmatter field, and a skill name exists once in the tap. Start from
`templates/skill.md` and keep the final checklist near the end.
