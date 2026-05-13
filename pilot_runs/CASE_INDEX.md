# Pilot Case Index

Use this index before creating a new `pilot_runs/` artifact, answering where to record an update, or routing a short follow-up that may belong to an existing case.

## Match Rule

- Strong match: explicit `case_id`, exact project name, or at least two aliases from the same row.
- Probable match: one distinctive alias plus protocol/failure words from the same row.
- If a strong or probable match exists, open the case directory `README.md` and update the relevant `latest-*` artifact instead of creating a new top-level file.
- If multiple rows match, list the candidate case IDs and ask for confirmation before writing.

## Current Cases

| case_id | aliases / quick-match tokens | current_entry_points | status | last_updated | routing note |
|---|---|---|---|---|---|
| A57-EDP | `A57`, `a57`, `eDP`, `EDP`, `edp`, `DS90UB984`, `984`, `AUX`, `HPD`, `CR`, `EQ`, `CR/EQ`, `EQ/CR`, `训练字`, `SerDes`, `AU15P`, `Redriver`, `解码板`, `不出图`, `出图异常` | `pilot_runs/a57_edp/latest-input-cleaning.md`; `pilot_runs/a57_edp/latest-architecture-first.md` | active unresolved pilot case | 2026-05-13 | Treat short follow-ups as evidence updates. For CR/EQ fail, update Mode A AUX/DPCD training-control branch first. |
| HOTSWAP-SOA | `hotswap`, `hot-swap`, `SOA`, `MOSFET`, `inrush`, `浪涌`, `热插拔`, `高边`, `线性区` | `pilot_runs/PILOT-HOTSWAP-MOSFET-SOA.md` | pilot record | 2026-05-08 | Use for MOSFET SOA / inrush stress follow-ups. |
| LA1010-KINGSTVIS | `LA1010`, `KINGSTVIS`, `logic analyzer`, `USB`, `cable`, `枚举`, `连接线` | `pilot_runs/PILOT-LA1010-KINGSTVIS-105.md` | pilot record | 2026-05-08 | Use for LA1010 / USB cable pilot follow-ups. |

## Maintenance

- Update this table whenever a new pilot/debug case directory is created.
- Add aliases after real user wording appears in a chat or raw input.
- Keep aliases compact; this is a routing index, not a full case summary.
- Do not store root-cause claims here unless the case is solved and promoted through the retrospective gate.
