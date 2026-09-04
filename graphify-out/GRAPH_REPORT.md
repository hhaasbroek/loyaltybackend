# Graph Report - loyaltybackend  (2026-09-04)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 79 nodes · 135 edges · 17 communities (6 shown, 3 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `10ddf6f8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cards.py
- main.py
- deploy
- auth.py
- Settings
- get_current_user
- UserDB
- app/__init__.py
- models/__init__.py

## God Nodes (most connected - your core abstractions)
1. `UserDB` - 13 edges
2. `get_current_user()` - 9 edges
3. `LoyaltyCardDB` - 7 edges
4. `create_card()` - 7 edges
5. `LoyaltyCard` - 6 edges
6. `get_card()` - 6 edges
7. `list_cards()` - 6 edges
8. `get_firebase_app()` - 6 edges
9. `delete_card()` - 5 edges
10. `_fake_current_user()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `test_cards_require_auth()` --indirect_call--> `get_current_user()`  [INFERRED]
  tests/test_main.py → app/core/auth.py
- `create_card()` --uses--> `UserDB`  [INFERRED]
  app/api/v1/endpoints/cards.py → app/models/user.py
- `delete_card()` --uses--> `UserDB`  [INFERRED]
  app/api/v1/endpoints/cards.py → app/models/user.py
- `get_card()` --uses--> `UserDB`  [INFERRED]
  app/api/v1/endpoints/cards.py → app/models/user.py
- `list_cards()` --uses--> `UserDB`  [INFERRED]
  app/api/v1/endpoints/cards.py → app/models/user.py

## Import Cycles
- None detected.

## Communities (17 total, 3 thin omitted)

### Community 0 - "cards.py"
Cohesion: 0.24
Nodes (14): create_card(), delete_card(), get_card(), list_cards(), get, Session, LoyaltyCardDB, Base (+6 more)

### Community 1 - "main.py"
Cohesion: 0.19
Nodes (11): App, health_check(), HealthCheckResponse, BaseModel, get, Health check endpoint for container orchestrators (like Railway) and uptime…, get_firebase_app(), lifespan() (+3 more)

### Community 2 - "deploy"
Cohesion: 0.20
Nodes (9): build, builder, dockerfilePath, deploy, healthcheckPath, healthcheckTimeout, restartPolicyMaxRetries, restartPolicyType (+1 more)

### Community 4 - "Settings"
Cohesion: 0.50
Nodes (3): Settings, BaseSettings, field_validator

### Community 6 - "get_current_user"
Cohesion: 0.50
Nodes (4): get_current_user(), Session, HTTPAuthorizationCredentials, test_cards_require_auth()

### Community 7 - "UserDB"
Cohesion: 0.67
Nodes (4): Base, UserDB, _fake_current_user(), test_cards_are_scoped_to_user()

## Knowledge Gaps
- **7 isolated node(s):** `builder`, `dockerfilePath`, `healthcheckPath`, `healthcheckTimeout`, `restartPolicyMaxRetries` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 35 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UserDB` connect `UserDB` to `cards.py`, `auth.py`, `test_main.py`, `get_current_user`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `main.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `get_current_user()` connect `get_current_user` to `cards.py`, `main.py`, `auth.py`, `test_main.py`, `UserDB`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `UserDB` (e.g. with `create_card()` and `delete_card()`) actually correct?**
  _`UserDB` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LoyaltyCardDB` (e.g. with `create_card()` and `delete_card()`) actually correct?**
  _`LoyaltyCardDB` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `create_card()` (e.g. with `LoyaltyCardDB` and `UserDB`) actually correct?**
  _`create_card()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `builder`, `dockerfilePath`, `healthcheckPath` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._