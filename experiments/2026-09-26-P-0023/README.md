# P-0023: golive-skill, account-free detect and plan, and does apply refuse without --yes?

Run 26 Sep 2026, about 23:42 to 23:44, from the nightly. Source: harvest H-0022
(mikehasa/golive-skill). Script: `sandbox/p0023_golive.py`. Full CLI output in `results-run.json`.

## How it was isolated

Installed `golive@alpha` (0.1.0-alpha.4, one package, no dependencies) from npm into the sandbox,
not through its skill installer, which writes into the home directory. Every command ran with HOME
and XDG_CONFIG_HOME pointed at an empty fake home inside the sandbox, a four-variable environment
and stdin closed, so no real provider login, token or credentials file was visible. `--yes` was
never passed.

## What happened

- **detect** (0.6 s) on a scratch Next.js app with Supabase, Resend and Stripe in `package.json`
  and four names in `.env.example`: found the framework and all three providers, mapped every env
  name to a provider key, and flagged the two `NEXT_PUBLIC_` names as client-exposed. Correct on
  every count.
- **plan** before `init`: refused, "no golive.yaml yet". `init --stack ...` wrote `golive.yaml`,
  the only file golive wrote in the app.
- **doctor**: exit 2, every provider unreachable, with per-provider login instructions and the path
  its credentials file would use (inside the fake home, so the isolation held).
- **plan**: printed plan id `aa01065b3dc3`, but its only steps are five human handoffs (log in to
  Vercel, Supabase, Stripe, Resend; activate Stripe). All provider steps are left out with a warning
  that access could not be verified. So account-free you get a real, inspectable plan of what a
  human must do, and none of what golive would do.
- **apply** with no plan: refused, needs `--plan`. **apply --plan aa01065b3dc3**: refused,
  "refusing to write without --yes". Same with `--confirm-live` added. No file written.

## What I did not do

Did not pass `--yes`, connect any account or test the teardown, the drift check or the credentials
prompt. The README's own caveat stands untested either way: an agent already logged in to a
provider can write there with no golive plan at all.

## Verdict

Works, for the slice tested. Detection is accurate, the gates refuse as documented and write
nothing. The account-free plan is only a login checklist, so the part worth judging (the actual
provider steps) needs accounts I do not hold.
