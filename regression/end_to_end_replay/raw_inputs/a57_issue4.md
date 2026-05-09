# Raw Input: A57 Issue4 Evidence Update

A57 这个 eDP 案子有新补充，不是全新 case，是对之前后两通道不出图问题的更新。

- eDP1、eDP2 对应解码板上的一颗 DS90UB984，eDP3、eDP4 对应另一颗 DS90UB984。
- 现在不是只有后两通道有问题，eDP1、eDP2、eDP3、eDP4 都有概率出现出图异常。
- 一共测了 4 块解码板，板间表现不同：一块板 eDP3/eDP4 异常概率高，另外三块板 eDP1/eDP2 异常概率高。
- 同一颗 DS90UB984 下两个通道也没有严格一致性，会出现一个好、一个不好的情况。
- Redriver 位于 eDP mainstream 中间，设备上电后已经配置，后续重复测试时不重新配置。
- 当前重复测试是对 DS90UB984 解码芯片重新上下电和重新配置。
- 前后 2 通道 eDP SerDes 电路差异已确认无差异。
- 前 2 通道 eDP DS90UB984 IIC 指令与后 2 通道 IIC 指令对比已完成，指令和 ini/参数下发未发现问题。
- Redriver 4 通道上电 PWDN 信号及 I2C/出图 PWDN 信号仍待确认。
- 读 eDP 解码芯片相关寄存器，以及模拟出图输出相关寄存器是否存在，需要和厂家确认。
- 旧版 context 中 AUX 正常、AU15P CDR/comma 异常、SerDes reset 无改善等信息没有在当前四通道故障窗口重新确认。

请更新 input-cleaning 和 Architecture-First 输出。不要直接下 root cause 结论。

