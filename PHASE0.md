# Phase 0: Luke's one sitting

The agent's session was refused three actions by the Claude Code classifier (self-modification for
the permission file, data exfiltration for the public push) even with your approval on record. They
are yours to run, once, from any terminal. Idempotent.

## 1. Permission file (so a scheduled Proteus run can never hang on a prompt)

```bash
cp /Users/triton/PROTEUS/.claude/settings.json.staged /Users/triton/PROTEUS/.claude/settings.json
```

## 2. Public repo and lab page

```bash
gh repo create proteus-lab --public --description "Proteus: an AI persona that explores instead of executes. Paper desks, public track record, field notes." --source /Users/triton/PROTEUS --remote origin --push
```

```bash
gh api -X POST repos/triton-xxix/proteus-lab/pages -f "source[branch]=main" -f "source[path]=/docs"
```

The lab page then lives at https://triton-xxix.github.io/proteus-lab/ after the first Pages build
(about a minute).

## 3. Sign the charter

Open `/Users/triton/PROTEUS/CHARTER.md`, read it, put your name and the date at the bottom.

## 4. 1Password

Tag these existing items `proteus` so Proteus may read them at runtime: The Odds API,
SportsGameOdds API, Youtube API Data v3, Browserless API, Gemini API - Florist Lab. Nothing new to
create today.

## 5. Card

Load a virtual card with a £50 monthly cap and keep the details to yourself. Proteus names a
service in Field Notes when a free tier runs out; you enter the card there once.

## 6. In a session with the agent, same sitting

Load the two scheduled tasks from `scheduled-tasks/proteus-nightly/SKILL.md` and
`scheduled-tasks/proteus-weekly/SKILL.md`, and add the two rows to
`TRITON-CORE/Systems/automation-registry.md`. Job control needs you present; the agent does the
typing.
