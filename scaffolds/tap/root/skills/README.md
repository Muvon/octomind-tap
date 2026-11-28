# Skills

This directory holds shared skills: skills that two or more agent namespaces use, at
`skills/<name>/SKILL.md`, bound to those namespaces by `domains:` in the
frontmatter. A skill that only one namespace uses is an owned skill and lives at
`agents/<ns>/skills/<name>/SKILL.md` with no `domains:` line; the base agent and
every variant of the namespace get it.

Skills follow the AgentSkills format. The directory name must match the `name`
frontmatter field, and a skill name exists once in the tap. Start from
`templates/skill.md` and keep the final checklist near the end.
