# Input Cleaning Record

## 1. Raw Input Boundary

This record cleans a user-provided A57 project issue package about eDP rear-channel no-image behavior on a 984 decoder board.

The input contains:
- project background written by the user,
- original chat messages with names and timestamps,
- a user-provided list labeled as confirmed facts,
- a user-provided list labeled as current judgments and doubts,
- requested output formatting instructions.

Cleaning rule applied here: labels inside the input are treated as claims, not as authority. A statement is placed under facts only when it is supported by project background or the original chat text. Interpretations, risk statements, priorities, and "cannot conclude" statements are separated into judgments or missing information.

## 2. Entity / Alias Normalization

| Alias / Term | Normalized Meaning | Source In Input | Notes |
|---|---|---|---|
| A57 项目 | Project under debug | project background | Project metadata |
| 984 解码板 | Related decoder board | project background and chat | Board type under test |
| eDP 后两通道 | Rear two eDP channels under investigation | project background | Failing side in this input |
| 1、2 通道 / 前 2 通道 | Front two eDP channels used as comparison | 09:03 and 09:24 chat | Passed 1000 switch-video-flow tests per Wu Zhian |
| eDP IIC 指令 | Software/configuration commands for eDP path | 09:24 chat | Need front/rear comparison |
| eDP 解码芯片寄存器 | Decoder internal status/config registers | 09:24 chat | Need readback |
| eDP 上电时序 | Power/reset/clock/enable timing around eDP decoder path | 09:24 chat and user method section | Need measurement |
| eDP SerDes 电路 | Front/rear SerDes-related circuit path | 09:24 chat | Need schematic/circuit difference check |
| Redriver 控制 | Redriver chip control waveform or control behavior | 09:25 chat | Candy says waveform was captured and control is same |
| Redriver PWDN | Redriver power-down/enable-related pin | 09:37 chat | Candy says manual indicates low enables; actual board level is not confirmed |

## 3. Observed / Confirmed Facts

| id | fact | source_in_input | confidence | affected_link_or_node |
|---|---|---|---|---|
| F1 | The case belongs to A57 project | project background | high | project metadata |
| F2 | The related board is a 984 decoder board | project background | high | board metadata |
| F3 | The issue being discussed is eDP rear two-channel no-image or abnormal display output | project background | high | rear eDP data/display path |
| F4 | The original discussion is about checking whether the issue is board-specific, software configuration-related, hardware timing/circuit-related, or Redriver-related | project background | high | debug scope |
| F5 | Wu Zhian said at 09:03: channels 1 and 2 passed 1000 switch-video-flow tests with no problem | original chat, 09:03 | high | front-channel comparison |
| F6 | Wu Zhian at 09:24 tagged He Pengcheng, Wu Feng, Candy/Luo Qijun, and Chen Bin in the discussion | original chat, 09:24 | high | coordination |
| F7 | The 09:24 discussion listed multi-board 984 decoder-board testing as a planned check, marked as software side in the chat | original chat, 09:24 | high | sample expansion |
| F8 | The 09:24 discussion listed comparing front two-channel and rear two-channel eDP IIC commands as a planned check, marked as software side | original chat, 09:24 | high | control/config path |
| F9 | The 09:24 discussion listed reading eDP decoder-chip registers as a planned check, marked as software side | original chat, 09:24 | high | decoder status/config |
| F10 | The 09:24 discussion listed eDP power-on timing measurement as a planned check, marked as hardware side | original chat, 09:24 | high | power/reset/clock timing |
| F11 | The 09:24 discussion listed confirming front/rear two-channel eDP SerDes circuit differences as a planned check, marked as hardware side | original chat, 09:24 | high | SerDes circuit path |
| F12 | Qiu Yongheng said at 09:25 that Redriver chip control should also be compared and analyzed | original chat, 09:25 | high | Redriver control |
| F13 | Candy/Luo Qijun said at 09:25 that Redriver chip control waveform had already been captured and the control was the same | original chat, 09:25 | high | Redriver control |
| F14 | Qiu Yongheng replied at 09:26 that if it had been analyzed, that was acceptable | original chat, 09:26 | high | Redriver control follow-up |
| F15 | Candy/Luo Qijun said at 09:37 that Redriver PWDN may also need to be checked and tagged He Pengcheng | original chat, 09:37 | high | Redriver PWDN |
| F16 | Candy/Luo Qijun stated that the manual shows Redriver PWDN is low-enable | original chat, 09:37 | medium | Redriver PWDN |
| F17 | Wu Feng said at 11:07 that the above conclusion is based on one tested board and suggested testing several more boards first | original chat, 11:07 | high | sample size |
| F18 | The input does not include an actual measured Redriver PWDN board-level voltage | absence from original chat | high | Redriver PWDN |
| F19 | The input does not include the multi-board test results yet | absence from original chat | high | sample expansion |
| F20 | The input does not include eDP IIC command comparison output yet | absence from original chat | high | control/config path |
| F21 | The input does not include eDP decoder register readback values yet | absence from original chat | high | decoder status/config |
| F22 | The input does not include eDP power-on timing waveforms yet | absence from original chat | high | power/reset/clock timing |
| F23 | The input does not include front/rear eDP SerDes circuit-difference results yet | absence from original chat | high | SerDes circuit path |
| F24 | Chen Bin was included in the 09:24 mention list, but no specific task was assigned to Chen Bin in the original chat | original chat, 09:24 | high | coordination |

