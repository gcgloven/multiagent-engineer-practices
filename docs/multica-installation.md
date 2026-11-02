# Install or refresh Multica configuration

For the complete host/toolkit installation and fresh-workspace test suite, follow [Set up and test a fresh workspace](new-workspace-pilot.md). The [version 2 workflow](workflow-and-roles-v2.md) defines the nine roles and five squad routes.

The lower-level installer configures nine reusable agents, twelve complete method archives, and one or all squad presets using an authenticated Multica CLI 0.7.1 or newer. It does not install host backends or start issues. Use the unified `scripts/setup.py` when preparing a new execution host. The `extract-paper-pdf` skill supplies Docling usage instructions; Docling itself is an optional execution dependency outside the current pinned research pack.

```bash
multica workspace list --full-id
multica --workspace-id WORKSPACE_UUID runtime list --output json
python3 -B scripts/install_multica.py --workspace-id WORKSPACE_UUID \
  --runtime-id RUNTIME_UUID --squad-profile all
```

Add `--apply` after checking the target and preview. A member UUID is not a runtime UUID. Add `--profile NAME` for a named CLI connection; the installer does not change the default workspace.

Select `research-engineering`, `open-research`, `analytics-engineering`, `software-delivery`, or `engineering-design` for one preset. Use `--squad-name NAME` for one customized squad; it cannot be combined with `all`. Every preset uses the shared nine-role pool from [the registry](../scripts/catalog.py). Membership means availability, not mandatory dispatch.

| Preset | Default installed name |
| --- | --- |
| `research-engineering` | Engineering Practice Squad |
| `open-research` | Open Research Squad |
| `analytics-engineering` | Analytics Engineering Squad |
| `software-delivery` | Software Delivery Squad |
| `engineering-design` | Engineering Design Squad |

The installer matches squads by exact name. When upgrading an existing installation with older names, rename each existing squad to its matching default before running setup. This keeps its UUID and existing issue assignments:

```bash
multica --workspace-id WORKSPACE_UUID squad list --output json
multica --workspace-id WORKSPACE_UUID squad update SQUAD_UUID \
  --name "Software Delivery Squad" --output json
```

Use the correct UUID and name for each preset, then inspect the list again. For intentionally customized names, retain the custom name through `--squad-name` and supply the corresponding `--squad-map` to the test-ticket utility.

For a deliberate refresh, include `--update-existing` in both preview and apply. Unchanged content is reused; changed managed instructions, descriptions, runtimes, skill bindings and selected squad rosters are reconciled. Agent model/access settings and human members are preserved. Additional agent skill bindings and out-of-roster agent memberships are replaced. This can affect other squads sharing those agents. The generic legacy Engineer is not a managed target and is neither renamed nor deleted.

Use `--reuse-existing` when adding a new squad from exactly compatible existing profiles without changing them. Additional agent skill bindings are preserved in reuse mode. Missing objects are created; incompatible objects or an existing target squad stop reuse. Do not use reuse as a migration of old profiles. Skill overwrite requires workspace ownership/permissions; `--overwrite-skills` is the explicit skill-only conflict option and cannot be combined with reuse.

The all-profile operation preflights every selected squad before its first workspace write. Installation is not atomic: interrupted writes can leave objects present without a returned ID. Inspect all planned names before retrying; the script does not blindly retry creation or automatically roll back.

```bash
multica --workspace-id WORKSPACE_UUID agent list --output json
multica --workspace-id WORKSPACE_UUID squad list --output json
multica --workspace-id WORKSPACE_UUID skill list --output json
multica --workspace-id WORKSPACE_UUID skill get SKILL_UUID --with-content --output json
multica --workspace-id WORKSPACE_UUID agent skills list AGENT_UUID --output json
multica --workspace-id WORKSPACE_UUID squad member list SQUAD_UUID --output json
```

Generated agent files combine the common specialist contract and the role. Engineering squad files combine shared engineering coordination and the preset; Open Research combines its research-specific coordination policy with the preset. Skill archives retain complete linked resources. The generator manifest is a local inventory, not a Multica import schema. Tool executables remain in the host environment rather than inside Markdown-only skill archives.

Only Lead is assumed to receive squad policy. Its assignments must carry relevant criteria, exact candidate/input references, human authority, budget and one return route. Read-back proves configuration consistency; it does not prove runtime delivery, tool access, independent review, human gates or budget adherence. Run the [nine-case pilot](new-workspace-pilot.md) and inspect actual behavior before relying on the refreshed setup.
