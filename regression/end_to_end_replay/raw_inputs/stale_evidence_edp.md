# Raw Input: Stale Evidence eDP

A57 eDP 后通道不出图，AUX 正常，AU15P CDR 不锁、comma fail，SerDes reset 无效。

补充：之前发现 aux_in 初始电平差异，尝试弱下拉没有解决；但这是早期记录。现在没有同一故障窗口的新 AUX 波形，也没有同一故障窗口的新 AU15P CDR/comma 状态。

请用 DebugTool 输出 input-cleaning 和 Architecture-First 排查策略。注意：旧 aux_in 弱下拉信息只能作为 stale context，不能直接降低或提高当前概率。