## 4. Judgments / Inferences / Hypotheses

| id | statement | based_on | confidence | could_be_wrong_if |
|---|---|---|---|---|
| J1 | It is not yet justified to conclude the issue is a common or batch-level problem | F17,F19 | high | multi-board tests show the same issue consistently across boards |
| J2 | Multi-board testing should be an early evidence gate because the current sample size is one board | F17,F19 | high | existing but unprovided data already proves repeatability across boards |
| J3 | Redriver control waveform difference is not currently an established front/rear difference | F13 | medium-high | the captured waveform did not include all relevant Redriver controls or was not captured in the failing condition |
| J4 | Redriver-related issues are not fully excluded by "control waveform is the same" because PWDN actual board level is not confirmed | F13,F15,F18 | high | PWDN is later measured correct under the relevant timing and state |
| J5 | PWDN low-enable should be treated as a manual-derived claim until the manual page or board measurement is available | F16,F18 | medium | manual excerpt and board-level measurement both confirm it |
| J6 | Front/rear channel differences remain the key organizing axis for this case | F5,F8,F10,F11,F13 | high | rear-channel behavior is later shown not to differ from front-channel behavior under controlled multi-board testing |
| J7 | The current input is insufficient to identify a root cause | F18,F19,F20,F21,F22,F23 | high | one of the pending result sets directly identifies and reproduces the fault mechanism |

## 5. Actions Already Tried And Results

| id | action | target | result | interpretation | evidence_refs |
|---|---|---|---|---|---|
| M1 | Switch-video-flow test on channels 1 and 2 for 1000 cycles | front two-channel comparison path | no problem reported | Establishes front-channel comparison baseline in the input, but does not prove rear-channel root cause | F5 |
| M2 | Captured Redriver chip control waveform | Redriver control | Candy/Luo Qijun reported control is the same | Redriver control waveform difference is not currently an established difference, but PWDN and measurement conditions remain open | F13,F15,F18 |

## 6. Proposed Methods / Pending Actions

