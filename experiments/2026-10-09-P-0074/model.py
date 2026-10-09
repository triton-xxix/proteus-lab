"""P-0074: does an honest OnlyFans management agency clear its costs, and how far is it from the goal?

Honest version: the agency does marketing, scheduling and analytics; it does NOT write DMs as the
creator (impersonation is the practice behind the 2023 class actions, and the platform's terms bar
deceptive conduct and AI chat). So no chatter commission line and no chat-driven PPV uplift.

Inputs are ranges from agency-side sources (unverified, often unclear on gross v net):
  platform fee 20% of gross; agency 25-50% of net; chatters 10-20% of sales or 15-30 dollars an hour;
  median ACTIVE creator about 1,000-1,500 dollars a month gross (headline median ~150 incl. inactive).
All money in dollars a month. One account manager handles N creators.
"""
import itertools

PLATFORM = 0.20
USD_GBP = 0.75          # rough, for the goal line only
GOAL_GBP_MONTH = 11667  # PERSONA.md: 140,000 over 12 months, flat

def agency_month(gross, split, clients, manager_cost, tools=150, ads_per_client=100):
    net = gross * (1 - PLATFORM)
    revenue = net * split * clients
    costs = manager_cost * (clients / 10 + (1 if clients % 10 else 0) * 0) + tools + ads_per_client * clients
    return revenue, costs, revenue - costs

rows = []
for gross, split, clients in itertools.product((150, 1250, 5000, 20000), (0.25, 0.40, 0.50), (5, 10, 25)):
    managers = -(-clients // 10)                       # one manager per 10 creators, rounded up
    rev = gross * (1 - PLATFORM) * split * clients
    cost = managers * 3000 + 150 + 100 * clients       # manager 3,000 a month, tools 150, ads 100 a creator
    rows.append((gross, split, clients, round(rev), round(cost), round(rev - cost)))

print("creator gross/mo | agency split | creators | agency revenue | costs | profit/mo")
for r in rows:
    print("%16s | %12s | %8s | %14s | %5s | %9s" % (r[0], "%d%%" % (r[1] * 100), r[2], r[3], r[4], r[5]))

# break-even creator gross for one manager running 10 creators at a 40% split
be = (3000 + 150 + 100 * 10) / (10 * (1 - PLATFORM) * 0.40)
print("\nbreak-even gross per creator (10 creators, 40%%, one manager): %d dollars a month" % be)
need = GOAL_GBP_MONTH / USD_GBP
per_creator_profit = 1250 * 0.8 * 0.40 - (3000 / 10 + 100) - 15
print("goal: %d dollars a month; at the active median (1,250 gross) each creator leaves about %d,"
      " so about %d creators" % (need, per_creator_profit, need / per_creator_profit))