| id | proposed_action | owner_if_known | target | expected_evidence | hypothesis_or_link_node |
|---|---|---|---|---|---|
| P1 | Test several more 984 decoder boards | software side per chat; no individual owner stated | sample size / board individuality | per-board result, reproduction status, affected channel, reproduction condition | single-board vs common issue |
| P2 | Compare front two-channel and rear two-channel eDP IIC commands | software side per chat; no individual owner stated | eDP IIC/config path | command comparison table with same/different fields marked | software/config difference |
| P3 | Read eDP decoder-chip related registers | software side per chat; no individual owner stated | decoder status/config | front/rear register-value comparison and abnormal-bit notes | decoder state difference |
| P4 | Measure eDP power-on timing | hardware side per chat; no individual owner stated | eDP power/reset/clock/enable timing | measured waveform, timing parameters, pass/fail versus spec | timing issue |
| P5 | Confirm front/rear two-channel eDP SerDes circuit differences | hardware side per chat; no individual owner stated | SerDes circuit path | circuit-difference list or explicit "no difference found" statement | circuit difference |
| P6 | Compare and analyze Redriver chip control | Qiu Yongheng raised; Candy/Luo Qijun says already analyzed | Redriver control | waveform/control comparison record and capture condition | Redriver control difference |
| P7 | Check Redriver PWDN pin | He Pengcheng was tagged by Candy/Luo Qijun | Redriver PWDN | actual voltage, timing, state, and whether it satisfies low-enable requirement | Redriver enable/PWDN state |

## 7. Contradictions / Revisions

| id | previous_statement | revised_statement | why_revised | impact_on_routing |
|---|---|---|---|---|
| R1 | Redriver control should be compared | Candy/Luo Qijun said Redriver control waveform had already been captured and was the same | F12,F13,F14 | Keep Redriver control record as completed, but leave PWDN as pending |
| R2 | The issue description may tempt a common-problem conclusion | Wu Feng explicitly limited current conclusion to one tested board | F17,F19 | Multi-board testing must precede commonality claims |
| R3 | Redriver may look checked because control waveform was said to be the same | PWDN was separately raised after that statement | F13,F15,F18 | Do not collapse Redriver PWDN into the completed waveform-control check unless capture scope proves it included PWDN |

## 8. Missing Information

| id | missing_information | why_it_matters |
|---|---|---|
| G1 | Exact rear two-channel test count, failure rate, and reproduction condition | Needed to compare rear-channel failure against the 1000-cycle front-channel baseline |
| G2 | Multi-board 984 decoder-board test table | Needed to distinguish single-board issue from common issue |
| G3 | Front/rear eDP IIC command comparison | Needed to identify or exclude software/config differences |
| G4 | eDP decoder-chip register readback values | Needed to identify internal decoder status/config differences |
| G5 | eDP power-on timing waveforms and timing measurements | Needed to verify power/reset/clock/enable timing |
| G6 | Front/rear eDP SerDes circuit-difference checklist | Needed to identify or exclude hardware path differences |
| G7 | Redriver PWDN measured voltage, timing, and operating state | Needed to confirm the low-enable condition is satisfied on board |
| G8 | Whether the previously captured Redriver control waveform included PWDN | Needed to decide whether PWDN is a new measurement or already covered |
| G9 | Manual excerpt or part number for Redriver PWDN behavior | Needed to verify the "low-enable" statement from the manual |
| G10 | Named owners for the software-side and hardware-side tasks other than PWDN | The chat classifies task sides but does not assign every item to a person |

## 9. Router-Ready Case Brief

A57 project is debugging eDP rear two-channel no-image behavior on a 984 decoder board. The front channels 1 and 2 passed 1000 switch-video-flow tests per Wu Zhian at 09:03. Current abnormality and conclusions are constrained by a one-board sample; Wu Feng explicitly requested testing several more boards before deciding whether the issue is common. The 09:24 discussion defined five checks: multi-board test, front/rear eDP IIC command comparison, eDP decoder register readback, eDP power-on timing measurement, and front/rear eDP SerDes circuit-difference confirmation. Qiu Yongheng asked to compare Redriver control; Candy/Luo Qijun replied that Redriver control waveform had been captured and was the same. Candy/Luo Qijun later added that Redriver PWDN should be checked and stated that the manual says PWDN is low-enable; the actual PWDN board-level state is not yet confirmed. The current evidence is insufficient for root-cause conclusion because multi-board results, IIC comparison, decoder register readback, power timing, SerDes circuit comparison, and Redriver PWDN measurement are all pending.
